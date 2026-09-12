from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import NormalDist


FREEZE_SCHEMA = "SLK_PEDICULARIS_G3_G5_PRECISION_FREEZE_V1"
VAR_SCHEMA = "SLK_PEDICULARIS_G3_G5_PLANNING_VARIANCE_V1"
FITNESS_SCALE_ID = "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER"
ALLOWED_TARGET_SOURCES = {
    "DOWNSTREAM_DECISION_INVARIANCE",
    "EXTERNAL_BIOLOGICAL_BOUND",
    "COMBINED_PREDECLARED",
}


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _positive(value: object, label: str) -> float:
    _need(isinstance(value, (int, float)) and not isinstance(value, bool), f"{label} must be numeric")
    out = float(value)
    _need(math.isfinite(out) and out > 0, f"{label} must be finite and > 0")
    return out


def _filled(value: object, label: str) -> str:
    out = str(value).strip()
    _need(bool(out) and "REQUIRED_BEFORE_USE" not in out, f"unfrozen {label}")
    return out


def _z(p: float) -> float:
    _need(0 < p < 1, "normal quantile probability must be in (0,1)")
    return NormalDist().inv_cdf(p)


def _inflate(n: int, attrition: float) -> int:
    return math.ceil(n / (1 - attrition))


def plan(freeze: dict, variance: dict) -> dict:
    _need(freeze.get("schema_version") == FREEZE_SCHEMA, "wrong G3-G5 precision freeze schema")
    _need(freeze.get("status") == "FROZEN_CANDIDATE", "precision freeze status must be FROZEN_CANDIDATE")
    _need(freeze.get("production_status") == "PEDICULARIS_G3_G5_PRECISION_PROSPECTIVELY_FROZEN", "wrong precision production status")
    _need(variance.get("schema_version") == VAR_SCHEMA, "wrong planning variance schema")
    _need(variance.get("status") == "G3_G5_PLANNING_VARIANCE_READY", "planning variance is not ready")

    ctx = freeze.get("context", {})
    vctx = variance.get("context", {})
    _need(ctx.get("system") == "Pedicularis rex", "wrong system")
    for key in ("context_id", "population_id", "season_id", "fitness_scale_id", "time_horizon_id"):
        _filled(ctx.get(key), f"context.{key}")
        _need(ctx.get(key) == vctx.get(key), f"precision/variance context mismatch: {key}")
    _need(ctx.get("fitness_scale_id") == FITNESS_SCALE_ID, "wrong fitness scale")
    _need(ctx.get("d0_qualification_dataset_id") == "PED_D0_QUAL_CONFIRM_V1", "wrong source dataset")
    _need(ctx.get("frozen_before_g3_g5_outcomes") is True, "precision targets not frozen before G3-G5 outcomes")

    targets = freeze.get("targets", {})
    z_levels = targets.get("registered_z_levels")
    _need(isinstance(z_levels, int) and z_levels >= 5, "registered_z_levels must be an integer >= 5")
    half_width = _positive(targets.get("world_cell_mean_half_width"), "world cell mean half-width")
    min_r = _positive(targets.get("minimum_recoverable_benefit_R"), "minimum recoverable R")
    min_phi = _positive(targets.get("minimum_abs_architecture_value_Phi"), "minimum absolute Phi")
    source_type = _filled(targets.get("target_source_type"), "target_source_type")
    _need(source_type in ALLOWED_TARGET_SOURCES, "target source type is not allowed")
    _filled(targets.get("target_source_reference"), "target_source_reference")
    _filled(targets.get("biological_rationale"), "biological_rationale")

    transport = freeze.get("variance_transport", {})
    _need(transport.get("use_max_independent_world_sd") is True, "v1 requires maximum independent world SD")
    multiplier = _positive(transport.get("sd_safety_multiplier"), "sd safety multiplier")
    _need(multiplier >= 1, "sd safety multiplier must be >= 1")
    _filled(transport.get("multiplier_source"), "multiplier_source")
    _filled(transport.get("multiplier_rationale"), "multiplier_rationale")

    planning = freeze.get("planning", {})
    alpha = float(planning.get("familywise_alpha"))
    power = float(planning.get("power"))
    attrition = float(planning.get("attrition"))
    _need(0 < alpha < 1, "familywise alpha must be in (0,1)")
    _need(0 < power < 1, "power must be in (0,1)")
    _need(0 <= attrition < 1, "attrition must be in [0,1)")
    _need(planning.get("bonferroni_across_world_x_z_cell_means") is True, "cell-mean multiplicity rule disabled")
    _need(planning.get("two_sided_R_and_Phi_planning") is True, "R/Phi two-sided planning rule disabled")

    firewall = freeze.get("firewall", {})
    for key in (
        "d0_qualification_units_planning_only",
        "d0_qualification_units_effect_estimation_forbidden",
        "targets_cannot_be_derived_from_g3_g5_outcomes",
        "sd_multiplier_cannot_be_reduced_after_g3_g5_outcomes",
        "sample_size_cannot_be_reduced_after_g3_g5_outcomes",
    ):
        _need(firewall.get(key) is True, f"precision firewall disabled: {key}")

    metadata = freeze.get("freeze_metadata", {})
    for key in ("slk_source_commit", "d0_qualification_receipt_reference", "freeze_commit", "freeze_timestamp"):
        _filled(metadata.get(key), f"freeze_metadata.{key}")

    sd0 = _positive(variance.get("max_world_sd"), "maximum source world SD")
    sd = sd0 * multiplier

    # Simultaneous precision across the three decomposition worlds and every registered z cell.
    number_cells = 3 * z_levels
    alpha_cell = alpha / number_cells
    z_cell = _z(1 - alpha_cell / 2)
    n_cell = max(2, math.ceil((z_cell * sd / half_width) ** 2))

    # Two-sided normal-approximation planning for R and Phi. Split the familywise alpha across the two focal contrasts.
    alpha_contrast = alpha / 2
    z_contrast = _z(1 - alpha_contrast / 2)
    z_power = _z(power)
    n_r = max(2, math.ceil(2 * ((z_contrast + z_power) * sd / min_r) ** 2))
    n_phi = max(2, math.ceil(2 * ((z_contrast + z_power) * sd / min_phi) ** 2))

    base_decomposition = max(n_cell, n_r, n_phi)
    recruit_decomposition = _inflate(base_decomposition, attrition)

    # A separate direct-Phi block needs S and D only. Use its own simultaneous cell precision plus the Phi contrast target.
    direct_cells = 2 * z_levels
    alpha_direct_cell = alpha / direct_cells
    z_direct_cell = _z(1 - alpha_direct_cell / 2)
    n_direct_cell = max(2, math.ceil((z_direct_cell * sd / half_width) ** 2))
    base_direct = max(n_direct_cell, n_phi)
    recruit_direct = _inflate(base_direct, attrition)

    drivers = []
    if base_decomposition == n_cell:
        drivers.append("WORLD_X_Z_CELL_PRECISION")
    if base_decomposition == n_r:
        drivers.append("MINIMUM_R_EFFECT")
    if base_decomposition == n_phi:
        drivers.append("MINIMUM_ABS_PHI_EFFECT")

    return {
        "schema_version": "SLK_PEDICULARIS_G3_G5_PRECISION_PLAN_V1",
        "status": "G3_G5_EFFECT_SAMPLE_SIZE_PROSPECTIVELY_PLANNED",
        "context": {
            "system": "Pedicularis rex",
            "context_id": ctx["context_id"],
            "population_id": ctx["population_id"],
            "season_id": ctx["season_id"],
            "fitness_scale_id": ctx["fitness_scale_id"],
            "time_horizon_id": ctx["time_horizon_id"],
            "source_dataset_id": ctx["d0_qualification_dataset_id"],
        },
        "variance_input": {
            "max_world_sd": sd0,
            "sd_safety_multiplier": multiplier,
            "planning_sd": sd,
        },
        "targets": {
            "registered_z_levels": z_levels,
            "world_cell_mean_half_width": half_width,
            "minimum_recoverable_benefit_R": min_r,
            "minimum_abs_architecture_value_Phi": min_phi,
        },
        "components": {
            "decomposition_cell_precision_n_per_world": n_cell,
            "R_effect_n_per_world": n_r,
            "Phi_effect_n_per_world": n_phi,
            "direct_block_cell_precision_n_per_world": n_direct_cell,
        },
        "decomposition": {
            "minimum_analyzable_plants_per_world": base_decomposition,
            "recruitment_plants_per_world": recruit_decomposition,
            "driving_criteria": drivers,
        },
        "independent_direct_phi": {
            "minimum_analyzable_plants_per_world": base_direct,
            "recruitment_plants_per_world": recruit_direct,
        },
        "planning_boundary": (
            "Normal approximations and independent D0-qualification fitness SDs set prospective sample floors only. "
            "Final G3-G5 inference remains the registered complete-grid plant bootstrap with z-grid re-optimization."
        ),
        "firewall": {
            "source_d0_qualification_units_effect_estimation_ineligible": True,
            "g3_g5_outcomes_opened": False,
        },
        "claim_ceiling": "SAMPLE_SIZE_PLAN_ONLY_NO_G3_G5_BIOLOGICAL_EFFECT",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Plan Pedicularis G3-G5 effect sample size")
    parser.add_argument("precision_freeze_json", type=Path)
    parser.add_argument("planning_variance_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = plan(
        json.loads(args.precision_freeze_json.read_text(encoding="utf-8")),
        json.loads(args.planning_variance_json.read_text(encoding="utf-8")),
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
