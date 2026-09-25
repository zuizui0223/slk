from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RENDER = ROOT / "scripts" / "render_pedicularis_wave1_permission_messages.py"
GUARD = ROOT / "scripts" / "validate_pedicularis_wave1_permission_messages_for_send.py"
APPLY = ROOT / "scripts" / "apply_pedicularis_permission_send_receipt.py"
LEDGER = ROOT / "data" / "PEDICULARIS_WAVE1_PERMISSION_OUTREACH_LEDGER_TEMPLATE_V1.csv"

spec = importlib.util.spec_from_file_location("ped_send_render", RENDER)
render = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(render)

spec2 = importlib.util.spec_from_file_location("ped_send_guard", GUARD)
guard = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(guard)

spec3 = importlib.util.spec_from_file_location("ped_send_apply", APPLY)
apply = importlib.util.module_from_spec(spec3)
assert spec3.loader is not None
spec3.loader.exec_module(apply)


def _rows() -> list[dict[str, str]]:
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _ready(candidate_id: str = "SONGZANLIN_EIA_2025") -> dict:
    payload = render.render(candidate_id)
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


def _receipt(ready: dict, route_id: str = "SONGZANLIN_FORESTRY_REGULATOR") -> dict:
    message = next(m for m in ready["messages"] if m["route_id"] == route_id)
    canonical_contact = message["public_contact"]
    contact_options = [x.strip() for x in canonical_contact.split(";") if x.strip()]
    sent_to_contact = contact_options[0]
    send_channel = "EMAIL" if "@" in sent_to_contact else "PHONE_SCRIPT"
    return {
        "schema_version": "SLK_PEDICULARIS_WAVE1_PERMISSION_SEND_RECEIPT_V1",
        "status": "MANUAL_SEND_RECORDED",
        "candidate_id": ready["candidate"]["candidate_id"],
        "route_id": route_id,
        "send_event_id": f"SEND-{route_id}-001",
        "sent_at": "2027-05-01T09:30:00+08:00",
        "send_channel": send_channel,
        "canonical_contact_snapshot": canonical_contact,
        "sent_to_contact": sent_to_contact,
        "sent_message_reference": f"LOCAL-SENT-{route_id}-001",
        "sent_content_sha256": message["message_content_sha256"],
        "manual_send_confirmed": True,
        "sender_identity_reference": "LOCAL-SENDER-IDENTITY-001",
        "notes": "",
    }


def test_valid_send_receipt_moves_only_target_route_to_awaiting_response() -> None:
    rows = _rows()
    ready = _ready()
    updated, event = apply.apply_send_receipt(
        rows,
        ready,
        _receipt(ready),
    )
    target = next(
        row for row in updated
        if row["route_id"] == "SONGZANLIN_FORESTRY_REGULATOR"
    )
    assert target["outreach_status"] == "SENT_AWAITING_RESPONSE"
    assert target["outreach_date"] == "2027-05-01"
    assert target["response_status"] == "NO_RESPONSE"
    assert target["next_action"] == "AWAIT_RESPONSE"
    untouched = next(
        row for row in updated
        if row["route_id"] == "SONGZANLIN_SITE_MANAGEMENT"
    )
    assert untouched["outreach_status"] == "NOT_SENT"
    assert event["status"] == "MANUAL_SEND_EVENT_VALIDATED"
    assert event["automatic_send_used"] is False
    assert event["manager_receipt_status"] == (
        "WAVE1_PERMISSION_OUTREACH_LEDGER_VALIDATED"
    )


def test_send_receipt_rejects_content_hash_mismatch() -> None:
    ready = _ready()
    receipt = _receipt(ready)
    receipt["sent_content_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="content hash/message mismatch"):
        apply.apply_send_receipt(_rows(), ready, receipt)


def test_ready_message_mutation_after_review_is_rejected() -> None:
    ready = _ready()
    receipt = _receipt(ready)
    ready["messages"][0]["body_en"] += "\nChanged after review."
    with pytest.raises(ValueError, match="ready message content hash mismatch"):
        apply.apply_send_receipt(_rows(), ready, receipt)


def test_send_receipt_contact_must_match_reviewed_message() -> None:
    ready = _ready()
    receipt = _receipt(ready)
    receipt["sent_to_contact"] = "DIFFERENT_CONTACT"
    with pytest.raises(ValueError, match="not a registered canonical contact option"):
        apply.apply_send_receipt(_rows(), ready, receipt)


def test_send_receipt_requires_timezone_aware_sent_at() -> None:
    ready = _ready()
    receipt = _receipt(ready)
    receipt["sent_at"] = "2027-05-01T09:30:00"
    with pytest.raises(ValueError, match="timezone offset"):
        apply.apply_send_receipt(_rows(), ready, receipt)


def test_send_receipt_requires_manual_confirmation() -> None:
    ready = _ready()
    receipt = _receipt(ready)
    receipt["manual_send_confirmed"] = False
    with pytest.raises(ValueError, match="manual_send_confirmed"):
        apply.apply_send_receipt(_rows(), ready, receipt)


def test_same_route_cannot_be_registered_as_sent_twice() -> None:
    ready = _ready()
    receipt = _receipt(ready)
    updated, _ = apply.apply_send_receipt(_rows(), ready, receipt)
    with pytest.raises(ValueError, match="not in NOT_SENT state"):
        apply.apply_send_receipt(updated, ready, receipt)


def test_send_receipt_candidate_must_match_message_bundle() -> None:
    ready = _ready()
    receipt = _receipt(ready)
    receipt["candidate_id"] = "SHANGRILA_WUFENG"
    with pytest.raises(ValueError, match="candidate/message mismatch"):
        apply.apply_send_receipt(_rows(), ready, receipt)


def test_unreviewed_message_bundle_cannot_register_send() -> None:
    payload = render.render("SONGZANLIN_EIA_2025")
    for message in payload["messages"]:
        message["body_cn"] = message["body_cn"].replace(
            "REQUIRED_BEFORE_SEND",
            "PROJECT_CONTACT",
        )
        message["body_en"] = message["body_en"].replace(
            "REQUIRED_BEFORE_SEND",
            "PROJECT_CONTACT",
        )
    unreviewed = guard.validate_and_prepare(
        payload,
        human_review_approved=False,
    )
    route = "SONGZANLIN_FORESTRY_REGULATOR"
    message = next(m for m in unreviewed["messages"] if m["route_id"] == route)
    receipt = {
        "schema_version": "SLK_PEDICULARIS_WAVE1_PERMISSION_SEND_RECEIPT_V1",
        "status": "MANUAL_SEND_RECORDED",
        "candidate_id": "SONGZANLIN_EIA_2025",
        "route_id": route,
        "send_event_id": "SEND-UNREVIEWED-001",
        "sent_at": "2027-05-01T09:30:00+08:00",
        "send_channel": "PHONE_SCRIPT",
        "canonical_contact_snapshot": message["public_contact"],
        "sent_to_contact": message["public_contact"],
        "sent_message_reference": "LOCAL-SENT-UNREVIEWED",
        "sent_content_sha256": message["message_content_sha256"],
        "manual_send_confirmed": True,
        "sender_identity_reference": "LOCAL-SENDER-IDENTITY-001",
        "notes": "",
    }
    with pytest.raises(ValueError, match="not ready for manual send"):
        apply.apply_send_receipt(_rows(), unreviewed, receipt)



def test_send_receipt_canonical_contact_snapshot_must_match_reviewed_message() -> None:
    ready = _ready()
    receipt = _receipt(ready)
    receipt["canonical_contact_snapshot"] = "OTHER_CANONICAL_CONTACT"
    with pytest.raises(ValueError, match="canonical contact/message mismatch"):
        apply.apply_send_receipt(_rows(), ready, receipt)


def test_multi_contact_route_can_use_one_registered_email_option() -> None:
    ready = _ready("SHANGRILA_ALPINE_BOT_GARDEN")
    route = "ALPINE_GARDEN_SITE_CONTACT"
    receipt = _receipt(ready, route)
    assert receipt["send_channel"] == "EMAIL"
    assert "@" in receipt["sent_to_contact"]
    updated, event = apply.apply_send_receipt(_rows(), ready, receipt)
    target = next(row for row in updated if row["route_id"] == route)
    assert target["outreach_status"] == "SENT_AWAITING_RESPONSE"
    assert event["canonical_contact_snapshot"] == (
        next(m for m in ready["messages"] if m["route_id"] == route)[
            "public_contact"
        ]
    )


def test_email_channel_rejects_phone_contact() -> None:
    ready = _ready()
    receipt = _receipt(ready)
    receipt["send_channel"] = "EMAIL"
    with pytest.raises(ValueError, match="EMAIL send channel requires"):
        apply.apply_send_receipt(_rows(), ready, receipt)


def test_phone_channel_rejects_non_phone_contact() -> None:
    ready = _ready("SHANGRILA_ALPINE_BOT_GARDEN")
    route = "ALPINE_GARDEN_SITE_CONTACT"
    receipt = _receipt(ready, route)
    receipt["send_channel"] = "PHONE_SCRIPT"
    receipt["sent_to_contact"] = "598226819@qq.com"
    with pytest.raises(ValueError, match="PHONE_SCRIPT send channel requires"):
        apply.apply_send_receipt(_rows(), ready, receipt)



def test_descriptive_canonical_contact_can_use_extracted_phone_number() -> None:
    ready = _ready("SHANGRILA_WUFENG")
    route = "WUFENG_JIANTANG_FOREST_FARM"
    receipt = _receipt(ready, route)
    receipt["send_channel"] = "PHONE_SCRIPT"
    receipt["sent_to_contact"] = "0887-8222611"
    updated, event = apply.apply_send_receipt(_rows(), ready, receipt)
    target = next(row for row in updated if row["route_id"] == route)
    assert target["outreach_status"] == "SENT_AWAITING_RESPONSE"
    assert event["sent_to_contact"] == "0887-8222611"
