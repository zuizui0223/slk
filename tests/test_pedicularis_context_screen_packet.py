from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_pedicularis_context_screen_packet.py"
SUMMARIZER = ROOT / "scripts" / "summarize_pedicularis_context_screen_packet.py"
ADJUDICATOR = ROOT / "scripts" / "adjudicate_pedicularis_context_screen.py"

spec = importlib.util.spec_from_file_location("ped_context_packet_gen", GENERATOR)
gen = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(gen)

spec2 = importlib.util.spec_from_file_location("ped_context_packet_summary", SUMMARIZER)
sum_mod = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(sum_mod)

spec3 = importlib.util.spec_from_file_location("ped_context_packet_adj", ADJUDICATOR)
adj = importlib.util.module_from_spec(spec3)
assert spec3.loader is not None
spec3.loader.exec_module(adj)


def _freeze() -> dict:
    required_fields = [
        "screen_effort.minimum_pollinator_observation_minutes_total",
        "screen_effort.minimum_pollinator_observation_bouts",
        "screen_effort.minimum_predator_screen_flowers",
        "screen_effort.minimum_water_state_plants",
        "screen_effort.minimum_capacity_margin_fraction",
        "decision_thresholds.minimum_legitimate_pollinator_visits",
        "decision_thresholds.minimum_predator_attacked_flowers",
        "decision_thresholds.minimum_water_positive_plants",
    ]
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
            "threshold_source_records": [
                {
                    "field_id": field,
                    "source_type": "DOWNSTREAM_DESIGN_REQUIREMENT",
                    "source_reference": "TEST_SOURCE",
                    "rationale": "test fixture",
                }
                for field in required_fields
            ],
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


def _completed_rows() -> list[dict[str, str]]:
    rows = gen.generate(_freeze())
    for row in rows:
        if row["record_type"] == "CENSUS":
            row["flowering_plants_censused"] = "120"
            row["population_census_exhausted"] = "false"
        elif row["record_type"] == "POLLINATOR_BOUT":
            row["observed_observation_minutes"] = row["planned_observation_minutes"]
            row["legitimate_pollinator_visits"] = "1" if row["record_id"] == "POLL-001" else "0"
        elif row["record_type"] == "PREDATOR_FLOWER":
            row["plant_id"] = f"P-{row['record_id']}"
            row["flower_id"] = f"F-{row['record_id']}"
            row["predator_attack_present"] = "true" if row["record_id"] == "PRED-001" else "false"
        elif row["record_type"] == "WATER_PLANT":
            row["plant_id"] = f"P-{row['record_id']}"
            row["water_positive"] = "true"
    return rows


def test_generator_expands_registered_screen_effort() -> None:
    rows = gen.generate(_freeze())
    assert sum(r["record_type"] == "CENSUS" for r in rows) == 1
    assert sum(r["record_type"] == "POLLINATOR_BOUT" for r in rows) == 6
    assert sum(r["record_type"] == "PREDATOR_FLOWER" for r in rows) == 30
    assert sum(r["record_type"] == "WATER_PLANT" for r in rows) == 20
    assert all(r["screen_only"] == "true" for r in rows)
    assert all(r["confirmatory_eligible"] == "false" for r in rows)
    census = next(r for r in rows if r["record_type"] == "CENSUS")
    assert "exhaust the focal population" in census["notes"]


def test_completed_packet_summarizes_registered_effort_and_signals() -> None:
    receipt = sum_mod.summarize(_completed_rows())
    assert receipt["effort"]["population_census_exhausted"] is False
    assert receipt["effort"]["pollinator_observation_bouts"] == 6
    assert receipt["effort"]["predator_screen_flowers"] == 30
    assert receipt["effort"]["water_state_plants"] == 20
    assert receipt["observations"]["legitimate_pollinator_visits"] == 1
    assert receipt["observations"]["predator_attacked_flowers"] == 1
    assert receipt["observations"]["water_positive_plants"] == 20


def test_packet_summary_and_adjudicator_unlock_calibration_end_to_end() -> None:
    receipt = sum_mod.summarize(_completed_rows())
    result = adj.adjudicate(receipt, _freeze())
    assert result["status"] == "CONTEXT_SCREEN_PASS_CALIBRATION_READY"
    assert result["next_action"]["calibration_unlocked"] is True
    assert result["firewall"]["screen_is_logistical_not_g1_g2"] is True


def test_below_capacity_packet_without_exhaustion_stays_incomplete() -> None:
    rows = _completed_rows()
    census = next(r for r in rows if r["record_type"] == "CENSUS")
    census["flowering_plants_censused"] = "90"
    census["population_census_exhausted"] = "false"
    receipt = sum_mod.summarize(rows)
    result = adj.adjudicate(receipt, _freeze())
    assert result["status"] == "CONTEXT_SCREEN_INCOMPLETE"
    assert result["next_action"]["continue_capacity_census"] is True


def test_below_capacity_packet_with_exhaustion_is_capacity_limited() -> None:
    rows = _completed_rows()
    census = next(r for r in rows if r["record_type"] == "CENSUS")
    census["flowering_plants_censused"] = "90"
    census["population_census_exhausted"] = "true"
    receipt = sum_mod.summarize(rows)
    result = adj.adjudicate(receipt, _freeze())
    assert result["status"] == "CONTEXT_SIGNAL_PRESENT_CAPACITY_LIMITED"


def test_incomplete_packet_remains_incomplete_in_summary() -> None:
    rows = _completed_rows()
    target = next(r for r in rows if r["record_id"] == "POLL-006")
    target["observed_observation_minutes"] = ""
    target["legitimate_pollinator_visits"] = ""
    receipt = sum_mod.summarize(rows)
    assert receipt["packet_completion"]["completed_pollinator_rows"] == 5


def test_packet_row_cannot_be_promoted_to_confirmatory() -> None:
    rows = _completed_rows()
    rows[0]["confirmatory_eligible"] = "true"
    with pytest.raises(ValueError, match="cannot be confirmatory eligible"):
        sum_mod.summarize(rows)


def test_predator_and_water_rows_require_actual_plant_ids() -> None:
    rows = _completed_rows()
    target = next(r for r in rows if r["record_type"] == "PREDATOR_FLOWER")
    target["plant_id"] = ""
    with pytest.raises(ValueError, match="missing plant_id"):
        sum_mod.summarize(rows)
