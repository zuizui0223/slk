from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_pedicularis_p0_relevance_qualification.py"

spec = importlib.util.spec_from_file_location("ped_p0_source_qual", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def _row(input_id: str, route: str) -> dict:
    external = route == "EXTERNAL_NUMERIC_TRANSPORT"
    metrics = {
        "P0_POLLINATOR_MIN_RATE": (
            "LEGITIMATE_VISITS_PER_FLOWER_MINUTE",
            "LEGITIMATE_VISITS_PER_FLOWER_MINUTE",
            0.02,
        ),
        "P0_PREDATOR_MIN_PREVALENCE": (
            "EARLY_ATTACK_OR_OVIPOSITION_POSITIVE_FLOWERS_PER_SCREENED_FLOWERS",
            "PROPORTION_0_1",
            0.05,
        ),
        "P0_WATER_POSITIVE_PREVALENCE": (
            "WATER_POSITIVE_FLOWERING_PLANTS_PER_SCREENED_FLOWERING_PLANTS",
            "PROPORTION_0_1",
            0.50,
        ),
    }
    target, units, value = metrics[input_id]
    return {
        "input_id": input_id,
        "target_metric": target,
        "qualification_route": route,
        "source_type": "EXTERNAL_MATCHED_PRIMARY_SOURCE" if external else "INDEPENDENT_NATURAL_HISTORY_CALIBRATION",
        "source_reference": f"SRC:{input_id}",
        "source_metric": target,
        "numeric_value": value,
        "numeric_units": units,
        "endpoint_match": True,
        "unit_or_denominator_match": True,
        "context_transport_justified": external,
        "fresh_calibration_units_independent_of_p0": not external,
        "fresh_calibration_units_downstream_confirmatory_ineligible": not external,
        "biological_rationale": "prospectively qualified test source",
        "qualification_status": "NUMERIC_TRANSPORT_QUALIFIED" if external else "FRESH_CALIBRATION_QUALIFIED",
        "frozen_before_p0_outcomes": True,
    }


def _payload() -> dict:
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
        "inputs": [
            _row("P0_POLLINATOR_MIN_RATE", "EXTERNAL_NUMERIC_TRANSPORT"),
            _row("P0_PREDATOR_MIN_PREVALENCE", "FRESH_INDEPENDENT_CALIBRATION"),
            _row("P0_WATER_POSITIVE_PREVALENCE", "FRESH_INDEPENDENT_CALIBRATION"),
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


def _input(payload: dict, input_id: str) -> dict:
    return next(x for x in payload["inputs"] if x["input_id"] == input_id)


def test_mixed_external_and_fresh_routes_can_qualify() -> None:
    result = mod.validate(_payload())
    assert result["status"] == "P0_MINIMUM_RELEVANCE_INPUTS_QUALIFIED"
    assert set(result["qualified_inputs"]) == {
        "P0_POLLINATOR_MIN_RATE",
        "P0_PREDATOR_MIN_PREVALENCE",
        "P0_WATER_POSITIVE_PREVALENCE",
    }
    assert result["values"]["P0_POLLINATOR_MIN_RATE"]["units"] == "LEGITIMATE_VISITS_PER_FLOWER_MINUTE"


def test_external_route_requires_context_transport_justification() -> None:
    payload = _payload()
    _input(payload, "P0_POLLINATOR_MIN_RATE")["context_transport_justified"] = False
    with pytest.raises(ValueError, match="context transport"):
        mod.validate(payload)


def test_external_route_cannot_use_unqualified_figure_read_off() -> None:
    payload = _payload()
    _input(payload, "P0_POLLINATOR_MIN_RATE")["qualification_status"] = "PARTIAL_EXTERNAL_ANCHOR"
    with pytest.raises(ValueError, match="qualification status"):
        mod.validate(payload)


def test_predator_final_seed_predation_endpoint_cannot_substitute() -> None:
    payload = _payload()
    row = _input(payload, "P0_PREDATOR_MIN_PREVALENCE")
    row["endpoint_match"] = False
    row["source_metric"] = "FINAL_SEED_PREDATION"
    with pytest.raises(ValueError, match="endpoint mismatch"):
        mod.validate(payload)


def test_fresh_route_requires_independent_firewalled_units() -> None:
    payload = _payload()
    row = _input(payload, "P0_WATER_POSITIVE_PREVALENCE")
    row["fresh_calibration_units_downstream_confirmatory_ineligible"] = False
    with pytest.raises(ValueError, match="not firewalled"):
        mod.validate(payload)


def test_p0_outcome_peeking_blocks_source_qualification() -> None:
    payload = _payload()
    payload["context"]["p0_outcomes_opened"] = True
    with pytest.raises(ValueError, match="already opened"):
        mod.validate(payload)


def test_pollinator_units_must_be_flower_minute_based() -> None:
    payload = _payload()
    _input(payload, "P0_POLLINATOR_MIN_RATE")["numeric_units"] = "LEGITIMATE_VISITS_PER_MINUTE"
    with pytest.raises(ValueError, match="flower-minute"):
        mod.validate(payload)
