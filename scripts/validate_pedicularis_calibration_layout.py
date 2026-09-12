from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


Y_DATASET_ID = "PED_Y_CAL_V1"
D0_DATASET_ID = "PED_D0_CAL_V1"
FITNESS_SCALE_ID = "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER"
Y_MIN_PLANTS = 36
Y_MIN_FLOWERS_PER_PLANT = 3
D0_MIN_LOW_PLANTS = 24
D0_MIN_HIGH_PLANTS = 24
LOW_REQUIRED = {"S_CAL", "SHAM_CAL", "D0_CAL"}
HIGH_REQUIRED = {"D_CAL", "D_DRAIN_CAL"}


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    _need(bool(rows), f"empty CSV: {path}")
    return rows


def _one_value(rows: list[dict[str, str]], key: str, label: str) -> str:
    values = {row.get(key, "").strip() for row in rows}
    _need("" not in values and len(values) == 1, f"{label} must have one non-empty {key}")
    return next(iter(values))


def _bool_false(value: str) -> bool:
    return str(value).strip().lower() == "false"


def _bool_true(value: str) -> bool:
    return str(value).strip().lower() == "true"


def validate_rows(y_rows: list[dict[str, str]], d0_rows: list[dict[str, str]]) -> dict:
    for rows, dataset_id, label in (
        (y_rows, Y_DATASET_ID, "Y-CAL"),
        (d0_rows, D0_DATASET_ID, "D0-CAL"),
    ):
        _need(_one_value(rows, "dataset_id", label) == dataset_id, f"wrong dataset_id for {label}")
        _need(
            _one_value(rows, "fitness_scale_id", label) == FITNESS_SCALE_ID,
            f"wrong fitness_scale_id for {label}",
        )
        _one_value(rows, "time_horizon_id", label)
        for row in rows:
            _need(_bool_false(row.get("confirmatory_eligible", "")), f"{label} row marked confirmatory eligible")
            _need(_bool_true(row.get("assignment_frozen", "")), f"{label} assignment not frozen")
            _need(row.get("plant_id", "").strip(), f"{label} missing plant_id")
            _need(row.get("flower_id", "").strip(), f"{label} missing flower_id")

    context_y = (
        _one_value(y_rows, "context_id", "Y-CAL"),
        _one_value(y_rows, "population_id", "Y-CAL"),
        _one_value(y_rows, "season_id", "Y-CAL"),
        _one_value(y_rows, "fitness_scale_id", "Y-CAL"),
        _one_value(y_rows, "time_horizon_id", "Y-CAL"),
    )
    context_d0 = (
        _one_value(d0_rows, "context_id", "D0-CAL"),
        _one_value(d0_rows, "population_id", "D0-CAL"),
        _one_value(d0_rows, "season_id", "D0-CAL"),
        _one_value(d0_rows, "fitness_scale_id", "D0-CAL"),
        _one_value(d0_rows, "time_horizon_id", "D0-CAL"),
    )
    _need(context_y == context_d0, "Y-CAL and D0-CAL context mismatch")

    y_flowers = [row["flower_id"] for row in y_rows]
    d0_flowers = [row["flower_id"] for row in d0_rows]
    _need(len(y_flowers) == len(set(y_flowers)), "duplicate Y-CAL flower_id")
    _need(len(d0_flowers) == len(set(d0_flowers)), "duplicate D0-CAL flower_id")

    y_by_plant: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in y_rows:
        y_by_plant[row["plant_id"]].append(row)
    _need(len(y_by_plant) >= Y_MIN_PLANTS, "Y-CAL has fewer than 36 independent plants")
    for plant_id, rows in y_by_plant.items():
        _need(len(rows) >= Y_MIN_FLOWERS_PER_PLANT, f"Y-CAL plant has fewer than 3 flowers: {plant_id}")
        _need(
            all(row.get("treatment") == "Y_CAL_REPEATED_MEASUREMENT" for row in rows),
            f"unexpected Y-CAL treatment: {plant_id}",
        )

    d0_by_plant: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in d0_rows:
        d0_by_plant[row["plant_id"]].append(row)

    low = {
        plant_id: rows
        for plant_id, rows in d0_by_plant.items()
        if {row.get("phenotype_stratum") for row in rows} == {"LOW_Y"}
    }
    high = {
        plant_id: rows
        for plant_id, rows in d0_by_plant.items()
        if {row.get("phenotype_stratum") for row in rows} == {"HIGH_Y"}
    }
    _need(len(low) >= D0_MIN_LOW_PLANTS, "D0-CAL has fewer than 24 LOW-Y plants")
    _need(len(high) >= D0_MIN_HIGH_PLANTS, "D0-CAL has fewer than 24 HIGH-Y plants")
    _need(len(low) + len(high) == len(d0_by_plant), "D0-CAL plant has invalid/mixed phenotype stratum")

    for plant_id, rows in low.items():
        treatments = Counter(row.get("treatment") for row in rows)
        _need(set(treatments) <= LOW_REQUIRED, f"unexpected LOW-Y treatment: {plant_id}")
        _need(all(treatments[t] >= 1 for t in LOW_REQUIRED), f"LOW-Y treatment set incomplete: {plant_id}")
    for plant_id, rows in high.items():
        treatments = Counter(row.get("treatment") for row in rows)
        _need(set(treatments) <= HIGH_REQUIRED, f"unexpected HIGH-Y treatment: {plant_id}")
        _need(all(treatments[t] >= 1 for t in HIGH_REQUIRED), f"HIGH-Y treatment set incomplete: {plant_id}")

    y_plants = set(y_by_plant)
    d0_plants = set(d0_by_plant)
    _need(not (y_plants & d0_plants), "Y-CAL and D0-CAL plant IDs overlap")

    seeds = {row.get("randomization_seed", "").strip() for row in d0_rows}
    _need("" not in seeds and len(seeds) == 1, "D0-CAL randomization seed must be fixed and recorded")

    return {
        "schema_version": "SLK_PEDICULARIS_CALIBRATION_LAYOUT_VALIDATION_V1",
        "status": "CALIBRATION_LAYOUT_VALIDATED",
        "context_id": context_y[0],
        "population_id": context_y[1],
        "season_id": context_y[2],
        "fitness_scale_id": context_y[3],
        "time_horizon_id": context_y[4],
        "y_cal": {
            "independent_plants": len(y_by_plant),
            "rows": len(y_rows),
        },
        "d0_cal": {
            "independent_plants": len(d0_by_plant),
            "low_y_plants": len(low),
            "high_y_plants": len(high),
            "rows": len(d0_rows),
            "randomization_seed": next(iter(seeds)),
        },
        "firewall": {
            "plant_ids_disjoint_between_calibration_cohorts": True,
            "all_calibration_rows_confirmatory_ineligible": True,
        },
        "claim_ceiling": "LAYOUT_ONLY_NO_CALIBRATION_OR_BIOLOGICAL_GATE_RESULT",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Pedicularis Y-CAL and D0-CAL field layout")
    parser.add_argument("y_cal_csv", type=Path)
    parser.add_argument("d0_cal_csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = validate_rows(_read_csv(args.y_cal_csv), _read_csv(args.d0_cal_csv))
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
