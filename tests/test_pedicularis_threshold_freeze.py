from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.validate_pedicularis_threshold_freeze import validate


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "data" / "PEDICULARIS_THRESHOLD_FREEZE_TEMPLATE_V1.json"


def _frozen_manifest() -> dict:
    data = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    data["status"] = "THRESHOLDS_PROSPECTIVELY_FROZEN"
    data["context"].update(
        {
            "population_id": "P_REX_POP_A",
            "season_id": "2027",
            "calibration_dataset_id": "CAL_2027_A",
            "qualification_dataset_id": "QUAL_2027_A",
        }
    )
    data["provenance"].update(
        {
            "sch_source_commit": "a" * 40,
            "slk_source_commit": "b" * 40,
            "freeze_commit": "c" * 40,
            "freeze_timestamp": "2027-05-01T00:00:00+09:00",
        }
    )

    for block in ("qz", "qp", "qg"):
        for name, entry in data[block]["parameters"].items():
            if entry["threshold_class"] == "design_floor":
                entry["value"] = 8
                entry["source_type"] = "prospective_precision"
            elif entry["threshold_class"] == "natural_history_timing":
                entry["value"] = 12 if name.startswith("min_") else 30
                entry["source_type"] = "independent_calibration"
            elif entry["threshold_class"] == "target_effect":
                entry["value"] = 0.05
                entry["source_type"] = "biological_relevance"
            else:
                entry["value"] = 0.10
                entry["source_type"] = "measurement_repeatability"
            entry["source_reference"] = "FROZEN_REFERENCE"
            entry["biological_rationale"] = "Prospectively justified before qualification outcomes were opened."
    return data


def test_complete_prospective_manifest_validates() -> None:
    result = validate(_frozen_manifest())
    assert result["status"] == "THRESHOLD_FREEZE_VALIDATED"
    assert result["parameter_counts"] == {"qz": 11, "qp": 10, "qg": 15}
    assert result["effective_qg_design_floor"] == {
        "min_paired_plants": 8,
        "min_flowers_per_treatment": 8,
    }


def test_template_placeholder_cannot_be_promoted() -> None:
    manifest = _frozen_manifest()
    manifest["qz"]["parameters"]["min_plants"]["value"] = "REQUIRED_BEFORE_USE"
    with pytest.raises(ValueError, match="must be numeric"):
        validate(manifest)


def test_calibration_and_qualification_sets_must_be_distinct() -> None:
    manifest = _frozen_manifest()
    manifest["context"]["qualification_dataset_id"] = manifest["context"]["calibration_dataset_id"]
    with pytest.raises(ValueError, match="must be distinct"):
        validate(manifest)


def test_confirmatory_outcomes_cannot_precede_freeze() -> None:
    manifest = _frozen_manifest()
    manifest["provenance"]["confirmatory_outcomes_opened_before_freeze"] = True
    with pytest.raises(ValueError, match="must remain unopened"):
        validate(manifest)


def test_qg_timing_window_must_be_ordered() -> None:
    manifest = _frozen_manifest()
    manifest["qg"]["parameters"]["min_hours_after_anthesis_before_barrier"]["value"] = 36
    manifest["qg"]["parameters"]["max_hours_after_anthesis_before_barrier"]["value"] = 24
    with pytest.raises(ValueError, match="min < max"):
        validate(manifest)


def test_qg_boolean_safety_requirements_are_not_relaxed() -> None:
    manifest = _frozen_manifest()
    manifest["qg"]["fixed_boolean_requirements"]["require_barrier_not_cover_pollinator_entry"] = False
    with pytest.raises(ValueError, match="must remain all true"):
        validate(manifest)
