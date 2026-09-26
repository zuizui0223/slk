from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "pedicularis_permission_scope.py"
RESP_TEST = ROOT / "tests" / "test_pedicularis_wave1_permission_responses.py"

spec = importlib.util.spec_from_file_location("ped_permission_scope", VALIDATOR)
scope = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(scope)

spec2 = importlib.util.spec_from_file_location("ped_permission_fixture_source", RESP_TEST)
fixtures = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(fixtures)


def _receipt() -> dict:
    return fixtures.adj.adjudicate(fixtures._songzanlin_bundle())


def test_confirmed_scope_receipt_full_provenance_validates() -> None:
    receipt = _receipt()
    out = scope.validate_confirmed_scope_receipt(
        receipt,
        expected_candidate_id="SONGZANLIN_EIA_2025",
    )
    assert out["candidate_id"] == "SONGZANLIN_EIA_2025"
    assert out["adjudication_commit"] == "perm123"
    assert out["sampling_permission_reference"].endswith("@perm123")


def test_scope_receipt_requires_adjudication_metadata() -> None:
    receipt = _receipt()
    receipt.pop("adjudication_metadata")
    with pytest.raises(ValueError, match="adjudication metadata missing"):
        scope.validate_confirmed_scope_receipt(receipt)


def test_scope_receipt_requires_response_provenance() -> None:
    receipt = _receipt()
    receipt["responses"][0].pop("source_response_content_sha256")
    with pytest.raises(ValueError, match="source_response_content_sha256"):
        scope.validate_confirmed_scope_receipt(receipt)


def test_scope_receipt_requires_activity_decision_evidence() -> None:
    receipt = _receipt()
    receipt["responses"][0]["activity_decision_details"]["A"][
        "decision_evidence_locator"
    ] = None
    with pytest.raises(ValueError, match="decision_evidence_locator"):
        scope.validate_confirmed_scope_receipt(receipt)


def test_scope_receipt_requires_decision_evidence_in_positive_validity_interval() -> None:
    receipt = _receipt()
    receipt["required_activity_validity"]["A"]["regulatory"][0].pop(
        "decision_extraction_reference"
    )
    with pytest.raises(ValueError, match="decision_extraction_reference"):
        scope.validate_confirmed_scope_receipt(receipt)


def test_scope_receipt_candidate_binding_fails_closed() -> None:
    receipt = _receipt()
    with pytest.raises(ValueError, match="candidate mismatch"):
        scope.validate_confirmed_scope_receipt(
            receipt,
            expected_candidate_id="OTHER_CANDIDATE",
        )


def test_scope_receipt_rejects_duplicate_source_response_event() -> None:
    receipt = _receipt()
    receipt["responses"][1]["source_response_event_id"] = receipt[
        "responses"
    ][0]["source_response_event_id"]
    with pytest.raises(ValueError, match="duplicate source response event"):
        scope.validate_confirmed_scope_receipt(receipt)


def test_scope_receipt_rejects_mutated_activity_definition() -> None:
    receipt = _receipt()
    receipt["required_activity_validity"]["A"]["site"][0][
        "registered_activity_definition_reference"
    ] = "SLK_PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1#B"
    with pytest.raises(ValueError, match="activity definition mismatch"):
        scope.validate_confirmed_scope_receipt(receipt)



def test_scope_receipt_interval_route_must_match_source_response() -> None:
    receipt = _receipt()
    receipt["required_activity_validity"]["A"]["regulatory"][0][
        "route_id"
    ] = "OTHER-ROUTE"
    with pytest.raises(ValueError, match="route/response mismatch"):
        scope.validate_confirmed_scope_receipt(receipt)


def test_scope_receipt_interval_extraction_cannot_predate_source_response() -> None:
    receipt = _receipt()
    receipt["required_activity_validity"]["A"]["regulatory"][0][
        "decision_extraction_date"
    ] = "2027-05-09"
    with pytest.raises(ValueError, match="outside response/adjudication window"):
        scope.validate_confirmed_scope_receipt(receipt)


def test_scope_receipt_interval_locator_must_match_source_channel() -> None:
    receipt = _receipt()
    receipt["required_activity_validity"]["A"]["regulatory"][0][
        "decision_evidence_locator"
    ] = "CALL_NOTE:line-1"
    with pytest.raises(ValueError, match="locator/channel mismatch"):
        scope.validate_confirmed_scope_receipt(receipt)
