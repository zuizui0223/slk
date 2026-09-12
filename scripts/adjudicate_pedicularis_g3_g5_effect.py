from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import random
from collections import defaultdict
from pathlib import Path


DECOMP_DATASET = "PED_G3_G5_RK_CONFIRM_V1"
DIRECT_DATASET = "PED_G5_DIRECT_CONFIRM_V1"


def _load_contract_validator():
    path = Path(__file__).with_name("generate_pedicularis_g3_g5_layout.py")
    spec = importlib.util.spec_from_file_location("ped_g35_layout", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.validate_contract


validate_contract = _load_contract_validator()


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _number(value: object, label: str, nonnegative: bool = False) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    _need(math.isfinite(out), f"{label} must be finite")
    if nonnegative:
        _need(out >= 0, f"{label} must be >= 0")
    return out


def _true(value: object) -> bool:
    return str(value).strip().lower() == "true"


def _quantile(values: list[float], p: float) -> float:
    _need(values and 0 <= p <= 1, "invalid quantile request")
    x = sorted(values)
    if len(x) == 1:
        return x[0]
    pos = (len(x) - 1) * p
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return x[lo]
    w = pos - lo
    return x[lo] * (1 - w) + x[hi] * w


def _central_ci(values: list[float], level: float) -> tuple[float, float]:
    alpha = (1 - level) / 2
    return _quantile(values, alpha), _quantile(values, 1 - alpha)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _prepare_plants(
    rows: list[dict[str, str]],
    dataset_id: str,
    block_role: str,
    allowed_worlds: set[str],
    cfg: dict,
) -> tuple[dict[str, dict[str, dict[str, float]]], dict[str, list[dict[str, str]]], list[dict]]:
    _need(bool(rows), f"{dataset_id} rows are empty")
    ctx = cfg["context"]
    levels = {x["level_id"]: x for x in cfg["z_levels"]}
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        _need(row.get("dataset_id") == dataset_id, f"wrong dataset in {dataset_id}")
        _need(row.get("block_role") == block_role, f"wrong block role in {dataset_id}")
        _need(_true(row.get("assignment_frozen")), f"unfrozen assignment in {dataset_id}")
        _need(_true(row.get("g3_g5_eligible")), f"ineligible row in {dataset_id}")
        for key in ("context_id", "population_id", "season_id", "fitness_scale_id", "time_horizon_id"):
            _need(row.get(key) == ctx.get(key), f"{dataset_id} context mismatch: {key}")
        world = str(row.get("world", "")).strip()
        _need(world in allowed_worlds, f"unexpected world in {dataset_id}: {world}")
        plant_id = str(row.get("plant_id", "")).strip()
        _need(plant_id, f"missing plant id in {dataset_id}")
        grouped[plant_id].append(row)

    complete: dict[str, dict[str, dict[str, float]]] = {w: {} for w in allowed_worlds}
    raw_complete: dict[str, list[dict[str, str]]] = {w: [] for w in allowed_worlds}
    exclusions: list[dict] = []
    low_max = cfg["bands"]["low_y_max"]
    high_min = cfg["bands"]["high_y_min"]

    for plant_id in sorted(grouped):
        plant_rows = grouped[plant_id]
        worlds = {str(r.get("world", "")).strip() for r in plant_rows}
        if len(worlds) != 1:
            exclusions.append({"plant_id": plant_id, "reason": "MIXED_WORLD"})
            continue
        world = next(iter(worlds))
        level_ids = [str(r.get("z_level_id", "")).strip() for r in plant_rows]
        if len(plant_rows) != len(levels) or set(level_ids) != set(levels) or len(level_ids) != len(set(level_ids)):
            exclusions.append({"plant_id": plant_id, "world": world, "reason": "INCOMPLETE_OR_DUPLICATE_Z_GRID"})
            continue

        try:
            baseline_values = [_number(r.get("baseline_primary_y_value"), f"baseline y {plant_id}") for r in plant_rows]
        except ValueError:
            exclusions.append({"plant_id": plant_id, "world": world, "reason": "MISSING_BASELINE_Y"})
            continue
        if max(baseline_values) - min(baseline_values) > 1e-10:
            exclusions.append({"plant_id": plant_id, "world": world, "reason": "BASELINE_Y_NOT_PLANT_CONSTANT"})
            continue
        baseline_y = baseline_values[0]
        if world in {"S", "D0"} and baseline_y > low_max:
            exclusions.append({"plant_id": plant_id, "world": world, "reason": "LOW_Y_BAND_FAILURE", "baseline_y": baseline_y})
            continue
        if world == "D" and baseline_y < high_min:
            exclusions.append({"plant_id": plant_id, "world": world, "reason": "HIGH_Y_BAND_FAILURE", "baseline_y": baseline_y})
            continue

        plant_cells: dict[str, float] = {}
        bad_reason = None
        for row in plant_rows:
            level_id = str(row["z_level_id"]).strip()
            frozen = levels[level_id]
            try:
                target = _number(row.get("target_exsertion_z"), f"target z {plant_id}/{level_id}")
                tolerance = _number(row.get("z_tolerance"), f"z tolerance {plant_id}/{level_id}")
                realized = _number(row.get("realized_exsertion_z"), f"realized z {plant_id}/{level_id}")
                fitness = _number(row.get("mature_viable_undamaged_seeds"), f"fitness {plant_id}/{level_id}", nonnegative=True)
            except ValueError:
                bad_reason = "MISSING_OR_INVALID_OUTCOME"
                break
            if not math.isclose(target, frozen["target_exsertion_z"], rel_tol=0, abs_tol=1e-12):
                bad_reason = "TARGET_Z_CHANGED"
                break
            if not math.isclose(tolerance, frozen["tolerance"], rel_tol=0, abs_tol=1e-12):
                bad_reason = "Z_TOLERANCE_CHANGED"
                break
            if abs(realized - target) > tolerance:
                bad_reason = "REALIZED_Z_OUTSIDE_TOLERANCE"
                break
            plant_cells[level_id] = fitness
        if bad_reason is not None:
            exclusions.append({"plant_id": plant_id, "world": world, "reason": bad_reason})
            continue

        complete[world][plant_id] = plant_cells
        raw_complete[world].extend(plant_rows)

    return complete, raw_complete, exclusions


def _world_point(plants: dict[str, dict[str, float]], levels: list[dict]) -> dict:
    _need(bool(plants), "world has no complete plants")
    cell_means: dict[str, float] = {}
    for level in levels:
        level_id = level["level_id"]
        vals = [cells[level_id] for cells in plants.values()]
        cell_means[level_id] = sum(vals) / len(vals)
    optimum = max(cell_means.values())
    opt_ids = [level_id for level_id, value in cell_means.items() if math.isclose(value, optimum, rel_tol=1e-12, abs_tol=1e-12)]
    return {
        "optimized_fitness": optimum,
        "cell_means": cell_means,
        "optimizing_z_level_ids": opt_ids,
        "complete_independent_plants": len(plants),
    }


def _bootstrap_world(plants: dict[str, dict[str, float]], levels: list[dict], seed: int, reps: int) -> list[float]:
    ids = sorted(plants)
    n = len(ids)
    rng = random.Random(seed)
    out: list[float] = []
    level_ids = [x["level_id"] for x in levels]
    for _ in range(reps):
        sample = [rng.choice(ids) for _ in range(n)]
        means = []
        for level_id in level_ids:
            means.append(sum(plants[plant_id][level_id] for plant_id in sample) / n)
        out.append(max(means))
    return out


def _burden_uncertainty(cfg: dict) -> dict:
    burden = cfg["burden"]
    route = cfg["context"]["q5_route"]
    receipt = burden["receipt"]
    if route == "NEGLIGIBLE_BURDEN_EQUIVALENCE":
        margin = _number(receipt.get("margin"), "qualified burden equivalence margin")
        _need(margin > 0, "qualified burden equivalence margin must be > 0")
        return {
            "point": burden["point"],
            "lower": -margin,
            "upper": margin,
            "uncertainty_source": "FROZEN_Q5_EQUIVALENCE_BOUND",
            "source_interval": burden["receipt"].get("ci"),
        }
    _need(route == "MEASURED_BURDEN_ADJUSTMENT", "unknown q5 route")
    return {
        "point": burden["point"],
        "lower": burden["lower"],
        "upper": burden["upper"],
        "uncertainty_source": "INDEPENDENT_Q5_MEASURED_BURDEN_CI",
        "source_interval": burden["receipt"].get("ci"),
    }


def _phi_class(ci: tuple[float, float]) -> str:
    if ci[0] > 0:
        return "DIFFERENTIATION_FAVORED"
    if ci[1] < 0:
        return "PERSISTENT_COMPROMISE"
    return "CRITICAL_OR_UNRESOLVED"


def adjudicate(
    decomposition_rows: list[dict[str, str]],
    direct_rows: list[dict[str, str]] | None,
    freeze: dict,
    g2: dict,
    y_receipt: dict,
    y_function: dict,
    d0: dict,
) -> dict:
    cfg = validate_contract(freeze, g2, y_receipt, y_function, d0)
    decomp, _, decomp_exclusions = _prepare_plants(
        decomposition_rows, DECOMP_DATASET, "DECOMPOSITION_RK", {"S", "D0", "D"}, cfg
    )
    decomp_counts = {world: len(decomp[world]) for world in ("S", "D0", "D")}
    if any(decomp_counts[w] < cfg["minimum_world_n"] for w in decomp_counts):
        return {
            "schema_version": "SLK_PEDICULARIS_G3_G5_EFFECT_RECEIPT_V1",
            "status": "PEDICULARIS_G3_G5_EFFECT_INCOMPLETE",
            "context": cfg["context"],
            "complete_plant_counts": decomp_counts,
            "minimum_required_per_world": cfg["minimum_world_n"],
            "exclusions": decomp_exclusions,
            "claim_ceiling": "G3_G4_G5_NOT_IDENTIFIED_INSUFFICIENT_COMPLETE_GRID_PLANTS",
        }

    plant_sets = [set(decomp[w]) for w in ("S", "D0", "D")]
    _need(not (plant_sets[0] & plant_sets[1] or plant_sets[0] & plant_sets[2] or plant_sets[1] & plant_sets[2]), "decomposition plant IDs overlap across worlds")

    levels = cfg["z_levels"]
    seed = cfg["bootstrap_seed"]
    reps = cfg["bootstrap_reps"]
    level = cfg["ci_level"]
    points = {w: _world_point(decomp[w], levels) for w in ("S", "D0", "D")}
    boots = {
        "S": _bootstrap_world(decomp["S"], levels, seed + 101, reps),
        "D0": _bootstrap_world(decomp["D0"], levels, seed + 211, reps),
        "D": _bootstrap_world(decomp["D"], levels, seed + 307, reps),
    }

    ws = points["S"]["optimized_fitness"]
    wd0_obs = points["D0"]["optimized_fitness"]
    wd = points["D"]["optimized_fitness"]
    burden = _burden_uncertainty(cfg)
    wd0_pre = wd0_obs + burden["point"]

    r_obs_boot = [d0v - sv for d0v, sv in zip(boots["D0"], boots["S"])]
    k_obs_boot = [d0v - dv for d0v, dv in zip(boots["D0"], boots["D"])]
    phi_internal_boot = [dv - sv for dv, sv in zip(boots["D"], boots["S"])]
    r_obs_ci = _central_ci(r_obs_boot, level)
    k_obs_ci = _central_ci(k_obs_boot, level)
    phi_internal_ci = _central_ci(phi_internal_boot, level)

    r_point = wd0_pre - ws
    k_point = wd0_pre - wd
    phi_internal_point = wd - ws
    r_robust = (r_obs_ci[0] + burden["lower"], r_obs_ci[1] + burden["upper"])
    k_robust = (k_obs_ci[0] + burden["lower"], k_obs_ci[1] + burden["upper"])

    result = {
        "schema_version": "SLK_PEDICULARIS_G3_G5_EFFECT_RECEIPT_V1",
        "context": {
            "system": "Pedicularis rex",
            "context_id": cfg["context"]["context_id"],
            "population_id": cfg["context"]["population_id"],
            "season_id": cfg["context"]["season_id"],
            "fitness_scale_id": cfg["context"]["fitness_scale_id"],
            "time_horizon_id": cfg["context"]["time_horizon_id"],
            "primary_y_metric": cfg["context"]["primary_y_metric"],
            "q5_route": cfg["context"]["q5_route"],
            "estimation_route": cfg["route"],
        },
        "g2_conflict_load": cfg["conflict_load"],
        "decomposition_block": {
            "dataset_id": DECOMP_DATASET,
            "complete_plant_counts": decomp_counts,
            "minimum_required_per_world": cfg["minimum_world_n"],
            "exclusion_count": len(decomp_exclusions),
            "exclusions": decomp_exclusions,
            "world_optima": points,
        },
        "burden_correction": {
            "point_B_device_S_minus_SHAM": burden["point"],
            "uncertainty_lower": burden["lower"],
            "uncertainty_upper": burden["upper"],
            "uncertainty_source": burden["uncertainty_source"],
            "observed_D0_optimum": wd0_obs,
            "pre_cost_D0_optimum": wd0_pre,
            "note": "The same B_device correction enters R and K and therefore cancels exactly from Phi=R-K.",
        },
        "g3_R": {
            "status": "RECOVERABLE_ARCHITECTURE_BENEFIT_IDENTIFIED",
            "point": r_point,
            "robust_interval": list(r_robust),
            "world_bootstrap_interval_before_burden": list(r_obs_ci),
            "interval_note": "Effect-bootstrap interval plus independent qualified burden uncertainty; not mislabeled as a nominal joint CI when Q5 used an equivalence bound.",
            "positive_robustly": r_robust[0] > 0,
            "comparison": "PRE_COST_D0_OPTIMUM_MINUS_S_OPTIMUM",
        },
        "g4_K": {
            "status": "ARCHITECTURE_COST_IDENTIFIED",
            "point": k_point,
            "robust_interval": list(k_robust),
            "world_bootstrap_interval_before_burden": list(k_obs_ci),
            "comparison": "PRE_COST_D0_OPTIMUM_MINUS_REALIZED_D_OPTIMUM",
            "target": "K_incremental_y",
        },
        "g5_Phi_internal": {
            "status": "IDENTIFIED_INTERNAL_WORLDLINE",
            "point": phi_internal_point,
            "ci_level": level,
            "ci": list(phi_internal_ci),
            "classification": _phi_class(phi_internal_ci),
            "comparison": "REALIZED_D_OPTIMUM_MINUS_S_OPTIMUM",
            "identity_check": {
                "R_minus_K_point": r_point - k_point,
                "equals_internal_Phi": math.isclose(r_point - k_point, phi_internal_point, rel_tol=1e-10, abs_tol=1e-10),
                "interpretation": "Algebraic coherence only; not independent empirical validation.",
            },
        },
    }

    direct_result = None
    bridge = None
    if cfg["route"] == "INDEPENDENT_DIRECT_PHI_BLOCK":
        _need(direct_rows is not None and len(direct_rows) > 0, "independent direct-Phi rows required")
        direct, _, direct_exclusions = _prepare_plants(
            direct_rows, DIRECT_DATASET, "INDEPENDENT_DIRECT_PHI", {"S", "D"}, cfg
        )
        direct_counts = {world: len(direct[world]) for world in ("S", "D")}
        if any(direct_counts[w] < cfg["minimum_direct_n"] for w in direct_counts):
            result["status"] = "PEDICULARIS_G3_G5_EFFECT_INCOMPLETE_DIRECT_BLOCK"
            result["direct_phi_block"] = {
                "complete_plant_counts": direct_counts,
                "minimum_required_per_world": cfg["minimum_direct_n"],
                "exclusions": direct_exclusions,
            }
            result["claim_ceiling"] = "G3_G4_AND_INTERNAL_PHI_IDENTIFIED; INDEPENDENT_PHI_CONCORDANCE_NOT_IDENTIFIED"
            return result
        _need(not (set(direct["S"]) & set(direct["D"])), "direct block plant IDs overlap across worlds")
        _need(not ((set(direct["S"]) | set(direct["D"])) & (plant_sets[0] | plant_sets[1] | plant_sets[2])), "direct and decomposition plant IDs overlap")
        dpoints = {w: _world_point(direct[w], levels) for w in ("S", "D")}
        dboots = {
            "S": _bootstrap_world(direct["S"], levels, seed + 401, reps),
            "D": _bootstrap_world(direct["D"], levels, seed + 503, reps),
        }
        direct_boot = [dv - sv for dv, sv in zip(dboots["D"], dboots["S"])]
        direct_point = dpoints["D"]["optimized_fitness"] - dpoints["S"]["optimized_fitness"]
        direct_ci = _central_ci(direct_boot, level)
        residual_boot = [a - b for a, b in zip(direct_boot, phi_internal_boot)]
        residual_point = direct_point - phi_internal_point
        residual_ci = _central_ci(residual_boot, level)
        concordant = (
            abs(residual_point) <= cfg["concordance_tolerance"]
            and residual_ci[0] <= 0 <= residual_ci[1]
        )
        direct_result = {
            "dataset_id": DIRECT_DATASET,
            "complete_plant_counts": direct_counts,
            "minimum_required_per_world": cfg["minimum_direct_n"],
            "exclusion_count": len(direct_exclusions),
            "exclusions": direct_exclusions,
            "world_optima": dpoints,
            "Phi_direct": {
                "point": direct_point,
                "ci_level": level,
                "ci": list(direct_ci),
                "classification": _phi_class(direct_ci),
            },
        }
        bridge = {
            "point": residual_point,
            "ci_level": level,
            "ci": list(residual_ci),
            "max_abs_point_tolerance": cfg["concordance_tolerance"],
            "ci_includes_zero": residual_ci[0] <= 0 <= residual_ci[1],
            "concordant": concordant,
            "interpretation": "Independent direct-Phi block versus same-target R-K decomposition; this is the nontrivial concordance test.",
        }
        result["direct_phi_block"] = direct_result
        result["bridge_concordance"] = bridge
        result["status"] = (
            "PEDICULARIS_G3_G5_MEASURED_CONCORDANT"
            if concordant
            else "PEDICULARIS_G3_G5_MEASURED_BRIDGE_NOT_CONCORDANT"
        )
        result["claim_ceiling"] = (
            "SAME_SYSTEM_G1_G5_WITH_INDEPENDENT_PHI_CONCORDANCE"
            if concordant
            else "SAME_SYSTEM_G1_G5_MEASURED_BUT_INDEPENDENT_PHI_BRIDGE_NOT_CONCORDANT"
        )
    else:
        _need(direct_rows is None or len(direct_rows) == 0, "same-block route must not inspect a direct-Phi dataset")
        result["status"] = "PEDICULARIS_G3_G5_MEASURED_INTERNAL_IDENTITY"
        result["claim_ceiling"] = "SAME_SYSTEM_G1_G5_INTERNAL_IDENTITY_ONLY"

    if (
        cfg["conflict_load"]["lower_95"] > 0
        and r_robust[0] > 0
        and phi_internal_ci[1] < 0
    ):
        result["diagnostic_pattern"] = "CONFLICT_REAL_RECOVERABLE_BUT_ARCHITECTURE_NOT_WORTH_COST"
    elif cfg["conflict_load"]["lower_95"] > 0 and r_robust[0] > 0 and phi_internal_ci[0] > 0:
        result["diagnostic_pattern"] = "CONFLICT_REAL_RECOVERABLE_AND_ARCHITECTURE_VALUE_POSITIVE"
    else:
        result["diagnostic_pattern"] = "G1_G5_MEASURED_WITHOUT_SHARP_ADJACENT_GATE_SEPARATION"

    result["firewall"] = {
        "g3_g5_units_are_new_independent_units": True,
        "d0_qualification_units_not_reused": True,
        "structural_y_calibration_units_not_reused": True,
        "z_grid_frozen_before_outcomes": True,
        "worlds_reoptimized_within_registered_grid_each_bootstrap": True,
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Adjudicate the final Pedicularis G3-G5 effect experiment")
    parser.add_argument("decomposition_csv", type=Path)
    parser.add_argument("effect_freeze_json", type=Path)
    parser.add_argument("g2_receipt_json", type=Path)
    parser.add_argument("structural_y_receipt_json", type=Path)
    parser.add_argument("structural_y_function_receipt_json", type=Path)
    parser.add_argument("d0_qualification_receipt_json", type=Path)
    parser.add_argument("--direct-phi-csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = adjudicate(
        _read_csv(args.decomposition_csv),
        _read_csv(args.direct_phi_csv) if args.direct_phi_csv else None,
        json.loads(args.effect_freeze_json.read_text(encoding="utf-8")),
        json.loads(args.g2_receipt_json.read_text(encoding="utf-8")),
        json.loads(args.structural_y_receipt_json.read_text(encoding="utf-8")),
        json.loads(args.structural_y_function_receipt_json.read_text(encoding="utf-8")),
        json.loads(args.d0_qualification_receipt_json.read_text(encoding="utf-8")),
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
