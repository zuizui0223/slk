from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "apply_pedicularis_permission_response_receipt.py"
LEDGER = ROOT / "data" / "PEDICULARIS_WAVE1_PERMISSION_OUTREACH_LEDGER_TEMPLATE_V1.csv"
RESPONSE_TEMPLATE = ROOT / "data" / "PEDICULARIS_WAVE1_INCOMING_RESPONSE_RECEIPT_TEMPLATE_V1.json"

spec = importlib.util.spec_from_file_location("ped_response_receipt", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def _rows() -> list[dict[str, str]]:
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _sent_rows(*route_ids: str) -> list[dict[str, str]]:
    rows = _rows()
    for route_id in route_ids:
        row = next(r for r in rows if r["route_id"] == route_id)
        row["outreach_status"] = "SENT_AWAITING_RESPONSE"
        row["outreach_date"] = "2027-05-01"
        row["outreach_reference"] = f"SEND-{route_id}-001"
        row["next_action"] = "AWAIT_RESPONSE"
    return rows


def _receipt(
    rows: list[dict[str, str]],
    route_id: str,
    *,
    status: str = "SUBSTANTIVE_RESPONSE_RECEIVED",
    received_at: str = "2027-05-05T10:00:00+08:00",
    recorded_at: str = "2027-05-05T12:00:00+08:00",
) -> dict:
    row = next(r for r in rows if r["route_id"] == route_id)
    routing = (
        {
            "organization": "NEW ROUTED AUTHORITY",
            "contact": "NEW-ROUTE-CONTACT",
        }
        if status == "ROUTING_RESPONSE_ONLY"
        else {"organization": "", "contact": ""}
    )
    return {
        "schema_version": "SLK_PEDICULARIS_WAVE1_INCOMING_RESPONSE_RECEIPT_V1",
        "status": "INCOMING_RESPONSE_RECORDED",
        "candidate_id": row["candidate_id"],
        "route_id": route_id,
        "response_event_id": f"RESPONSE-EVENT-{route_id}-001",
        "received_at": received_at,
        "recorded_at": recorded_at,
        "receive_channel": "EMAIL",
        "responding_organization": row["organization"],
        "responding_contact": "reply@example.org",
        "response_reference": f"LOCAL-RESPONSE-{route_id}-001",
        "response_subject": "Re: research permission inquiry",
        "response_capture_text": "Captured authority response text for audit.",
        "attachments": [],
        "response_content_sha256": None,
        "classification": {
            "response_status": status,
            "reviewed_by": "TEST-REVIEWER",
            "review_date": received_at[:10],
            "review_reference": f"CLASS-REVIEW-{route_id}-001",
            "rationale": "Response contains activity-specific authority information.",
        },
        "routing_destination": routing,
        "notes": "",
    }


def test_substantive_response_updates_route_with_audited_provenance() -> None:
    route = "SONGZANLIN_FORESTRY_REGULATOR"
    rows = _sent_rows(route)
    receipt = _receipt(rows, route)
    updated, event = mod.apply_response_receipt(rows, receipt)
    target = next(r for r in updated if r["route_id"] == route)

    assert target["outreach_status"] == "RESPONSE_RECEIVED"
    assert target["response_status"] == "SUBSTANTIVE_RESPONSE_RECEIVED"
    assert target["response_date"] == "2027-05-05"
    assert target["response_received_at"] == "2027-05-05T10:00:00+08:00"
    assert target["response_event_id"] == receipt["response_event_id"]
    assert target["response_receive_channel"] == "EMAIL"
    assert len(target["response_content_sha256"]) == 64
    assert target["response_classification_review_reference"].startswith(
        "CLASS-REVIEW-"
    )
    assert event["status"] == "INCOMING_RESPONSE_EVENT_VALIDATED"
    assert event["response_content_sha256"] == target["response_content_sha256"]
    assert event["candidate_ready_to_build_permission_response_bundle"] is False
    assert event["next_action_after"] == "AWAIT_OTHER_AUTHORIZING_RESPONSE"


def test_regulatory_plus_site_response_makes_candidate_bundle_ready() -> None:
    reg = "SONGZANLIN_FORESTRY_REGULATOR"
    site = "SONGZANLIN_SITE_MANAGEMENT"
    rows = _sent_rows(reg, site)

    rows, first = mod.apply_response_receipt(rows, _receipt(rows, reg))
    assert first["candidate_ready_to_build_permission_response_bundle"] is False

    rows, second = mod.apply_response_receipt(rows, _receipt(rows, site))
    assert second["candidate_ready_to_build_permission_response_bundle"] is True
    assert second["next_action_after"] == "BUILD_PERMISSION_RESPONSE_DRAFT"
    site_row = next(r for r in rows if r["route_id"] == site)
    assert site_row["next_action"] == "BUILD_PERMISSION_RESPONSE_DRAFT"


def test_routing_response_updates_route_without_authorization_readiness() -> None:
    route = "WUFENG_LOCAL_ROUTING"
    rows = _sent_rows(route)
    receipt = _receipt(rows, route, status="ROUTING_RESPONSE_ONLY")
    updated, event = mod.apply_response_receipt(rows, receipt)
    target = next(r for r in updated if r["route_id"] == route)

    assert target["outreach_status"] == "ROUTED_TO_ANOTHER_AUTHORITY"
    assert target["response_status"] == "ROUTING_RESPONSE_ONLY"
    assert target["routed_to_organization"] == "NEW ROUTED AUTHORITY"
    assert target["routed_to_contact"] == "NEW-ROUTE-CONTACT"
    assert target["next_action"] == "REGISTER_ROUTED_AUTHORITY_AND_SEND_NEW_INQUIRY"
    assert event["candidate_ready_to_build_permission_response_bundle"] is False


def test_routing_only_route_cannot_be_classified_as_substantive() -> None:
    route = "WUFENG_LOCAL_ROUTING"
    rows = _sent_rows(route)
    with pytest.raises(ValueError, match="routing-only route cannot be classified"):
        mod.apply_response_receipt(rows, _receipt(rows, route))


def test_response_requires_sent_awaiting_state() -> None:
    rows = _rows()
    route = "SONGZANLIN_FORESTRY_REGULATOR"
    with pytest.raises(ValueError, match="requires SENT_AWAITING_RESPONSE"):
        mod.apply_response_receipt(rows, _receipt(rows, route))


def test_response_cannot_be_registered_twice() -> None:
    route = "SONGZANLIN_FORESTRY_REGULATOR"
    rows = _sent_rows(route)
    receipt = _receipt(rows, route)
    updated, _ = mod.apply_response_receipt(rows, receipt)
    with pytest.raises(ValueError, match="requires SENT_AWAITING_RESPONSE"):
        mod.apply_response_receipt(updated, receipt)


def test_response_organization_must_match_canonical_route() -> None:
    route = "SONGZANLIN_FORESTRY_REGULATOR"
    rows = _sent_rows(route)
    receipt = _receipt(rows, route)
    receipt["responding_organization"] = "OTHER ORGANIZATION"
    with pytest.raises(ValueError, match="organization/route mismatch"):
        mod.apply_response_receipt(rows, receipt)


def test_response_received_before_initial_send_is_rejected() -> None:
    route = "SONGZANLIN_FORESTRY_REGULATOR"
    rows = _sent_rows(route)
    receipt = _receipt(
        rows,
        route,
        received_at="2027-04-30T10:00:00+08:00",
        recorded_at="2027-05-01T12:00:00+08:00",
    )
    with pytest.raises(ValueError, match="received before initial outreach"):
        mod.apply_response_receipt(rows, receipt)


def test_recorded_at_cannot_precede_received_at() -> None:
    route = "SONGZANLIN_FORESTRY_REGULATOR"
    rows = _sent_rows(route)
    receipt = _receipt(
        rows,
        route,
        received_at="2027-05-05T10:00:00+08:00",
        recorded_at="2027-05-05T09:00:00+08:00",
    )
    with pytest.raises(ValueError, match="cannot precede received_at"):
        mod.apply_response_receipt(rows, receipt)


def test_classification_review_date_must_be_between_receipt_and_recording() -> None:
    route = "SONGZANLIN_FORESTRY_REGULATOR"
    rows = _sent_rows(route)
    receipt = _receipt(rows, route)
    receipt["classification"]["review_date"] = "2027-05-04"
    with pytest.raises(ValueError, match="must fall between receipt and recording"):
        mod.apply_response_receipt(rows, receipt)


def test_supplied_response_hash_must_match_captured_content() -> None:
    route = "SONGZANLIN_FORESTRY_REGULATOR"
    rows = _sent_rows(route)
    receipt = _receipt(rows, route)
    receipt["response_content_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="supplied hash does not match"):
        mod.apply_response_receipt(rows, receipt)


def test_content_hash_changes_when_captured_response_changes() -> None:
    route = "SONGZANLIN_FORESTRY_REGULATOR"
    rows = _sent_rows(route)
    receipt = _receipt(rows, route)
    first = mod.response_content_sha256(receipt)
    receipt["response_capture_text"] += " Additional text."
    second = mod.response_content_sha256(receipt)
    assert first != second


def test_followup_after_already_received_reply_is_flagged_as_protocol_deviation() -> None:
    route = "SONGZANLIN_FORESTRY_REGULATOR"
    rows = _sent_rows(route)
    target = next(r for r in rows if r["route_id"] == route)
    target["followup_attempts_completed"] = "1"
    target["last_followup_date"] = "2027-05-10"
    target["last_followup_reference"] = "FOLLOWUP-001"

    receipt = _receipt(
        rows,
        route,
        received_at="2027-05-09T10:00:00+08:00",
        recorded_at="2027-05-11T12:00:00+08:00",
    )
    receipt["classification"]["review_date"] = "2027-05-11"
    _, event = mod.apply_response_receipt(rows, receipt)
    assert event["followup_preemption_violation"] is True
    assert event["protocol_deviation_requires_review"] is True



def test_incoming_response_template_keeps_content_hash_unset_until_capture() -> None:
    payload = json.loads(RESPONSE_TEMPLATE.read_text())
    assert payload["schema_version"] == (
        "SLK_PEDICULARIS_WAVE1_INCOMING_RESPONSE_RECEIPT_V1"
    )
    assert payload["status"] == "TEMPLATE_ONLY_NOT_DATA"
    assert payload["response_content_sha256"] is None
    assert payload["attachments"] == []
    assert payload["classification"]["response_status"] == "REQUIRED_BEFORE_USE"



def test_attachment_hash_contributes_to_response_content_hash() -> None:
    route = "SONGZANLIN_FORESTRY_REGULATOR"
    rows = _sent_rows(route)
    receipt = _receipt(rows, route)
    receipt["attachments"] = [
        {
            "reference": "ATT-001",
            "sha256": "1" * 64,
            "media_type": "application/pdf",
            "file_name": "authority-letter.pdf",
        }
    ]
    first = mod.response_content_sha256(receipt)
    receipt["attachments"][0]["sha256"] = "2" * 64
    second = mod.response_content_sha256(receipt)
    assert first != second


def test_attachment_hash_must_be_sha256() -> None:
    route = "SONGZANLIN_FORESTRY_REGULATOR"
    rows = _sent_rows(route)
    receipt = _receipt(rows, route)
    receipt["attachments"] = [
        {
            "reference": "ATT-001",
            "sha256": "bad",
            "media_type": "application/pdf",
            "file_name": "authority-letter.pdf",
        }
    ]
    with pytest.raises(ValueError, match="attachments/0/sha256 must be sha256"):
        mod.response_content_sha256(receipt)


def test_attachment_references_must_be_unique() -> None:
    route = "SONGZANLIN_FORESTRY_REGULATOR"
    rows = _sent_rows(route)
    receipt = _receipt(rows, route)
    receipt["attachments"] = [
        {
            "reference": "ATT-001",
            "sha256": "1" * 64,
            "media_type": "application/pdf",
            "file_name": "a.pdf",
        },
        {
            "reference": "ATT-001",
            "sha256": "2" * 64,
            "media_type": "application/pdf",
            "file_name": "b.pdf",
        },
    ]
    with pytest.raises(ValueError, match="duplicate attachment reference"):
        mod.response_content_sha256(receipt)


def test_response_event_preserves_attachment_hash_manifest() -> None:
    route = "SONGZANLIN_FORESTRY_REGULATOR"
    rows = _sent_rows(route)
    receipt = _receipt(rows, route)
    receipt["attachments"] = [
        {
            "reference": "ATT-001",
            "sha256": "3" * 64,
            "media_type": "application/pdf",
            "file_name": "authority-letter.pdf",
        }
    ]
    _, event = mod.apply_response_receipt(rows, receipt)
    assert event["attachment_count"] == 1
    assert event["attachment_hashes"] == [
        {"reference": "ATT-001", "sha256": "3" * 64}
    ]
