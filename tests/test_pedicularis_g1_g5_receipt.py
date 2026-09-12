from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "adjudicate_pedicularis_g1_g5_receipt.py"
spec = importlib.util.spec_from_file_location("ped_g1_g5", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)
adjudicate = module.adjudicate


def _receipt():
    return {
        "receipt_schema_version": "SLK_PEDICULARIS_G1_G5_RECEIPT_V1",
        "context": {
            "context_id": "ped-rex-pop1-2027-v1",
            "system": "Pedicularis rex",
            "population_id": "pop1",
            "season_id": "2027",
            "fitness_scale_id": "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER",
            "time_horizon_id": "flower-to-mature-seed",
            "z_trait_id": "exsertion",
            "y_trait_id": "water-retention-performance",
        },
        "upstream_g1_g2": {
            "g1": "DIRECT_PASS",
            "g2": "DIRECT_PASS",
            "g2_detail": "G2_DIRECT_PASS_POSITIVE",
            "conflict_load": {"point": 4.0, "lower_95": 2.0, "upper_95": 6.0},
            "anti_circularity": {
                "water_used_as_sch_antagonist_G": False,
                "independent_predator_exposure_used": True,
                "water_y_held_fixed_during_sch_surface": True,
            },
        },
        "functional_state_lane": {"status": "DIRECT_PASS"},
        "structural_y": {
            "status": "QUALIFIED",
            "Y0_repeatable_variation": True,
            "Y1_x_y_independence_audited": True,
            "Y2_preferential_loading": True,
            "Y2_pollination_cross_effect_bounded": True,
            "Y3_intervention_or_natural_experiment": True,
        },
        "d0_qualification": {
            "status": "QUALIFIED",
            "D0_Q1_z_preserved": True,
            "D0_Q2_functional_benefit_matched": True,
            "D0_Q3_pollination_facing_equivalent": True,
            "D0_Q4_antagonist_channel_fidelity": True,
            "D0_Q5_apparatus_burden_accounted": True,
            "D0_Q6_common_horizon": True,
        },
        "worlds": {
            "S": {"registered_prospectively": True, "optimized_fitness": {"point": 10.0, "lower_95": 9.0, "upper_95": 11.0}},
            "D0": {"registered_prospectively": True, "optimized_fitness": {"point": 13.0, "lower_95": 12.0, "upper_95": 14.0}},
            "D": {"registered_prospectively": True, "optimized_fitness": {"point": 9.0, "lower_95": 8.0, "upper_95": 10.0}},
        },
        "g3_R": {"status": "RECOVERABLE_ARCHITECTURE_BENEFIT_IDENTIFIED", "comparison": "S_TO_D0", "point": 3.0, "lower_95": 1.0, "upper_95": 5.0},
        "g4_K": {"status": "ARCHITECTURE_COST_IDENTIFIED", "comparison": "D0_TO_D", "point": 4.0, "lower_95": 2.0, "upper_95": 6.0, "double_counting_audit_pass": True},
        "g5_Phi": {
            "direct": {"status": "IDENTIFIED", "comparison": "S_TO_D", "point": -1.0, "lower_95": -2.0, "upper_95": -0.2},
            "decomposed": {"status": "IDENTIFIED", "point": -1.0, "lower_95": -2.2, "upper_95": -0.1},
            "bridge_residual": {"point": 0.0, "lower_95": -0.2, "upper_95": 0.2},
            "bridge_concordance": {"frozen_before_confirmatory_outcomes": True, "max_abs_point": 0.25},
        },
    }


def test_closes_same_system_g1_g5_and_recovers_diagnostic_pattern():
    result = adjudicate(_receipt())
    assert result["status"] == "STRUCTURAL_G1_G5_CLOSED_CONCORDANT"
    assert result["claim_ceiling"] == "SAME_SYSTEM_G1_G5"
    assert result["Phi_class"] == "PERSISTENT_COMPROMISE"
    assert result["diagnostic_pattern"] == "CONFLICT_REAL_RECOVERABLE_BUT_ARCHITECTURE_NOT_WORTH_COST"


def test_invalid_d0_falls_back_to_direct_phi_without_fake_k():
    r = _receipt()
    r["d0_qualification"]["D0_Q2_functional_benefit_matched"] = False
    result = adjudicate(r)
    assert result["status"] == "STRUCTURAL_DIRECT_PHI_IDENTIFIED"
    assert result["claim_ceiling"] == "DIRECT_ARCHITECTURE_VALUE_ONLY"


def test_functional_state_does_not_promote_structural_chain():
    r = _receipt()
    r["structural_y"]["status"] = "NOT_QUALIFIED"
    result = adjudicate(r)
    assert result["status"] == "FUNCTIONAL_STATE_RELEASE_ONLY"


def test_water_as_g_is_rejected():
    r = _receipt()
    r["upstream_g1_g2"]["anti_circularity"]["water_used_as_sch_antagonist_G"] = True
    with pytest.raises(ValueError, match="water-as-G"):
        adjudicate(r)


def test_broken_R_identity_is_rejected():
    r = _receipt()
    r["g3_R"]["point"] = 2.5
    with pytest.raises(ValueError, match="R identity"):
        adjudicate(r)
