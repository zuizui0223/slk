from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_pedicularis_d0_margin_freeze.py"
TEMPLATE = ROOT / "data" / "PEDICULARIS_D0_MARGIN_FREEZE_TEMPLATE_V1.json"

spec = importlib.util.spec_from_file_location("ped_d0_margin", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)
validate = module.validate


def _manifest(q5_route: str = "NEGLIGIBLE_BURDEN_EQUIVALENCE") -> dict:
    m = json.loads(TEMPLATE.read_text())
    m["status"] = "FROZEN_CANDIDATE"
    m["context"].update(
        {
            "population_id": "pop1",
            "season_id": "2027",
            "time_horizon_id": "FLOWER_TO_MATURE_VIABLE_SEED",
            "confirmatory_dataset_id": "PED_D0_CONFIRM_V1",
            "q5_route": q5_route,
        }
    )
    m["freeze_metadata"] = {
        "slk_source_commit": "abc123",
        "freeze_commit": "def456",
        "freeze_timestamp": "2027-05-01T00:00:00Z",
    }

    for endpoint in m["endpoints"]:
        endpoint_id = endpoint["endpoint_id"]
        criterion = endpoint["criterion_type"]
        if criterion != "EXACT_IDENTITY":
            endpoint["value"] = 0.1
        endpoint["margin_basis"] = "independent biological or decision-invariance calibration"
        endpoint["source_reference"] = ["CALIBRATION:PED_D0_CAL_V1"]
        endpoint["biological_rationale"] = "preserves the registered biological interpretation"
        endpoint["calibration_dataset_id"] = "PED_D0_CAL_V1"
        endpoint["variance_only_basis"] = False
        endpoint["derived_from_confirmatory_outcome"] = False
        endpoint["frozen_before_confirmatory_outcomes"] = True

        if endpoint_id == "D0_Q4_WET_EFFECT":
            endpoint["source_type"] = "BIOLOGICAL_RELEVANCE_PLUS_CALIBRATION"
        elif endpoint_id in {"D0_Q5_BURDEN_EQ", "D0_Q5_BURDEN_PRECISION"}:
            endpoint["source_type"] = "DOWNSTREAM_DECISION_INVARIANCE"
        elif endpoint_id == "D0_Q6_HORIZON":
            endpoint["source_type"] = "DESIGN_INVARIANCE"
            endpoint["calibration_dataset_id"] = None
        else:
            endpoint["source_type"] = "FUNCTIONAL_INVARIANCE"

    return m


def _endpoint(m: dict, endpoint_id: str) -> dict:
    return next(x for x in m["endpoints"] if x["endpoint_id"] == endpoint_id)


def test_valid_negligible_burden_route_freezes_margins() -> None:
    result = validate(_manifest())
    assert result["status"] == "FROZEN_FOR_CONFIRMATORY_USE"
    assert result["q5_route"] == "NEGLIGIBLE_BURDEN_EQUIVALENCE"
    assert "D0_Q5_BURDEN_EQ" in result["validated_endpoints"]
    assert "D0_Q5_BURDEN_PRECISION" in result["route_skipped_endpoints"]


def test_valid_measured_burden_route_uses_precision_target() -> None:
    result = validate(_manifest("MEASURED_BURDEN_ADJUSTMENT"))
    assert result["status"] == "FROZEN_FOR_CONFIRMATORY_USE"
    assert "D0_Q5_BURDEN_PRECISION" in result["validated_endpoints"]
    assert "D0_Q5_BURDEN_EQ" in result["route_skipped_endpoints"]


def test_template_is_not_accidentally_production_ready() -> None:
    raw = json.loads(TEMPLATE.read_text())
    with pytest.raises(ValueError):
        validate(raw)


def test_variance_only_margin_is_rejected() -> None:
    m = _manifest()
    _endpoint(m, "D0_Q2_DURATION")["variance_only_basis"] = True
    with pytest.raises(ValueError, match="variance-only margin forbidden"):
        validate(m)


def test_confirmatory_outcome_peeking_is_rejected() -> None:
    m = _manifest()
    m["context"]["confirmatory_outcomes_opened"] = True
    with pytest.raises(ValueError, match="confirmatory outcomes already opened"):
        validate(m)


def test_nonsignificant_pvalue_cannot_define_equivalence() -> None:
    m = _manifest()
    _endpoint(m, "D0_Q3_VISIT")["source_type"] = "NONSIGNIFICANT_P_VALUE"
    with pytest.raises(ValueError, match="unapproved source_type"):
        validate(m)


def test_calibration_units_cannot_be_reused_as_confirmatory_dataset() -> None:
    m = _manifest()
    _endpoint(m, "D0_Q3_POLLEN")["calibration_dataset_id"] = "PED_D0_CONFIRM_V1"
    with pytest.raises(ValueError, match="calibration/confirmatory dataset reuse"):
        validate(m)


def test_missing_source_reference_is_rejected() -> None:
    m = _manifest()
    _endpoint(m, "D0_Q1_Z")["source_reference"] = []
    with pytest.raises(ValueError, match="source_reference missing"):
        validate(m)


def test_q6_requires_exact_same_horizon_identity() -> None:
    m = _manifest()
    _endpoint(m, "D0_Q6_HORIZON")["value"] = "ALMOST_SAME"
    with pytest.raises(ValueError, match="invalid exact identity"):
        validate(m)


def test_missing_numeric_margin_is_rejected() -> None:
    m = _manifest()
    _endpoint(m, "D0_Q2_PROTECTION")["value"] = None
    with pytest.raises(ValueError, match="missing/invalid numeric value"):
        validate(m)


def test_firewall_cannot_be_disabled() -> None:
    m = _manifest()
    m["firewall"]["variance_only_margin_basis_forbidden"] = False
    with pytest.raises(ValueError, match="firewall not active"):
        validate(m)
