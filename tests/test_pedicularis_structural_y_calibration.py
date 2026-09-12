from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_pedicularis_calibration_layout.py"
SUMMARIZER = ROOT / "scripts" / "summarize_pedicularis_structural_y_calibration.py"
FREEZE_TEMPLATE = ROOT / "data" / "PEDICULARIS_STRUCTURAL_Y_METRIC_FREEZE_TEMPLATE_V1.json"

spec = importlib.util.spec_from_file_location("ped_cal_gen_y", GENERATOR)
gen = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(gen)

spec2 = importlib.util.spec_from_file_location("ped_y_summary", SUMMARIZER)
summary = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(summary)


def _freeze(metric: str = "RETENTION_MEAN_MAX_ML") -> dict:
    f = json.loads(FREEZE_TEMPLATE.read_text())
    f["status"] = "FROZEN_CANDIDATE"
    f["context"].update(
        {
            "population_id": "pop1",
            "season_id": "2027",
            "primary_y_metric": metric,
            "frozen_before_y_cal_outcomes": True,
        }
    )
    f["freeze_metadata"] = {
        "slk_source_commit": "abc123",
        "freeze_commit": "def456",
        "freeze_timestamp": "2027-05-01T00:00:00Z",
    }
    return f


def _rows(strong_range: bool = True) -> list[dict[str, str]]:
    rows, _, _ = gen.generate_layout(
        "ctx1", "pop1", "2027", "FLOWER_TO_MATURE_VIABLE_SEED", 1729
    )
    out = copy.deepcopy(rows)
    for row in out:
        i = int(row["plant_id"].rsplit("-", 1)[1])
        slot = int(row["flower_slot"])
        if strong_range:
            base = 1.0 + 0.10 * i + 0.01 * slot
            t1 = base - 0.01 * ((i + slot) % 3)
            t2 = base + 0.01 * ((i + 2 * slot) % 3)
        else:
            base = 1.0 + 0.001 * ((i + slot) % 3)
            t1 = base - 0.20 * ((i + slot) % 2)
            t2 = base + 0.20 * ((i + slot) % 2)
        row["retention_trial1_max_ml"] = str(t1)
        row["retention_trial2_max_ml"] = str(t2)
        row["exsertion_z"] = str(0.25 + 0.002 * i + 0.0005 * slot)
    return out


def test_strong_resolved_range_freezes_disjoint_d0_recruitment_bands() -> None:
    receipt = summary.summarize(_rows(True), _freeze())
    assert receipt["status"] == "STRUCTURAL_Y_Y0_RANGE_QUALIFIED_Y1_AUDITED"
    assert receipt["complete_independent_plants"] == 36
    assert receipt["complete_plant_floor_pass"] is True
    assert receipt["band_freeze"]["dynamic_range_pass"] is True
    assert receipt["band_freeze"]["recruitment_authorized_for_disjoint_d0_cal"] is True
    assert receipt["band_freeze"]["low_y_max"] < receipt["band_freeze"]["high_y_min"]
    assert receipt["variance_components"]["between_plant_sd"] > 0
    assert receipt["variance_components"]["measurement_error_sd_from_trial_pairs"] >= 0
    assert receipt["x_y_coupling_audit"]["y1_coupling_audited"] is True


def test_noisy_unresolved_range_does_not_authorize_d0_recruitment() -> None:
    receipt = summary.summarize(_rows(False), _freeze())
    assert receipt["status"] == "STRUCTURAL_Y_CALIBRATION_COMPLETE_RANGE_UNRESOLVED"
    assert receipt["band_freeze"]["dynamic_range_pass"] is False
    assert receipt["band_freeze"]["recruitment_authorized_for_disjoint_d0_cal"] is False


def test_primary_metric_must_be_frozen_before_y_cal_outcomes() -> None:
    f = _freeze()
    f["context"]["frozen_before_y_cal_outcomes"] = False
    with pytest.raises(ValueError, match="not frozen before Y-CAL outcomes"):
        summary.summarize(_rows(True), f)


def test_unregistered_primary_metric_is_rejected() -> None:
    f = _freeze("RETENTION_CUTE_BUT_POSTHOC")
    with pytest.raises(ValueError, match="unregistered primary y metric"):
        summary.summarize(_rows(True), f)


def test_one_incomplete_plant_drops_below_registered_floor() -> None:
    rows = _rows(True)
    target = next(
        row for row in rows
        if row["plant_id"] == "YCAL-001" and row["flower_slot"] == "1"
    )
    target["retention_trial2_max_ml"] = ""
    receipt = summary.summarize(rows, _freeze())
    assert receipt["complete_independent_plants"] == 35
    assert receipt["complete_plant_floor_pass"] is False
    assert receipt["status"] == "STRUCTURAL_Y_CALIBRATION_INCOMPLETE"
    assert receipt["band_freeze"]["recruitment_authorized_for_disjoint_d0_cal"] is False


def test_y_cal_row_cannot_be_promoted_to_confirmatory() -> None:
    rows = _rows(True)
    rows[0]["confirmatory_eligible"] = "true"
    with pytest.raises(ValueError, match="confirmatory eligible"):
        summary.summarize(rows, _freeze())


def test_freeze_and_y_cal_context_must_match() -> None:
    f = _freeze()
    f["context"]["population_id"] = "pop2"
    with pytest.raises(ValueError, match="population mismatch"):
        summary.summarize(_rows(True), f)
