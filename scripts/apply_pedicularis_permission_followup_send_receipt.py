from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INITIAL_SEND_PATH = ROOT / "scripts" / "apply_pedicularis_permission_send_receipt.py"
PLANNER_PATH = ROOT / "scripts" / "plan_pedicularis_wave1_permission_followups.py"
MANAGER_PATH = ROOT / "scripts" / "manage_pedicularis_wave1_permission_outreach.py"

_spec_send = importlib.util.spec_from_file_location("ped_initial_send", INITIAL_SEND_PATH)
initial_send = importlib.util.module_from_spec(_spec_send)
assert _spec_send.loader is not None
_spec_send.loader.exec_module(initial_send)

_spec_plan = importlib.util.spec_from_file_location("ped_followup_plan", PLANNER_PATH)
planner = importlib.util.module_from_spec(_spec_plan)
assert _spec_plan.loader is not None
_spec_plan.loader.exec_module(planner)

_spec_manager = importlib.util.spec_from_file_location("ped_outreach_manager_followup", MANAGER_PATH)
manager = importlib.util.module_from_spec(_spec_manager)
assert _spec_manager.loader is not None
_spec_manager.loader.exec_module(manager)

SCHEMA = "SLK_PEDICULARIS_WAVE1_PERMISSION_FOLLOWUP_SEND_RECEIPT_V1"


def _positive_int(value: object, label: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{label} must be a positive integer")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be a positive integer") from exc
    if not number.is_integer() or number <= 0:
        raise ValueError(f"{label} must be a positive integer")
    return int(number)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def apply_followup_send_receipt(
    rows: list[dict[str, str]],
    ready_messages: dict,
    receipt: dict,
    policy_payload: dict,
) -> tuple[list[dict[str, str]], dict]:
    initial_send._need(
        receipt.get("schema_version") == SCHEMA,
        "wrong permission follow-up send-receipt schema",
    )
    initial_send._need(
        receipt.get("status") == "MANUAL_FOLLOWUP_SEND_RECORDED",
        "permission follow-up send receipt is not filled",
    )

    candidate_id = initial_send._filled(
        receipt.get("candidate_id"),
        "candidate_id",
    )
    route_id = initial_send._filled(receipt.get("route_id"), "route_id")
    followup_number = _positive_int(
        receipt.get("followup_number"),
        "followup_number",
    )
    send_event_id = initial_send._filled(
        receipt.get("send_event_id"),
        "send_event_id",
    )
    sent_at = initial_send._sent_at(receipt.get("sent_at"))
    send_channel = initial_send._filled(
        receipt.get("send_channel"),
        "send_channel",
    )
    initial_send._need(
        send_channel in initial_send.ALLOWED_CHANNELS,
        f"unregistered manual send channel: {send_channel}",
    )
    sent_language = initial_send._filled(
        receipt.get("sent_language"),
        "sent_language",
    )
    initial_send._need(
        sent_language in initial_send.ALLOWED_SENT_LANGUAGES,
        f"unregistered sent language: {sent_language}",
    )
    canonical_contact_snapshot = initial_send._filled(
        receipt.get("canonical_contact_snapshot"),
        "canonical_contact_snapshot",
    )
    sent_to_contact = initial_send._filled(
        receipt.get("sent_to_contact"),
        "sent_to_contact",
    )
    sent_message_reference = initial_send._filled(
        receipt.get("sent_message_reference"),
        "sent_message_reference",
    )
    sent_content_sha256 = initial_send._filled(
        receipt.get("sent_content_sha256"),
        "sent_content_sha256",
    )
    sender_identity_reference = initial_send._filled(
        receipt.get("sender_identity_reference"),
        "sender_identity_reference",
    )
    initial_send._need(
        receipt.get("manual_send_confirmed") is True,
        "manual_send_confirmed must be true",
    )

    ready = initial_send._ready_message(ready_messages, route_id)
    initial_send._need(
        ready["candidate_id"] == candidate_id,
        "follow-up send receipt candidate/message mismatch",
    )
    message = ready["message"]
    initial_send._need(
        ready_messages.get("message_kind") == "FOLLOWUP"
        and message.get("message_kind") == "FOLLOWUP",
        "ready message bundle is not a follow-up draft",
    )
    initial_send._need(
        _positive_int(message.get("followup_number"), "message.followup_number")
        == followup_number,
        "follow-up number/message mismatch",
    )

    message_contact = str(message.get("public_contact", "")).strip()
    initial_send._need(
        canonical_contact_snapshot == message_contact,
        "follow-up canonical contact/message mismatch",
    )
    allowed_contacts = initial_send._allowed_specific_contacts(message_contact)
    initial_send._need(
        sent_to_contact in allowed_contacts,
        "follow-up contact is not a registered canonical contact option",
    )
    initial_send._validate_channel_contact(send_channel, sent_to_contact)

    expected_hash = ready["message_content_sha256_by_language"][
        sent_language
    ]
    initial_send._need(
        sent_content_sha256 == expected_hash,
        "follow-up content hash/message mismatch",
    )

    route_rows = [
        row for row in rows
        if str(row.get("route_id", "")).strip() == route_id
    ]
    initial_send._need(
        len(route_rows) == 1,
        f"outreach route not uniquely found: {route_id}",
    )
    target = route_rows[0]
    initial_send._need(
        str(target.get("candidate_id", "")).strip() == candidate_id,
        "follow-up candidate/outreach mismatch",
    )
    initial_send._need(
        str(target.get("outreach_status", "")).strip()
        == "SENT_AWAITING_RESPONSE",
        "follow-up route is not awaiting response",
    )
    initial_send._need(
        str(target.get("response_status", "")).strip() == "NO_RESPONSE",
        "follow-up route already carries a response",
    )

    plan = planner.plan(
        rows,
        policy_payload,
        as_of_date=sent_at.date().isoformat(),
    )
    route_plan = next(
        item for item in plan["routes"] if item["route_id"] == route_id
    )
    initial_send._need(
        route_plan["action"] == "FOLLOWUP_DUE",
        f"follow-up is not due under frozen policy: {route_plan['action']}",
    )
    initial_send._need(
        route_plan["followup_number"] == followup_number,
        "follow-up receipt number/planner mismatch",
    )
    initial_send._need(
        message.get("policy_due_date") == route_plan["due_date"],
        "follow-up message due-date/planner mismatch",
    )

    policy_freeze_time = datetime.fromisoformat(
        plan["policy_freeze_timestamp"]
    )
    initial_send._need(
        policy_freeze_time <= sent_at,
        "follow-up policy freeze timestamp occurs after follow-up send",
    )

    updated = [dict(row) for row in rows]
    updated_target = next(
        row for row in updated
        if str(row.get("route_id", "")).strip() == route_id
    )
    updated_target["followup_attempts_completed"] = str(followup_number)
    updated_target["last_followup_date"] = sent_at.date().isoformat()
    updated_target["last_followup_reference"] = sent_message_reference
    updated_target["next_action"] = "AWAIT_RESPONSE"
    note_parts = [
        part for part in (
            str(updated_target.get("notes", "")).strip(),
            f"followup_event_id={send_event_id}",
            f"followup_number={followup_number}",
            f"followup_channel={send_channel}",
            f"followup_language={sent_language}",
            f"followup_message_sha256={sent_content_sha256}",
            f"sender_identity_reference={sender_identity_reference}",
        )
        if part
    ]
    updated_target["notes"] = " | ".join(note_parts)

    manager_receipt = manager.validate(updated)
    event = {
        "schema_version": "SLK_PEDICULARIS_WAVE1_PERMISSION_FOLLOWUP_SEND_EVENT_V1",
        "status": "MANUAL_FOLLOWUP_SEND_EVENT_VALIDATED",
        "candidate_id": candidate_id,
        "route_id": route_id,
        "followup_number": followup_number,
        "send_event_id": send_event_id,
        "sent_at": sent_at.isoformat(),
        "send_channel": send_channel,
        "sent_language": sent_language,
        "canonical_contact_snapshot": canonical_contact_snapshot,
        "sent_to_contact": sent_to_contact,
        "sent_message_reference": sent_message_reference,
        "message_content_sha256": sent_content_sha256,
        "sender_identity_reference": sender_identity_reference,
        "policy_due_date": route_plan["due_date"],
        "followup_policy_freeze_commit": plan["policy_freeze_commit"],
        "outreach_status_after": "SENT_AWAITING_RESPONSE",
        "followup_attempts_completed_after": followup_number,
        "automatic_send_used": False,
        "manager_receipt_status": manager_receipt["status"],
        "claim_ceiling": (
            "MANUAL_FOLLOWUP_SEND_EVENT_ONLY_NO_RESPONSE_"
            "NO_PERMISSION_NO_FRESH_CONTEXT_NO_P0_SIGNAL"
        ),
    }
    return updated, event


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apply a manually sent, prospectively due WAVE1 permission follow-up receipt"
    )
    parser.add_argument("outreach_ledger_csv", type=Path)
    parser.add_argument("ready_followup_messages_json", type=Path)
    parser.add_argument("followup_send_receipt_json", type=Path)
    parser.add_argument("followup_policy_json", type=Path)
    parser.add_argument("--ledger-output", required=True, type=Path)
    parser.add_argument("--event-output", required=True, type=Path)
    args = parser.parse_args()

    rows = _read(args.outreach_ledger_csv)
    ready = json.loads(
        args.ready_followup_messages_json.read_text(encoding="utf-8")
    )
    receipt = json.loads(
        args.followup_send_receipt_json.read_text(encoding="utf-8")
    )
    policy = json.loads(
        args.followup_policy_json.read_text(encoding="utf-8")
    )
    updated, event = apply_followup_send_receipt(
        rows,
        ready,
        receipt,
        policy,
    )

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
