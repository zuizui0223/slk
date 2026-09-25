from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RENDER = ROOT / "scripts" / "render_pedicularis_wave1_permission_followup.py"
GUARD = ROOT / "scripts" / "validate_pedicularis_wave1_permission_messages_for_send.py"
APPLY = ROOT / "scripts" / "apply_pedicularis_permission_followup_send_receipt.py"
LEDGER = ROOT / "data" / "PEDICULARIS_WAVE1_PERMISSION_OUTREACH_LEDGER_TEMPLATE_V1.csv"
POLICY = ROOT / "data" / "PEDICULARIS_WAVE1_PERMISSION_FOLLOWUP_POLICY_TEMPLATE_V1.json"

spec = importlib.util.spec_from_file_location("ped_followup_render", RENDER)
render = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(render)

spec2 = importlib.util.spec_from_file_location("ped_followup_guard", GUARD)
guard = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(guard)

spec3 = importlib.util.spec_from_file_location("ped_followup_apply", APPLY)
apply = importlib.util.module_from_spec(spec3)
assert spec3.loader is not None
spec3.loader.exec_module(apply)


def _policy() -> dict:
    payload = json.loads(POLICY.read_text())
    payload["status"] = "FROZEN_POLICY"
    payload["production_status"] = (
        "PEDICULARIS_WAVE1_PERMISSION_FOLLOWUP_POLICY_PROSPECTIVELY_FROZEN"
    )
    payload["policy"].update(
        {
            "followup_offsets_days": [7, 14],
            "escalation_review_after_days": 21,
            "frozen_before_first_send": True,
        }
    )
    payload["freeze_metadata"] = {
        "slk_source_commit": "abc123",
        "freeze_commit": "followup-freeze-001",
        "freeze_timestamp": "2027-04-20T00:00:00+08:00",
        "policy_rationale_reference": "ADMIN-POLICY-001",
    }
    return payload


def _rows() -> list[dict[str, str]]:
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    row = next(
        r for r in rows
        if r["route_id"] == "SONGZANLIN_FORESTRY_REGULATOR"
    )
    row["outreach_status"] = "SENT_AWAITING_RESPONSE"
    row["outreach_date"] = "2027-05-01"
    row["outreach_reference"] = "INITIAL-SEND-001"
    row["next_action"] = "AWAIT_RESPONSE"
    return rows


def _ready_followup(
    *,
    as_of_date: str = "2027-05-08",
    rows: list[dict[str, str]] | None = None,
) -> dict:
    payload = render.render_followup(
        rows or _rows(),
        _policy(),
        route_id="SONGZANLIN_FORESTRY_REGULATOR",
        as_of_date=as_of_date,
    )
    for message in payload["messages"]:
        message["body_cn"] = message["body_cn"].replace(
            "REQUIRED_BEFORE_SEND",
            "PROJECT_CONTACT",
        )
        message["body_en"] = message["body_en"].replace(
            "REQUIRED_BEFORE_SEND",
            "PROJECT_CONTACT",
        )
    return guard.validate_and_prepare(
        payload,
        human_review_approved=True,
    )


def _receipt(ready: dict, *, sent_at: str = "2027-05-08T09:30:00+08:00") -> dict:
    message = ready["messages"][0]
    canonical = message["public_contact"]
    contacts = [x.strip() for x in canonical.split(";") if x.strip()]
    sent_to = contacts[0]
    channel = "EMAIL" if "@" in sent_to else "PHONE_SCRIPT"
    return {
        "schema_version": "SLK_PEDICULARIS_WAVE1_PERMISSION_FOLLOWUP_SEND_RECEIPT_V1",
        "status": "MANUAL_FOLLOWUP_SEND_RECORDED",
        "candidate_id": ready["candidate"]["candidate_id"],
        "route_id": message["route_id"],
        "followup_number": message["followup_number"],
        "send_event_id": f"FOLLOWUP-SEND-{message['followup_number']}-001",
        "sent_at": sent_at,
        "send_channel": channel,
        "sent_language": "BILINGUAL",
        "canonical_contact_snapshot": canonical,
        "sent_to_contact": sent_to,
        "sent_message_reference": f"FOLLOWUP-REF-{message['followup_number']}",
        "sent_content_sha256": message["message_content_sha256_bilingual"],
        "manual_send_confirmed": True,
        "sender_identity_reference": "LOCAL-SENDER-001",
        "notes": "",
    }


def test_due_followup_renderer_creates_single_unsent_followup_message() -> None:
    out = render.render_followup(
        _rows(),
        _policy(),
        route_id="SONGZANLIN_FORESTRY_REGULATOR",
        as_of_date="2027-05-08",
    )
    assert out["status"] == "DRAFT_NOT_SENT"
    assert out["message_kind"] == "FOLLOWUP"
    assert len(out["messages"]) == 1
    message = out["messages"][0]
    assert message["followup_number"] == 1
    assert message["policy_due_date"] == "2027-05-08"
    assert message["prior_contact_date"] == "2027-05-01"
    assert message["prior_contact_reference"] == "INITIAL-SEND-001"
    assert message["send_guard"]["automatic_send_allowed"] is False


def test_followup_renderer_refuses_route_before_due_date() -> None:
    with pytest.raises(ValueError, match="not due"):
        render.render_followup(
            _rows(),
            _policy(),
            route_id="SONGZANLIN_FORESTRY_REGULATOR",
            as_of_date="2027-05-07",
        )


def test_followup_renderer_refuses_route_after_response() -> None:
    rows = _rows()
    row = next(
        r for r in rows
        if r["route_id"] == "SONGZANLIN_FORESTRY_REGULATOR"
    )
    row["outreach_status"] = "RESPONSE_RECEIVED"
    row["response_status"] = "SUBSTANTIVE_RESPONSE_RECEIVED"
    row["response_date"] = "2027-05-06"
    row["response_reference"] = "RESPONSE-001"
    with pytest.raises(ValueError, match="not due"):
        render.render_followup(
            rows,
            _policy(),
            route_id="SONGZANLIN_FORESTRY_REGULATOR",
            as_of_date="2027-05-08",
        )


def test_second_followup_references_first_followup_event() -> None:
    rows = _rows()
    row = next(
        r for r in rows
        if r["route_id"] == "SONGZANLIN_FORESTRY_REGULATOR"
    )
    row["followup_attempts_completed"] = "1"
    row["last_followup_date"] = "2027-05-08"
    row["last_followup_reference"] = "FOLLOWUP-REF-1"
    out = render.render_followup(
        rows,
        _policy(),
        route_id="SONGZANLIN_FORESTRY_REGULATOR",
        as_of_date="2027-05-15",
    )
    message = out["messages"][0]
    assert message["followup_number"] == 2
    assert message["prior_contact_date"] == "2027-05-08"
    assert message["prior_contact_reference"] == "FOLLOWUP-REF-1"


def test_valid_followup_send_receipt_increments_attempt_count() -> None:
    rows = _rows()
    ready = _ready_followup(rows=rows)
    receipt = _receipt(ready)
    updated, event = apply.apply_followup_send_receipt(
        rows,
        ready,
        receipt,
        _policy(),
    )
    target = next(
        r for r in updated
        if r["route_id"] == "SONGZANLIN_FORESTRY_REGULATOR"
    )
    assert target["outreach_status"] == "SENT_AWAITING_RESPONSE"
    assert target["followup_attempts_completed"] == "1"
    assert target["last_followup_date"] == "2027-05-08"
    assert target["last_followup_reference"] == "FOLLOWUP-REF-1"
    assert event["status"] == "MANUAL_FOLLOWUP_SEND_EVENT_VALIDATED"
    assert event["followup_number"] == 1
    assert event["automatic_send_used"] is False


def test_followup_send_receipt_cannot_be_applied_before_due_date() -> None:
    rows = _rows()
    ready = _ready_followup(rows=rows)
    receipt = _receipt(ready, sent_at="2027-05-07T09:30:00+08:00")
    with pytest.raises(ValueError, match="not due under frozen policy"):
        apply.apply_followup_send_receipt(
            rows,
            ready,
            receipt,
            _policy(),
        )


def test_followup_number_must_match_reviewed_message_and_planner() -> None:
    rows = _rows()
    ready = _ready_followup(rows=rows)
    receipt = _receipt(ready)
    receipt["followup_number"] = 2
    with pytest.raises(ValueError, match="number/message mismatch"):
        apply.apply_followup_send_receipt(
            rows,
            ready,
            receipt,
            _policy(),
        )


def test_followup_body_mutation_after_review_is_rejected() -> None:
    rows = _rows()
    ready = _ready_followup(rows=rows)
    receipt = _receipt(ready)
    ready["messages"][0]["body_en"] += "\nChanged after review."
    with pytest.raises(ValueError, match="ready EN message content hash mismatch"):
        apply.apply_followup_send_receipt(
            rows,
            ready,
            receipt,
            _policy(),
        )


def test_followup_send_cannot_be_registered_after_response_arrives() -> None:
    rows = _rows()
    ready = _ready_followup(rows=rows)
    receipt = _receipt(ready)
    row = next(
        r for r in rows
        if r["route_id"] == "SONGZANLIN_FORESTRY_REGULATOR"
    )
    row["outreach_status"] = "RESPONSE_RECEIVED"
    row["response_status"] = "SUBSTANTIVE_RESPONSE_RECEIVED"
    row["response_date"] = "2027-05-08"
    row["response_reference"] = "RESPONSE-001"
    with pytest.raises(ValueError, match="not awaiting response"):
        apply.apply_followup_send_receipt(
            rows,
            ready,
            receipt,
            _policy(),
        )


def test_same_followup_cannot_be_registered_twice() -> None:
    rows = _rows()
    ready = _ready_followup(rows=rows)
    receipt = _receipt(ready)
    updated, _ = apply.apply_followup_send_receipt(
        rows,
        ready,
        receipt,
        _policy(),
    )
    with pytest.raises(ValueError):
        apply.apply_followup_send_receipt(
            updated,
            ready,
            receipt,
            _policy(),
        )


def test_followup_receipt_cn_hash_must_match_cn_language() -> None:
    rows = _rows()
    ready = _ready_followup(rows=rows)
    receipt = _receipt(ready)
    message = ready["messages"][0]
    receipt["sent_language"] = "CN"
    receipt["sent_content_sha256"] = message["message_content_sha256_cn"]
    _, event = apply.apply_followup_send_receipt(
        rows,
        ready,
        receipt,
        _policy(),
    )
    assert event["sent_language"] == "CN"
    assert event["message_content_sha256"] == message["message_content_sha256_cn"]
