from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path

MESSAGE_SCHEMA = "SLK_PEDICULARIS_WAVE1_PERMISSION_MESSAGE_DRAFTS_V1"
PROFILE_SCHEMA = "SLK_PEDICULARIS_PERMISSION_REQUESTER_PROFILE_V1"
MESSAGE_INPUT_STATUS = "DRAFT_NOT_SENT"
PROFILE_STATUS = "LOCAL_PROFILE_FILLED"
OUTPUT_STATUS = "DRAFT_REQUESTER_FILLED_AWAITING_HUMAN_REVIEW"

PLACEHOLDERS = {
    "requester_name": "REQUIRED_BEFORE_SEND_NAME",
    "institution": "REQUIRED_BEFORE_SEND_INSTITUTION",
    "contact_email": "REQUIRED_BEFORE_SEND_EMAIL",
}

EMAIL_RE = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
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
        and "REQUIRED_BEFORE_LOCAL_USE" not in text
        and "REQUIRED_BEFORE_SEND" not in text
        and text.lower() not in {"none", "null"},
        f"unresolved {label}",
    )
    return text


def validate_profile(profile: dict) -> dict[str, str]:
    _need(
        profile.get("schema_version") == PROFILE_SCHEMA,
        "wrong requester-profile schema",
    )
    _need(
        profile.get("status") == PROFILE_STATUS,
        "requester profile is not LOCAL_PROFILE_FILLED",
    )
    name = _filled(profile.get("requester_name"), "requester_name")
    institution = _filled(profile.get("institution"), "institution")
    email = _filled(profile.get("contact_email"), "contact_email")
    _need(
        EMAIL_RE.fullmatch(email) is not None,
        "contact_email must be a valid email address",
    )
    reference = _filled(
        profile.get("profile_reference"),
        "profile_reference",
    )
    _need(
        profile.get("privacy_policy")
        == "FILLED_PROFILE_LOCAL_GITIGNORED_DO_NOT_COMMIT",
        "requester profile privacy policy changed",
    )
    return {
        "requester_name": name,
        "institution": institution,
        "contact_email": email,
        "profile_reference": reference,
    }


def compile_profile(message_payload: dict, profile: dict) -> dict:
    _need(
        message_payload.get("schema_version") == MESSAGE_SCHEMA,
        "wrong permission message-draft schema",
    )
    _need(
        message_payload.get("status") == MESSAGE_INPUT_STATUS,
        "requester profile compiler requires DRAFT_NOT_SENT messages",
    )
    values = validate_profile(profile)
    messages = message_payload.get("messages")
    _need(
        isinstance(messages, list) and messages,
        "permission message drafts missing",
    )

    out = copy.deepcopy(message_payload)
    for index, message in enumerate(out["messages"]):
        _need(
            message.get("status") == MESSAGE_INPUT_STATUS,
            f"message is not DRAFT_NOT_SENT: {index}",
        )
        guard = message.get("send_guard")
        _need(
            isinstance(guard, dict),
            f"message send_guard missing: {index}",
        )
        _need(
            guard.get("automatic_send_allowed") is False,
            f"automatic send must remain disabled: {index}",
        )

        for body_key in ("body_cn", "body_en"):
            body = str(message.get(body_key, ""))
            for field, token in PLACEHOLDERS.items():
                _need(
                    body.count(token) == 1,
                    f"{body_key} must contain exactly one {token}: {index}",
                )
                body = body.replace(token, values[field])
            _need(
                "REQUIRED_BEFORE_SEND" not in body,
                f"{body_key} still contains send placeholders: {index}",
            )
            message[body_key] = body

        guard["requester_identity_filled"] = True
        guard["institution_filled"] = True
        guard["reply_contact_filled"] = True
        guard["human_review_required"] = True
        guard["human_review_approved"] = False
        guard["automatic_send_allowed"] = False
        message["status"] = OUTPUT_STATUS

    out["status"] = OUTPUT_STATUS
    out["requester_profile_reference"] = values["profile_reference"]
    out["send_policy"] = {
        "manual_send_only": True,
        "automatic_send_allowed": False,
        "human_review_approved": False,
    }
    out["claim_ceiling"] = (
        "REQUESTER_FILLED_MESSAGE_DRAFTS_ONLY_AWAITING_HUMAN_REVIEW_"
        "NO_CONTACT_EXECUTED_NO_PERMISSION_NO_FRESH_CONTEXT"
    )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fill WAVE1 permission message drafts from a local requester profile"
    )
    parser.add_argument("message_drafts_json", type=Path)
    parser.add_argument("requester_profile_json", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    messages = json.loads(
        args.message_drafts_json.read_text(encoding="utf-8")
    )
    profile = json.loads(
        args.requester_profile_json.read_text(encoding="utf-8")
    )
    result = compile_profile(messages, profile)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
