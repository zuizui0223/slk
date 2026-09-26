from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANAGER_PATH = ROOT / "scripts" / "manage_pedicularis_wave1_permission_outreach.py"
ROUTES = ROOT / "data" / "PEDICULARIS_WAVE1_PERMISSION_CONTACT_ROUTES_V1.csv"

_spec_manager = importlib.util.spec_from_file_location(
    "ped_outreach_manager",
    MANAGER_PATH,
)
manager = importlib.util.module_from_spec(_spec_manager)
assert _spec_manager.loader is not None
_spec_manager.loader.exec_module(manager)

RESPONSE_RECEIPT_SCHEMA = "SLK_PEDICULARIS_WAVE1_INCOMING_RESPONSE_RECEIPT_V1"
ALLOWED_RECEIVE_CHANNELS = {
    "EMAIL",
    "WEB_PORTAL",
    "LETTER",
    "PHONE_CALL",
    "IN_PERSON",
}
ALLOWED_CLASSIFICATIONS = {
    "ROUTING_RESPONSE_ONLY",
    "SUBSTANTIVE_RESPONSE_RECEIVED",
}
SITE_AUTHORIZING_ROUTE_TYPES = {
    "SITE_MANAGEMENT_ROUTING",
    "INSTITUTIONAL_SITE_ROUTING",
}


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


def _optional_text(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _aware_datetime(value: object, label: str) -> datetime:
    text = _filled(value, label)
    try:
        out = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} must be ISO 8601 datetime") from exc
    _need(out.tzinfo is not None, f"{label} must include timezone offset")
    return out


def _iso_date(value: object, label: str) -> date:
    text = _filled(value, label)
    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{label} must be ISO YYYY-MM-DD") from exc


def _is_sha256(value: str) -> bool:
    return (
        len(value) == 64
        and all(ch in "0123456789abcdef" for ch in value.lower())
    )


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _canonical_routes() -> dict[str, dict[str, str]]:
    with ROUTES.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {
        row["route_id"].strip(): row
        for row in rows
        if row["recovery_wave"].strip() == "WAVE1"
    }


def response_content_sha256(receipt: dict) -> str:
    attachments = receipt.get("attachments")
    _need(
        isinstance(attachments, list),
        "attachments must be a list",
    )
    normalized_attachments = []
    seen_attachment_refs: set[str] = set()
    for index, attachment in enumerate(attachments):
        _need(
            isinstance(attachment, dict),
            f"attachments/{index} must be an object",
        )
        reference = _filled(
            attachment.get("reference"),
            f"attachments/{index}/reference",
        )
        _need(
            reference not in seen_attachment_refs,
            f"duplicate attachment reference: {reference}",
        )
        seen_attachment_refs.add(reference)
        sha256 = _filled(
            attachment.get("sha256"),
            f"attachments/{index}/sha256",
        )
        _need(
            _is_sha256(sha256),
            f"attachments/{index}/sha256 must be sha256",
        )
        normalized_attachments.append(
            {
                "reference": reference,
                "sha256": sha256.lower(),
                "media_type": _optional_text(
                    attachment.get("media_type")
                ),
                "file_name": _optional_text(
                    attachment.get("file_name")
                ),
            }
        )

    payload = {
        "candidate_id": _filled(receipt.get("candidate_id"), "candidate_id"),
        "route_id": _filled(receipt.get("route_id"), "route_id"),
        "receive_channel": _filled(
            receipt.get("receive_channel"),
            "receive_channel",
        ),
        "responding_organization": _filled(
            receipt.get("responding_organization"),
            "responding_organization",
        ),
        "responding_contact": _filled(
            receipt.get("responding_contact"),
            "responding_contact",
        ),
        "response_subject": _optional_text(
            receipt.get("response_subject")
        ),
        "response_capture_text": _filled(
            receipt.get("response_capture_text"),
            "response_capture_text",
        ),
        "attachments": normalized_attachments,
    }
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _validate_classification(
    receipt: dict,
    *,
    received_at: datetime,
    recorded_at: datetime,
) -> tuple[str, dict]:
    classification = receipt.get("classification")
    _need(
        isinstance(classification, dict),
        "response classification must be an object",
    )
    response_status = _filled(
        classification.get("response_status"),
        "classification.response_status",
    )
    _need(
        response_status in ALLOWED_CLASSIFICATIONS,
        f"unregistered response classification: {response_status}",
    )
    reviewed_by = _filled(
        classification.get("reviewed_by"),
        "classification.reviewed_by",
    )
    review_date = _iso_date(
        classification.get("review_date"),
        "classification.review_date",
    )
    review_reference = _filled(
        classification.get("review_reference"),
        "classification.review_reference",
    )
    rationale = _filled(
        classification.get("rationale"),
        "classification.rationale",
    )
    _need(
        received_at.date() <= review_date <= recorded_at.date(),
        "response classification review date must fall between receipt and recording",
    )
    return response_status, {
        "reviewed_by": reviewed_by,
        "review_date": review_date.isoformat(),
        "review_reference": review_reference,
        "rationale": rationale,
    }


def apply_response_receipt(
    rows: list[dict[str, str]],
    response_receipt: dict,
) -> tuple[list[dict[str, str]], dict]:
    _need(
        response_receipt.get("schema_version") == RESPONSE_RECEIPT_SCHEMA,
        "wrong incoming-response receipt schema",
    )
    _need(
        response_receipt.get("status") == "INCOMING_RESPONSE_RECORDED",
        "incoming-response receipt is not filled",
    )

    candidate_id = _filled(
        response_receipt.get("candidate_id"),
        "candidate_id",
    )
    route_id = _filled(response_receipt.get("route_id"), "route_id")
    response_event_id = _filled(
        response_receipt.get("response_event_id"),
        "response_event_id",
    )
    received_at = _aware_datetime(
        response_receipt.get("received_at"),
        "received_at",
    )
    recorded_at = _aware_datetime(
        response_receipt.get("recorded_at"),
        "recorded_at",
    )
    _need(
        received_at <= recorded_at,
        "recorded_at cannot precede received_at",
    )
    receive_channel = _filled(
        response_receipt.get("receive_channel"),
        "receive_channel",
    )
    _need(
        receive_channel in ALLOWED_RECEIVE_CHANNELS,
        f"unregistered receive channel: {receive_channel}",
    )
    responding_organization = _filled(
        response_receipt.get("responding_organization"),
        "responding_organization",
    )
    responding_contact = _filled(
        response_receipt.get("responding_contact"),
        "responding_contact",
    )
    response_reference = _filled(
        response_receipt.get("response_reference"),
        "response_reference",
    )
    response_hash = response_content_sha256(response_receipt)
    supplied_hash = response_receipt.get("response_content_sha256")
    if supplied_hash not in (None, ""):
        _need(
            str(supplied_hash).strip() == response_hash,
            "incoming-response supplied hash does not match captured content",
        )

    response_status, classification = _validate_classification(
        response_receipt,
        received_at=received_at,
        recorded_at=recorded_at,
    )

    canonical = _canonical_routes()
    _need(route_id in canonical, f"response route is not canonical: {route_id}")
    route = canonical[route_id]
    _need(
        route["candidate_id"].strip() == candidate_id,
        "incoming response candidate/route mismatch",
    )
    _need(
        route["organization"].strip() == responding_organization,
        "incoming response organization/route mismatch",
    )
    route_type = route["route_type"].strip()

    routing_destination = response_receipt.get("routing_destination")
    if not isinstance(routing_destination, dict):
        routing_destination = {}
    routed_org = _optional_text(routing_destination.get("organization"))
    routed_contact = _optional_text(routing_destination.get("contact"))

    if response_status == "ROUTING_RESPONSE_ONLY":
        _need(
            bool(routed_org) and bool(routed_contact),
            "routing response requires destination organization/contact",
        )
        outreach_status_after = "ROUTED_TO_ANOTHER_AUTHORITY"
        next_action = "REGISTER_ROUTED_AUTHORITY_AND_SEND_NEW_INQUIRY"
    else:
        _need(
            route_type == "REGULATORY_ROUTING"
            or route_type in SITE_AUTHORIZING_ROUTE_TYPES,
            "routing-only route cannot be classified as substantive authorization response",
        )
        _need(
            not routed_org and not routed_contact,
            "substantive response cannot also carry routing destination",
        )
        outreach_status_after = "RESPONSE_RECEIVED"
        next_action = "AWAIT_OTHER_AUTHORIZING_RESPONSE"

    matches = [
        row
        for row in rows
        if str(row.get("route_id", "")).strip() == route_id
    ]
    _need(len(matches) == 1, f"outreach route not uniquely found: {route_id}")
    target = matches[0]
    _need(
        str(target.get("candidate_id", "")).strip() == candidate_id,
        "incoming response candidate/outreach mismatch",
    )
    _need(
        str(target.get("outreach_status", "")).strip()
        == "SENT_AWAITING_RESPONSE",
        "incoming response requires SENT_AWAITING_RESPONSE route",
    )
    _need(
        str(target.get("response_status", "")).strip() == "NO_RESPONSE",
        "outreach route already carries a response",
    )

    outreach_date = _iso_date(
        target.get("outreach_date"),
        f"outreach_date/{route_id}",
    )
    _need(
        received_at.date() >= outreach_date,
        "incoming response received before initial outreach",
    )

    last_followup_date_text = str(
        target.get("last_followup_date", "")
    ).strip()
    followup_preemption_violation = False
    if last_followup_date_text:
        last_followup_date = _iso_date(
            last_followup_date_text,
            f"last_followup_date/{route_id}",
        )
        followup_preemption_violation = (
            received_at.date() < last_followup_date
        )

    updated = [dict(row) for row in rows]
    updated_target = next(
        row
        for row in updated
        if str(row.get("route_id", "")).strip() == route_id
    )
    updated_target["outreach_status"] = outreach_status_after
    updated_target["response_status"] = response_status
    updated_target["response_date"] = received_at.date().isoformat()
    updated_target["response_received_at"] = received_at.isoformat()
    updated_target["response_reference"] = response_reference
    updated_target["response_event_id"] = response_event_id
    updated_target["response_receive_channel"] = receive_channel
    updated_target["response_content_sha256"] = response_hash
    updated_target["response_classification_review_reference"] = (
        classification["review_reference"]
    )
    updated_target["routed_to_organization"] = routed_org
    updated_target["routed_to_contact"] = routed_contact
    updated_target["next_action"] = next_action

    note_parts = [
        part
        for part in (
            str(updated_target.get("notes", "")).strip(),
            f"response_event_id={response_event_id}",
            f"response_channel={receive_channel}",
            f"response_sha256={response_hash}",
            f"responding_contact={responding_contact}",
            f"classification_reviewed_by={classification['reviewed_by']}",
            (
                "followup_preemption_violation=true"
                if followup_preemption_violation
                else ""
            ),
        )
        if part
    ]
    updated_target["notes"] = " | ".join(note_parts)

    manager_receipt = manager.validate(updated)
    progress = manager_receipt["candidate_progress"][candidate_id]
    if (
        response_status == "SUBSTANTIVE_RESPONSE_RECEIVED"
        and progress["ready_to_build_permission_response_bundle"]
    ):
        updated_target["next_action"] = "BUILD_PERMISSION_RESPONSE_DRAFT"
        manager_receipt = manager.validate(updated)
        progress = manager_receipt["candidate_progress"][candidate_id]

    event_receipt = {
        "schema_version": "SLK_PEDICULARIS_WAVE1_INCOMING_RESPONSE_EVENT_V1",
        "status": "INCOMING_RESPONSE_EVENT_VALIDATED",
        "candidate_id": candidate_id,
        "route_id": route_id,
        "route_type": route_type,
        "response_event_id": response_event_id,
        "received_at": received_at.isoformat(),
        "recorded_at": recorded_at.isoformat(),
        "receive_channel": receive_channel,
        "responding_organization": responding_organization,
        "responding_contact": responding_contact,
        "response_reference": response_reference,
        "response_content_sha256": response_hash,
        "attachment_count": len(response_receipt.get("attachments", [])),
        "attachment_hashes": [
            {
                "reference": attachment["reference"],
                "sha256": attachment["sha256"].lower(),
            }
            for attachment in response_receipt.get("attachments", [])
        ],
        "response_status": response_status,
        "classification": classification,
        "routing_destination": (
            {
                "organization": routed_org,
                "contact": routed_contact,
            }
            if response_status == "ROUTING_RESPONSE_ONLY"
            else None
        ),
        "outreach_status_after": outreach_status_after,
        "next_action_after": updated_target["next_action"],
        "followup_preemption_violation": followup_preemption_violation,
        "protocol_deviation_requires_review": followup_preemption_violation,
        "candidate_ready_to_build_permission_response_bundle": progress[
            "ready_to_build_permission_response_bundle"
        ],
        "manager_receipt_status": manager_receipt["status"],
        "claim_ceiling": (
            "INCOMING_RESPONSE_PROVENANCE_AND_CLASSIFICATION_ONLY_"
            "NO_ACTIVITY_PERMISSION_DECISION_NO_FRESH_CONTEXT_NO_P0_RESULT"
        ),
    }
    return updated, event_receipt


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apply an audited incoming WAVE1 permission response to the outreach ledger"
    )
    parser.add_argument("outreach_ledger_csv", type=Path)
    parser.add_argument("incoming_response_receipt_json", type=Path)
    parser.add_argument("--ledger-output", required=True, type=Path)
    parser.add_argument("--event-output", required=True, type=Path)
    args = parser.parse_args()

    rows = _read_csv(args.outreach_ledger_csv)
    receipt = json.loads(
        args.incoming_response_receipt_json.read_text(encoding="utf-8")
    )
    updated, event = apply_response_receipt(rows, receipt)

    fieldnames = list(updated[0].keys())
    with args.ledger_output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated)

    args.event_output.write_text(
        json.dumps(event, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
