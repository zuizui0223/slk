from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SUMMARIZER = ROOT / "scripts" / "summarize_pedicularis_g3_g5_planning_variance.py"
PLANNER = ROOT / "scripts" / "plan_pedicularis_g3_g5_effect_precision.py"

spec = importlib.util.spec_from_file_location("ped_g35_var", SUMMARIZER)
varmod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(varmod)

spec2 = importlib.util.spec_from_file_location("ped_g35_precision", PLANNER)
planmod = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(planmod)


CTX = {
    "context_id": "ped-rex-pop1-2027-v1",
    "population_id": "pop1",
    "season_id": "2027",
    "fitness_scale_id": "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER",
    "time_horizon_id": "FLOWER_TO_MATURE_VIABLE_SEED",
}


def _d0_receipt() -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_D0_CONFIRMATORY_RECEIPT_V1",
        "status": "D0_FULLY_QUALIFIED",
        "context": {
            "system": "Pedicularis rex",
            "dataset_id": "PED_D0_QUAL_CONFIRM_V1",
            **CTX,
            "primary_y_metric": "RETENTION_MEAN_MAX_ML",
            "q5_route": "NEGLIGIBLE_BURDEN_EQUIVALENCE",
        },
        "precision_plan": {
            "observed_low_y_plants": 3,
            "observed_high_y_plants": 3,
        },
        "gates": {
            "D0_Q1_z_preserved": True,
            "D0_Q2_functional_benefit_matched": True,
            "D0_Q3_pollination_facing_equivalent": True,
            "D0_Q4_antagonist_channel_fidelity": True,
            "D0_Q5_apparatus_burden_accounted": True,
            "D0_Q6_common_horizon": True,
        },
        "firewall": {"d0_qualification_units_g3_g5_ineligible": True},
    }


def _row(plant_id: str, treatment: str, seeds: float) -> dict[str, str]:
    return {
        "dataset_id": "PED_D0_QUAL_CONFIRM_V1",
        "g3_g5_eligible": "false",
        **{k: str(v) for k, v in CTX.items()},
        "plant_id": plant_id,
        "treatment": treatment,
        "mature_viable_undamaged_seeds": str(seeds),
    }


def _rows() -> list[dict[str, str]]:
    rows = []
    for i, (s, d0) in enumerate([(10.0, 12.0), (11.0, 14.0), (12.0, 13.0)], start=1):
        rows.append(_row(f"L{i}", "S_QUAL", s))
        rows.append(_row(f"L{i}", "D0_QUAL", d0))
    for i, d in enumerate([9.0, 10.5, 11.0], start=1):
        rows.append(_row(f"H{i}", "D_QUAL", d))
    return rows


def _freeze() -> dict:
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
            "world_cell_mean_half_width": 0.50,
            "minimum_recoverable_benefit_R": 1.00,
            "minimum_abs_architecture_value_Phi": 0.80,
            "target_source_type": "DOWNSTREAM_DECISION_INVARIANCE",
            "target_source_reference": "SLK:G3_G5_DECISION_TARGETS_V1",
            "biological_rationale": "resolve the smallest architecture-value effects worth interpreting",
        },
        "variance_transport": {
            "use_max_independent_world_sd": True,
            "sd_safety_multiplier": 1.20,
            "multiplier_source": "PREDECLARED_TRANSPORT_SAFETY_V1",
            "multiplier_rationale": "inflate single-state D0 qualification SD for transport across the later z grid",
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


def test_completed_d0_qualification_yields_planning_variance_receipt() -> None:
    result = varmod.summarize(_rows(), _d0_receipt())
    assert result["status"] == "G3_G5_PLANNING_VARIANCE_READY"
    assert result["max_world_sd"] > 0
    assert result["world_variance"]["S"]["independent_plants"] == 3
    assert result["world_variance"]["D0"]["independent_plants"] == 3
    assert result["world_variance"]["D"]["independent_plants"] == 3
    assert result["firewall"]["source_units_g3_g5_effect_estimation_ineligible"] is True


def test_missing_final_fitness_keeps_planning_variance_incomplete() -> None:
    rows = _rows()
    rows = [r for r in rows if not (r["plant_id"] == "H3" and r["treatment"] == "D_QUAL")]
    result = varmod.summarize(rows, _d0_receipt())
    assert result["status"] == "G3_G5_PLANNING_VARIANCE_INCOMPLETE"
    assert result["expected_complete_followup"]["all_qualified_plants_have_final_fitness"] is False


def test_d0_qualification_row_cannot_be_reused_as_effect_unit() -> None:
    rows = _rows()
    rows[0]["g3_g5_eligible"] = "true"
    with pytest.raises(ValueError, match="cannot be G3-G5 eligible"):
        varmod.summarize(rows, _d0_receipt())


def test_precision_plan_uses_max_world_sd_times_frozen_multiplier() -> None:
    variance = varmod.summarize(_rows(), _d0_receipt())
    freeze = _freeze()
    result = planmod.plan(freeze, variance)
    assert result["status"] == "G3_G5_EFFECT_SAMPLE_SIZE_PROSPECTIVELY_PLANNED"
    assert result["variance_input"]["planning_sd"] == pytest.approx(
        variance["max_world_sd"] * freeze["variance_transport"]["sd_safety_multiplier"]
    )
    assert result["decomposition"]["recruitment_plants_per_world"] >= result["decomposition"]["minimum_analyzable_plants_per_world"]
    assert result["independent_direct_phi"]["recruitment_plants_per_world"] >= result["independent_direct_phi"]["minimum_analyzable_plants_per_world"]


def test_more_conservative_transport_or_precision_never_reduces_n() -> None:
    variance = varmod.summarize(_rows(), _d0_receipt())
    base = planmod.plan(_freeze(), variance)

    larger_sd = _freeze()
    larger_sd["variance_transport"]["sd_safety_multiplier"] = 1.50
    p_sd = planmod.plan(larger_sd, variance)
    assert p_sd["decomposition"]["minimum_analyzable_plants_per_world"] >= base["decomposition"]["minimum_analyzable_plants_per_world"]

    tighter = _freeze()
    tighter["targets"]["world_cell_mean_half_width"] = 0.30
    p_tight = planmod.plan(tighter, variance)
    assert p_tight["decomposition"]["minimum_analyzable_plants_per_world"] >= base["decomposition"]["minimum_analyzable_plants_per_world"]

    smaller_effect = _freeze()
    smaller_effect["targets"]["minimum_abs_architecture_value_Phi"] = 0.50
    p_effect = planmod.plan(smaller_effect, variance)
    assert p_effect["decomposition"]["minimum_analyzable_plants_per_world"] >= base["decomposition"]["minimum_analyzable_plants_per_world"]


def test_variance_only_target_source_is_rejected() -> None:
    variance = varmod.summarize(_rows(), _d0_receipt())
    freeze = _freeze()
    freeze["targets"]["target_source_type"] = "PILOT_SD_MULTIPLE_ONLY"
    with pytest.raises(ValueError, match="target source type"):
        planmod.plan(freeze, variance)


def test_precision_context_mismatch_is_rejected() -> None:
    variance = varmod.summarize(_rows(), _d0_receipt())
    freeze = _freeze()
    freeze["context"]["population_id"] = "pop2"
    with pytest.raises(ValueError, match="context mismatch"):
        planmod.plan(freeze, variance)
