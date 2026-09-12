from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_pedicularis_g3_g5_layout.py"
ADJUDICATOR = ROOT / "scripts" / "adjudicate_pedicularis_g3_g5_effect.py"

spec = importlib.util.spec_from_file_location("ped_g35_gen", GENERATOR)
gen = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(gen)

spec2 = importlib.util.spec_from_file_location("ped_g35_adj", ADJUDICATOR)
adj = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(adj)


CTX = {
    "system": "Pedicularis rex",
    "context_id": "ped-rex-pop1-2027-v1",
    "population_id": "pop1",
    "season_id": "2027",
    "fitness_scale_id": "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER",
    "time_horizon_id": "FLOWER_TO_MATURE_VIABLE_SEED",
    "primary_y_metric": "RETENTION_MEAN_MAX_ML",
    "q5_route": "NEGLIGIBLE_BURDEN_EQUIVALENCE",
}


def _freeze(route: str = "SAME_BLOCK_INTERNAL_IDENTITY", q5_route: str = "NEGLIGIBLE_BURDEN_EQUIVALENCE") -> dict:
    direct = route == "INDEPENDENT_DIRECT_PHI_BLOCK"
    context = dict(CTX)
    context["q5_route"] = q5_route
    return {
        "schema_version": "SLK_PEDICULARIS_G3_G5_EFFECT_FREEZE_V1",
        "status": "FROZEN_CANDIDATE",
        "context": {
            **context,
            "estimation_route": route,
            "decomposition_dataset_id": "PED_G3_G5_RK_CONFIRM_V1",
            "direct_phi_dataset_id": "PED_G5_DIRECT_CONFIRM_V1",
            "frozen_before_g3_g5_outcomes": True,
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
            "minimum_analyzable_plants_per_world": 6,
            "recruitment_plants_per_world": 8,
            "minimum_analyzable_plants_per_direct_world": 6 if direct else None,
            "recruitment_plants_per_direct_world": 8 if direct else None,
            "flowers_per_z_level_per_plant": 1,
            "sample_size_source": "PROSPECTIVE_EFFECT_PRECISION_PLAN_V1",
            "sample_size_rationale": "registered CI-width and minimum-effect planning before outcomes",
        },
        "analysis": {
            "grid_estimand": "MAX_REGISTERED_WORLD_X_Z_CELL_MEAN",
            "bootstrap_reoptimizes_grid_maximum_each_replicate": True,
            "bootstrap_seed": 991,
            "bootstrap_reps": 1000,
            "minimum_bootstrap_reps": 1000,
            "minimum_valid_fraction": 0.90,
            "ci_level": 0.95,
            "resampling_unit": "INDEPENDENT_PLANT_WITH_COMPLETE_Z_GRID",
            "burden_correction": "ADD_INDEPENDENT_D0_QUALIFICATION_B_DEVICE_TO_OBSERVED_D0_WORLD",
            "burden_uncertainty_rule": "CONSERVATIVE_INTERVAL_ADDITION_FOR_R_AND_K; CANCELLATION_RETAINED_FOR_PHI",
        },
        "independent_concordance": {
            "max_abs_phi_point_difference": 0.30 if direct else None,
            "residual_ci_must_include_zero": True,
            "required_only_for_route": "INDEPENDENT_DIRECT_PHI_BLOCK",
        },
        "firewall": {
            "g1_g2_units_reused_for_g3_g5_forbidden": True,
            "y_cal_units_reused_for_g3_g5_forbidden": True,
            "d0_cal_units_reused_for_g3_g5_forbidden": True,
            "d0_qualification_units_reused_for_g3_g5_forbidden": True,
            "structural_y_function_units_reused_for_g3_g5_forbidden": True,
            "z_grid_change_after_outcomes_forbidden": True,
            "world_definition_change_after_outcomes_forbidden": True,
            "sample_size_reduction_after_outcomes_forbidden": True,
            "route_change_after_outcomes_forbidden": True,
            "burden_correction_source_change_after_outcomes_forbidden": True,
        },
        "freeze_metadata": {
            "slk_source_commit": "abc123",
            "g2_receipt_reference": "g2-receipt-1",
            "structural_y_receipt_reference": "y-receipt-1",
            "structural_y_function_receipt_reference": "yf-receipt-1",
            "d0_qualification_receipt_reference": "d0-receipt-1",
            "freeze_commit": "freeze123",
            "freeze_timestamp": "2027-05-01T00:00:00Z",
        },
        "production_status": "PEDICULARIS_G3_G5_EFFECT_PROSPECTIVELY_FROZEN",
    }


def _g2() -> dict:
    return {
        "g1": "DIRECT_PASS",
        "g2": "DIRECT_PASS",
        "g2_detail": "G2_DIRECT_PASS_POSITIVE",
        "context": {
            "context_id": CTX["context_id"],
            "system": "Pedicularis rex",
            "population_id": CTX["population_id"],
            "season_id": CTX["season_id"],
            "fitness_scale_id": CTX["fitness_scale_id"],
        },
        "conflict_load": {"point": 4.0, "lower_95": 2.0, "upper_95": 6.0},
        "downstream_balance_eligible": True,
        "downstream_bita_non_circular_eligible": True,
    }


def _y_receipt() -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_STRUCTURAL_Y_CALIBRATION_RECEIPT_V1",
        "status": "STRUCTURAL_Y_Y0_RANGE_QUALIFIED_Y1_AUDITED",
        "context": {
            "system": "Pedicularis rex",
            "context_id": CTX["context_id"],
            "population_id": CTX["population_id"],
            "season_id": CTX["season_id"],
            "fitness_scale_id": CTX["fitness_scale_id"],
            "time_horizon_id": CTX["time_horizon_id"],
            "y_cal_dataset_id": "PED_Y_CAL_V1",
        },
        "primary_y_metric": CTX["primary_y_metric"],
        "band_freeze": {
            "low_y_max": 2.0,
            "high_y_min": 4.0,
            "recruitment_authorized_for_disjoint_d0_cal": True,
        },
    }


def _y_function() -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_STRUCTURAL_Y_FUNCTION_RECEIPT_V1",
        "status": "STRUCTURAL_Y_Y2_PREFERENTIAL_LOADING_Y3_PERFORMANCE_INTERVENTION",
        "context": {
            "system": "Pedicularis rex",
            "population_id": CTX["population_id"],
            "season_id": CTX["season_id"],
            "fitness_scale_id": CTX["fitness_scale_id"],
            "time_horizon_id": CTX["time_horizon_id"],
            "d0_cal_dataset_id": "PED_D0_CAL_V1",
        },
        "primary_y_metric": CTX["primary_y_metric"],
        "y2": {"pass": True},
        "y3": {"pass": True},
    }


def _d0(route: str = "NEGLIGIBLE_BURDEN_EQUIVALENCE") -> dict:
    burden = {
        "pass": True,
        "complete_n": 24,
        "required_n": 24,
        "point_difference": 0.20,
        "criterion": "EQUIVALENCE" if route == "NEGLIGIBLE_BURDEN_EQUIVALENCE" else "MAX_CI_HALF_WIDTH",
        "ci": [0.10, 0.30],
    }
    if route == "NEGLIGIBLE_BURDEN_EQUIVALENCE":
        burden.update({"margin": 0.50, "ci_level": 0.90})
    else:
        burden.update({"max_ci_half_width": 0.20, "observed_half_width": 0.10, "ci_level": 0.95})
    return {
        "schema_version": "SLK_PEDICULARIS_D0_CONFIRMATORY_RECEIPT_V1",
        "status": "D0_FULLY_QUALIFIED",
        "context": {
            "system": "Pedicularis rex",
            "dataset_id": "PED_D0_QUAL_CONFIRM_V1",
            "context_id": CTX["context_id"],
            "population_id": CTX["population_id"],
            "season_id": CTX["season_id"],
            "fitness_scale_id": CTX["fitness_scale_id"],
            "time_horizon_id": CTX["time_horizon_id"],
            "primary_y_metric": CTX["primary_y_metric"],
            "q5_route": route,
        },
        "gates": {
            "D0_Q1_z_preserved": True,
            "D0_Q2_functional_benefit_matched": True,
            "D0_Q3_pollination_facing_equivalent": True,
            "D0_Q4_antagonist_channel_fidelity": True,
            "D0_Q5_apparatus_burden_accounted": True,
            "D0_Q6_common_horizon": True,
        },
        "apparatus_burden_receipt": burden,
        "firewall": {"d0_qualification_units_g3_g5_ineligible": True},
    }


def _make(route: str = "SAME_BLOCK_INTERNAL_IDENTITY", q5_route: str = "NEGLIGIBLE_BURDEN_EQUIVALENCE"):
    freeze = _freeze(route, q5_route=q5_route)
    d0 = _d0(q5_route)
    decomp, direct, meta = gen.generate_layout(
        freeze, _g2(), _y_receipt(), _y_function(), d0, randomization_seed=77
    )
    return freeze, decomp, direct, meta, d0


def _fill(rows: list[dict[str, str]], direct_shift: float = 0.0) -> list[dict[str, str]]:
    out = copy.deepcopy(rows)
    for row in out:
        i = int(row["plant_id"].rsplit("-", 1)[1])
        z = float(row["target_exsertion_z"])
        row["baseline_primary_y_value"] = "1.5" if row["world"] in {"S", "D0"} else "4.5"
        row["realized_exsertion_z"] = str(z + 0.001 * ((i % 3) - 1))
        noise = 0.015 * ((i % 5) - 2)
        if row["world"] == "S":
            value = 10.0 - 5.0 * (z - 0.30) ** 2 + noise
        elif row["world"] == "D0":
            value = 11.8 - 4.0 * (z - 0.40) ** 2 + noise
        else:
            value = 9.0 - 4.0 * (z - 0.30) ** 2 + noise + direct_shift
        row["mature_viable_undamaged_seeds"] = str(value)
    return out


def test_generator_creates_registered_complete_grid_worlds() -> None:
    freeze, decomp, direct, meta, _ = _make()
    assert direct == []
    assert len(decomp) == 3 * 8 * 5
    assert meta["decomposition"]["recruitment_plants_per_world"] == 8
    assert meta["z_grid"] == freeze["z_grid"]["levels"]
    assert {row["world"] for row in decomp} == {"S", "D0", "D"}


def test_same_block_closes_g3_g5_and_recovers_persistent_compromise_pattern() -> None:
    freeze, decomp, _, _, d0 = _make()
    result = adj.adjudicate(_fill(decomp), None, freeze, _g2(), _y_receipt(), _y_function(), d0)
    assert result["status"] == "PEDICULARIS_G3_G5_MEASURED_INTERNAL_IDENTITY"
    assert result["g3_R"]["positive_robustly"] is True
    assert result["g5_Phi_internal"]["classification"] == "PERSISTENT_COMPROMISE"
    assert result["g5_Phi_internal"]["identity_check"]["equals_internal_Phi"] is True
    assert result["diagnostic_pattern"] == "CONFLICT_REAL_RECOVERABLE_BUT_ARCHITECTURE_NOT_WORTH_COST"
    assert result["burden_correction"]["pre_cost_D0_optimum"] == pytest.approx(
        result["burden_correction"]["observed_D0_optimum"] + 0.20
    )


def test_burden_correction_enters_R_and_K_but_cancels_from_phi() -> None:
    freeze, decomp, _, _, d0a = _make()
    d0b = copy.deepcopy(d0a)
    d0b["apparatus_burden_receipt"]["point_difference"] = 0.40
    d0b["apparatus_burden_receipt"]["ci"] = [0.30, 0.50]
    a = adj.adjudicate(_fill(decomp), None, freeze, _g2(), _y_receipt(), _y_function(), d0a)
    b = adj.adjudicate(_fill(decomp), None, freeze, _g2(), _y_receipt(), _y_function(), d0b)
    assert b["g3_R"]["point"] - a["g3_R"]["point"] == pytest.approx(0.20)
    assert b["g4_K"]["point"] - a["g4_K"]["point"] == pytest.approx(0.20)
    assert b["g5_Phi_internal"]["point"] == pytest.approx(a["g5_Phi_internal"]["point"])


def test_measured_burden_route_uses_independent_burden_ci() -> None:
    freeze, decomp, _, _, d0 = _make(q5_route="MEASURED_BURDEN_ADJUSTMENT")
    result = adj.adjudicate(_fill(decomp), None, freeze, _g2(), _y_receipt(), _y_function(), d0)
    assert result["burden_correction"]["uncertainty_source"] == "INDEPENDENT_Q5_MEASURED_BURDEN_CI"
    assert result["burden_correction"]["uncertainty_lower"] == pytest.approx(0.10)
    assert result["burden_correction"]["uncertainty_upper"] == pytest.approx(0.30)


def test_independent_direct_phi_can_close_nontrivial_concordance() -> None:
    freeze, decomp, direct, _, d0 = _make("INDEPENDENT_DIRECT_PHI_BLOCK")
    result = adj.adjudicate(_fill(decomp), _fill(direct), freeze, _g2(), _y_receipt(), _y_function(), d0)
    assert result["status"] == "PEDICULARIS_G3_G5_MEASURED_CONCORDANT"
    assert result["bridge_concordance"]["concordant"] is True
    assert result["bridge_concordance"]["ci_includes_zero"] is True


def test_independent_direct_phi_disagreement_is_not_silently_promoted() -> None:
    freeze, decomp, direct, _, d0 = _make("INDEPENDENT_DIRECT_PHI_BLOCK")
    result = adj.adjudicate(
        _fill(decomp), _fill(direct, direct_shift=2.0), freeze, _g2(), _y_receipt(), _y_function(), d0
    )
    assert result["status"] == "PEDICULARIS_G3_G5_MEASURED_BRIDGE_NOT_CONCORDANT"
    assert result["bridge_concordance"]["concordant"] is False


def test_z_tolerance_failures_can_drop_world_below_registered_floor() -> None:
    freeze, decomp, _, _, d0 = _make()
    rows = _fill(decomp)
    s_plant_ids = sorted({row["plant_id"] for row in rows if row["world"] == "S"})
    bad_plants = set(s_plant_ids[:3])
    for row in rows:
        if row["plant_id"] in bad_plants:
            row["realized_exsertion_z"] = str(float(row["target_exsertion_z"]) + 0.10)
    result = adj.adjudicate(rows, None, freeze, _g2(), _y_receipt(), _y_function(), d0)
    assert result["status"] == "PEDICULARIS_G3_G5_EFFECT_INCOMPLETE"


def test_effect_chain_requires_fully_qualified_d0() -> None:
    freeze, decomp, _, _, d0 = _make()
    d0["status"] = "D0_FUNCTION_MATCH_ONLY"
    with pytest.raises(ValueError, match="fully qualified"):
        adj.adjudicate(_fill(decomp), None, freeze, _g2(), _y_receipt(), _y_function(), d0)


def test_effect_chain_requires_same_g2_context() -> None:
    freeze, decomp, _, _, d0 = _make()
    g2 = _g2()
    g2["context"]["population_id"] = "pop2"
    with pytest.raises(ValueError, match="G2/effect context mismatch"):
        adj.adjudicate(_fill(decomp), None, freeze, g2, _y_receipt(), _y_function(), d0)


def test_same_block_route_refuses_direct_dataset_peeking() -> None:
    freeze, decomp, _, _, d0 = _make()
    fake_direct = copy.deepcopy(_fill(decomp[:10]))
    with pytest.raises(ValueError, match="must not inspect"):
        adj.adjudicate(_fill(decomp), fake_direct, freeze, _g2(), _y_receipt(), _y_function(), d0)
