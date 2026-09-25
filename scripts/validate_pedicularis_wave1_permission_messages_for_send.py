from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

SCHEMA = "SLK_PEDICULARIS_WAVE1_PERMISSION_MESSAGE_DRAFTS_V1"
ALLOWED_INPUT_STATUS = {"DRAFT_NOT_SENT", "READY_FOR_MANUAL_SEND"}


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _filled(value: object, label: str) -> str:
    text = str(value).strip()
    _need(
        bool(text)
        and "REQUIRED_BEFORE_SEND" not in text
        and text.lower() != "none",
        f"unfilled {label}",
    )
    return text


def _message_content_sha256(message: dict) -> str:
    payload = {
        "route_id": _filled(message.get("route_id"), "route_id"),
        "organization": _filled(message.get("organization"), "organization"),
        "public_contact": _filled(message.get("public_contact"), "public_contact"),
        "subject_cn": _filled(message.get("subject_cn"), "subject_cn"),
        "body_cn": _filled(message.get("body_cn"), "body_cn"),
        "subject_en": _filled(message.get("subject_en"), "subject_en"),
        "body_en": _filled(message.get("body_en"), "body_en"),
    }
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def validate_and_prepare(payload: dict, *, human_review_approved: bool) -> dict:
    _need(payload.get("schema_version") == SCHEMA, "wrong permission message-draft schema")
    _need(
        payload.get("status") in ALLOWED_INPUT_STATUS,
        "permission message draft status is not preparable",
    )
    messages = payload.get("messages")
    _need(isinstance(messages, list) and messages, "permission message drafts missing")

    out = copy.deepcopy(payload)
    for index, message in enumerate(out["messages"]):
        _need(
            message.get("status") in {"DRAFT_NOT_SENT", "READY_FOR_MANUAL_SEND"},
            f"message status invalid: {index}",
        )
        guard = message.get("send_guard")
        _need(isinstance(guard, dict), f"message send_guard missing: {index}")
        _need(
            guard.get("automatic_send_allowed") is False,
            f"automatic send must remain disabled: {index}",
        )

        body_cn = _filled(message.get("body_cn"), f"body_cn/{index}")
        body_en = _filled(message.get("body_en"), f"body_en/{index}")
        for label, body in (("body_cn", body_cn), ("body_en", body_en)):
            _need(
                "REQUIRED_BEFORE_SEND" not in body,
                f"{label} still contains requester placeholders: {index}",
            )

        guard["requester_identity_filled"] = True
        guard["institution_filled"] = True
        guard["reply_contact_filled"] = True
        guard["human_review_required"] = True
        guard["human_review_approved"] = bool(human_review_approved)
        guard["automatic_send_allowed"] = False
        message["message_content_sha256"] = _message_content_sha256(
            message
        )
        message["status"] = (
            "READY_FOR_MANUAL_SEND"
            if human_review_approved
            else "DRAFT_NOT_SENT"
        )

    out["status"] = (
        "READY_FOR_MANUAL_SEND"
        if human_review_approved
        else "DRAFT_NOT_SENT"
    )
    out["send_policy"] = {
        "manual_send_only": True,
        "automatic_send_allowed": False,
        "human_review_approved": bool(human_review_approved),
    }
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate requester-completed WAVE1 permission messages for manual sending"
    )
    parser.add_argument("message_drafts_json", type=Path)
    parser.add_argument("--human-review-approved", action="store_true")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    payload = json.loads(args.message_drafts_json.read_text(encoding="utf-8"))
    result = validate_and_prepare(
        payload,
        human_review_approved=args.human_review_approved,
    )
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
