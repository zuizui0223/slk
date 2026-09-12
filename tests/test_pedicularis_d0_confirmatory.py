from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_pedicularis_d0_confirmatory_layout.py"
ADJUDICATOR = ROOT / "scripts" / "adjudicate_pedicularis_d0_confirmatory.py"
MARGIN_TEMPLATE = ROOT / "data" / "PEDICULARIS_D0_MARGIN_FREEZE_TEMPLATE_V1.json"

spec = importlib.util.spec_from_file_location("ped_d0_q_gen", GENERATOR)
gen = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(gen)

spec2 = importlib.util.spec_from_file_location("ped_d0_q_adj", ADJUDICATOR)
adj = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(adj)


def _y_receipt() -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_STRUCTURAL_Y_CALIBRATION_RECEIPT_V1",
        "status": "STRUCTURAL_Y_Y0_RANGE_QUALIFIED_Y1_AUDITED",
        "context": {
            "system": "Pedicularis rex",
            "context_id": "ctx1",
            "population_id": "pop1",
            "season_id": "2027",
            "fitness_scale_id": "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER",
            "time_horizon_id": "FLOWER_TO_MATURE_VIABLE_SEED",
            "y_cal_dataset_id": "PED_Y_CAL_V1",
        },
        "primary_y_metric": "RETENTION_MEAN_MAX_ML",
        "band_freeze": {
            "low_y_max": 2.0,
            "high_y_min": 3.0,
            "dynamic_range_pass": True,
            "recruitment_authorized_for_disjoint_d0_cal": True,
        },
    }


def _analysis_freeze(route: str = "NEGLIGIBLE_BURDEN_EQUIVALENCE") -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_D0_CONFIRMATORY_ANALYSIS_FREEZE_V1",
        "status": "D0_CONFIRMATORY_ANALYSIS_PROSPECTIVELY_FROZEN",
        "context": {
            "system": "Pedicularis rex",
            "dataset_id": "PED_D0_QUAL_CONFIRM_V1",
            "context_id": "ctx1",
            "population_id": "pop1",
            "season_id": "2027",
            "primary_y_metric": "RETENTION_MEAN_MAX_ML",
            "fitness_scale_id": "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER",
            "time_horizon_id": "FLOWER_TO_MATURE_VIABLE_SEED",
            "q5_route": route,
            "frozen_before_confirmatory_outcomes": True,
        },
        "analysis": {
            "equivalence_ci_level": 0.90,
            "directional_superiority_alpha": 0.05,
            "burden_precision_ci_level": 0.95,
            "bootstrap_seed": 404,
            "bootstrap_reps": 2000,
            "minimum_bootstrap_reps": 2000,
            "minimum_valid_fraction": 0.90,
            "resampling_unit": "INDEPENDENT_PLANT",
        },
        "layout": {
            "low_y_treatments": ["S_QUAL", "SHAM_QUAL", "D0_QUAL"],
            "high_y_treatments": ["D_QUAL"],
            "low_y_within_plant_randomized": True,
            "high_y_single_natural_state": True,
        },
        "firewall": {
            "d0_qualification_units_g3_g5_ineligible": True,
            "margins_cannot_be_revised_from_confirmatory_outcomes": True,
            "sample_size_cannot_be_reduced_after_outcomes": True,
            "failed_gate_cannot_be_rescued_by_endpoint_switch": True,
            "q5_route_cannot_change_after_outcomes": True,
        },
        "freeze_metadata": {
            "slk_source_commit": "slk123",
            "margin_freeze_commit": "margin123",
            "precision_plan_reference": "precision123",
            "structural_y_receipt_reference": "yreceipt123",
            "freeze_commit": "confirm123",
            "freeze_timestamp": "2027-05-02T00:00:00Z",
        },
        "production_status": "D0_CONFIRMATORY_ANALYSIS_PROSPECTIVELY_FROZEN",
    }


def _margin(route: str = "NEGLIGIBLE_BURDEN_EQUIVALENCE") -> dict:
    m = json.loads(MARGIN_TEMPLATE.read_text())
    m["status"] = "FROZEN_CANDIDATE"
    m["context"].update(
        {
            "population_id": "pop1",
            "season_id": "2027",
            "time_horizon_id": "FLOWER_TO_MATURE_VIABLE_SEED",
            "confirmatory_dataset_id": "PED_D0_QUAL_CONFIRM_V1",
            "q5_route": route,
        }
    )
    values = {
        "D0_Q1_Z": 0.01,
        "D0_Q1_OPENING": 0.20,
        "D0_Q1_STIGMA": 0.20,
        "D0_Q1_ORIENTATION": 2.0,
        "D0_Q1_DAMAGE": 0.03,
        "D0_Q2_VOLUME": 0.20,
        "D0_Q2_DURATION": 2.0,
        "D0_Q2_COVERAGE": 0.05,
        "D0_Q2_PROTECTION": 0.05,
        "D0_Q3_VISIT": 0.20,
        "D0_Q3_POLLEN": 1.0,
        "D0_Q3_INITIAL_SEED": 0.03,
        "D0_Q4_WET_EFFECT": 0.10,
        "D0_Q4_DRY_RESIDUAL": 0.03,
        "D0_Q5_BURDEN_EQ": 1.0,
        "D0_Q5_BURDEN_PRECISION": 0.50,
    }
    for endpoint in m["endpoints"]:
        eid = endpoint["endpoint_id"]
        if eid in values:
            endpoint["value"] = values[eid]
        endpoint["margin_basis"] = "prospectively frozen biological or decision-invariance margin"
        endpoint["source_reference"] = ["fixture-independent-freeze"]
        endpoint["biological_rationale"] = "preserve registered D0 interpretation"
        endpoint["calibration_dataset_id"] = "PED_D0_CAL_V1"
        endpoint["variance_only_basis"] = False
        endpoint["derived_from_confirmatory_outcome"] = False
        endpoint["frozen_before_confirmatory_outcomes"] = True
        if eid == "D0_Q4_WET_EFFECT":
            endpoint["source_type"] = "BIOLOGICAL_RELEVANCE_PLUS_CALIBRATION"
        elif eid in {"D0_Q5_BURDEN_EQ", "D0_Q5_BURDEN_PRECISION"}:
            endpoint["source_type"] = "DOWNSTREAM_DECISION_INVARIANCE"
        elif eid == "D0_Q6_HORIZON":
            endpoint["source_type"] = "DESIGN_INVARIANCE"
            endpoint["calibration_dataset_id"] = None
        else:
            endpoint["source_type"] = "FUNCTIONAL_INVARIANCE"
    m["freeze_metadata"] = {
        "slk_source_commit": "slk123",
        "freeze_commit": "margin123",
        "freeze_timestamp": "2027-05-01T00:00:00Z",
    }
    return m


def _precision(route: str = "NEGLIGIBLE_BURDEN_EQUIVALENCE") -> dict:
    return {
        "planner_schema_version": "SLK_PEDICULARIS_Y_D0_PRECISION_PLAN_V1",
        "status": "PLANNING_ONLY_NOT_A_BIOLOGICAL_RECEIPT",
        "input_provenance": {
            "population_id": "pop1",
            "season_id": "2027",
            "fitness_scale_id": "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER",
            "time_horizon_id": "FLOWER_TO_MATURE_VIABLE_SEED",
            "y_cal_dataset_id": "PED_Y_CAL_V1",
            "d0_cal_dataset_id": "PED_D0_CAL_V1",
            "confirmatory_dataset_id": "PED_D0_QUAL_CONFIRM_V1",
            "confirmatory_outcomes_opened": False,
            "margin_freeze_commit": "margin123",
            "q5_route": route,
        },
        "results": [],
        "maxima_by_allocation_unit": {
            "paired_plants_total": {"inflated_required_n": 24, "driving_endpoints": ["D0_Q3_POLLEN"]},
            "plants_per_group": {"inflated_required_n": 24, "driving_endpoints": ["D0_Q2_VOLUME"]},
            "plants_total": {"inflated_required_n": 20, "driving_endpoints": ["D0_Q5_BURDEN_PRECISION"]},
        },
    }


def _layout(route: str = "NEGLIGIBLE_BURDEN_EQUIVALENCE") -> list[dict[str, str]]:
    rows, _ = gen.generate_layout(_precision(route), _y_receipt(), _analysis_freeze(route), 777)
    out = copy.deepcopy(rows)
    for row in out:
        i = int(row["plant_id"].rsplit("-", 1)[1])
        t = row["treatment"]
        if row["phenotype_stratum"] == "LOW_Y":
            natural_y = 1.35 + 0.005 * i
        else:
            natural_y = 3.55 + 0.006 * i
        y = 3.58 + 0.004 * i if t == "D0_QUAL" else natural_y

        row["retention_trial1_max_ml"] = str(y - 0.01)
        row["retention_trial2_max_ml"] = str(y + 0.01)
        row["retention_trial1_depth_mm"] = str(8.0 + 0.05 * i + (0.10 if t == "D_QUAL" else 0.0))
        row["retention_trial2_depth_mm"] = str(8.1 + 0.05 * i + (0.10 if t == "D_QUAL" else 0.0))
        if t in {"D0_QUAL", "D_QUAL"}:
            half = 38.0 + 0.08 * i + (0.30 if t == "D_QUAL" else 0.0)
            coverage = 0.76 + 0.001 * i + (0.005 if t == "D_QUAL" else 0.0)
        else:
            half = 10.0 + 0.05 * i
            coverage = 0.22 + 0.001 * i
        row["retention_trial1_half_life_min"] = str(half - 0.2)
        row["retention_trial2_half_life_min"] = str(half + 0.2)
        row["retention_trial1_protected_fraction"] = str(coverage - 0.003)
        row["retention_trial2_protected_fraction"] = str(coverage + 0.003)

        base_z = 0.30 + 0.0006 * i
        if t == "D0_QUAL":
            z = base_z + 0.001 + 0.00001 * i
        elif t == "SHAM_QUAL":
            z = base_z + 0.0002 * (i % 2)
        else:
            z = base_z
        row["exsertion_z"] = str(z)
        row["opening_width_mm"] = str(4.0 + 0.01 * i + (0.02 if t == "D0_QUAL" else 0.0))
        row["stigma_position_mm"] = str(2.0 + 0.005 * i + (0.01 if t == "D0_QUAL" else 0.0))
        row["orientation_deg"] = str(20.0 + 0.2 * i + (0.20 if t == "D0_QUAL" else 0.0))
        row["mechanical_damage_post_prop"] = str(0.010 + 0.0001 * i + (0.002 if t == "D0_QUAL" else 0.0))

        if t == "D0_QUAL":
            attack = 0.20 + 0.0008 * i
        elif t == "D_QUAL":
            attack = 0.205 + 0.0007 * i
        elif t == "SHAM_QUAL":
            attack = 0.42 + 0.0008 * i
        else:
            attack = 0.415 + 0.0007 * i
        row["early_attack_prop"] = str(attack)
        row["seed_predation_prop"] = str(min(0.95, attack + 0.08))

        row["pollinator_observation_minutes"] = "10"
        row["legitimate_visits"] = str(4 + (i % 4))
        row["handling_time_s"] = str(2.0 + 0.01 * (i % 3))
        row["pollen_receipt_grains"] = str(12.0 + 0.2 * i + (0.10 if t == "D0_QUAL" else 0.0))
        row["initial_seed_set_prop"] = str(0.34 + 0.001 * i + (0.002 if t == "D0_QUAL" else 0.0))

        if t == "S_QUAL":
            seeds = 12.0 + 0.15 * i
        elif t == "SHAM_QUAL":
            seeds = 11.8 + 0.145 * i
        elif t == "D0_QUAL":
            seeds = 15.0 + 0.16 * i
        else:
            seeds = 14.9 + 0.155 * i
        row["mature_viable_undamaged_seeds"] = str(seeds)
    return out


def test_precision_plan_drives_low_and_high_confirmatory_allocation() -> None:
    rows, meta = gen.generate_layout(_precision(), _y_receipt(), _analysis_freeze(), 777)
    assert meta["allocation"]["low_y_independent_plants"] == 24
    assert meta["allocation"]["high_y_independent_plants"] == 24
    assert len(rows) == 24 * 3 + 24
    assert all(row["g3_g5_eligible"] == "false" for row in rows)


def test_registered_pass_fixture_fully_qualifies_d0() -> None:
    result = adj.adjudicate(_layout(), _margin(), _precision(), _y_receipt(), _analysis_freeze())
    assert result["status"] == "D0_FULLY_QUALIFIED"
    assert all(result["gates"].values())
    assert result["structural_y_band_failure_count"] == 0
    assert result["firewall"]["d0_qualification_units_g3_g5_ineligible"] is True


def test_q2_benefit_mismatch_makes_d0_not_qualified() -> None:
    rows = _layout()
    for row in rows:
        if row["treatment"] == "D0_QUAL":
            row["retention_trial1_max_ml"] = "2.4"
            row["retention_trial2_max_ml"] = "2.4"
    result = adj.adjudicate(rows, _margin(), _precision(), _y_receipt(), _analysis_freeze())
    assert result["gates"]["D0_Q2_functional_benefit_matched"] is False
    assert result["status"] == "D0_NOT_QUALIFIED"


def test_q3_pollination_contamination_keeps_only_function_match() -> None:
    rows = _layout()
    for row in rows:
        if row["treatment"] == "D0_QUAL":
            row["pollen_receipt_grains"] = str(float(row["pollen_receipt_grains"]) + 4.0)
    result = adj.adjudicate(rows, _margin(), _precision(), _y_receipt(), _analysis_freeze())
    assert result["gates"]["D0_Q2_functional_benefit_matched"] is True
    assert result["gates"]["D0_Q3_pollination_facing_equivalent"] is False
    assert result["status"] == "D0_FUNCTION_MATCH_ONLY"


def test_q5_large_apparatus_burden_blocks_full_qualification() -> None:
    rows = _layout()
    for row in rows:
        if row["treatment"] == "SHAM_QUAL":
            row["mature_viable_undamaged_seeds"] = str(float(row["mature_viable_undamaged_seeds"]) - 3.0)
    result = adj.adjudicate(rows, _margin(), _precision(), _y_receipt(), _analysis_freeze())
    assert result["gates"]["D0_Q5_apparatus_burden_accounted"] is False
    assert result["status"] == "D0_FUNCTION_MATCH_ONLY"


def test_measured_burden_adjustment_route_can_fully_qualify() -> None:
    route = "MEASURED_BURDEN_ADJUSTMENT"
    result = adj.adjudicate(
        _layout(route), _margin(route), _precision(route), _y_receipt(), _analysis_freeze(route)
    )
    assert result["status"] == "D0_FULLY_QUALIFIED"
    assert result["context"]["q5_route"] == route
    burden = result["apparatus_burden_receipt"]
    assert burden["criterion"] == "MAX_CI_HALF_WIDTH"
    assert burden["pass"] is True


def test_precision_plan_from_wrong_margin_freeze_is_rejected() -> None:
    plan = _precision()
    plan["input_provenance"]["margin_freeze_commit"] = "other-margin"
    with pytest.raises(ValueError, match="different margin freeze"):
        adj.adjudicate(_layout(), _margin(), plan, _y_receipt(), _analysis_freeze())


def test_g3_g5_eligibility_leak_is_rejected() -> None:
    rows = _layout()
    rows[0]["g3_g5_eligible"] = "true"
    with pytest.raises(ValueError, match="leaked into G3-G5"):
        adj.adjudicate(rows, _margin(), _precision(), _y_receipt(), _analysis_freeze())
