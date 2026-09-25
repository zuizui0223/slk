from __future__ import annotations

import argparse
import json
from pathlib import Path

SCHEMA = "SLK_PEDICULARIS_WAVE1_PERMISSION_FOLLOWUP_POLICY_V1"
PRODUCTION_STATUS = (
    "PEDICULARIS_WAVE1_PERMISSION_FOLLOWUP_POLICY_PROSPECTIVELY_FROZEN"
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
        and "REQUIRED_BEFORE_USE" not in text
        and text.lower() not in {"none", "null"},
        f"unresolved {label}",
    )
    return text


def _positive_int(value: object, label: str) -> int:
    _need(not isinstance(value, bool), f"{label} must be a positive integer")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be a positive integer") from exc
    _need(
        number.is_integer() and number > 0,
        f"{label} must be a positive integer",
    )
    return int(number)


def validate(payload: dict) -> dict:
    _need(payload.get("schema_version") == SCHEMA, "wrong follow-up policy schema")
    _need(
        payload.get("status") == "FROZEN_POLICY",
        "follow-up policy must be FROZEN_POLICY",
    )
    _need(
        payload.get("production_status") == PRODUCTION_STATUS,
        "wrong follow-up policy production status",
    )

    policy = payload.get("policy")
    _need(isinstance(policy, dict), "follow-up policy block missing")
    _need(
        policy.get("calendar_basis") == "CALENDAR_DAYS",
        "follow-up calendar basis changed",
    )
    offsets_raw = policy.get("followup_offsets_days")
    _need(
        isinstance(offsets_raw, list) and offsets_raw,
        "follow-up offsets must be a non-empty list",
    )
    offsets = [
        _positive_int(value, f"followup_offsets_days/{index}")
        for index, value in enumerate(offsets_raw)
    ]
    _need(
        offsets == sorted(set(offsets)),
        "follow-up offsets must be unique and strictly increasing",
    )
    escalation = _positive_int(
        policy.get("escalation_review_after_days"),
        "escalation_review_after_days",
    )
    _need(
        escalation > offsets[-1],
        "escalation review must occur after the last follow-up offset",
    )
    _need(
        policy.get("automatic_close_allowed") is False,
        "automatic closure after no response is forbidden",
    )
    _need(
        policy.get("response_receipt_preempts_followup") is True,
        "response receipt must preempt follow-up",
    )
    _need(
        policy.get("routing_response_preempts_same_route_followup") is True,
        "routing response must preempt same-route follow-up",
    )

    metadata = payload.get("freeze_metadata")
    _need(isinstance(metadata, dict), "follow-up freeze metadata missing")
    for key in (
        "slk_source_commit",
        "freeze_commit",
        "freeze_timestamp",
        "policy_rationale_reference",
    ):
        _filled(metadata.get(key), f"freeze_metadata.{key}")

    return {
        "schema_version": "SLK_PEDICULARIS_WAVE1_PERMISSION_FOLLOWUP_POLICY_RECEIPT_V1",
        "status": "FOLLOWUP_POLICY_VALIDATED",
        "followup_offsets_days": offsets,
        "followup_attempt_count": len(offsets),
        "escalation_review_after_days": escalation,
        "automatic_close_allowed": False,
        "response_receipt_preempts_followup": True,
        "routing_response_preempts_same_route_followup": True,
        "freeze_commit": metadata["freeze_commit"],
        "policy_rationale_reference": metadata["policy_rationale_reference"],
        "claim_ceiling": (
            "ADMINISTRATIVE_FOLLOWUP_TIMING_ONLY_NO_PERMISSION_"
            "NO_FRESH_CONTEXT_NO_P0_SIGNAL"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a prospectively frozen WAVE1 permission follow-up policy"
    )
    parser.add_argument("policy_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = validate(json.loads(args.policy_json.read_text(encoding="utf-8")))
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
