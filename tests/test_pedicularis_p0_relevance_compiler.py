from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
QUALIFIER = ROOT / "scripts" / "validate_pedicularis_p0_relevance_qualification.py"
COMPILER = ROOT / "scripts" / "compile_pedicularis_p0_relevance_into_effort_freeze.py"
TEMPLATE = ROOT / "data" / "PEDICULARIS_CONTEXT_SCREEN_EFFORT_FREEZE_TEMPLATE_V1.json"

spec = importlib.util.spec_from_file_location("ped_p0_qual_for_compile", QUALIFIER)
qual = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(qual)

spec2 = importlib.util.spec_from_file_location("ped_p0_rel_compile", COMPILER)
comp = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(comp)

import json


def _row(input_id: str, value: float) -> dict:
    metrics = {
        "P0_POLLINATOR_MIN_RATE": ("LEGITIMATE_VISITS_PER_FLOWER_MINUTE", "LEGITIMATE_VISITS_PER_FLOWER_MINUTE"),
        "P0_PREDATOR_MIN_PREVALENCE": ("EARLY_ATTACK_OR_OVIPOSITION_POSITIVE_FLOWERS_PER_SCREENED_FLOWERS", "PROPORTION_0_1"),
        "P0_WATER_POSITIVE_PREVALENCE": ("WATER_POSITIVE_FLOWERING_PLANTS_PER_SCREENED_FLOWERING_PLANTS", "PROPORTION_0_1"),
    }
    target, units = metrics[input_id]
    return {
        "input_id": input_id,
        "target_metric": target,
        "qualification_route": "FRESH_INDEPENDENT_CALIBRATION",
        "source_type": "INDEPENDENT_NATURAL_HISTORY_CALIBRATION",
        "source_reference": f"FRESH:{input_id}",
        "source_metric": target,
        "numeric_value": value,
        "numeric_units": units,
        "endpoint_match": True,
        "unit_or_denominator_match": True,
        "context_transport_justified": False,
        "fresh_calibration_units_independent_of_p0": True,
        "fresh_calibration_units_downstream_confirmatory_ineligible": True,
        "biological_rationale": "fresh disjoint natural-history calibration",
        "qualification_status": "FRESH_CALIBRATION_QUALIFIED",
        "frozen_before_p0_outcomes": True,
    }


def _qualification() -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_P0_RELEVANCE_QUALIFICATION_V1",
        "status": "QUALIFICATION_CANDIDATE",
        "context": {
            "system": "Pedicularis rex",
            "candidate_site_id": "site1",
            "population_id": "pop1",
            "season_id": "2027",
            "screen_window_id": "screen1",
            "p0_outcomes_opened": False,
        },
        "physical_unit_firewall_handoff": {
            "schema_version": "SLK_PEDICULARIS_PHYSICAL_PLANT_FIREWALL_V1",
            "require_nonempty_physical_plant_tag": True,
            "prior_physical_plant_tags_forbidden": ["PHY-CAL-1"],
            "prior_tag_source_references": ["TEST_FRESH_CALIBRATION"],
            "prior_tag_set_sha256": "f6086223edbe01f333626e0caaa298686716cc3a9d917685e66dea2f338b413b",
            "frozen_before_outcomes": True,
        },
        "inputs": [
            _row("P0_POLLINATOR_MIN_RATE", 0.02),
            _row("P0_PREDATOR_MIN_PREVALENCE", 0.05),
            _row("P0_WATER_POSITIVE_PREVALENCE", 0.50),
        ],
        "allowed_routes": ["EXTERNAL_NUMERIC_TRANSPORT", "FRESH_INDEPENDENT_CALIBRATION"],
        "firewall": {
            "figure_read_off_without_exact_source_forbidden": True,
            "endpoint_substitution_forbidden": True,
            "historical_sample_size_as_numeric_source_forbidden": True,
            "fresh_calibration_units_p0_decision_reuse_forbidden": True,
            "fresh_calibration_units_downstream_confirmatory_reuse_forbidden": True,
            "qualification_must_precede_p0_outcomes": True,
        },
        "qualification_metadata": {
            "slk_source_commit": "abc123",
            "qualification_commit": "qual123",
            "qualification_timestamp": "2027-05-01T00:00:00Z",
        },
    }


def _effort() -> dict:
    payload = json.loads(TEMPLATE.read_text())
    payload["context"].update(
        {
            "candidate_site_id": "site1",
            "population_id": "pop1",
            "season_id": "2027",
            "screen_window_id": "screen1",
        }
    )
    return payload


def test_qualified_relevance_values_compile_into_effort_template() -> None:
    result = comp.compile_relevance(_effort(), _qualification())
    assert result["status"] == "RELEVANCE_COMPILED_AWAITING_DESIGN_DECISIONS"
    assert result["pollinator_detection"]["minimum_relevant_visit_rate_per_flower_min"] == pytest.approx(0.02)
    assert result["pollinator_detection"]["visit_rate_unit"] == "LEGITIMATE_VISITS_PER_FLOWER_MINUTE"
    assert result["predator_detection"]["minimum_relevant_attack_fraction"] == pytest.approx(0.05)
    assert result["water_state_detection"]["minimum_relevant_positive_fraction"] == pytest.approx(0.50)
    assert result["context"]["frozen_before_screen_outcomes"] is False
    assert "qual123" in result["freeze_metadata"]["relevance_qualification_reference"]


def test_context_mismatch_blocks_compilation() -> None:
    effort = _effort()
    effort["context"]["population_id"] = "pop2"
    with pytest.raises(ValueError, match="context mismatch"):
        comp.compile_relevance(effort, _qualification())
