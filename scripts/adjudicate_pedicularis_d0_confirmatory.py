from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import random
from collections import defaultdict
from pathlib import Path


DATASET_ID = "PED_D0_QUAL_CONFIRM_V1"
MARGIN_SCHEMA = "SLK_PEDICULARIS_D0_MARGIN_FREEZE_V1"
FITNESS_SCALE_ID = "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER"
PAIR_SPECS = {
    "D0_Q1_Z": ("D0_QUAL", "SHAM_QUAL", "exsertion_z", "difference"),
    "D0_Q1_OPENING": ("D0_QUAL", "SHAM_QUAL", "opening_width_mm", "difference"),
    "D0_Q1_STIGMA": ("D0_QUAL", "SHAM_QUAL", "stigma_position_mm", "difference"),
    "D0_Q1_ORIENTATION": ("D0_QUAL", "SHAM_QUAL", "orientation_deg", "circular_difference_deg"),
    "D0_Q1_DAMAGE": ("D0_QUAL", "SHAM_QUAL", "mechanical_damage_post_prop", "difference"),
    "D0_Q3_VISIT": ("D0_QUAL", "SHAM_QUAL", "visit_rate_per_min", "difference"),
    "D0_Q3_POLLEN": ("D0_QUAL", "SHAM_QUAL", "pollen_receipt_grains", "difference"),
    "D0_Q3_INITIAL_SEED": ("D0_QUAL", "SHAM_QUAL", "initial_seed_set_prop", "difference"),
    "D0_Q4_WET_EFFECT": ("SHAM_QUAL", "D0_QUAL", "early_attack_prop", "difference"),
    "D0_Q4_DRY_RESIDUAL": ("SHAM_QUAL", "S_QUAL", "early_attack_prop", "difference"),
    "D0_Q5_BURDEN_EQ": ("S_QUAL", "SHAM_QUAL", "mature_viable_undamaged_seeds", "difference"),
    "D0_Q5_BURDEN_PRECISION": ("S_QUAL", "SHAM_QUAL", "mature_viable_undamaged_seeds", "difference"),
}
TWO_GROUP_SPECS = {
    "D0_Q2_VOLUME": ("D0_QUAL", "D_QUAL", "retention_mean_max_ml"),
    "D0_Q2_DURATION": ("D0_QUAL", "D_QUAL", "retention_mean_half_life_min"),
    "D0_Q2_COVERAGE": ("D0_QUAL", "D_QUAL", "retention_mean_protected_fraction"),
    "D0_Q2_PROTECTION": ("D0_QUAL", "D_QUAL", "early_attack_prop"),
}
PROPORTIONS = {
    "mechanical_damage_post_prop",
    "initial_seed_set_prop",
    "early_attack_prop",
    "seed_predation_prop",
    "retention_trial1_protected_fraction",
    "retention_trial2_protected_fraction",
}
Y_METRICS = {
    "RETENTION_MEAN_MAX_ML": "retention_mean_max_ml",
    "RETENTION_MEAN_DEPTH_MM": "retention_mean_depth_mm",
    "RETENTION_MEAN_HALF_LIFE_MIN": "retention_mean_half_life_min",
    "RETENTION_MEAN_PROTECTED_FRACTION": "retention_mean_protected_fraction",
}


def _load_module(filename: str, module_name: str):
    path = Path(__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


generator = _load_module("generate_pedicularis_d0_confirmatory_layout.py", "ped_d0_confirm_layout")
margin_validator = _load_module("validate_pedicularis_d0_margin_freeze.py", "ped_d0_margin_validate")


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _number(row: dict[str, str], field: str) -> float:
    raw = str(row.get(field, "")).strip()
    _need(raw != "", f"missing {field}")
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"non-numeric {field}: {raw}") from exc
    _need(math.isfinite(value), f"non-finite {field}")
    if field in PROPORTIONS:
        _need(0 <= value <= 1, f"{field} must be in [0,1]")
    return value


def _mean_available(values: list[float]) -> float:
    _need(values, "mean requires values")
    return sum(values) / len(values)


def _derived(row: dict[str, str], field: str) -> float:
    if field == "visit_rate_per_min":
        visits = _number(row, "legitimate_visits")
        minutes = _number(row, "pollinator_observation_minutes")
        _need(minutes > 0 and visits >= 0, "invalid visitation measurement")
        return visits / minutes
    if field == "retention_mean_max_ml":
        return _mean_available([_number(row, "retention_trial1_max_ml"), _number(row, "retention_trial2_max_ml")])
    if field == "retention_mean_depth_mm":
        return _mean_available([_number(row, "retention_trial1_depth_mm"), _number(row, "retention_trial2_depth_mm")])
    if field == "retention_mean_half_life_min":
        return _mean_available([_number(row, "retention_trial1_half_life_min"), _number(row, "retention_trial2_half_life_min")])
    if field == "retention_mean_protected_fraction":
        return _mean_available([_number(row, "retention_trial1_protected_fraction"), _number(row, "retention_trial2_protected_fraction")])
    value = _number(row, field)
    if field in {"pollen_receipt_grains", "mature_viable_undamaged_seeds", "legitimate_visits"}:
        _need(value >= 0, f"{field} must be >= 0")
    return value


def _circular_difference_deg(a: float, b: float) -> float:
    return ((a - b + 180.0) % 360.0) - 180.0


def _quantile(values: list[float], p: float) -> float:
    _need(values, "quantile requires values")
    xs = sorted(values)
    h = (len(xs) - 1) * p
    lo = math.floor(h)
    hi = math.ceil(h)
    if lo == hi:
        return xs[lo]
    frac = h - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


def _central_ci(values: list[float], level: float) -> tuple[float, float]:
    alpha = 1 - level
    return _quantile(values, alpha / 2), _quantile(values, 1 - alpha / 2)


def _bootstrap_mean(values: list[float], seed: int, reps: int) -> list[float]:
    rng = random.Random(seed)
    n = len(values)
    return [sum(values[rng.randrange(n)] for _ in range(n)) / n for _ in range(reps)]


def _bootstrap_two_group_difference(g1: list[float], g2: list[float], seed: int, reps: int) -> list[float]:
    rng = random.Random(seed)
    n1 = len(g1)
    n2 = len(g2)
    out: list[float] = []
    for _ in range(reps):
        m1 = sum(g1[rng.randrange(n1)] for _ in range(n1)) / n1
        m2 = sum(g2[rng.randrange(n2)] for _ in range(n2)) / n2
        out.append(m1 - m2)
    return out


def _group_rows(rows: list[dict[str, str]]) -> tuple[dict[str, dict[str, dict[str, str]]], dict[str, str]]:
    by_plant: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    strata: dict[str, str] = {}
    for row in rows:
        plant_id = str(row.get("plant_id", "")).strip()
        treatment = str(row.get("treatment", "")).strip()
        stratum = str(row.get("phenotype_stratum", "")).strip()
        _need(plant_id and treatment and stratum, "confirmatory row missing identifiers")
        _need(treatment not in by_plant[plant_id], f"duplicate plant/treatment row: {plant_id}/{treatment}")
        by_plant[plant_id][treatment] = row
        if plant_id in strata:
            _need(strata[plant_id] == stratum, f"mixed stratum within plant: {plant_id}")
        else:
            strata[plant_id] = stratum
    return by_plant, strata


def _paired_differences(
    by_plant: dict[str, dict[str, dict[str, str]]],
    strata: dict[str, str],
    endpoint_id: str,
) -> list[float]:
    a_t, b_t, field, operation = PAIR_SPECS[endpoint_id]
    out: list[float] = []
    for plant_id in sorted(by_plant):
        if strata[plant_id] != "LOW_Y":
            continue
        treatments = by_plant[plant_id]
        if a_t not in treatments or b_t not in treatments:
            continue
        try:
            a = _derived(treatments[a_t], field)
            b = _derived(treatments[b_t], field)
        except ValueError:
            continue
        out.append(_circular_difference_deg(a, b) if operation == "circular_difference_deg" else a - b)
    return out


def _two_group_values(
    by_plant: dict[str, dict[str, dict[str, str]]],
    strata: dict[str, str],
    endpoint_id: str,
) -> tuple[list[float], list[float]]:
    low_t, high_t, field = TWO_GROUP_SPECS[endpoint_id]
    low: list[float] = []
    high: list[float] = []
    for plant_id in sorted(by_plant):
        treatments = by_plant[plant_id]
        try:
            if strata[plant_id] == "LOW_Y" and low_t in treatments:
                low.append(_derived(treatments[low_t], field))
            elif strata[plant_id] == "HIGH_Y" and high_t in treatments:
                high.append(_derived(treatments[high_t], field))
        except ValueError:
            continue
    return low, high


def _validate_precision_provenance(plan: dict, freeze_ctx: dict, margin: dict) -> tuple[int, int, dict]:
    low_n, high_n, source_n = generator._required_n(plan)
    provenance = plan.get("input_provenance")
    _need(isinstance(provenance, dict), "precision plan is missing input provenance")
    for key in ("population_id", "season_id", "fitness_scale_id", "time_horizon_id"):
        _need(provenance.get(key) == freeze_ctx.get(key), f"precision/confirmatory mismatch: {key}")
    _need(provenance.get("confirmatory_dataset_id") == DATASET_ID, "precision plan targets a different confirmatory dataset")
    _need(provenance.get("q5_route") == freeze_ctx.get("q5_route"), "precision q5 route mismatch")
    _need(
        provenance.get("margin_freeze_commit") == margin.get("freeze_metadata", {}).get("freeze_commit"),
        "precision plan uses a different margin freeze",
    )
    _need(provenance.get("confirmatory_outcomes_opened") is False, "precision plan provenance shows opened outcomes")
    return low_n, high_n, source_n


def adjudicate(
    rows: list[dict[str, str]],
    margin_manifest: dict,
    precision_plan: dict,
    structural_y_receipt: dict,
    analysis_freeze: dict,
) -> dict:
    freeze_ctx = generator._validate_analysis_freeze(analysis_freeze)
    bands = generator._validate_y_receipt(structural_y_receipt, freeze_ctx)
    margin_result = margin_validator.validate(margin_manifest)
    _need(margin_manifest.get("schema_version") == MARGIN_SCHEMA, "wrong margin schema")
    mctx = margin_manifest.get("context", {})
    for key in ("population_id", "season_id", "fitness_scale_id", "time_horizon_id"):
        _need(mctx.get(key) == freeze_ctx.get(key), f"margin/confirmatory mismatch: {key}")
    _need(mctx.get("confirmatory_dataset_id") == DATASET_ID, "margin manifest targets a different confirmatory dataset")
    _need(margin_result.get("q5_route") == freeze_ctx.get("q5_route"), "margin q5 route mismatch")
    low_required, high_required, source_n = _validate_precision_provenance(
        precision_plan, freeze_ctx, margin_manifest
    )

    _need(bool(rows), "D0 confirmatory rows are empty")
    for row in rows:
        _need(row.get("dataset_id") == DATASET_ID, "wrong D0 confirmatory dataset id")
        _need(row.get("analysis_partition") == "D0_CONFIRMATORY_QUALIFICATION_ONLY", "wrong analysis partition")
        _need(str(row.get("d0_qualification_eligible", "")).lower() == "true", "row is not D0 qualification eligible")
        _need(str(row.get("g3_g5_eligible", "")).lower() == "false", "D0 qualification row leaked into G3-G5 eligibility")
        for key in ("context_id", "population_id", "season_id", "fitness_scale_id", "time_horizon_id", "primary_y_metric"):
            _need(str(row.get(key, "")).strip() == str(freeze_ctx.get(key, "")).strip(), f"row/freeze mismatch: {key}")

    by_plant, strata = _group_rows(rows)
    low_plants = [p for p in by_plant if strata[p] == "LOW_Y"]
    high_plants = [p for p in by_plant if strata[p] == "HIGH_Y"]
    _need(len(low_plants) >= low_required, "LOW-Y confirmatory plants below precision plan")
    _need(len(high_plants) >= high_required, "HIGH-Y confirmatory plants below precision plan")

    for plant_id in low_plants:
        _need(set(by_plant[plant_id]) == {"S_QUAL", "SHAM_QUAL", "D0_QUAL"}, f"LOW-Y treatment set incomplete: {plant_id}")
    for plant_id in high_plants:
        _need(set(by_plant[plant_id]) == {"D_QUAL"}, f"HIGH-Y treatment set invalid: {plant_id}")

    metric = freeze_ctx["primary_y_metric"]
    metric_field = Y_METRICS.get(metric)
    _need(metric_field is not None, "unregistered primary y metric in confirmatory freeze")
    low_max = float(bands["low_y_max"])
    high_min = float(bands["high_y_min"])
    band_failures: list[str] = []
    for plant_id in low_plants:
        try:
            y = _derived(by_plant[plant_id]["S_QUAL"], metric_field)
        except ValueError:
            band_failures.append(plant_id)
            continue
        if y > low_max:
            band_failures.append(plant_id)
    for plant_id in high_plants:
        try:
            y = _derived(by_plant[plant_id]["D_QUAL"], metric_field)
        except ValueError:
            band_failures.append(plant_id)
            continue
        if y < high_min:
            band_failures.append(plant_id)

    analysis = analysis_freeze["analysis"]
    eq_level = float(analysis["equivalence_ci_level"])
    superiority_alpha = float(analysis["directional_superiority_alpha"])
    burden_level = float(analysis["burden_precision_ci_level"])
    seed = int(analysis["bootstrap_seed"])
    reps = int(analysis["bootstrap_reps"])
    margin_map = {x["endpoint_id"]: x for x in margin_manifest["endpoints"]}
    active_ids = set(margin_result["validated_endpoints"])

    endpoint_results: dict[str, dict] = {}
    seed_offset = 0
    for endpoint_id in sorted(active_ids):
        if endpoint_id == "D0_Q6_HORIZON":
            endpoint_results[endpoint_id] = {
                "pass": True,
                "criterion": "EXACT_IDENTITY",
                "observed": freeze_ctx["time_horizon_id"],
            }
            continue
        margin = float(margin_map[endpoint_id]["value"])
        if endpoint_id in PAIR_SPECS:
            diffs = _paired_differences(by_plant, strata, endpoint_id)
            complete_n = len(diffs)
            floor_pass = complete_n >= low_required
            boot = _bootstrap_mean(diffs, seed + seed_offset, reps) if floor_pass else []
            point = sum(diffs) / complete_n if complete_n else None
            criterion = margin_map[endpoint_id]["criterion_type"]
            if criterion in {"EQUIVALENCE", "CONTAMINATION_BOUND"}:
                ci = _central_ci(boot, eq_level) if boot else None
                passed = bool(ci and ci[0] > -margin and ci[1] < margin)
                detail = {
                    "criterion": criterion,
                    "margin": margin,
                    "ci_level": eq_level,
                    "ci": list(ci) if ci else None,
                }
            elif criterion == "MINIMUM_USEFUL_EFFECT":
                lower = _quantile(boot, superiority_alpha) if boot else None
                passed = lower is not None and lower > margin
                detail = {
                    "criterion": criterion,
                    "minimum_effect": margin,
                    "one_sided_alpha": superiority_alpha,
                    "lower_bound": lower,
                }
            elif criterion == "MAX_CI_HALF_WIDTH":
                ci = _central_ci(boot, burden_level) if boot else None
                half_width = ((ci[1] - ci[0]) / 2) if ci else None
                passed = half_width is not None and half_width <= margin
                detail = {
                    "criterion": criterion,
                    "max_ci_half_width": margin,
                    "ci_level": burden_level,
                    "ci": list(ci) if ci else None,
                    "observed_half_width": half_width,
                }
            else:
                raise ValueError(f"unsupported paired criterion: {endpoint_id}/{criterion}")
            endpoint_results[endpoint_id] = {
                "pass": passed,
                "complete_n": complete_n,
                "required_n": low_required,
                "point_difference": point,
                **detail,
            }
            seed_offset += 1
        elif endpoint_id in TWO_GROUP_SPECS:
            g1, g2 = _two_group_values(by_plant, strata, endpoint_id)
            floor_pass = len(g1) >= source_n["plants_per_group"] and len(g2) >= source_n["plants_per_group"]
            boot = _bootstrap_two_group_difference(g1, g2, seed + seed_offset, reps) if floor_pass else []
            point = (sum(g1) / len(g1) - sum(g2) / len(g2)) if g1 and g2 else None
            ci = _central_ci(boot, eq_level) if boot else None
            passed = bool(ci and ci[0] > -margin and ci[1] < margin)
            endpoint_results[endpoint_id] = {
                "pass": passed,
                "n_d0": len(g1),
                "n_d": len(g2),
                "required_n_per_group": source_n["plants_per_group"],
                "point_difference_d0_minus_d": point,
                "criterion": "EQUIVALENCE",
                "margin": margin,
                "ci_level": eq_level,
                "ci": list(ci) if ci else None,
            }
            seed_offset += 1
        else:
            raise ValueError(f"no confirmatory estimator for active endpoint: {endpoint_id}")

    q1_ids = {x for x in active_ids if x.startswith("D0_Q1_")}
    q2_ids = {x for x in active_ids if x.startswith("D0_Q2_")}
    q3_ids = {x for x in active_ids if x.startswith("D0_Q3_")}
    q4_ids = {x for x in active_ids if x.startswith("D0_Q4_")}
    q5_ids = {x for x in active_ids if x.startswith("D0_Q5_")}
    q6_ids = {"D0_Q6_HORIZON"}

    def gate_pass(ids: set[str]) -> bool:
        return bool(ids) and all(endpoint_results[x]["pass"] for x in ids)

    gates = {
        "D0_Q1_z_preserved": gate_pass(q1_ids),
        "D0_Q2_functional_benefit_matched": gate_pass(q2_ids),
        "D0_Q3_pollination_facing_equivalent": gate_pass(q3_ids),
        "D0_Q4_antagonist_channel_fidelity": gate_pass(q4_ids),
        "D0_Q5_apparatus_burden_accounted": gate_pass(q5_ids),
        "D0_Q6_common_horizon": gate_pass(q6_ids),
    }
    all_pass = all(gates.values()) and not band_failures
    if all_pass:
        final_status = "D0_FULLY_QUALIFIED"
    elif gates["D0_Q2_functional_benefit_matched"]:
        final_status = "D0_FUNCTION_MATCH_ONLY"
    else:
        final_status = "D0_NOT_QUALIFIED"

    q5_endpoint = next(iter(q5_ids)) if q5_ids else None
    burden_receipt = endpoint_results.get(q5_endpoint) if q5_endpoint else None

    return {
        "schema_version": "SLK_PEDICULARIS_D0_CONFIRMATORY_RECEIPT_V1",
        "status": final_status,
        "context": {
            "system": "Pedicularis rex",
            "dataset_id": DATASET_ID,
            "context_id": freeze_ctx["context_id"],
            "population_id": freeze_ctx["population_id"],
            "season_id": freeze_ctx["season_id"],
            "fitness_scale_id": freeze_ctx["fitness_scale_id"],
            "time_horizon_id": freeze_ctx["time_horizon_id"],
            "primary_y_metric": freeze_ctx["primary_y_metric"],
            "q5_route": freeze_ctx["q5_route"],
        },
        "precision_plan": {
            "required_low_y_plants": low_required,
            "required_high_y_plants": high_required,
            "source_allocation_maxima": source_n,
            "observed_low_y_plants": len(low_plants),
            "observed_high_y_plants": len(high_plants),
        },
        "structural_y_band_failure_count": len(band_failures),
        "gates": gates,
        "endpoint_results": endpoint_results,
        "apparatus_burden_receipt": burden_receipt,
        "firewall": {
            "d0_qualification_units_g3_g5_ineligible": True,
            "margins_frozen_before_confirmatory_outcomes": True,
            "q5_route_frozen_before_confirmatory_outcomes": True,
        },
        "claim_ceiling": (
            "D0_COMPARATOR_QUALIFICATION_ONLY; G3_R, G4_K, G5_PHI_REQUIRE_A_NEW_INDEPENDENT_G3_G5_EXPERIMENT"
            if final_status == "D0_FULLY_QUALIFIED"
            else "D0_NOT_FULLY_QUALIFIED_NO_G3_G4_DECOMPOSITION_PROMOTION"
        ),
    }


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description="Adjudicate Pedicularis D0 confirmatory qualification")
    parser.add_argument("confirmatory_csv", type=Path)
    parser.add_argument("margin_manifest_json", type=Path)
    parser.add_argument("precision_plan_json", type=Path)
    parser.add_argument("structural_y_receipt_json", type=Path)
    parser.add_argument("analysis_freeze_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = adjudicate(
        _read_csv(args.confirmatory_csv),
        json.loads(args.margin_manifest_json.read_text(encoding="utf-8")),
        json.loads(args.precision_plan_json.read_text(encoding="utf-8")),
        json.loads(args.structural_y_receipt_json.read_text(encoding="utf-8")),
        json.loads(args.analysis_freeze_json.read_text(encoding="utf-8")),
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
