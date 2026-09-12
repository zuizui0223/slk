from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PLANNER = ROOT / "scripts" / "plan_pedicularis_g3_g5_effect_precision.py"
COMPILER = ROOT / "scripts" / "compile_pedicularis_g3_g5_effect_sampling.py"

spec = importlib.util.spec_from_file_location("ped_g35_plan_compile", PLANNER)
planmod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(planmod)

spec2 = importlib.util.spec_from_file_location("ped_g35_compile", COMPILER)
compiler = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(compiler)


CTX = {
    "context_id": "ped-rex-pop1-2027-v1",
    "population_id": "pop1",
    "season_id": "2027",
    "fitness_scale_id": "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER",
    "time_horizon_id": "FLOWER_TO_MATURE_VIABLE_SEED",
}


def _precision_freeze() -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_G3_G5_PRECISION_FREEZE_V1",
        "status": "FROZEN_CANDIDATE",
        "context": {
            "system": "Pedicularis rex",
            **CTX,
            "d0_qualification_dataset_id": "PED_D0_QUAL_CONFIRM_V1",
            "frozen_before_g3_g5_outcomes": True,
        },
        "targets": {
            "registered_z_levels": 5,
            "world_cell_mean_half_width": 0.5,
            "minimum_recoverable_benefit_R": 1.0,
            "minimum_abs_architecture_value_Phi": 0.8,
            "target_source_type": "DOWNSTREAM_DECISION_INVARIANCE",
            "target_source_reference": "SLK:G3_G5_DECISION_TARGETS_V1",
            "biological_rationale": "predeclared resolution target",
        },
        "variance_transport": {
            "use_max_independent_world_sd": True,
            "sd_safety_multiplier": 1.2,
            "multiplier_source": "PREDECLARED_TRANSPORT_SAFETY_V1",
            "multiplier_rationale": "conservative transport across the later z grid",
        },
        "planning": {
            "familywise_alpha": 0.05,
            "power": 0.80,
            "attrition": 0.15,
            "bonferroni_across_world_x_z_cell_means": True,
            "two_sided_R_and_Phi_planning": True,
        },
        "firewall": {
            "d0_qualification_units_planning_only": True,
            "d0_qualification_units_effect_estimation_forbidden": True,
            "targets_cannot_be_derived_from_g3_g5_outcomes": True,
            "sd_multiplier_cannot_be_reduced_after_g3_g5_outcomes": True,
            "sample_size_cannot_be_reduced_after_g3_g5_outcomes": True,
        },
        "freeze_metadata": {
            "slk_source_commit": "abc123",
            "d0_qualification_receipt_reference": "d0-qual-receipt-1",
            "freeze_commit": "precision-freeze-1",
            "freeze_timestamp": "2027-05-01T00:00:00Z",
        },
        "production_status": "PEDICULARIS_G3_G5_PRECISION_PROSPECTIVELY_FROZEN",
    }


def _variance() -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_G3_G5_PLANNING_VARIANCE_V1",
        "status": "G3_G5_PLANNING_VARIANCE_READY",
        "context": {
            "system": "Pedicularis rex",
            **CTX,
            "source_dataset_id": "PED_D0_QUAL_CONFIRM_V1",
        },
        "max_world_sd": 1.1,
        "firewall": {
            "source_units_planning_only": True,
            "source_units_g3_g5_effect_estimation_ineligible": True,
        },
    }


def _effect(route: str = "SAME_BLOCK_INTERNAL_IDENTITY") -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_G3_G5_EFFECT_FREEZE_V1",
        "status": "TEMPLATE_ONLY_NOT_FROZEN",
        "context": {
            "system": "Pedicularis rex",
            **CTX,
            "primary_y_metric": "RETENTION_MEAN_MAX_ML",
            "q5_route": "NEGLIGIBLE_BURDEN_EQUIVALENCE",
            "estimation_route": route,
            "decomposition_dataset_id": "PED_G3_G5_RK_CONFIRM_V1",
            "direct_phi_dataset_id": "PED_G5_DIRECT_CONFIRM_V1",
            "frozen_before_g3_g5_outcomes": False,
        },
        "allowed_estimation_routes": ["SAME_BLOCK_INTERNAL_IDENTITY", "INDEPENDENT_DIRECT_PHI_BLOCK"],
        "worlds": {
            "S": "LOW_Y_NO_EXTERNAL_RETENTION",
            "D0": "LOW_Y_EXTERNAL_QUALIFIED_RETENTION",
            "D": "HIGH_Y_NATURAL_STRUCTURAL_RETENTION",
        },
        "z_grid": {
            "levels": [
                {"level_id": f"Z{i}", "target_exsertion_z": 0.1 * i, "tolerance": 0.02}
                for i in range(1, 6)
            ],
            "minimum_levels": 5,
            "strictly_increasing_targets_required": True,
            "each_level_requires_id_target_and_tolerance": True,
        },
        "sampling": {
            "minimum_analyzable_plants_per_world": None,
            "recruitment_plants_per_world": None,
            "minimum_analyzable_plants_per_direct_world": None,
            "recruitment_plants_per_direct_world": None,
            "flowers_per_z_level_per_plant": 1,
            "sample_size_source": "REQUIRED_BEFORE_USE",
            "sample_size_rationale": "REQUIRED_BEFORE_USE",
        },
        "analysis": {},
        "independent_concordance": {},
        "firewall": {},
        "freeze_metadata": {},
        "production_status": "PEDICULARIS_G3_G5_EFFECT_PROSPECTIVELY_FROZEN",
    }


def _plan() -> dict:
    return planmod.plan(_precision_freeze(), _variance())


def test_same_block_sampling_is_compiled_without_direct_block_n() -> None:
    plan = _plan()
    out = compiler.compile_sampling(_effect(), _precision_freeze(), plan)
    assert out["status"] == "SAMPLING_COMPILED_AWAITING_FINAL_EFFECT_FREEZE"
    assert out["sampling"]["minimum_analyzable_plants_per_world"] == plan["decomposition"]["minimum_analyzable_plants_per_world"]
    assert out["sampling"]["recruitment_plants_per_world"] == plan["decomposition"]["recruitment_plants_per_world"]
    assert out["sampling"]["minimum_analyzable_plants_per_direct_world"] is None
    assert out["sampling"]["recruitment_plants_per_direct_world"] is None
    assert "precision-freeze-1" in out["sampling"]["sample_size_source"]
    assert out["context"]["frozen_before_g3_g5_outcomes"] is False


def test_independent_route_receives_direct_block_sample_sizes() -> None:
    plan = _plan()
    out = compiler.compile_sampling(_effect("INDEPENDENT_DIRECT_PHI_BLOCK"), _precision_freeze(), plan)
    assert out["sampling"]["minimum_analyzable_plants_per_direct_world"] == plan["independent_direct_phi"]["minimum_analyzable_plants_per_world"]
    assert out["sampling"]["recruitment_plants_per_direct_world"] == plan["independent_direct_phi"]["recruitment_plants_per_world"]


def test_z_grid_count_mismatch_is_rejected() -> None:
    effect = _effect()
    effect["z_grid"]["levels"] = effect["z_grid"]["levels"][:-1]
    with pytest.raises(ValueError, match="z-level count mismatch"):
        compiler.compile_sampling(effect, _precision_freeze(), _plan())


def test_context_mismatch_is_rejected() -> None:
    effect = _effect()
    effect["context"]["population_id"] = "pop2"
    with pytest.raises(ValueError, match="context mismatch"):
        compiler.compile_sampling(effect, _precision_freeze(), _plan())


def test_compiler_refuses_an_already_final_frozen_effect_contract() -> None:
    effect = _effect()
    effect["context"]["frozen_before_g3_g5_outcomes"] = True
    with pytest.raises(ValueError, match="before final effect freeze"):
        compiler.compile_sampling(effect, _precision_freeze(), _plan())


def test_tampered_precision_target_is_rejected() -> None:
    plan = copy.deepcopy(_plan())
    plan["targets"]["minimum_abs_architecture_value_Phi"] = 0.9
    with pytest.raises(ValueError, match="Phi target mismatch"):
        compiler.compile_sampling(_effect(), _precision_freeze(), plan)
