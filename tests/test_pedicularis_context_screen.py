from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "adjudicate_pedicularis_context_screen.py"

spec = importlib.util.spec_from_file_location("ped_context_screen", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def _source_records() -> list[dict]:
    fields = [
        "screen_effort.minimum_pollinator_observation_minutes_total",
        "screen_effort.minimum_pollinator_observation_bouts",
        "screen_effort.minimum_predator_screen_flowers",
        "screen_effort.minimum_water_state_plants",
        "screen_effort.minimum_capacity_margin_fraction",
        "decision_thresholds.minimum_legitimate_pollinator_visits",
        "decision_thresholds.minimum_predator_attacked_flowers",
        "decision_thresholds.minimum_water_positive_plants",
    ]
    return [
        {
            "field_id": field,
            "source_type": "DOWNSTREAM_DESIGN_REQUIREMENT",
            "source_reference": "TEST_ONLY_PROSPECTIVE_SOURCE",
            "rationale": "synthetic regression-test threshold provenance",
        }
        for field in fields
    ]


def _freeze() -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_CONTEXT_SCREEN_FREEZE_V1",
        "status": "FROZEN_CANDIDATE",
        "context": {
            "system": "Pedicularis rex",
            "candidate_site_id": "site1",
            "population_id": "pop1",
            "season_id": "2027",
            "screen_window_id": "screen1",
            "frozen_before_screen_outcomes": True,
        },
        "screen_effort": {
            "capacity_census_rule": "STOP_AT_REQUIRED_CAPACITY_OR_EXHAUST_FOCAL_POPULATION",
            "minimum_pollinator_observation_minutes_total": 60,
            "minimum_pollinator_observation_bouts": 6,
            "minimum_predator_screen_flowers": 30,
            "minimum_water_state_plants": 20,
            "minimum_capacity_margin_fraction": 0.10,
        },
        "decision_thresholds": {
            "minimum_legitimate_pollinator_visits": 1,
            "minimum_predator_attacked_flowers": 1,
            "minimum_predator_attack_fraction": None,
            "minimum_water_positive_plants": 1,
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
            "threshold_source_records": _source_records(),
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
            "slk_source_commit": "abc123",
            "freeze_commit": "def456",
            "freeze_timestamp": "2027-05-01T00:00:00Z",
        },
        "production_status": "PEDICULARIS_CONTEXT_SCREEN_PROSPECTIVELY_FROZEN",
    }


def _receipt() -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_CONTEXT_SCREEN_RECEIPT_V1",
        "status": "FILLED_SCREEN_DATA",
        "context": {
            "system": "Pedicularis rex",
            "candidate_site_id": "site1",
            "population_id": "pop1",
            "season_id": "2027",
            "screen_window_id": "screen1",
        },
        "effort": {
            "independent_flowering_plants_censused": 120,
            "population_census_exhausted": False,
            "pollinator_observation_minutes_total": 75,
            "pollinator_observation_bouts": 8,
            "predator_screen_flowers": 40,
            "water_state_plants": 25,
        },
        "observations": {
            "legitimate_pollinator_visits": 3,
            "predator_attacked_flowers": 4,
            "water_positive_plants": 20,
            "notes_on_predator_evidence": "oviposition/early attack signs observed",
            "notes_on_water_state": "cupulate bracts retained measurable water",
        },
        "pollen_limitation": {
            "status": "UNRESOLVED_UNTIL_QP_CALIBRATION",
            "used_as_context_screen_pass_gate": False,
        },
        "firewall": {
            "screen_units_confirmatory_eligible": False,
            "screen_used_for_treatment_effect_estimation": False,
            "zero_detection_interpreted_as_biological_absence": False,
        },
        "final_adjudication": "NOT_YET_EXECUTED",
    }


def test_signal_positive_context_with_capacity_unlocks_calibration() -> None:
    result = module.adjudicate(_receipt(), _freeze())
    assert result["status"] == "CONTEXT_SCREEN_PASS_CALIBRATION_READY"
    assert result["next_action"]["calibration_unlocked"] is True
    assert result["capacity"]["required_with_reserve"] == 93
    assert result["capacity"]["resolved"] is True
    assert result["signals"]["pollen_limitation"] == "UNRESOLVED_UNTIL_QP_CALIBRATION"


def test_zero_predator_detection_is_uninformative_not_negative() -> None:
    receipt = _receipt()
    receipt["observations"]["predator_attacked_flowers"] = 0
    result = module.adjudicate(receipt, _freeze())
    assert result["status"] == "CONTEXT_UNINFORMATIVE_PREDATOR_LOW"
    assert result["next_action"]["relocation_recommended"] is True
    assert result["next_action"]["low_signal_is_biological_negative"] is False


def test_capacity_shortfall_requires_exhaustive_census_before_limited_status() -> None:
    receipt = _receipt()
    receipt["effort"]["independent_flowering_plants_censused"] = 90
    receipt["effort"]["population_census_exhausted"] = True
    result = module.adjudicate(receipt, _freeze())
    assert result["status"] == "CONTEXT_SIGNAL_PRESENT_CAPACITY_LIMITED"
    assert result["capacity"]["pass"] is False
    assert result["capacity"]["resolved"] is True
    assert result["firewall"]["capacity_shortfall_declared_only_after_exhaustive_census"] is True


def test_capacity_below_requirement_without_exhaustive_census_is_incomplete() -> None:
    receipt = _receipt()
    receipt["effort"]["independent_flowering_plants_censused"] = 90
    receipt["effort"]["population_census_exhausted"] = False
    result = module.adjudicate(receipt, _freeze())
    assert result["status"] == "CONTEXT_SCREEN_INCOMPLETE"
    assert result["effort"]["signal_effort_complete"] is True
    assert result["capacity"]["resolved"] is False
    assert result["next_action"]["continue_capacity_census"] is True
    assert result["signals"]["pollinator"]["pass"] is True


def test_incomplete_registered_signal_effort_never_calls_low_signal() -> None:
    receipt = _receipt()
    receipt["effort"]["pollinator_observation_minutes_total"] = 20
    receipt["observations"]["legitimate_pollinator_visits"] = 0
    result = module.adjudicate(receipt, _freeze())
    assert result["status"] == "CONTEXT_SCREEN_INCOMPLETE"
    assert result["signals"]["pollinator"]["pass"] is None


def test_multiple_low_signals_are_not_collapsed_to_one_cause() -> None:
    receipt = _receipt()
    receipt["observations"]["legitimate_pollinator_visits"] = 0
    receipt["observations"]["predator_attacked_flowers"] = 0
    result = module.adjudicate(receipt, _freeze())
    assert result["status"] == "CONTEXT_UNINFORMATIVE_MULTIPLE_SIGNALS"


def test_pollen_limitation_cannot_be_used_as_p0_gate() -> None:
    receipt = _receipt()
    receipt["pollen_limitation"]["used_as_context_screen_pass_gate"] = True
    with pytest.raises(ValueError, match="cannot be a P0 pass gate"):
        module.adjudicate(receipt, _freeze())


def test_missing_threshold_provenance_fails_freeze_validation() -> None:
    freeze = _freeze()
    freeze["source_policy"]["threshold_source_records"] = freeze["source_policy"]["threshold_source_records"][:-1]
    with pytest.raises(ValueError, match="provenance"):
        module.validate_freeze(freeze)


def test_screen_outcome_posthoc_source_is_rejected() -> None:
    freeze = _freeze()
    freeze["source_policy"]["threshold_source_records"][0]["source_type"] = "SCREEN_OUTCOME_POSTHOC"
    with pytest.raises(ValueError, match="unapproved threshold source"):
        module.validate_freeze(freeze)


def test_context_mismatch_is_rejected() -> None:
    receipt = _receipt()
    receipt["context"]["population_id"] = "pop2"
    with pytest.raises(ValueError, match="context mismatch"):
        module.adjudicate(receipt, _freeze())
