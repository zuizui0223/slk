from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import stdev


SCHEMA = "SLK_PEDICULARIS_D0_VARIANCE_INPUT_V1"
D0_DATASET_ID = "PED_D0_CAL_V1"
Y_DATASET_ID = "PED_Y_CAL_V1"
FITNESS_SCALE_ID = "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER"
LOW_FLOOR = 24
HIGH_FLOOR = 24

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
    if field == "pollinator_observation_minutes":
        _need(value > 0, "pollinator_observation_minutes must be > 0")
    return value


def _mean_available(values: list[float | None]) -> float | None:
    keep = [x for x in values if x is not None]
    if not keep:
        return None
    return sum(keep) / len(keep)


def _derived_value(row: dict[str, str], endpoint: str) -> float | None:
    if endpoint == "visit_rate_per_min":
        visits = _number(row, "legitimate_visits")
        minutes = _number(row, "pollinator_observation_minutes")
        if visits is None or minutes is None:
            return None
        return visits / minutes
    if endpoint == "retention_mean_max_ml":
        return _mean_available([
            _number(row, "retention_trial1_max_ml"),
            _number(row, "retention_trial2_max_ml"),
        ])
    if endpoint == "retention_mean_half_life_min":
        return _mean_available([
            _number(row, "retention_trial1_half_life_min"),
            _number(row, "retention_trial2_half_life_min"),
        ])
    if endpoint == "retention_mean_protected_fraction":
        return _mean_available([
            _number(row, "retention_trial1_protected_fraction"),
            _number(row, "retention_trial2_protected_fraction"),
        ])
    return _number(row, endpoint)


def _circular_difference_deg(a: float, b: float) -> float:
    return ((a - b + 180.0) % 360.0) - 180.0


def _one_per_treatment(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    by_treatment: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_treatment[row.get("treatment", "")].append(row)
    out: dict[str, dict[str, str]] = {}
    for treatment, items in by_treatment.items():
        _need(len(items) == 1, f"expected one row per plant/treatment, found {len(items)} for {treatment}")
        out[treatment] = items[0]
    return out


def _sample_sd(values: list[float]) -> float | None:
    if len(values) < 2:
        return None
    return float(stdev(values))


def _pooled_sd(group1: list[float], group2: list[float]) -> float | None:
    if len(group1) < 2 or len(group2) < 2:
        return None
    s1 = stdev(group1)
    s2 = stdev(group2)
    df = len(group1) + len(group2) - 2
    if df <= 0:
        return None
    return math.sqrt(((len(group1) - 1) * s1 * s1 + (len(group2) - 1) * s2 * s2) / df)


def _paired_receipt(low_by_plant: dict[str, dict[str, dict[str, str]]], endpoint_id: str) -> dict:
    treatment_a, treatment_b, field, operation = PAIR_SPECS[endpoint_id]
    diffs: list[float] = []
    for plant_id in sorted(low_by_plant):
        treatment_rows = low_by_plant[plant_id]
        if treatment_a not in treatment_rows or treatment_b not in treatment_rows:
            continue
        a = _derived_value(treatment_rows[treatment_a], field)
        b = _derived_value(treatment_rows[treatment_b], field)
        if a is None or b is None:
            continue
        diff = _circular_difference_deg(a, b) if operation == "circular_difference_deg" else a - b
        diffs.append(diff)
    sd = _sample_sd(diffs)
    meets = len(diffs) >= LOW_FLOOR and sd is not None and sd > 0
    return {
        "endpoint_id": endpoint_id,
        "variance_kind": "sd_diff",
        "value": sd,
        "analysis_unit": "independent_plant",
        "calibration_dataset_id": D0_DATASET_ID,
        "analysis_n": len(diffs),
        "registered_floor_n": LOW_FLOOR,
        "meets_registered_floor": meets,
        "raw_endpoint": field,
        "contrast": f"{treatment_a}_MINUS_{treatment_b}",
        "mean_difference": (sum(diffs) / len(diffs)) if diffs else None,
    }


def _two_group_receipt(low_by_plant: dict[str, dict[str, dict[str, str]]], high_by_plant: dict[str, dict[str, dict[str, str]]], endpoint_id: str) -> dict:
    treatment_low, treatment_high, field = TWO_GROUP_SPECS[endpoint_id]
    g1: list[float] = []
    g2: list[float] = []
    for plant_id in sorted(low_by_plant):
        row = low_by_plant[plant_id].get(treatment_low)
        if row is not None:
            value = _derived_value(row, field)
            if value is not None:
                g1.append(value)
    for plant_id in sorted(high_by_plant):
        row = high_by_plant[plant_id].get(treatment_high)
        if row is not None:
            value = _derived_value(row, field)
            if value is not None:
                g2.append(value)
    sd = _pooled_sd(g1, g2)
    meets = len(g1) >= LOW_FLOOR and len(g2) >= HIGH_FLOOR and sd is not None and sd > 0
    return {
        "endpoint_id": endpoint_id,
        "variance_kind": "sd",
        "value": sd,
        "analysis_unit": "independent_plant",
        "calibration_dataset_id": D0_DATASET_ID,
        "analysis_n_group_d0": len(g1),
        "analysis_n_group_d": len(g2),
        "registered_floor_n_group_d0": LOW_FLOOR,
        "registered_floor_n_group_d": HIGH_FLOOR,
        "meets_registered_floor": meets,
        "raw_endpoint": field,
        "contrast": f"{treatment_low}_VERSUS_{treatment_high}",
        "mean_d0": (sum(g1) / len(g1)) if g1 else None,
        "mean_d": (sum(g2) / len(g2)) if g2 else None,
    }


def summarize(rows: list[dict[str, str]], confirmatory_dataset_id: str, alpha: float = 0.05, power: float = 0.80, attrition: float = 0.15) -> dict:
    _need(bool(rows), "D0-CAL rows are empty")
    _need(confirmatory_dataset_id and confirmatory_dataset_id != D0_DATASET_ID, "invalid confirmatory_dataset_id")
    _need(0 < alpha < 1, "alpha must be in (0,1)")
    _need(0 < power < 1, "power must be in (0,1)")
    _need(0 <= attrition < 1, "attrition must be in [0,1)")

    for row in rows:
        _need(row.get("dataset_id") == D0_DATASET_ID, "wrong dataset_id in D0-CAL")
        _need(str(row.get("confirmatory_eligible", "")).strip().lower() == "false", "calibration row marked confirmatory eligible")

    contexts = {
        (
            row.get("context_id"),
            row.get("population_id"),
            row.get("season_id"),
            row.get("fitness_scale_id"),
            row.get("time_horizon_id"),
        )
        for row in rows
    }
    _need(len(contexts) == 1, "D0-CAL contains multiple contexts")
    context_id, population_id, season_id, fitness_scale_id, time_horizon_id = next(iter(contexts))
    _need(bool(context_id and population_id and season_id and fitness_scale_id and time_horizon_id), "D0-CAL context fields must be non-empty")
    _need(fitness_scale_id == FITNESS_SCALE_ID, "wrong D0-CAL fitness scale")

    raw_by_plant: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        plant_id = str(row.get("plant_id", "")).strip()
        _need(plant_id, "missing plant_id")
        raw_by_plant[plant_id].append(row)

    low_by_plant: dict[str, dict[str, dict[str, str]]] = {}
    high_by_plant: dict[str, dict[str, dict[str, str]]] = {}
    for plant_id, plant_rows in raw_by_plant.items():
        strata = {row.get("phenotype_stratum") for row in plant_rows}
        _need(len(strata) == 1, f"mixed phenotype stratum for {plant_id}")
        treatments = _one_per_treatment(plant_rows)
        stratum = next(iter(strata))
        if stratum == "LOW_Y":
            low_by_plant[plant_id] = treatments
        elif stratum == "HIGH_Y":
            high_by_plant[plant_id] = treatments
        else:
            raise ValueError(f"invalid D0-CAL stratum for {plant_id}: {stratum}")

    _need(len(low_by_plant) >= LOW_FLOOR, "fewer than 24 LOW-Y calibration plants")
    _need(len(high_by_plant) >= HIGH_FLOOR, "fewer than 24 HIGH-Y calibration plants")

    endpoint_rows = [
        _paired_receipt(low_by_plant, endpoint_id) for endpoint_id in PAIR_SPECS
    ] + [
        _two_group_receipt(low_by_plant, high_by_plant, endpoint_id) for endpoint_id in TWO_GROUP_SPECS
    ]
    endpoint_rows.sort(key=lambda x: x["endpoint_id"])
    all_ready = all(row["meets_registered_floor"] for row in endpoint_rows)

    return {
        "schema_version": SCHEMA,
        "status": "INDEPENDENT_CALIBRATION_VARIANCE_READY" if all_ready else "INDEPENDENT_CALIBRATION_VARIANCE_INCOMPLETE",
        "context": {
            "system": "Pedicularis rex",
            "context_id": context_id,
            "population_id": population_id,
            "season_id": season_id,
            "fitness_scale_id": fitness_scale_id,
            "time_horizon_id": time_horizon_id,
            "y_cal_dataset_id": Y_DATASET_ID,
            "d0_cal_dataset_id": D0_DATASET_ID,
            "confirmatory_dataset_id": confirmatory_dataset_id,
            "confirmatory_outcomes_opened": False,
        },
        "planner_defaults": {"alpha": alpha, "power": power, "attrition": attrition},
        "endpoints": endpoint_rows,
        "source_counts": {"low_y_plants": len(low_by_plant), "high_y_plants": len(high_by_plant)},
        "claim_ceiling": "CALIBRATION_VARIANCE_ONLY_NO_D0_OR_G3_G5_EFFECT",
    }


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize completed Pedicularis D0-CAL into plant-level precision variance inputs")
    parser.add_argument("d0_cal_csv", type=Path)
    parser.add_argument("--confirmatory-dataset-id", required=True)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--power", type=float, default=0.80)
    parser.add_argument("--attrition", type=float, default=0.15)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = summarize(_read_csv(args.d0_cal_csv), args.confirmatory_dataset_id, alpha=args.alpha, power=args.power, attrition=args.attrition)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
