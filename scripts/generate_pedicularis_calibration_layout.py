from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path


Y_DATASET_ID = "PED_Y_CAL_V1"
D0_DATASET_ID = "PED_D0_CAL_V1"
FITNESS_SCALE_ID = "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER"
Y_PLANTS = 36
Y_FLOWERS_PER_PLANT = 3
D0_LOW_PLANTS = 24
D0_HIGH_PLANTS = 24

FIELDS = [
    "dataset_id",
    "context_id",
    "population_id",
    "season_id",
    "fitness_scale_id",
    "time_horizon_id",
    "plant_id",
    "phenotype_stratum",
    "flower_id",
    "flower_slot",
    "calibration_roles",
    "treatment",
    "assignment_frozen",
    "randomization_seed",
    "whorl_id",
    "flowering_date",
    "block_id",
    "apparatus_id",
    "sham_id",
    "flower_length_mm",
    "bract_height_mm",
    "exsertion_z",
    "opening_width_mm",
    "stigma_position_mm",
    "orientation_deg",
    "mechanical_condition_pre",
    "mechanical_damage_post_prop",
    "retention_trial1_max_ml",
    "retention_trial1_depth_mm",
    "retention_trial1_half_life_min",
    "retention_trial1_leakage_ml_per_min",
    "retention_trial1_protected_fraction",
    "retention_trial2_max_ml",
    "retention_trial2_depth_mm",
    "retention_trial2_half_life_min",
    "retention_trial2_leakage_ml_per_min",
    "retention_trial2_protected_fraction",
    "pollinator_observation_minutes",
    "legitimate_visits",
    "handling_time_s",
    "pollen_receipt_grains",
    "initial_seed_set_prop",
    "anthesis_time",
    "pollination_window_end",
    "first_attack_time",
    "ovary_swelling_time",
    "early_attack_prop",
    "seed_predation_prop",
    "mature_viable_undamaged_seeds",
    "confirmatory_eligible",
    "notes",
]


def _blank_row() -> dict[str, str]:
    return {field: "" for field in FIELDS}


def generate_layout(
    context_id: str,
    population_id: str,
    season_id: str,
    time_horizon_id: str,
    randomization_seed: int,
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict]:
    if not context_id or not population_id or not season_id or not time_horizon_id:
        raise ValueError("context_id, population_id, season_id, and time_horizon_id are required")
    if not isinstance(randomization_seed, int):
        raise ValueError("randomization_seed must be an integer")

    rng = random.Random(randomization_seed)
    y_rows: list[dict[str, str]] = []
    d0_rows: list[dict[str, str]] = []

    common = {
        "context_id": context_id,
        "population_id": population_id,
        "season_id": season_id,
        "fitness_scale_id": FITNESS_SCALE_ID,
        "time_horizon_id": time_horizon_id,
        "assignment_frozen": "true",
        "randomization_seed": str(randomization_seed),
        "confirmatory_eligible": "false",
    }

    for p in range(1, Y_PLANTS + 1):
        plant_id = f"YCAL-{p:03d}"
        for slot in range(1, Y_FLOWERS_PER_PLANT + 1):
            row = _blank_row()
            row.update(common)
            row.update(
                {
                    "dataset_id": Y_DATASET_ID,
                    "plant_id": plant_id,
                    "phenotype_stratum": "UNCLASSIFIED_Y_CAL",
                    "flower_id": f"{plant_id}-F{slot}",
                    "flower_slot": str(slot),
                    "calibration_roles": "UC1_GEOMETRY;UC2_RETENTION",
                    "treatment": "Y_CAL_REPEATED_MEASUREMENT",
                }
            )
            y_rows.append(row)

    for p in range(1, D0_LOW_PLANTS + 1):
        plant_id = f"D0L-{p:03d}"
        treatments = ["S_CAL", "SHAM_CAL", "D0_CAL"]
        rng.shuffle(treatments)
        for slot, treatment in enumerate(treatments, start=1):
            row = _blank_row()
            row.update(common)
            row.update(
                {
                    "dataset_id": D0_DATASET_ID,
                    "plant_id": plant_id,
                    "phenotype_stratum": "LOW_Y",
                    "flower_id": f"{plant_id}-F{slot}",
                    "flower_slot": str(slot),
                    "calibration_roles": "UC3_POLLINATION;UC5_D0_APPARATUS;UC6_REPRODUCTIVE",
                    "treatment": treatment,
                }
            )
            d0_rows.append(row)

    for p in range(1, D0_HIGH_PLANTS + 1):
        plant_id = f"D0H-{p:03d}"
        treatments = ["D_CAL", "D_DRAIN_CAL"]
        rng.shuffle(treatments)
        for slot, treatment in enumerate(treatments, start=1):
            row = _blank_row()
            row.update(common)
            row.update(
                {
                    "dataset_id": D0_DATASET_ID,
                    "plant_id": plant_id,
                    "phenotype_stratum": "HIGH_Y",
                    "flower_id": f"{plant_id}-F{slot}",
                    "flower_slot": str(slot),
                    "calibration_roles": "UC4_ATTACK_TIMING;UC5_D0_APPARATUS;UC6_REPRODUCTIVE",
                    "treatment": treatment,
                }
            )
            d0_rows.append(row)

    metadata = {
        "schema_version": "SLK_PEDICULARIS_CALIBRATION_LAYOUT_V1",
        "status": "CALIBRATION_LAYOUT_GENERATED_CONFIRMATORY_UNOPENED",
        "context_id": context_id,
        "population_id": population_id,
        "season_id": season_id,
        "fitness_scale_id": FITNESS_SCALE_ID,
        "time_horizon_id": time_horizon_id,
        "randomization_seed": randomization_seed,
        "y_cal": {
            "dataset_id": Y_DATASET_ID,
            "independent_plants": Y_PLANTS,
            "flowers_per_plant": Y_FLOWERS_PER_PLANT,
            "rows": len(y_rows),
        },
        "d0_cal": {
            "dataset_id": D0_DATASET_ID,
            "low_y_plants": D0_LOW_PLANTS,
            "high_y_plants": D0_HIGH_PLANTS,
            "independent_plants": D0_LOW_PLANTS + D0_HIGH_PLANTS,
            "rows": len(d0_rows),
        },
        "firewall": {
            "calibration_units_confirmatory_eligible": False,
            "y_cal_and_d0_cal_plant_ids_must_be_disjoint": True,
        },
    }
    return y_rows, d0_rows, metadata


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Pedicularis Y-CAL and D0-CAL field layout")
    parser.add_argument("--context-id", required=True)
    parser.add_argument("--population-id", required=True)
    parser.add_argument("--season-id", required=True)
    parser.add_argument("--time-horizon-id", required=True)
    parser.add_argument("--randomization-seed", required=True, type=int)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    y_rows, d0_rows, metadata = generate_layout(
        args.context_id,
        args.population_id,
        args.season_id,
        args.time_horizon_id,
        args.randomization_seed,
    )
    _write_csv(args.output_dir / "PEDICULARIS_Y_CAL_FIELD_V1.csv", y_rows)
    _write_csv(args.output_dir / "PEDICULARIS_D0_CAL_FIELD_V1.csv", d0_rows)
    (args.output_dir / "PEDICULARIS_CALIBRATION_LAYOUT_METADATA_V1.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
