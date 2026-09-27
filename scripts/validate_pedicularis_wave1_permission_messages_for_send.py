from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import datetime
from pathlib import Path

SCHEMA = "SLK_PEDICULARIS_WAVE1_PERMISSION_MESSAGE_DRAFTS_V1"
REVIEW_SCHEMA = "SLK_PEDICULARIS_WAVE1_PERMISSION_MESSAGE_REVIEW_V1"
REVIEW_CHECK_FIELDS = {
    "requester_identity_verified",
    "institution_and_reply_contact_verified",
    "candidate_and_locator_wording_verified",
    "organization_and_contact_route_verified",
    "activity_A_F_wording_verified",
    "no_permission_or_biological_claim_verified",
    "manual_send_only_acknowledged",
}
ALLOWED_INPUT_STATUS = {
    "DRAFT_NOT_SENT",
    "DRAFT_REQUESTER_FILLED_AWAITING_HUMAN_REVIEW",
    "READY_FOR_MANUAL_SEND",
}


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


def _aware_datetime(value: object, label: str) -> datetime:
    text = _filled(value, label)
    try:
        out = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} must be ISO 8601 datetime") from exc
    _need(out.tzinfo is not None, f"{label} must include timezone offset")
    return out


def human_review_receipt_sha256(receipt: dict) -> str:
    payload = {
        "schema_version": _filled(
            receipt.get("schema_version"),
            "review.schema_version",
        ),
        "status": _filled(receipt.get("status"), "review.status"),
        "candidate_id": _filled(
            receipt.get("candidate_id"),
            "review.candidate_id",
        ),
        "review_bundle_id": _filled(
            receipt.get("review_bundle_id"),
            "review.review_bundle_id",
        ),
        "reviewer_name": _filled(
            receipt.get("reviewer_name"),
            "review.reviewer_name",
        ),
        "reviewer_reference": _filled(
            receipt.get("reviewer_reference"),
            "review.reviewer_reference",
        ),
        "reviewed_at": _filled(
            receipt.get("reviewed_at"),
            "review.reviewed_at",
        ),
        "route_reviews": receipt.get("route_reviews"),
        "review_policy": receipt.get("review_policy"),
        "privacy_policy": receipt.get("privacy_policy"),
    }
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _validate_review_receipt(
    payload: dict,
    review_receipt: dict | None,
    messages: list[dict],
) -> dict:
    _need(
        isinstance(review_receipt, dict),
        "human review approval requires review receipt",
    )
    _need(
        review_receipt.get("schema_version") == REVIEW_SCHEMA,
        "wrong permission message-review schema",
    )
    _need(
        review_receipt.get("status") == "HUMAN_REVIEW_APPROVED",
        "permission message review is not HUMAN_REVIEW_APPROVED",
    )

    candidate = payload.get("candidate")
    _need(isinstance(candidate, dict), "permission message candidate missing")
    candidate_id = _filled(candidate.get("candidate_id"), "candidate_id")
    _need(
        review_receipt.get("candidate_id") == candidate_id,
        "permission message review candidate mismatch",
    )

    review_bundle_id = _filled(
        review_receipt.get("review_bundle_id"),
        "review_bundle_id",
    )
    reviewer_name = _filled(
        review_receipt.get("reviewer_name"),
        "reviewer_name",
    )
    reviewer_reference = _filled(
        review_receipt.get("reviewer_reference"),
        "reviewer_reference",
    )
    reviewed_at = _aware_datetime(
        review_receipt.get("reviewed_at"),
        "reviewed_at",
    )
    _need(
        review_receipt.get("privacy_policy")
        == "FILLED_REVIEW_LOCAL_GITIGNORED_DO_NOT_COMMIT",
        "permission message review privacy policy changed",
    )
    policy = review_receipt.get("review_policy")
    _need(isinstance(policy, dict), "permission message review policy missing")
    for key in (
        "bilingual_message_hash_must_match",
        "every_registered_route_must_be_reviewed",
        "every_check_must_pass",
        "route_approval_required",
    ):
        _need(
            policy.get(key) is True,
            f"permission message review policy disabled: {key}",
        )
    _need(
        policy.get("automatic_send_allowed") is False,
        "permission message review cannot enable automatic send",
    )

    route_reviews = review_receipt.get("route_reviews")
    _need(
        isinstance(route_reviews, list) and route_reviews,
        "permission message route reviews missing",
    )
    by_route: dict[str, dict] = {}
    for row in route_reviews:
        _need(isinstance(row, dict), "permission message route review must be object")
        route_id = _filled(row.get("route_id"), "review route_id")
        _need(route_id not in by_route, f"duplicate message review route: {route_id}")
        by_route[route_id] = row

    message_routes = {
        _filled(message.get("route_id"), "message route_id")
        for message in messages
    }
    _need(
        set(by_route) == message_routes,
        "permission message review route inventory mismatch",
    )

    reviewed_routes = {}
    for message in messages:
        route_id = _filled(message.get("route_id"), "message route_id")
        row = by_route[route_id]
        expected_hash = message_content_sha256(
            message,
            language="BILINGUAL",
        )
        _need(
            row.get("reviewed_message_sha256_bilingual") == expected_hash,
            f"human review bilingual hash mismatch: {route_id}",
        )
        checks = row.get("checks")
        _need(
            isinstance(checks, dict)
            and set(checks) == REVIEW_CHECK_FIELDS,
            f"human review check inventory mismatch: {route_id}",
        )
        _need(
            all(checks[field] is True for field in REVIEW_CHECK_FIELDS),
            f"human review checks not all passed: {route_id}",
        )
        _need(
            row.get("approved_for_manual_send") is True,
            f"route not approved for manual send: {route_id}",
        )
        reviewed_routes[route_id] = {
            "reviewed_message_sha256_bilingual": expected_hash,
            "approved_for_manual_send": True,
        }

    validated = {
        "schema_version": REVIEW_SCHEMA,
        "status": "HUMAN_REVIEW_APPROVED",
        "candidate_id": candidate_id,
        "review_bundle_id": review_bundle_id,
        "reviewer_name": reviewer_name,
        "reviewer_reference": reviewer_reference,
        "reviewed_at": reviewed_at.isoformat(),
        "routes": reviewed_routes,
        "review_policy": copy.deepcopy(policy),
        "privacy_policy": review_receipt["privacy_policy"],
    }
    validated["review_receipt_sha256"] = human_review_receipt_sha256(
        review_receipt
    )
    return validated


def message_content_sha256(
    message: dict,
    *,
    language: str = "BILINGUAL",
) -> str:
    if language not in {"CN", "EN", "BILINGUAL"}:
        raise ValueError(f"unsupported message hash language: {language}")
    payload = {
        "route_id": _filled(message.get("route_id"), "route_id"),
        "organization": _filled(message.get("organization"), "organization"),
        "public_contact": _filled(message.get("public_contact"), "public_contact"),
        "language": language,
    }
    if language in {"CN", "BILINGUAL"}:
        payload["subject_cn"] = _filled(message.get("subject_cn"), "subject_cn")
        payload["body_cn"] = _filled(message.get("body_cn"), "body_cn")
    if language in {"EN", "BILINGUAL"}:
        payload["subject_en"] = _filled(message.get("subject_en"), "subject_en")
        payload["body_en"] = _filled(message.get("body_en"), "body_en")
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def validate_and_prepare(
    payload: dict,
    *,
    human_review_approved: bool,
    review_receipt: dict | None = None,
) -> dict:
    _need(payload.get("schema_version") == SCHEMA, "wrong permission message-draft schema")
    _need(
        payload.get("status") in ALLOWED_INPUT_STATUS,
        "permission message draft status is not preparable",
    )
    messages = payload.get("messages")
    _need(isinstance(messages, list) and messages, "permission message drafts missing")

    validated_review = None
    if human_review_approved:
        validated_review = _validate_review_receipt(
            payload,
            review_receipt,
            messages,
        )

    out = copy.deepcopy(payload)
    for index, message in enumerate(out["messages"]):
        _need(
            message.get("status") in {
                "DRAFT_NOT_SENT",
                "DRAFT_REQUESTER_FILLED_AWAITING_HUMAN_REVIEW",
                "READY_FOR_MANUAL_SEND",
            },
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
        if validated_review is not None:
            route_id = _filled(message.get("route_id"), f"route_id/{index}")
            guard["human_review_bundle_id"] = validated_review[
                "review_bundle_id"
            ]
            guard["human_review_receipt_sha256"] = validated_review[
                "review_receipt_sha256"
            ]
            guard["human_review_reviewer_name"] = validated_review[
                "reviewer_name"
            ]
            guard["human_review_reference"] = validated_review[
                "reviewer_reference"
            ]
            guard["human_reviewed_at"] = validated_review["reviewed_at"]
            guard["reviewed_message_sha256_bilingual"] = validated_review[
                "routes"
            ][route_id]["reviewed_message_sha256_bilingual"]
        message["message_content_sha256_cn"] = message_content_sha256(
            message,
            language="CN",
        )
        message["message_content_sha256_en"] = message_content_sha256(
            message,
            language="EN",
        )
        message["message_content_sha256_bilingual"] = message_content_sha256(
            message,
            language="BILINGUAL",
        )
        message["message_content_sha256"] = message[
            "message_content_sha256_bilingual"
        ]
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
    out["human_review_receipt"] = validated_review
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate requester-completed WAVE1 permission messages for manual sending"
    )
    parser.add_argument("message_drafts_json", type=Path)
    parser.add_argument("--human-review-approved", action="store_true")
    parser.add_argument("--review-receipt-json", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    payload = json.loads(args.message_drafts_json.read_text(encoding="utf-8"))
    review_receipt = (
        json.loads(args.review_receipt_json.read_text(encoding="utf-8"))
        if args.review_receipt_json
        else None
    )
    result = validate_and_prepare(
        payload,
        human_review_approved=args.human_review_approved,
        review_receipt=review_receipt,
    )
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
