from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import NormalDist, mean, stdev

D0_DATASET_ID = "PED_D0_CAL_V1"

PAIR_SPECS = {
    "D0_Q1_Z": ("D0_CAL", "SHAM_CAL", "exsertion_z", "difference"),
    "D0_Q1_OPENING": ("D0_CAL", "SHAM_CAL", "opening_width_mm", "difference"),
    "D0_Q1_STIGMA": ("D0_CAL", "SHAM_CAL", "stigma_position_mm", "difference"),
    "D0_Q1_ORIENTATION": ("D0_CAL", "SHAM_CAL", "orientation_deg", "circular_difference_deg"),
    "D0_Q1_DAMAGE": ("D0_CAL", "SHAM_CAL", "mechanical_damage_post_prop", "difference"),
    "D0_Q3_VISIT": ("D0_CAL", "SHAM_CAL", "visit_rate_per_min", "difference"),
    "D0_Q3_POLLEN": ("D0_CAL", "SHAM_CAL", "pollen_receipt_grains", "difference"),
    "D0_Q3_INITIAL_SEED": ("D0_CAL", "SHAM_CAL", "initial_seed_set_prop", "difference"),
    "D0_Q4_WET_EFFECT": ("SHAM_CAL", "D0_CAL", "early_attack_prop", "difference"),
    "D0_Q4_DRY_RESIDUAL": ("SHAM_CAL", "S_CAL", "early_attack_prop", "difference"),
    "D0_Q5_BURDEN_EQ": ("S_CAL", "SHAM_CAL", "mature_viable_undamaged_seeds", "difference"),
    "D0_Q5_BURDEN_PRECISION": ("S_CAL", "SHAM_CAL", "mature_viable_undamaged_seeds", "difference"),
}

TWO_GROUP_SPECS = {
    "D0_Q2_VOLUME": ("D0_CAL", "D_CAL", "retention_mean_max_ml"),
    "D0_Q2_DURATION": ("D0_CAL", "D_CAL", "retention_mean_half_life_min"),
    "D0_Q2_COVERAGE": ("D0_CAL", "D_CAL", "retention_mean_protected_fraction"),
    "D0_Q2_PROTECTION": ("D0_CAL", "D_CAL", "early_attack_prop"),
}

PROPORTION_FIELDS = {
    "mechanical_damage_post_prop",
    "initial_seed_set_prop",
    "early_attack_prop",
    "seed_predation_prop",
    "retention_trial1_protected_fraction",
    "retention_trial2_protected_fraction",
}


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _z(p: float) -> float:
    _need(0 < p < 1, "probability must be in (0,1)")
    return NormalDist().inv_cdf(p)


def _number(row: dict[str, str], field: str) -> float | None:
    raw = str(row.get(field, "")).strip()
    if raw == "":
        return None
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"non-numeric {field}: {raw}") from exc
    _need(math.isfinite(value), f"non-finite {field}")
    if field in PROPORTION_FIELDS:
        _need(0 <= value <= 1, f"{field} must be in [0,1]")
    return value


def _mean_available(values: list[float | None]) -> float | None:
    keep = [x for x in values if x is not None]
    if not keep:
        return None
    return sum(keep) / len(keep)


def _derived(row: dict[str, str], field: str) -> float | None:
    if field == "visit_rate_per_min":
        visits = _number(row, "legitimate_visits")
        minutes = _number(row, "pollinator_observation_minutes")
        if visits is None or minutes is None:
            return None
        _need(minutes > 0, "pollinator observation minutes must be positive")
        return visits / minutes
    if field == "retention_mean_max_ml":
        return _mean_available([
            _number(row, "retention_trial1_max_ml"),
            _number(row, "retention_trial2_max_ml"),
        ])
    if field == "retention_mean_half_life_min":
        return _mean_available([
            _number(row, "retention_trial1_half_life_min"),
            _number(row, "retention_trial2_half_life_min"),
        ])
    if field == "retention_mean_protected_fraction":
        return _mean_available([
            _number(row, "retention_trial1_protected_fraction"),
            _number(row, "retention_trial2_protected_fraction"),
        ])
    return _number(row, field)


def _circular_difference_deg(a: float, b: float) -> float:
    return ((a - b + 180.0) % 360.0) - 180.0


def _by_plant(rows: list[dict[str, str]]) -> tuple[dict[str, dict[str, dict[str, str]]], dict[str, dict[str, dict[str, str]]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        _need(row.get("dataset_id") == D0_DATASET_ID, "wrong D0-CAL dataset id")
        plant_id = str(row.get("plant_id", "")).strip()
        _need(plant_id, "missing plant_id")
        grouped[plant_id].append(row)

    low: dict[str, dict[str, dict[str, str]]] = {}
    high: dict[str, dict[str, dict[str, str]]] = {}
    for plant_id, plant_rows in grouped.items():
        strata = {str(x.get("phenotype_stratum", "")).strip() for x in plant_rows}
        _need(len(strata) == 1, f"mixed phenotype stratum: {plant_id}")
        treatments: dict[str, dict[str, str]] = {}
        for row in plant_rows:
            treatment = str(row.get("treatment", "")).strip()
            _need(treatment and treatment not in treatments, f"duplicate treatment: {plant_id}/{treatment}")
            treatments[treatment] = row
        stratum = next(iter(strata))
        if stratum == "LOW_Y":
            low[plant_id] = treatments
        elif stratum == "HIGH_Y":
            high[plant_id] = treatments
        else:
            raise ValueError(f"invalid phenotype stratum: {plant_id}/{stratum}")
    _need(low and high, "joint simulation requires LOW-Y and HIGH-Y D0-CAL plants")
    return low, high


def _low_vector(treatments: dict[str, dict[str, str]], endpoint_ids: list[str]) -> dict[str, float | None]:
    vector: dict[str, float | None] = {}
    for endpoint_id in endpoint_ids:
        if endpoint_id in PAIR_SPECS:
            a_t, b_t, field, operation = PAIR_SPECS[endpoint_id]
            if a_t not in treatments or b_t not in treatments:
                vector[endpoint_id] = None
                continue
            a = _derived(treatments[a_t], field)
            b = _derived(treatments[b_t], field)
            if a is None or b is None:
                vector[endpoint_id] = None
            else:
                vector[endpoint_id] = (
                    _circular_difference_deg(a, b)
                    if operation == "circular_difference_deg"
                    else a - b
                )
        elif endpoint_id in TWO_GROUP_SPECS:
            low_t, _high_t, field = TWO_GROUP_SPECS[endpoint_id]
            row = treatments.get(low_t)
            vector[endpoint_id] = None if row is None else _derived(row, field)
    return vector


def _high_vector(treatments: dict[str, dict[str, str]], endpoint_ids: list[str]) -> dict[str, float | None]:
    vector: dict[str, float | None] = {}
    for endpoint_id in endpoint_ids:
        if endpoint_id in TWO_GROUP_SPECS:
            _low_t, high_t, field = TWO_GROUP_SPECS[endpoint_id]
            row = treatments.get(high_t)
            vector[endpoint_id] = None if row is None else _derived(row, field)
    return vector


def _shift_complete(values: list[float | None], target_mean: float) -> list[float | None]:
    keep = [x for x in values if x is not None]
    _need(len(keep) >= 2, "planning endpoint has fewer than two calibration values")
    shift = target_mean - mean(keep)
    return [None if x is None else x + shift for x in values]


def _prepare_planning_vectors(
    low_vectors: list[dict[str, float | None]],
    high_vectors: list[dict[str, float | None]],
    compiled_precision_input: dict,
) -> tuple[list[dict[str, float | None]], list[dict[str, float | None]]]:
    endpoint_specs = {x["endpoint_id"]: x for x in compiled_precision_input["endpoints"]}

    out_low = [dict(x) for x in low_vectors]
    out_high = [dict(x) for x in high_vectors]

    for endpoint_id, spec in endpoint_specs.items():
        if endpoint_id in PAIR_SPECS:
            values = [x.get(endpoint_id) for x in out_low]
            if spec["kind"] in {"paired_equivalence"}:
                target = 0.0
            elif spec["kind"] == "paired_superiority":
                target = float(spec["planning_effect"])
            elif spec["kind"] == "mean_precision":
                keep = [x for x in values if x is not None]
                _need(keep, f"no calibration values: {endpoint_id}")
                target = mean(keep)
            else:
                raise ValueError(f"unsupported paired simulation kind: {endpoint_id}/{spec['kind']}")
            shifted = _shift_complete(values, target)
            for vector, value in zip(out_low, shifted):
                vector[endpoint_id] = value

        elif endpoint_id in TWO_GROUP_SPECS:
            low_values = [x.get(endpoint_id) for x in out_low]
            high_values = [x.get(endpoint_id) for x in out_high]
            low_keep = [x for x in low_values if x is not None]
            high_keep = [x for x in high_values if x is not None]
            _need(len(low_keep) >= 2 and len(high_keep) >= 2, f"too few Q2 calibration values: {endpoint_id}")
            common_center = 0.5 * (mean(low_keep) + mean(high_keep))
            low_shifted = _shift_complete(low_values, common_center)
            high_shifted = _shift_complete(high_values, common_center)
            for vector, value in zip(out_low, low_shifted):
                vector[endpoint_id] = value
            for vector, value in zip(out_high, high_shifted):
                vector[endpoint_id] = value
        else:
            raise ValueError(f"no simulation mapping for endpoint: {endpoint_id}")

    return out_low, out_high


def _sample_vectors(
    vectors: list[dict[str, float | None]],
    n_recruit: int,
    attrition: float,
    rng: random.Random,
) -> list[dict[str, float | None]]:
    _need(n_recruit >= 2, "candidate recruitment n must be >=2")
    sampled = [vectors[rng.randrange(len(vectors))] for _ in range(n_recruit)]
    return [x for x in sampled if rng.random() >= attrition]


def _sample_sd(values: list[float]) -> float | None:
    return stdev(values) if len(values) >= 2 else None


def _paired_pass(values: list[float], spec: dict, alpha: float) -> bool:
    n = len(values)
    if n < 2:
        return False
    sd = _sample_sd(values)
    if sd is None:
        return False
    se = sd / math.sqrt(n)
    m = mean(values)
    kind = spec["kind"]
    if kind == "paired_equivalence":
        z = _z(1 - alpha)
        margin = float(spec["margin"])
        return (m - z * se > -margin) and (m + z * se < margin)
    if kind == "paired_superiority":
        z = _z(1 - alpha if spec.get("directional", False) else 1 - alpha / 2)
        return m - z * se > float(spec["min_effect"])
    if kind == "mean_precision":
        z = _z(1 - alpha / 2)
        return z * se <= float(spec["half_width"])
    raise ValueError(f"unsupported paired kind: {kind}")


def _two_group_pass(g1: list[float], g2: list[float], spec: dict, alpha: float) -> bool:
    if len(g1) < 2 or len(g2) < 2:
        return False
    s1 = _sample_sd(g1)
    s2 = _sample_sd(g2)
    if s1 is None or s2 is None:
        return False
    se = math.sqrt(s1 * s1 / len(g1) + s2 * s2 / len(g2))
    diff = mean(g1) - mean(g2)
    z = _z(1 - alpha)
    margin = float(spec["margin"])
    return (diff - z * se > -margin) and (diff + z * se < margin)


def _mc_interval(successes: int, reps: int, level: float = 0.95) -> tuple[float, float]:
    _need(reps > 0, "simulation reps must be positive")
    p = successes / reps
    z = _z(0.5 + level / 2)
    # Wilson interval; avoids pathological negative lower bounds.
    denom = 1 + z * z / reps
    center = (p + z * z / (2 * reps)) / denom
    half = z * math.sqrt(p * (1 - p) / reps + z * z / (4 * reps * reps)) / denom
    return max(0.0, center - half), min(1.0, center + half)


def simulate_candidate(
    low_vectors: list[dict[str, float | None]],
    high_vectors: list[dict[str, float | None]],
    compiled_precision_input: dict,
    n_low_recruit: int,
    n_high_recruit: int,
    reps: int,
    seed: int,
) -> dict:
    defaults = compiled_precision_input["defaults"]
    attrition = float(defaults["attrition"])
    alpha_default = float(defaults["alpha"])
    endpoint_specs = {x["endpoint_id"]: x for x in compiled_precision_input["endpoints"]}
    endpoint_ids = sorted(endpoint_specs)
    rng = random.Random(seed)

    endpoint_passes = {endpoint_id: 0 for endpoint_id in endpoint_ids}
    gate_names = ["Q1", "Q2", "Q3", "Q4", "Q5"]
    gate_passes = {gate: 0 for gate in gate_names}
    all_passes = 0
    low_pool_too_small = 0
    high_pool_too_small = 0
    failure_patterns: dict[str, int] = {}

    planning_low, planning_high = _prepare_planning_vectors(
        low_vectors, high_vectors, compiled_precision_input
    )

    for _ in range(reps):
        low_sample = _sample_vectors(planning_low, n_low_recruit, attrition, rng)
        high_sample = _sample_vectors(planning_high, n_high_recruit, attrition, rng)

        if len(low_sample) < 2:
            low_pool_too_small += 1
        if len(high_sample) < 2:
            high_pool_too_small += 1

        passed_ids: list[str] = []
        failed_ids: list[str] = []

        for endpoint_id in endpoint_ids:
            spec = endpoint_specs[endpoint_id]
            alpha = float(spec.get("alpha", alpha_default))
            if endpoint_id in PAIR_SPECS:
                values = [x.get(endpoint_id) for x in low_sample]
                complete = [x for x in values if x is not None]
                passed = len(complete) >= 2 and _paired_pass(
                    complete, spec, alpha
                )
            else:
                g1 = [x.get(endpoint_id) for x in low_sample]
                g2 = [x.get(endpoint_id) for x in high_sample]
                g1c = [x for x in g1 if x is not None]
                g2c = [x for x in g2 if x is not None]
                passed = (
                    len(g1c) >= 2
                    and len(g2c) >= 2
                    and _two_group_pass(g1c, g2c, spec, alpha)
                )
            if passed:
                endpoint_passes[endpoint_id] += 1
                passed_ids.append(endpoint_id)
            else:
                failed_ids.append(endpoint_id)

        for gate in gate_names:
            gate_ids = [
                endpoint_id
                for endpoint_id in endpoint_ids
                if endpoint_id.startswith(f"D0_{gate}_")
            ]
            if gate_ids and all(
                endpoint_id in passed_ids for endpoint_id in gate_ids
            ):
                gate_passes[gate] += 1

        if not failed_ids:
            all_passes += 1
        pattern = ";".join(failed_ids) if failed_ids else "ALL_PASS"
        failure_patterns[pattern] = failure_patterns.get(pattern, 0) + 1

    all_pass_probability = all_passes / reps
    ci = _mc_interval(all_passes, reps)
    return {
        "n_low_recruit": n_low_recruit,
        "n_high_recruit": n_high_recruit,
        "field_burden": 3 * n_low_recruit + n_high_recruit,
        "simulation_reps": reps,
        "all_pass_probability": all_pass_probability,
        "all_pass_mc_interval_95": list(ci),
        "endpoint_pass_probabilities": {
            endpoint_id: endpoint_passes[endpoint_id] / reps
            for endpoint_id in endpoint_ids
        },
        "gate_pass_probabilities": {
            gate: gate_passes[gate] / reps for gate in gate_names
        },
        "low_retained_pool_below_two_probability": low_pool_too_small / reps,
        "high_retained_pool_below_two_probability": high_pool_too_small / reps,
        "failure_pattern_frequencies": dict(
            sorted(failure_patterns.items(), key=lambda item: (-item[1], item[0]))
        ),
    }


def simulate_joint_power(
    calibration_rows: list[dict[str, str]],
    compiled_precision_input: dict,
    planned_precision_output: dict,
    candidate_allocations: list[dict[str, int]],
    reps: int,
    seed: int,
    mc_level: float = 0.95,
) -> dict:
    _need(reps >= 1000, "joint simulation requires at least 1000 reps")
    _need(isinstance(seed, int), "simulation seed must be integer")
    _need(candidate_allocations, "candidate allocation grid is empty")
    _need(0 < mc_level < 1, "mc_level must be in (0,1)")

    endpoint_ids = [x["endpoint_id"] for x in compiled_precision_input["endpoints"]]
    low_by_plant, high_by_plant = _by_plant(calibration_rows)
    low_vectors = [_low_vector(x, endpoint_ids) for x in low_by_plant.values()]
    high_vectors = [_high_vector(x, endpoint_ids) for x in high_by_plant.values()]

    payload = json.loads(json.dumps(compiled_precision_input))

    target = float(
        planned_precision_output["joint_qualification_design"][
            "target_all_pass_power"
        ]
    )
    results: list[dict] = []
    for index, candidate in enumerate(candidate_allocations):
        n_low = int(candidate["n_low_recruit"])
        n_high = int(candidate["n_high_recruit"])
        result = simulate_candidate(
            low_vectors,
            high_vectors,
            payload,
            n_low,
            n_high,
            reps,
            seed + 100003 * index,
        )
        # Recompute CI at requested level if non-default.
        successes = round(result["all_pass_probability"] * reps)
        result["all_pass_mc_interval"] = list(_mc_interval(successes, reps, mc_level))
        result["meets_joint_target_by_lower_mc_bound"] = (
            result["all_pass_mc_interval"][0] >= target
        )
        results.append(result)

    feasible = [x for x in results if x["meets_joint_target_by_lower_mc_bound"]]
    selected = (
        min(feasible, key=lambda x: (x["field_burden"], x["n_low_recruit"], x["n_high_recruit"]))
        if feasible
        else None
    )
    return {
        "schema_version": "SLK_PEDICULARIS_D0_JOINT_POWER_SIMULATION_V1",
        "status": (
            "JOINT_SIMULATION_DESIGN_FOUND"
            if selected is not None
            else "NO_CANDIDATE_REACHES_JOINT_TARGET"
        ),
        "simulation_model": "WHOLE_PLANT_EMPIRICAL_RESAMPLING_NORMAL_APPROX_ENDPOINT_ADJUDICATION",
        "simulation_seed": seed,
        "simulation_reps": reps,
        "mc_interval_level": mc_level,
        "target_all_pass_power": target,
        "candidate_results": results,
        "selected_allocation": selected,
        "claim_ceiling": "PROSPECTIVE_SAMPLE_SIZE_DESIGN_ONLY_NO_BIOLOGICAL_D0_RESULT",
    }


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate Pedicularis D0 full-qualification power from independent D0-CAL")
    parser.add_argument("d0_cal_csv", type=Path)
    parser.add_argument("compiled_precision_input_json", type=Path)
    parser.add_argument("planned_precision_output_json", type=Path)
    parser.add_argument("candidate_grid_json", type=Path)
    parser.add_argument("--reps", type=int, default=5000)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--mc-level", type=float, default=0.95)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    candidates = json.loads(args.candidate_grid_json.read_text(encoding="utf-8"))
    result = simulate_joint_power(
        _read_csv(args.d0_cal_csv),
        json.loads(args.compiled_precision_input_json.read_text(encoding="utf-8")),
        json.loads(args.planned_precision_output_json.read_text(encoding="utf-8")),
        candidates["candidate_allocations"],
        args.reps,
        args.seed,
        args.mc_level,
    )
    text_out = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text_out, encoding="utf-8")
    else:
        print(text_out, end="")


if __name__ == "__main__":
    main()
