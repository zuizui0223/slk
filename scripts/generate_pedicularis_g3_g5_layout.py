from __future__ import annotations

import argparse
import csv
import json
import math
import random
from pathlib import Path


FREEZE_SCHEMA = "SLK_PEDICULARIS_G3_G5_EFFECT_FREEZE_V1"
FITNESS_SCALE_ID = "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER"
G2_POSITIVE = "G2_DIRECT_PASS_POSITIVE"
Y_READY = "STRUCTURAL_Y_Y0_RANGE_QUALIFIED_Y1_AUDITED"
Y_FUNCTION_READY = "STRUCTURAL_Y_Y2_PREFERENTIAL_LOADING_Y3_PERFORMANCE_INTERVENTION"
D0_READY = "D0_FULLY_QUALIFIED"
DECOMP_DATASET = "PED_G3_G5_RK_CONFIRM_V1"
DIRECT_DATASET = "PED_G5_DIRECT_CONFIRM_V1"
ROUTES = {"SAME_BLOCK_INTERNAL_IDENTITY", "INDEPENDENT_DIRECT_PHI_BLOCK"}
Q5_ROUTES = {"NEGLIGIBLE_BURDEN_EQUIVALENCE", "MEASURED_BURDEN_ADJUSTMENT"}

FIELDS = [
    "dataset_id",
    "block_role",
    "context_id",
    "population_id",
    "season_id",
    "fitness_scale_id",
    "time_horizon_id",
    "plant_id",
    "expected_structural_y_stratum",
    "world",
    "baseline_primary_y_value",
    "z_level_id",
    "target_exsertion_z",
    "z_tolerance",
    "flower_id",
    "flower_slot",
    "realized_exsertion_z",
    "mature_viable_undamaged_seeds",
    "assignment_frozen",
    "randomization_seed",
    "g3_g5_eligible",
    "notes",
]


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _text(value: object, label: str) -> str:
    out = str(value).strip()
    _need(bool(out) and "REQUIRED_BEFORE_USE" not in out, f"unfrozen {label}")
    return out


def _positive_int(value: object, label: str) -> int:
    _need(isinstance(value, int) and not isinstance(value, bool) and value > 0, f"{label} must be a positive integer")
    return int(value)


def _positive_float(value: object, label: str) -> float:
    _need(isinstance(value, (int, float)) and not isinstance(value, bool), f"{label} must be numeric")
    out = float(value)
    _need(math.isfinite(out) and out > 0, f"{label} must be finite and > 0")
    return out


def _finite_float(value: object, label: str) -> float:
    _need(isinstance(value, (int, float)) and not isinstance(value, bool), f"{label} must be numeric")
    out = float(value)
    _need(math.isfinite(out), f"{label} must be finite")
    return out


def _validate_freeze(freeze: dict) -> dict:
    _need(freeze.get("schema_version") == FREEZE_SCHEMA, "wrong G3-G5 freeze schema")
    _need(freeze.get("status") == "FROZEN_CANDIDATE", "G3-G5 freeze status must be FROZEN_CANDIDATE")
    _need(freeze.get("production_status") == "PEDICULARIS_G3_G5_EFFECT_PROSPECTIVELY_FROZEN", "wrong production status")

    ctx = freeze.get("context", {})
    _need(ctx.get("system") == "Pedicularis rex", "wrong system")
    for key in (
        "context_id", "population_id", "season_id", "time_horizon_id", "primary_y_metric",
        "q5_route", "estimation_route", "decomposition_dataset_id", "direct_phi_dataset_id",
    ):
        _text(ctx.get(key), f"context.{key}")
    _need(ctx.get("fitness_scale_id") == FITNESS_SCALE_ID, "wrong fitness scale")
    _need(ctx.get("decomposition_dataset_id") == DECOMP_DATASET, "decomposition dataset id changed")
    _need(ctx.get("direct_phi_dataset_id") == DIRECT_DATASET, "direct dataset id changed")
    route = ctx.get("estimation_route")
    _need(route in ROUTES and route in set(freeze.get("allowed_estimation_routes", [])), "invalid estimation route")
    _need(ctx.get("q5_route") in Q5_ROUTES, "invalid q5 route")
    _need(ctx.get("frozen_before_g3_g5_outcomes") is True, "G3-G5 contract not frozen before outcomes")

    _need(
        freeze.get("worlds") == {
            "S": "LOW_Y_NO_EXTERNAL_RETENTION",
            "D0": "LOW_Y_EXTERNAL_QUALIFIED_RETENTION",
            "D": "HIGH_Y_NATURAL_STRUCTURAL_RETENTION",
        },
        "world definitions changed",
    )

    zblock = freeze.get("z_grid", {})
    levels = zblock.get("levels", [])
    minimum_levels = _positive_int(zblock.get("minimum_levels"), "z_grid.minimum_levels")
    _need(minimum_levels >= 5, "z grid minimum must be >= 5")
    _need(isinstance(levels, list) and len(levels) >= minimum_levels, "insufficient frozen z levels")
    ids: list[str] = []
    targets: list[float] = []
    clean_levels: list[dict] = []
    for i, level in enumerate(levels):
        _need(isinstance(level, dict), f"z level {i} must be an object")
        level_id = _text(level.get("level_id"), f"z_grid.levels[{i}].level_id")
        target = _finite_float(level.get("target_exsertion_z"), f"z target {level_id}")
        tolerance = _positive_float(level.get("tolerance"), f"z tolerance {level_id}")
        ids.append(level_id)
        targets.append(target)
        clean_levels.append({"level_id": level_id, "target_exsertion_z": target, "tolerance": tolerance})
    _need(len(ids) == len(set(ids)), "duplicate z level id")
    _need(all(b > a for a, b in zip(targets, targets[1:])), "z targets must be strictly increasing")
    _need(zblock.get("strictly_increasing_targets_required") is True, "z increasing-target rule disabled")
    _need(zblock.get("each_level_requires_id_target_and_tolerance") is True, "z level identity rule disabled")

    sampling = freeze.get("sampling", {})
    min_world = _positive_int(sampling.get("minimum_analyzable_plants_per_world"), "minimum_analyzable_plants_per_world")
    rec_world = _positive_int(sampling.get("recruitment_plants_per_world"), "recruitment_plants_per_world")
    _need(rec_world >= min_world, "recruitment plants per world must be >= analyzable floor")
    _need(sampling.get("flowers_per_z_level_per_plant") == 1, "v1 requires one focal flower per z level per plant")
    _text(sampling.get("sample_size_source"), "sampling.sample_size_source")
    _text(sampling.get("sample_size_rationale"), "sampling.sample_size_rationale")

    min_direct = sampling.get("minimum_analyzable_plants_per_direct_world")
    rec_direct = sampling.get("recruitment_plants_per_direct_world")
    if route == "INDEPENDENT_DIRECT_PHI_BLOCK":
        min_direct = _positive_int(min_direct, "minimum_analyzable_plants_per_direct_world")
        rec_direct = _positive_int(rec_direct, "recruitment_plants_per_direct_world")
        _need(rec_direct >= min_direct, "direct recruitment must be >= direct analyzable floor")
    else:
        _need(min_direct in (None, 0) and rec_direct in (None, 0), "same-block route must not register a direct block sample")
        min_direct = 0
        rec_direct = 0

    analysis = freeze.get("analysis", {})
    _need(analysis.get("grid_estimand") == "MAX_REGISTERED_WORLD_X_Z_CELL_MEAN", "grid estimand changed")
    _need(analysis.get("bootstrap_reoptimizes_grid_maximum_each_replicate") is True, "bootstrap must reoptimize grid maximum")
    seed = analysis.get("bootstrap_seed")
    reps = analysis.get("bootstrap_reps")
    min_reps = analysis.get("minimum_bootstrap_reps")
    _need(isinstance(seed, int), "bootstrap seed must be integer")
    _need(isinstance(min_reps, int) and min_reps >= 1000, "bootstrap minimum reps must be >= 1000")
    _need(isinstance(reps, int) and reps >= min_reps, "bootstrap reps below frozen minimum")
    valid_fraction = float(analysis.get("minimum_valid_fraction"))
    _need(0 < valid_fraction <= 1, "invalid minimum valid fraction")
    ci_level = float(analysis.get("ci_level"))
    _need(0 < ci_level < 1, "invalid CI level")
    _need(analysis.get("resampling_unit") == "INDEPENDENT_PLANT_WITH_COMPLETE_Z_GRID", "wrong resampling unit")
    _need(analysis.get("burden_correction") == "ADD_INDEPENDENT_D0_QUALIFICATION_B_DEVICE_TO_OBSERVED_D0_WORLD", "burden correction changed")
    _need(analysis.get("burden_uncertainty_rule") == "CONSERVATIVE_INTERVAL_ADDITION_FOR_R_AND_K; CANCELLATION_RETAINED_FOR_PHI", "burden uncertainty rule changed")

    concordance = freeze.get("independent_concordance", {})
    concordance_tol = concordance.get("max_abs_phi_point_difference")
    if route == "INDEPENDENT_DIRECT_PHI_BLOCK":
        concordance_tol = _positive_float(concordance_tol, "max_abs_phi_point_difference")
        _need(concordance.get("residual_ci_must_include_zero") is True, "residual zero-inclusion rule disabled")
    else:
        _need(concordance_tol in (None, 0), "same-block route must not register independent concordance tolerance")
        concordance_tol = None

    firewall = freeze.get("firewall", {})
    for key in (
        "g1_g2_units_reused_for_g3_g5_forbidden",
        "y_cal_units_reused_for_g3_g5_forbidden",
        "d0_cal_units_reused_for_g3_g5_forbidden",
        "d0_qualification_units_reused_for_g3_g5_forbidden",
        "structural_y_function_units_reused_for_g3_g5_forbidden",
        "z_grid_change_after_outcomes_forbidden",
        "world_definition_change_after_outcomes_forbidden",
        "sample_size_reduction_after_outcomes_forbidden",
        "route_change_after_outcomes_forbidden",
        "burden_correction_source_change_after_outcomes_forbidden",
    ):
        _need(firewall.get(key) is True, f"G3-G5 firewall disabled: {key}")

    metadata = freeze.get("freeze_metadata", {})
    for key in (
        "slk_source_commit", "g2_receipt_reference", "structural_y_receipt_reference",
        "structural_y_function_receipt_reference", "d0_qualification_receipt_reference",
        "freeze_commit", "freeze_timestamp",
    ):
        _text(metadata.get(key), f"freeze_metadata.{key}")

    return {
        "context": ctx,
        "route": route,
        "z_levels": clean_levels,
        "minimum_world_n": min_world,
        "recruitment_world_n": rec_world,
        "minimum_direct_n": min_direct,
        "recruitment_direct_n": rec_direct,
        "bootstrap_seed": seed,
        "bootstrap_reps": reps,
        "minimum_valid_fraction": valid_fraction,
        "ci_level": ci_level,
        "concordance_tolerance": concordance_tol,
    }


def validate_contract(freeze: dict, g2: dict, y_receipt: dict, y_function: dict, d0: dict) -> dict:
    cfg = _validate_freeze(freeze)
    ctx = cfg["context"]

    _need(g2.get("g1") == "DIRECT_PASS" and g2.get("g2") == "DIRECT_PASS", "G1/G2 not directly passed")
    _need(g2.get("g2_detail") == G2_POSITIVE, "G2 positive conflict budget required")
    gctx = g2.get("context", {})
    for key in ("context_id", "population_id", "season_id", "fitness_scale_id"):
        _need(gctx.get(key) == ctx.get(key), f"G2/effect context mismatch: {key}")
    _need(gctx.get("system") == "Pedicularis rex", "wrong G2 system")
    load = g2.get("conflict_load", {})
    _need(float(load.get("lower_95")) > 0, "G2 conflict lower bound must exceed zero")

    _need(y_receipt.get("status") == Y_READY, "structural-y Y0/Y1 receipt not ready")
    yctx = y_receipt.get("context", {})
    for key in ("context_id", "population_id", "season_id", "fitness_scale_id", "time_horizon_id"):
        _need(yctx.get(key) == ctx.get(key), f"Y receipt/effect context mismatch: {key}")
    _need(y_receipt.get("primary_y_metric") == ctx.get("primary_y_metric"), "primary y metric mismatch")
    bands = y_receipt.get("band_freeze", {})
    _need(bands.get("recruitment_authorized_for_disjoint_d0_cal") is True, "structural-y bands not authorized")

    _need(y_function.get("status") == Y_FUNCTION_READY, "structural-y Y2/Y3 receipt not fully promoted")
    yfctx = y_function.get("context", {})
    for key in ("population_id", "season_id", "fitness_scale_id", "time_horizon_id"):
        _need(yfctx.get(key) == ctx.get(key), f"Y2/Y3/effect context mismatch: {key}")
    _need(y_function.get("primary_y_metric") == ctx.get("primary_y_metric"), "Y2/Y3 primary y mismatch")
    _need(y_function.get("y2", {}).get("pass") is True and y_function.get("y3", {}).get("pass") is True, "Y2 and Y3 must both pass")

    _need(d0.get("status") == D0_READY, "D0 comparator must be fully qualified")
    dctx = d0.get("context", {})
    for key in ("context_id", "population_id", "season_id", "fitness_scale_id", "time_horizon_id", "primary_y_metric", "q5_route"):
        _need(dctx.get(key) == ctx.get(key), f"D0/effect context mismatch: {key}")
    _need(all(d0.get("gates", {}).values()), "all D0 Q1-Q6 gates must pass")
    _need(d0.get("firewall", {}).get("d0_qualification_units_g3_g5_ineligible") is True, "D0 qualification firewall missing")
    burden = d0.get("apparatus_burden_receipt") or {}
    _need(burden.get("pass") is True, "D0 apparatus burden receipt not passed")
    point = _finite_float(burden.get("point_difference"), "apparatus burden point")
    ci = burden.get("ci")
    _need(isinstance(ci, list) and len(ci) == 2, "apparatus burden CI missing")
    blo = _finite_float(ci[0], "apparatus burden CI lower")
    bhi = _finite_float(ci[1], "apparatus burden CI upper")
    _need(blo <= point <= bhi, "apparatus burden point outside CI")

    cfg["bands"] = {
        "low_y_max": float(bands["low_y_max"]),
        "high_y_min": float(bands["high_y_min"]),
    }
    cfg["burden"] = {"point": point, "lower": blo, "upper": bhi, "receipt": burden}
    cfg["conflict_load"] = {
        "point": float(load["point"]),
        "lower_95": float(load["lower_95"]),
        "upper_95": float(load["upper_95"]),
    }
    return cfg


def _blank() -> dict[str, str]:
    return {field: "" for field in FIELDS}


def _world_rows(
    rng: random.Random,
    dataset_id: str,
    block_role: str,
    world: str,
    plant_ids: list[str],
    expected_stratum: str,
    levels: list[dict],
    ctx: dict,
    seed: int,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for plant_id in plant_ids:
        ordered = list(levels)
        rng.shuffle(ordered)
        for slot, level in enumerate(ordered, start=1):
            row = _blank()
            row.update(
                {
                    "dataset_id": dataset_id,
                    "block_role": block_role,
                    "context_id": ctx["context_id"],
                    "population_id": ctx["population_id"],
                    "season_id": ctx["season_id"],
                    "fitness_scale_id": ctx["fitness_scale_id"],
                    "time_horizon_id": ctx["time_horizon_id"],
                    "plant_id": plant_id,
                    "expected_structural_y_stratum": expected_stratum,
                    "world": world,
                    "z_level_id": level["level_id"],
                    "target_exsertion_z": str(level["target_exsertion_z"]),
                    "z_tolerance": str(level["tolerance"]),
                    "flower_id": f"{plant_id}-{level['level_id']}",
                    "flower_slot": str(slot),
                    "assignment_frozen": "true",
                    "randomization_seed": str(seed),
                    "g3_g5_eligible": "true",
                }
            )
            rows.append(row)
    return rows


def generate_layout(
    freeze: dict,
    g2: dict,
    y_receipt: dict,
    y_function: dict,
    d0: dict,
    randomization_seed: int,
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict]:
    _need(isinstance(randomization_seed, int), "randomization seed must be integer")
    cfg = validate_contract(freeze, g2, y_receipt, y_function, d0)
    ctx = cfg["context"]
    rng = random.Random(randomization_seed)
    n = cfg["recruitment_world_n"]

    low_pool = [f"G35-L-{i:03d}" for i in range(1, 2 * n + 1)]
    rng.shuffle(low_pool)
    s_plants = sorted(low_pool[:n])
    d0_plants = sorted(low_pool[n:])
    d_plants = [f"G35-H-{i:03d}" for i in range(1, n + 1)]

    decomposition = []
    decomposition += _world_rows(rng, DECOMP_DATASET, "DECOMPOSITION_RK", "S", s_plants, "LOW_Y", cfg["z_levels"], ctx, randomization_seed)
    decomposition += _world_rows(rng, DECOMP_DATASET, "DECOMPOSITION_RK", "D0", d0_plants, "LOW_Y", cfg["z_levels"], ctx, randomization_seed)
    decomposition += _world_rows(rng, DECOMP_DATASET, "DECOMPOSITION_RK", "D", d_plants, "HIGH_Y", cfg["z_levels"], ctx, randomization_seed)

    direct: list[dict[str, str]] = []
    if cfg["route"] == "INDEPENDENT_DIRECT_PHI_BLOCK":
        nd = cfg["recruitment_direct_n"]
        direct_s = [f"G5D-L-{i:03d}" for i in range(1, nd + 1)]
        direct_d = [f"G5D-H-{i:03d}" for i in range(1, nd + 1)]
        direct += _world_rows(rng, DIRECT_DATASET, "INDEPENDENT_DIRECT_PHI", "S", direct_s, "LOW_Y", cfg["z_levels"], ctx, randomization_seed)
        direct += _world_rows(rng, DIRECT_DATASET, "INDEPENDENT_DIRECT_PHI", "D", direct_d, "HIGH_Y", cfg["z_levels"], ctx, randomization_seed)

    metadata = {
        "schema_version": "SLK_PEDICULARIS_G3_G5_LAYOUT_V1",
        "status": "G3_G5_LAYOUT_GENERATED_OUTCOMES_UNOPENED",
        "context": {
            "system": "Pedicularis rex",
            "context_id": ctx["context_id"],
            "population_id": ctx["population_id"],
            "season_id": ctx["season_id"],
            "fitness_scale_id": ctx["fitness_scale_id"],
            "time_horizon_id": ctx["time_horizon_id"],
            "primary_y_metric": ctx["primary_y_metric"],
            "q5_route": ctx["q5_route"],
            "estimation_route": cfg["route"],
        },
        "randomization_seed": randomization_seed,
        "z_grid": cfg["z_levels"],
        "structural_y_bands": cfg["bands"],
        "decomposition": {
            "dataset_id": DECOMP_DATASET,
            "recruitment_plants_per_world": n,
            "minimum_analyzable_plants_per_world": cfg["minimum_world_n"],
            "worlds": ["S", "D0", "D"],
            "rows": len(decomposition),
        },
        "direct_phi": {
            "dataset_id": DIRECT_DATASET,
            "enabled": cfg["route"] == "INDEPENDENT_DIRECT_PHI_BLOCK",
            "recruitment_plants_per_world": cfg["recruitment_direct_n"],
            "minimum_analyzable_plants_per_world": cfg["minimum_direct_n"],
            "worlds": ["S", "D"] if direct else [],
            "rows": len(direct),
        },
        "firewall": {
            "all_rows_are_new_g3_g5_units": True,
            "prior_g1_g2_ycal_d0cal_d0qual_units_forbidden": True,
        },
    }
    return decomposition, direct, metadata


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the independent Pedicularis G3-G5 effect field layout")
    parser.add_argument("effect_freeze_json", type=Path)
    parser.add_argument("g2_receipt_json", type=Path)
    parser.add_argument("structural_y_receipt_json", type=Path)
    parser.add_argument("structural_y_function_receipt_json", type=Path)
    parser.add_argument("d0_qualification_receipt_json", type=Path)
    parser.add_argument("--randomization-seed", type=int, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    payloads = [
        json.loads(args.effect_freeze_json.read_text(encoding="utf-8")),
        json.loads(args.g2_receipt_json.read_text(encoding="utf-8")),
        json.loads(args.structural_y_receipt_json.read_text(encoding="utf-8")),
        json.loads(args.structural_y_function_receipt_json.read_text(encoding="utf-8")),
        json.loads(args.d0_qualification_receipt_json.read_text(encoding="utf-8")),
    ]
    decomposition, direct, metadata = generate_layout(*payloads, randomization_seed=args.randomization_seed)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(args.output_dir / "PEDICULARIS_G3_G5_RK_CONFIRM_V1.csv", decomposition)
    if direct:
        _write_csv(args.output_dir / "PEDICULARIS_G5_DIRECT_CONFIRM_V1.csv", direct)
    (args.output_dir / "PEDICULARIS_G3_G5_LAYOUT_METADATA_V1.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
