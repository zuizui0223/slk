from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUARD_PATH = (
    ROOT / "scripts" / "validate_pedicularis_wave1_permission_messages_for_send.py"
)

_spec = importlib.util.spec_from_file_location("ped_permission_message_guard", GUARD_PATH)
guard = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(guard)

MESSAGE_SCHEMA = "SLK_PEDICULARIS_WAVE1_PERMISSION_MESSAGE_DRAFTS_V1"
REVIEW_SCHEMA = "SLK_PEDICULARIS_WAVE1_PERMISSION_MESSAGE_REVIEW_V1"
ALLOWED_MESSAGE_STATUSES = {
    "DRAFT_REQUESTER_FILLED_AWAITING_HUMAN_REVIEW",
    "DRAFT_NOT_SENT",
}
CHECK_FIELDS = (
    "requester_identity_verified",
    "institution_and_reply_contact_verified",
    "candidate_and_locator_wording_verified",
    "organization_and_contact_route_verified",
    "activity_A_F_wording_verified",
    "no_permission_or_biological_claim_verified",
    "manual_send_only_acknowledged",
)


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _filled(value: object, label: str) -> str:
    if value is None:
        raise ValueError(f"unresolved {label}")
    text = str(value).strip()
    _need(
        bool(text)
        and "REQUIRED_BEFORE_SEND" not in text
        and text.lower() not in {"none", "null"},
        f"unresolved {label}",
    )
    return text


def build_review_draft(message_payload: dict) -> dict:
    _need(
        message_payload.get("schema_version") == MESSAGE_SCHEMA,
        "wrong permission message-draft schema",
    )
    _need(
        message_payload.get("status") in ALLOWED_MESSAGE_STATUSES,
        "message bundle is not requester-filled review input",
    )
    candidate = message_payload.get("candidate")
    _need(isinstance(candidate, dict), "permission message candidate missing")
    candidate_id = _filled(candidate.get("candidate_id"), "candidate_id")

    messages = message_payload.get("messages")
    _need(
        isinstance(messages, list) and messages,
        "permission message drafts missing",
    )
    route_ids = []
    route_reviews = []
    for index, message in enumerate(messages):
        _need(isinstance(message, dict), f"message must be object: {index}")
        route_id = _filled(message.get("route_id"), f"route_id/{index}")
        _need(route_id not in route_ids, f"duplicate message route_id: {route_id}")
        route_ids.append(route_id)
        _filled(message.get("body_cn"), f"body_cn/{route_id}")
        _filled(message.get("body_en"), f"body_en/{route_id}")
        bilingual_hash = guard.message_content_sha256(
            message,
            language="BILINGUAL",
        )
        route_reviews.append(
            {
                "route_id": route_id,
                "reviewed_message_sha256_bilingual": bilingual_hash,
                "checks": {field: False for field in CHECK_FIELDS},
                "approved_for_manual_send": False,
                "route_review_notes": "",
            }
        )

    return {
        "schema_version": REVIEW_SCHEMA,
        "status": "DRAFT_REVIEW_NOT_APPROVED",
        "candidate_id": candidate_id,
        "review_bundle_id": "REQUIRED_BEFORE_LOCAL_USE",
        "reviewer_name": "REQUIRED_BEFORE_LOCAL_USE",
        "reviewer_reference": "REQUIRED_BEFORE_LOCAL_USE",
        "reviewed_at": "REQUIRED_BEFORE_LOCAL_USE",
        "route_reviews": route_reviews,
        "review_policy": {
            "bilingual_message_hash_must_match": True,
            "every_registered_route_must_be_reviewed": True,
            "every_check_must_pass": True,
            "route_approval_required": True,
            "automatic_send_allowed": False,
        },
        "privacy_policy": "FILLED_REVIEW_LOCAL_GITIGNORED_DO_NOT_COMMIT",
        "next_action": (
            "Fill reviewer metadata; verify every route against its bilingual hash; "
            "set every review check and approved_for_manual_send=true only after human "
            "review; then set status=HUMAN_REVIEW_APPROVED."
        ),
        "claim_ceiling": (
            "HUMAN_REVIEW_DRAFT_ONLY_NO_CONTACT_EXECUTED_NO_PERMISSION_"
            "NO_FRESH_CONTEXT"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a local human-review receipt draft for WAVE1 permission messages"
    )
    parser.add_argument("requester_filled_messages_json", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    payload = json.loads(
        args.requester_filled_messages_json.read_text(encoding="utf-8")
    )
    result = build_review_draft(payload)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
