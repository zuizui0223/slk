from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path


DATASET_ID = "PED_D0_QUAL_CONFIRM_V1"
FITNESS_SCALE_ID = "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER"
ANALYSIS_FREEZE_SCHEMA = "SLK_PEDICULARIS_D0_CONFIRMATORY_ANALYSIS_FREEZE_V1"
Y_RECEIPT_SCHEMA = "SLK_PEDICULARIS_STRUCTURAL_Y_CALIBRATION_RECEIPT_V1"
Y_READY_STATUS = "STRUCTURAL_Y_Y0_RANGE_QUALIFIED_Y1_AUDITED"
PRECISION_SCHEMA = "SLK_PEDICULARIS_Y_D0_PRECISION_PLAN_V1"
PRECISION_STATUS = "PLANNING_ONLY_NOT_A_BIOLOGICAL_RECEIPT"
PRODUCTION_STATUS = "D0_CONFIRMATORY_ANALYSIS_PROSPECTIVELY_FROZEN"

FIELDS = [
    "dataset_id",
    "analysis_partition",
    "d0_qualification_eligible",
    "g3_g5_eligible",
    "context_id",
    "population_id",
    "season_id",
    "fitness_scale_id",
    "time_horizon_id",
    "plant_id",
    "phenotype_stratum",
    "required_y_band",
    "screening_y_value",
    "primary_y_metric",
    "flower_id",
    "flower_slot",
    "treatment",
    "assignment_frozen",
    "randomization_seed",
    "whorl_id",
    "flowering_date",
    "block_id",
    "exsertion_z",
    "opening_width_mm",
    "stigma_position_mm",
    "orientation_deg",
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
    "early_attack_prop",
    "seed_predation_prop",
    "mature_viable_undamaged_seeds",
    "notes",
]


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _filled(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip()) and "REQUIRED_BEFORE_USE" not in value


def _validate_analysis_freeze(freeze: dict) -> dict:
    _need(freeze.get("schema_version") == ANALYSIS_FREEZE_SCHEMA, "wrong D0 confirmatory freeze schema")
    _need(freeze.get("status") == PRODUCTION_STATUS, "D0 confirmatory analysis is not prospectively frozen")
    ctx = freeze.get("context", {})
    _need(ctx.get("system") == "Pedicularis rex", "wrong system")
    for key in (
        "dataset_id",
        "context_id",
        "population_id",
        "season_id",
        "primary_y_metric",
        "fitness_scale_id",
        "time_horizon_id",
        "q5_route",
    ):
        _need(_filled(ctx.get(key)), f"unfrozen confirmatory context field: {key}")
    _need(ctx.get("dataset_id") == DATASET_ID, "wrong confirmatory dataset id")
    _need(ctx.get("fitness_scale_id") == FITNESS_SCALE_ID, "wrong confirmatory fitness scale")
    _need(ctx.get("frozen_before_confirmatory_outcomes") is True, "confirmatory analysis not frozen before outcomes")
    _need(ctx.get("q5_route") in {"NEGLIGIBLE_BURDEN_EQUIVALENCE", "MEASURED_BURDEN_ADJUSTMENT"}, "invalid q5 route")

    analysis = freeze.get("analysis", {})
    _need(analysis.get("equivalence_ci_level") == 0.90, "v1 equivalence CI must remain 0.90")
    _need(analysis.get("directional_superiority_alpha") == 0.05, "v1 directional alpha must remain 0.05")
    _need(analysis.get("burden_precision_ci_level") == 0.95, "v1 burden precision CI must remain 0.95")
    seed = analysis.get("bootstrap_seed")
    reps = analysis.get("bootstrap_reps")
    minimum_reps = analysis.get("minimum_bootstrap_reps")
    _need(isinstance(seed, int), "bootstrap seed must be integer")
    _need(isinstance(minimum_reps, int) and minimum_reps >= 2000, "invalid minimum bootstrap reps")
    _need(isinstance(reps, int) and reps >= minimum_reps, "bootstrap reps below minimum")
    _need(analysis.get("minimum_valid_fraction") == 0.90, "v1 minimum valid fraction must remain 0.90")
    _need(analysis.get("resampling_unit") == "INDEPENDENT_PLANT", "wrong bootstrap unit")

    layout = freeze.get("layout", {})
    _need(layout.get("low_y_treatments") == ["S_QUAL", "SHAM_QUAL", "D0_QUAL"], "low-y layout changed")
    _need(layout.get("high_y_treatments") == ["D_QUAL"], "high-y layout changed")
    _need(layout.get("low_y_within_plant_randomized") is True, "low-y randomization disabled")
    _need(layout.get("high_y_single_natural_state") is True, "high-y state contract changed")

    firewall = freeze.get("firewall", {})
    for key in (
        "d0_qualification_units_g3_g5_ineligible",
        "margins_cannot_be_revised_from_confirmatory_outcomes",
        "sample_size_cannot_be_reduced_after_outcomes",
        "failed_gate_cannot_be_rescued_by_endpoint_switch",
        "q5_route_cannot_change_after_outcomes",
    ):
        _need(firewall.get(key) is True, f"confirmatory firewall disabled: {key}")

    metadata = freeze.get("freeze_metadata", {})
    for key in (
        "slk_source_commit",
        "margin_freeze_commit",
        "precision_plan_reference",
        "structural_y_receipt_reference",
        "freeze_commit",
        "freeze_timestamp",
    ):
        _need(_filled(metadata.get(key)), f"confirmatory freeze metadata missing: {key}")
    return ctx


def _validate_y_receipt(receipt: dict, ctx: dict) -> dict:
    _need(receipt.get("schema_version") == Y_RECEIPT_SCHEMA, "wrong structural-y receipt schema")
    _need(receipt.get("status") == Y_READY_STATUS, "structural-y receipt not ready")
    band = receipt.get("band_freeze", {})
    _need(band.get("recruitment_authorized_for_disjoint_d0_cal") is True, "structural-y bands do not authorize recruitment")
    rctx = receipt.get("context", {})
    for key in ("context_id", "population_id", "season_id", "fitness_scale_id", "time_horizon_id"):
        _need(rctx.get(key) == ctx.get(key), f"structural-y/confirmatory context mismatch: {key}")
    _need(receipt.get("primary_y_metric") == ctx.get("primary_y_metric"), "primary y metric mismatch")
    return band


def _required_n(precision_plan: dict) -> tuple[int, int, dict]:
    _need(precision_plan.get("planner_schema_version") == PRECISION_SCHEMA, "wrong precision plan schema")
    _need(precision_plan.get("status") == PRECISION_STATUS, "precision plan not frozen planning output")
    maxima = precision_plan.get("maxima_by_allocation_unit", {})
    _need(isinstance(maxima, dict) and maxima, "precision allocation maxima missing")

    def n_for(unit: str) -> int:
        block = maxima.get(unit)
        if block is None:
            return 0
        n = block.get("inflated_required_n")
        _need(isinstance(n, int) and n >= 2, f"invalid precision n for {unit}")
        return n

    paired_n = n_for("paired_plants_total")
    total_n = n_for("plants_total")
    per_group_n = n_for("plants_per_group")
    _need(per_group_n >= 2, "D0 confirmatory Q2 requires a plants_per_group precision result")
    low_n = max(paired_n, total_n, per_group_n)
    high_n = per_group_n
    _need(low_n >= 2 and high_n >= 2, "invalid confirmatory allocation")
    return low_n, high_n, {
        "paired_plants_total": paired_n,
        "plants_total": total_n,
        "plants_per_group": per_group_n,
    }


def generate_layout(
    precision_plan: dict,
    structural_y_receipt: dict,
    analysis_freeze: dict,
    randomization_seed: int,
) -> tuple[list[dict[str, str]], dict]:
    _need(isinstance(randomization_seed, int), "randomization_seed must be integer")
    ctx = _validate_analysis_freeze(analysis_freeze)
    band = _validate_y_receipt(structural_y_receipt, ctx)
    low_n, high_n, source_n = _required_n(precision_plan)
    rng = random.Random(randomization_seed)
    rows: list[dict[str, str]] = []

    common = {
        "dataset_id": DATASET_ID,
        "analysis_partition": "D0_CONFIRMATORY_QUALIFICATION_ONLY",
        "d0_qualification_eligible": "true",
        "g3_g5_eligible": "false",
        "context_id": ctx["context_id"],
        "population_id": ctx["population_id"],
        "season_id": ctx["season_id"],
        "fitness_scale_id": ctx["fitness_scale_id"],
        "time_horizon_id": ctx["time_horizon_id"],
        "primary_y_metric": ctx["primary_y_metric"],
        "assignment_frozen": "true",
        "randomization_seed": str(randomization_seed),
    }

    for i in range(1, low_n + 1):
        plant_id = f"D0Q-L-{i:04d}"
        treatments = ["S_QUAL", "SHAM_QUAL", "D0_QUAL"]
        rng.shuffle(treatments)
        for slot, treatment in enumerate(treatments, start=1):
            row = {field: "" for field in FIELDS}
            row.update(common)
            row.update(
                {
                    "plant_id": plant_id,
                    "phenotype_stratum": "LOW_Y",
                    "required_y_band": f"<= {band['low_y_max']}",
                    "flower_id": f"{plant_id}-F{slot}",
                    "flower_slot": str(slot),
                    "treatment": treatment,
                }
            )
            rows.append(row)

    for i in range(1, high_n + 1):
        plant_id = f"D0Q-H-{i:04d}"
        row = {field: "" for field in FIELDS}
        row.update(common)
        row.update(
            {
                "plant_id": plant_id,
                "phenotype_stratum": "HIGH_Y",
                "required_y_band": f">= {band['high_y_min']}",
                "flower_id": f"{plant_id}-F1",
                "flower_slot": "1",
                "treatment": "D_QUAL",
            }
        )
        rows.append(row)

    metadata = {
        "schema_version": "SLK_PEDICULARIS_D0_CONFIRMATORY_LAYOUT_V1",
        "status": "D0_CONFIRMATORY_LAYOUT_GENERATED_OUTCOMES_UNOPENED",
        "dataset_id": DATASET_ID,
        "context": ctx,
        "primary_y_metric": ctx["primary_y_metric"],
        "band_freeze": {
            "low_y_max": band["low_y_max"],
            "high_y_min": band["high_y_min"],
        },
        "allocation": {
            "low_y_independent_plants": low_n,
            "high_y_independent_plants": high_n,
            "low_y_rows": low_n * 3,
            "high_y_rows": high_n,
            "source_precision_maxima": source_n,
        },
        "randomization_seed": randomization_seed,
        "firewall": {
            "d0_qualification_eligible": True,
            "g3_g5_eligible": False,
        },
    }
    return rows, metadata


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Pedicularis D0 confirmatory qualification field layout")
    parser.add_argument("precision_plan_json", type=Path)
    parser.add_argument("structural_y_receipt_json", type=Path)
    parser.add_argument("analysis_freeze_json", type=Path)
    parser.add_argument("--randomization-seed", type=int, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    rows, metadata = generate_layout(
        json.loads(args.precision_plan_json.read_text(encoding="utf-8")),
        json.loads(args.structural_y_receipt_json.read_text(encoding="utf-8")),
        json.loads(args.analysis_freeze_json.read_text(encoding="utf-8")),
        args.randomization_seed,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(args.output_dir / "PEDICULARIS_D0_QUAL_CONFIRM_FIELD_V1.csv", rows)
    (args.output_dir / "PEDICULARIS_D0_QUAL_CONFIRM_METADATA_V1.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
