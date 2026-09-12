from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PLANNER = ROOT / "scripts" / "plan_pedicularis_context_screen_effort.py"
COMPILER = ROOT / "scripts" / "compile_pedicularis_context_screen_effort.py"

spec = importlib.util.spec_from_file_location("ped_p0_effort_plan", PLANNER)
planner = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(planner)

spec2 = importlib.util.spec_from_file_location("ped_p0_effort_compile", COMPILER)
compiler = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(compiler)


CTX = {
    "candidate_site_id": "site1",
    "population_id": "pop1",
    "season_id": "2027",
    "screen_window_id": "screen1",
}


def _effort_freeze() -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_CONTEXT_SCREEN_EFFORT_FREEZE_V1",
        "status": "FROZEN_CANDIDATE",
        "context": {
            "system": "Pedicularis rex",
            **CTX,
            "frozen_before_screen_outcomes": True,
        },
        "pollinator_detection": {
            "minimum_relevant_visit_rate_per_min": 0.02,
            "desired_detection_probability": 0.95,
            "minimum_temporal_bouts": 6,
            "minimum_minutes_per_bout": 20,
            "rate_source_type": "EXTERNAL_MATCHED_PRIMARY_SOURCE",
            "rate_source_reference": "TEST_POLLINATOR_RATE_SOURCE",
            "rate_rationale": "test-only minimum relevant visit rate",
            "coverage_source_type": "DOWNSTREAM_DESIGN_REQUIREMENT",
            "coverage_source_reference": "TEST_TEMPORAL_COVERAGE_SOURCE",
            "coverage_rationale": "spread observation across multiple bouts",
        },
        "predator_detection": {
            "minimum_relevant_attack_fraction": 0.05,
            "desired_detection_probability": 0.95,
            "source_type": "EXTERNAL_MATCHED_PRIMARY_SOURCE",
            "source_reference": "TEST_PREDATOR_RATE_SOURCE",
            "biological_rationale": "test-only minimum relevant attack prevalence",
        },
        "water_state_detection": {
            "minimum_relevant_positive_fraction": 0.50,
            "desired_detection_probability": 0.95,
            "source_type": "INDEPENDENT_NATURAL_HISTORY_CALIBRATION",
            "source_reference": "TEST_WATER_SOURCE",
            "biological_rationale": "test-only minimum relevant water-state prevalence",
        },
        "capacity": {
            "reserve_fraction": 0.10,
            "source_type": "DOWNSTREAM_DESIGN_REQUIREMENT",
            "source_reference": "Y_CAL_36_PLUS_D0_CAL_48",
            "rationale": "protect the 84-plant disjoint calibration base against modest attrition",
            "census_rule": "STOP_AT_REQUIRED_CAPACITY_OR_EXHAUST_FOCAL_POPULATION",
        },
        "source_policy": {
            "allowed_relevance_sources": [
                "DOWNSTREAM_DESIGN_REQUIREMENT",
                "INDEPENDENT_NATURAL_HISTORY_CALIBRATION",
                "EXTERNAL_MATCHED_PRIMARY_SOURCE",
                "COMBINED_PREDECLARED",
            ],
            "forbidden_relevance_sources": [
                "SCREEN_OUTCOME_POSTHOC",
                "HISTORICAL_SAMPLE_SIZE_ONLY",
                "NONSIGNIFICANT_P_VALUE",
                "CONVENIENCE_ONLY",
            ],
        },
        "firewall": {
            "minimum_relevant_rates_frozen_before_screen_outcomes": True,
            "desired_detection_probabilities_frozen_before_screen_outcomes": True,
            "zero_detection_remains_context_uninformative_not_absence": True,
            "historical_event_rates_not_copied_without_transport_justification": True,
            "planner_sets_effort_not_biological_effect_thresholds": True,
        },
        "freeze_metadata": {
            "slk_source_commit": "abc123",
            "freeze_commit": "p0-effort-freeze-1",
            "freeze_timestamp": "2027-05-01T00:00:00Z",
        },
        "production_status": "PEDICULARIS_CONTEXT_SCREEN_EFFORT_PROSPECTIVELY_FROZEN",
    }


def _screen_template() -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_CONTEXT_SCREEN_FREEZE_V1",
        "status": "TEMPLATE_ONLY_NOT_FROZEN",
        "context": {
            "system": "Pedicularis rex",
            **CTX,
            "frozen_before_screen_outcomes": False,
        },
        "screen_effort": {
            "capacity_census_rule": "STOP_AT_REQUIRED_CAPACITY_OR_EXHAUST_FOCAL_POPULATION",
            "minimum_pollinator_observation_minutes_total": None,
            "minimum_pollinator_observation_bouts": None,
            "minimum_predator_screen_flowers": None,
            "minimum_water_state_plants": None,
            "minimum_capacity_margin_fraction": None,
        },
        "decision_thresholds": {
            "minimum_legitimate_pollinator_visits": None,
            "minimum_predator_attacked_flowers": None,
            "minimum_predator_attack_fraction": None,
            "minimum_water_positive_plants": None,
            "minimum_water_positive_fraction": None,
            "minimum_flowering_plants_for_immediate_calibration": 84,
            "calibration_capacity_basis": "Y_CAL_36_PLUS_D0_CAL_48_DISJOINT_PLANTS",
            "pollen_limitation_screen_rule": "CALIBRATION_REQUIRED_NOT_ZERO_INFERENCE",
            "pollen_limitation_screen_threshold": None,
        },
        "source_policy": {
            "allowed_threshold_sources": [
                "DOWNSTREAM_DESIGN_REQUIREMENT",
                "INDEPENDENT_NATURAL_HISTORY_CALIBRATION",
                "EXTERNAL_MATCHED_PRIMARY_SOURCE",
                "COMBINED_PREDECLARED",
            ],
            "forbidden_threshold_sources": [
                "SCREEN_OUTCOME_POSTHOC",
                "NONSIGNIFICANT_P_VALUE",
                "HISTORICAL_SAMPLE_SIZE_ONLY",
                "CONVENIENCE_ONLY",
            ],
            "threshold_source_records": [],
        },
        "classification_rules": {},
        "firewall": {
            "context_screen_is_not_g1_or_g2_evidence": True,
            "low_signal_context_is_not_biological_absence": True,
            "screen_units_confirmatory_ineligible": True,
            "no_treatment_effect_estimation_from_screen": True,
            "thresholds_frozen_before_screen_outcomes": True,
            "failed_signal_context_may_trigger_relocation_without_negative_claim": True,
            "capacity_shortfall_requires_exhaustive_census": True,
        },
        "freeze_metadata": {
            "slk_source_commit": "REQUIRED_BEFORE_USE",
            "freeze_commit": "REQUIRED_BEFORE_USE",
            "freeze_timestamp": "REQUIRED_BEFORE_USE",
        },
        "production_status": "PEDICULARIS_CONTEXT_SCREEN_PROSPECTIVELY_FROZEN",
    }


def test_reference_detection_effort_values() -> None:
    result = planner.plan(_effort_freeze())
    assert result["pollinator"]["poisson_detection_minutes"] == 150
    assert result["pollinator"]["temporal_coverage_minutes"] == 120
    assert result["pollinator"]["planned_total_minutes"] == 150
    assert result["predator"]["planned_screen_flowers"] == 59
    assert result["water_state"]["planned_screen_plants"] == 5
    assert result["capacity"]["required_flowering_plants"] == 93


def test_more_demanding_detection_guarantee_never_reduces_effort() -> None:
    base = planner.plan(_effort_freeze())
    tougher = _effort_freeze()
    tougher["pollinator_detection"]["desired_detection_probability"] = 0.99
    tougher["predator_detection"]["desired_detection_probability"] = 0.99
    tougher["water_state_detection"]["desired_detection_probability"] = 0.99
    result = planner.plan(tougher)
    assert result["pollinator"]["planned_total_minutes"] >= base["pollinator"]["planned_total_minutes"]
    assert result["predator"]["planned_screen_flowers"] >= base["predator"]["planned_screen_flowers"]
    assert result["water_state"]["planned_screen_plants"] >= base["water_state"]["planned_screen_plants"]


def test_weaker_minimum_signal_requires_more_effort() -> None:
    base = planner.plan(_effort_freeze())
    weaker = _effort_freeze()
    weaker["pollinator_detection"]["minimum_relevant_visit_rate_per_min"] = 0.01
    weaker["predator_detection"]["minimum_relevant_attack_fraction"] = 0.02
    weaker["water_state_detection"]["minimum_relevant_positive_fraction"] = 0.25
    result = planner.plan(weaker)
    assert result["pollinator"]["planned_total_minutes"] > base["pollinator"]["planned_total_minutes"]
    assert result["predator"]["planned_screen_flowers"] > base["predator"]["planned_screen_flowers"]
    assert result["water_state"]["planned_screen_plants"] > base["water_state"]["planned_screen_plants"]


def test_posthoc_relevance_source_is_rejected() -> None:
    freeze = _effort_freeze()
    freeze["predator_detection"]["source_type"] = "SCREEN_OUTCOME_POSTHOC"
    with pytest.raises(ValueError, match="unapproved predator source type"):
        planner.plan(freeze)


def test_compiler_populates_p0_effort_without_finalizing_freeze() -> None:
    plan = planner.plan(_effort_freeze())
    result = compiler.compile_effort(_screen_template(), plan)
    assert result["status"] == "EFFORT_COMPILED_AWAITING_FINAL_P0_FREEZE"
    assert result["screen_effort"]["minimum_pollinator_observation_minutes_total"] == 150
    assert result["screen_effort"]["minimum_predator_screen_flowers"] == 59
    assert result["screen_effort"]["minimum_water_state_plants"] == 5
    assert result["screen_effort"]["minimum_capacity_margin_fraction"] == pytest.approx(0.10)
    assert result["decision_thresholds"]["minimum_legitimate_pollinator_visits"] == 1
    assert len(result["source_policy"]["threshold_source_records"]) == 8
    assert result["context"]["frozen_before_screen_outcomes"] is False


def test_compiler_rejects_context_mismatch() -> None:
    plan = planner.plan(_effort_freeze())
    screen = _screen_template()
    screen["context"]["population_id"] = "pop2"
    with pytest.raises(ValueError, match="context mismatch"):
        compiler.compile_effort(screen, plan)


def test_compiler_refuses_already_frozen_p0_contract() -> None:
    plan = planner.plan(_effort_freeze())
    screen = _screen_template()
    screen["status"] = "FROZEN_CANDIDATE"
    screen["context"]["frozen_before_screen_outcomes"] = True
    with pytest.raises(ValueError, match="unfrozen template"):
        compiler.compile_effort(screen, plan)
