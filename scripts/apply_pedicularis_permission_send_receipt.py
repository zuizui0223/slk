from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUARD_PATH = ROOT / "scripts" / "validate_pedicularis_wave1_permission_messages_for_send.py"
MANAGER_PATH = ROOT / "scripts" / "manage_pedicularis_wave1_permission_outreach.py"

_spec_guard = importlib.util.spec_from_file_location("ped_message_guard", GUARD_PATH)
guard = importlib.util.module_from_spec(_spec_guard)
assert _spec_guard.loader is not None
_spec_guard.loader.exec_module(guard)

_spec_manager = importlib.util.spec_from_file_location("ped_outreach_manager", MANAGER_PATH)
manager = importlib.util.module_from_spec(_spec_manager)
assert _spec_manager.loader is not None
_spec_manager.loader.exec_module(manager)

SEND_RECEIPT_SCHEMA = "SLK_PEDICULARIS_WAVE1_PERMISSION_SEND_RECEIPT_V1"
READY_MESSAGES_SCHEMA = "SLK_PEDICULARIS_WAVE1_PERMISSION_MESSAGE_DRAFTS_V1"
ALLOWED_CHANNELS = {"EMAIL", "WEB_FORM", "LETTER", "PHONE_SCRIPT", "IN_PERSON_HANDOFF"}


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _filled(value: object, label: str) -> str:
    if value is None:
        raise ValueError(f"unresolved {label}")
    text = str(value).strip()
    _need(
        bool(text)
        and "REQUIRED_BEFORE_USE" not in text
        and text.lower() not in {"none", "null"},
        f"unresolved {label}",
    )
    return text


def _allowed_specific_contacts(canonical: str) -> set[str]:
    parts = {
        part.strip()
        for part in canonical.split(";")
        if part.strip()
    }
    return parts or {canonical.strip()}


def _validate_channel_contact(channel: str, contact: str) -> None:
    if channel == "EMAIL":
        _need("@" in contact, "EMAIL send channel requires an email contact")
    elif channel == "PHONE_SCRIPT":
        _need(
            any(ch.isdigit() for ch in contact),
            "PHONE_SCRIPT send channel requires a phone-like contact",
        )


def _sent_at(value: object) -> datetime:
    text = _filled(value, "sent_at")
    try:
        out = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("sent_at must be ISO 8601 datetime") from exc
    _need(out.tzinfo is not None, "sent_at must include timezone offset")
    return out


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _ready_message(payload: dict, route_id: str) -> dict:
    _need(
        payload.get("schema_version") == READY_MESSAGES_SCHEMA,
        "wrong ready-message schema",
    )
    _need(
        payload.get("status") == "READY_FOR_MANUAL_SEND",
        "message bundle is not ready for manual send",
    )
    policy = payload.get("send_policy")
    _need(isinstance(policy, dict), "message send_policy missing")
    _need(policy.get("manual_send_only") is True, "message send policy changed")
    _need(
        policy.get("automatic_send_allowed") is False,
        "automatic send must remain disabled",
    )
    _need(
        policy.get("human_review_approved") is True,
        "human review approval missing",
    )

    candidate = payload.get("candidate", {})
    candidate_id = _filled(candidate.get("candidate_id"), "message candidate_id")
    messages = payload.get("messages")
    _need(isinstance(messages, list), "ready message list missing")
    matches = [
        message
        for message in messages
        if str(message.get("route_id", "")).strip() == route_id
    ]
    _need(len(matches) == 1, f"ready message not uniquely identified: {route_id}")
    message = matches[0]
    _need(
        message.get("status") == "READY_FOR_MANUAL_SEND",
        f"route message is not ready for manual send: {route_id}",
    )
    send_guard = message.get("send_guard", {})
    _need(
        isinstance(send_guard, dict)
        and send_guard.get("human_review_approved") is True
        and send_guard.get("automatic_send_allowed") is False,
        f"route message send guard invalid: {route_id}",
    )
    canonical_hash = guard.message_content_sha256(message)
    _need(
        message.get("message_content_sha256") == canonical_hash,
        f"ready message content hash mismatch: {route_id}",
    )
    return {
        "candidate_id": candidate_id,
        "message": message,
        "message_content_sha256": canonical_hash,
    }


def apply_send_receipt(
    rows: list[dict[str, str]],
    ready_messages: dict,
    send_receipt: dict,
) -> tuple[list[dict[str, str]], dict]:
    _need(
        send_receipt.get("schema_version") == SEND_RECEIPT_SCHEMA,
        "wrong permission send-receipt schema",
    )
    _need(
        send_receipt.get("status") == "MANUAL_SEND_RECORDED",
        "permission send receipt is not filled",
    )
    candidate_id = _filled(send_receipt.get("candidate_id"), "candidate_id")
    route_id = _filled(send_receipt.get("route_id"), "route_id")
    send_event_id = _filled(send_receipt.get("send_event_id"), "send_event_id")
    sent_at = _sent_at(send_receipt.get("sent_at"))
    send_channel = _filled(send_receipt.get("send_channel"), "send_channel")
    _need(
        send_channel in ALLOWED_CHANNELS,
        f"unregistered manual send channel: {send_channel}",
    )
    canonical_contact_snapshot = _filled(
        send_receipt.get("canonical_contact_snapshot"),
        "canonical_contact_snapshot",
    )
    sent_to_contact = _filled(
        send_receipt.get("sent_to_contact"),
        "sent_to_contact",
    )
    sent_message_reference = _filled(
        send_receipt.get("sent_message_reference"),
        "sent_message_reference",
    )
    sent_content_sha256 = _filled(
        send_receipt.get("sent_content_sha256"),
        "sent_content_sha256",
    )
    sender_identity_reference = _filled(
        send_receipt.get("sender_identity_reference"),
        "sender_identity_reference",
    )
    _need(
        send_receipt.get("manual_send_confirmed") is True,
        "manual_send_confirmed must be true",
    )

    ready = _ready_message(ready_messages, route_id)
    _need(
        ready["candidate_id"] == candidate_id,
        "send receipt candidate/message mismatch",
    )
    message = ready["message"]
    message_contact = str(message.get("public_contact", "")).strip()
    _need(
        canonical_contact_snapshot == message_contact,
        "send receipt canonical contact/message mismatch",
    )
    allowed_contacts = _allowed_specific_contacts(message_contact)
    _need(
        sent_to_contact in allowed_contacts,
        "send receipt contact is not a registered canonical contact option",
    )
    _validate_channel_contact(send_channel, sent_to_contact)
    _need(
        sent_content_sha256 == ready["message_content_sha256"],
        "send receipt content hash/message mismatch",
    )

    route_rows = [
        row
        for row in rows
        if str(row.get("route_id", "")).strip() == route_id
    ]
    _need(len(route_rows) == 1, f"outreach route not uniquely found: {route_id}")
    target = route_rows[0]
    _need(
        str(target.get("candidate_id", "")).strip() == candidate_id,
        "send receipt candidate/outreach mismatch",
    )
    _need(
        str(target.get("outreach_status", "")).strip() == "NOT_SENT",
        "outreach route is not in NOT_SENT state",
    )
    _need(
        str(target.get("response_status", "")).strip() == "NO_RESPONSE",
        "cannot send-register a route that already carries a response",
    )

    updated = [dict(row) for row in rows]
    updated_target = next(
        row for row in updated
        if str(row.get("route_id", "")).strip() == route_id
    )
    updated_target["outreach_status"] = "SENT_AWAITING_RESPONSE"
    updated_target["outreach_date"] = sent_at.date().isoformat()
    updated_target["outreach_reference"] = sent_message_reference
    updated_target["next_action"] = "AWAIT_RESPONSE"
    note_parts = [
        part
        for part in (
            str(updated_target.get("notes", "")).strip(),
            f"send_event_id={send_event_id}",
            f"send_channel={send_channel}",
            f"message_sha256={sent_content_sha256}",
            f"sender_identity_reference={sender_identity_reference}",
        )
        if part
    ]
    updated_target["notes"] = " | ".join(note_parts)

    manager_receipt = manager.validate(updated)
    event_receipt = {
        "schema_version": "SLK_PEDICULARIS_WAVE1_PERMISSION_SEND_EVENT_RECEIPT_V1",
        "status": "MANUAL_SEND_EVENT_VALIDATED",
        "candidate_id": candidate_id,
        "route_id": route_id,
        "send_event_id": send_event_id,
        "sent_at": sent_at.isoformat(),
        "outreach_date": sent_at.date().isoformat(),
        "send_channel": send_channel,
        "canonical_contact_snapshot": canonical_contact_snapshot,
        "sent_to_contact": sent_to_contact,
        "sent_message_reference": sent_message_reference,
        "message_content_sha256": sent_content_sha256,
        "sender_identity_reference": sender_identity_reference,
        "outreach_status_after": "SENT_AWAITING_RESPONSE",
        "automatic_send_used": False,
        "manager_receipt_status": manager_receipt["status"],
        "claim_ceiling": (
            "MANUAL_SEND_EVENT_ONLY_NO_RESPONSE_NO_PERMISSION_GRANTED_"
            "NO_FRESH_CONTEXT_NO_P0_SIGNAL"
        ),
    }
    return updated, event_receipt


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apply a validated manual-send receipt to the Pedicularis WAVE1 outreach ledger"
    )
    parser.add_argument("outreach_ledger_csv", type=Path)
    parser.add_argument("ready_messages_json", type=Path)
    parser.add_argument("send_receipt_json", type=Path)
    parser.add_argument("--ledger-output", required=True, type=Path)
    parser.add_argument("--event-output", required=True, type=Path)
    args = parser.parse_args()

    rows = _read_csv(args.outreach_ledger_csv)
    ready = json.loads(args.ready_messages_json.read_text(encoding="utf-8"))
    send_receipt = json.loads(args.send_receipt_json.read_text(encoding="utf-8"))
    updated, event = apply_send_receipt(rows, ready, send_receipt)

    fieldnames = list(updated[0].keys())
    with args.ledger_output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated)

    args.event_output.write_text(
        json.dumps(event, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
