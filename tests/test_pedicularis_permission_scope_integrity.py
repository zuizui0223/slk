from __future__ import annotations

import copy
import importlib.util
import json
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "pedicularis_permission_scope.py"
FIXTURE = (
    ROOT / "tests" / "fixtures"
    / "pedicularis_permission_scope_confirmed_v1.json"
)

spec = importlib.util.spec_from_file_location("ped_permission_scope", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def _receipt() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_fully_audited_permission_fixture_validates_end_to_end() -> None:
    validated = module.validate_confirmed_permission_scope(
        _receipt(),
        expected_candidate_id="SHANGRILA_WUFENG",
    )
    assert validated["candidate_id"] == "SHANGRILA_WUFENG"
    assert validated["sampling_permission_reference"].endswith("@testperm")
    assert set(validated["responses"][0]["activity_decision_details"]) == set(
        "ABCDEF"
    )
    assert module.activity_valid_on_day(
        validated,
        "A",
        date(2027, 6, 15),
    )
    assert module.activities_cover_window(
        validated,
        date(2027, 6, 20),
        date(2027, 7, 5),
    )


def test_permission_day_and_window_helpers_fail_outside_validity() -> None:
    validated = module.validate_confirmed_permission_scope(_receipt())
    assert not module.activity_valid_on_day(
        validated,
        "A",
        date(2027, 10, 1),
    )
    assert not module.activities_cover_window(
        validated,
        date(2027, 9, 25),
        date(2027, 10, 5),
    )


def test_confirmed_scope_requires_full_response_audit_trail() -> None:
    receipt = _receipt()
    receipt.pop("responses")
    with pytest.raises(ValueError, match="responses missing"):
        module.validate_confirmed_permission_scope(receipt)


def test_permission_matrix_is_recomputed_from_response_audit_trail() -> None:
    receipt = _receipt()
    receipt["all_activity_matrix"]["A"]["regulatory"] = "BLOCKED"
    with pytest.raises(ValueError, match="matrix does not match response audit trail"):
        module.validate_confirmed_permission_scope(receipt)


def test_permission_validity_is_recomputed_from_response_audit_trail() -> None:
    receipt = _receipt()
    receipt["all_activity_validity"]["A"]["regulatory"][0][
        "valid_through"
    ] = "2027-08-31"
    with pytest.raises(ValueError, match="validity does not match response audit trail"):
        module.validate_confirmed_permission_scope(receipt)


def test_source_response_hash_is_revalidated_downstream() -> None:
    receipt = _receipt()
    receipt["responses"][0]["source_response_content_sha256"] = "bad"
    with pytest.raises(ValueError, match="content hash must be sha256"):
        module.validate_confirmed_permission_scope(receipt)


def test_decision_evidence_locator_channel_is_revalidated_downstream() -> None:
    receipt = _receipt()
    receipt["responses"][0]["activity_decision_details"]["A"][
        "decision_evidence_locator"
    ] = "CALL_NOTE:lines-1-3"
    with pytest.raises(ValueError, match="locator/channel mismatch"):
        module.validate_confirmed_permission_scope(receipt)


def test_condition_review_definition_is_revalidated_downstream() -> None:
    receipt = _receipt()
    receipt["responses"][0]["activity_decision_details"]["B"][
        "registered_activity_definition_reference"
    ] = "SLK_PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1#A"
    with pytest.raises(ValueError, match="wrong registered activity definition"):
        module.validate_confirmed_permission_scope(receipt)


def test_decision_extraction_date_is_revalidated_downstream() -> None:
    receipt = _receipt()
    receipt["responses"][1]["activity_decision_details"]["A"][
        "decision_extraction_date"
    ] = "2027-05-14"
    with pytest.raises(ValueError, match="outside response/adjudication window"):
        module.validate_confirmed_permission_scope(receipt)


def test_required_validity_must_equal_all_activity_subset() -> None:
    receipt = _receipt()
    receipt["required_activity_validity"]["A"]["site"] = []
    with pytest.raises(ValueError, match="required permission validity"):
        module.validate_confirmed_permission_scope(receipt)


def test_recovery_handoff_reference_must_match_root_reference() -> None:
    receipt = _receipt()
    receipt["recovery_handoff"]["sampling_permission_reference"] = (
        "SLK_PEDICULARIS_WAVE1_PERMISSION_SCOPE_RECEIPT_V1@other"
    )
    with pytest.raises(ValueError, match="reference/handoff mismatch"):
        module.validate_confirmed_permission_scope(receipt)


def test_expected_candidate_is_enforced() -> None:
    with pytest.raises(ValueError, match="candidate mismatch"):
        module.validate_confirmed_permission_scope(
            _receipt(),
            expected_candidate_id="SONGZANLIN_EIA_2025",
        )
