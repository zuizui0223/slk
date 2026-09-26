from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

try:
    from scripts.manage_pedicularis_wave1_permission_outreach import (
        validate as validate_outreach,
    )
    from scripts.validate_pedicularis_wave1_permission_followup_policy import (
        validate as validate_followup_policy,
    )
    from scripts.validate_pedicularis_wave1_permission_messages_for_send import (
        message_content_sha256,
    )
except ImportError:
    from manage_pedicularis_wave1_permission_outreach import (
        validate as validate_outreach,
    )
    from validate_pedicularis_wave1_permission_followup_policy import (
        validate as validate_followup_policy,
    )
    from validate_pedicularis_wave1_permission_messages_for_send import (
        message_content_sha256,
    )


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = (
    ROOT / "data"
    / "PEDICULARIS_WAVE1_PERMISSION_OUTREACH_LEDGER_TEMPLATE_V1.csv"
)
MESSAGE_SCHEMA = "SLK_PEDICULARIS_WAVE1_PERMISSION_MESSAGE_DRAFTS_V1"


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _candidate_ready_messages(payload: dict) -> tuple[str, dict[str, dict]]:
    _need(
        payload.get("schema_version") == MESSAGE_SCHEMA,
        "wrong permission message bundle schema",
    )
    _need(
        payload.get("status") == "READY_FOR_MANUAL_SEND",
        "permission message bundle is not READY_FOR_MANUAL_SEND",
    )
    policy = payload.get("send_policy")
    _need(isinstance(policy, dict), "permission message send_policy missing")
    _need(
        policy.get("manual_send_only") is True,
        "permission messages must remain manual-send only",
    )
    _need(
        policy.get("automatic_send_allowed") is False,
        "automatic permission-message sending is forbidden",
    )
    _need(
        policy.get("human_review_approved") is True,
        "permission message human review is not approved",
    )

    candidate = payload.get("candidate")
    _need(isinstance(candidate, dict), "permission message candidate missing")
    candidate_id = str(candidate.get("candidate_id", "")).strip()
    _need(bool(candidate_id), "permission message candidate_id missing")

    messages = payload.get("messages")
    _need(isinstance(messages, list) and messages, "permission messages missing")
    by_route: dict[str, dict] = {}
    for message in messages:
        _need(isinstance(message, dict), "permission message must be an object")
        route_id = str(message.get("route_id", "")).strip()
        _need(bool(route_id), "permission message route_id missing")
        _need(route_id not in by_route, f"duplicate permission message route: {route_id}")
        _need(
            message.get("status") == "READY_FOR_MANUAL_SEND",
            f"route message is not ready for manual send: {route_id}",
        )
        guard = message.get("send_guard")
        _need(isinstance(guard, dict), f"route send_guard missing: {route_id}")
        _need(
            guard.get("human_review_approved") is True,
            f"route human review missing: {route_id}",
        )
        _need(
            guard.get("automatic_send_allowed") is False,
            f"route automatic send must remain disabled: {route_id}",
        )
        digest = message_content_sha256(message)
        _need(
            message.get("message_content_sha256") == digest,
            f"route reviewed-message hash mismatch: {route_id}",
        )
        by_route[route_id] = message
    return candidate_id, by_route


def audit(
    outreach_rows: list[dict[str, str]],
    *,
    followup_policy: dict | None = None,
    ready_message_payloads: list[dict] | None = None,
) -> dict:
    outreach_receipt = validate_outreach(outreach_rows)

    frozen_followup = None
    followup_state = "NOT_PROVIDED"
    if followup_policy is not None:
        frozen_followup = validate_followup_policy(followup_policy)
        followup_state = "FROZEN_AND_VALIDATED"

    ready_message_payloads = ready_message_payloads or []
    ready_by_candidate: dict[str, dict[str, dict]] = {}
    for payload in ready_message_payloads:
        candidate_id, messages = _candidate_ready_messages(payload)
        _need(
            candidate_id not in ready_by_candidate,
            f"duplicate ready-message bundle for candidate: {candidate_id}",
        )
        ready_by_candidate[candidate_id] = messages

    progress = outreach_receipt["candidate_progress"]
    route_results: list[dict] = []
    status_counts: dict[str, int] = {}

    for row in outreach_rows:
        candidate_id = str(row.get("candidate_id", "")).strip()
        route_id = str(row.get("route_id", "")).strip()
        outreach_status = str(row.get("outreach_status", "")).strip()
        response_status = str(row.get("response_status", "")).strip()
        blockers: list[str] = []
        administrative_state = "UNKNOWN"

        if outreach_status == "NOT_SENT":
            if frozen_followup is None:
                blockers.append("FOLLOWUP_POLICY_NOT_FROZEN")
            if route_id not in ready_by_candidate.get(candidate_id, {}):
                blockers.append("HUMAN_REVIEWED_MESSAGE_NOT_READY")
            if blockers:
                administrative_state = "BLOCKED_BEFORE_FIRST_SEND"
            else:
                administrative_state = "READY_FOR_MANUAL_SEND"
        elif outreach_status == "SENT_AWAITING_RESPONSE":
            administrative_state = "AWAITING_RESPONSE_OR_FOLLOWUP"
        elif outreach_status == "ROUTED_TO_ANOTHER_AUTHORITY":
            administrative_state = "ROUTING_DESTINATION_REQUIRES_CANONICAL_REGISTRATION"
        elif outreach_status == "RESPONSE_RECEIVED":
            if progress[candidate_id][
                "ready_to_build_permission_response_bundle"
            ]:
                administrative_state = "READY_TO_BUILD_PERMISSION_RESPONSE_DRAFT"
            else:
                administrative_state = "AWAITING_OTHER_AUTHORIZING_RESPONSE"
        elif outreach_status == "CLOSED_NO_ACTION":
            administrative_state = "CLOSED_NO_ACTION"
        else:
            raise ValueError(
                f"unsupported outreach state after validation: {route_id}/{outreach_status}"
            )

        status_counts[administrative_state] = (
            status_counts.get(administrative_state, 0) + 1
        )
        route_results.append(
            {
                "candidate_id": candidate_id,
                "route_id": route_id,
                "route_type": row["route_type"],
                "outreach_status": outreach_status,
                "response_status": response_status,
                "administrative_state": administrative_state,
                "blockers": blockers,
                "manual_send_only": True,
                "automatic_send_allowed": False,
            }
        )

    candidate_results: dict[str, dict] = {}
    for candidate_id in sorted(progress):
        rows = [r for r in route_results if r["candidate_id"] == candidate_id]
        candidate_results[candidate_id] = {
            "route_count": len(rows),
            "ready_for_manual_send_count": sum(
                r["administrative_state"] == "READY_FOR_MANUAL_SEND"
                for r in rows
            ),
            "blocked_before_first_send_count": sum(
                r["administrative_state"] == "BLOCKED_BEFORE_FIRST_SEND"
                for r in rows
            ),
            "awaiting_response_or_followup_count": sum(
                r["administrative_state"] == "AWAITING_RESPONSE_OR_FOLLOWUP"
                for r in rows
            ),
            "ready_to_build_permission_response_bundle": progress[
                candidate_id
            ]["ready_to_build_permission_response_bundle"],
            "canonical_route_update_required": progress[candidate_id][
                "canonical_route_update_required"
            ],
        }

    if status_counts.get("READY_TO_BUILD_PERMISSION_RESPONSE_DRAFT", 0):
        next_action = "BUILD_READY_PERMISSION_RESPONSE_DRAFTS"
    elif status_counts.get("READY_FOR_MANUAL_SEND", 0):
        next_action = "MANUALLY_SEND_READY_ROUTES"
    elif (
        status_counts.get("BLOCKED_BEFORE_FIRST_SEND", 0)
        and frozen_followup is None
    ):
        next_action = "FREEZE_FOLLOWUP_POLICY_BEFORE_FIRST_SEND"
    elif status_counts.get("BLOCKED_BEFORE_FIRST_SEND", 0):
        next_action = "COMPLETE_AND_HUMAN_REVIEW_PERMISSION_MESSAGES"
    elif status_counts.get("AWAITING_RESPONSE_OR_FOLLOWUP", 0):
        next_action = "USE_FROZEN_FOLLOWUP_PLANNER_OR_RECORD_RESPONSE"
    elif status_counts.get(
        "ROUTING_DESTINATION_REQUIRES_CANONICAL_REGISTRATION", 0
    ):
        next_action = "REGISTER_ROUTED_AUTHORITIES_BEFORE_NEW_INQUIRY"
    else:
        next_action = "NO_AUTOMATIC_ACTION_REVIEW_OUTREACH_STATE"

    all_routes_send_ready = bool(route_results) and all(
        r["administrative_state"] == "READY_FOR_MANUAL_SEND"
        for r in route_results
    )

    return {
        "schema_version": "SLK_PEDICULARIS_WAVE1_OUTREACH_READINESS_RECEIPT_V1",
        "status": "OUTREACH_READINESS_AUDITED",
        "followup_policy_state": followup_state,
        "followup_policy_freeze_commit": (
            frozen_followup["freeze_commit"] if frozen_followup else None
        ),
        "ready_message_candidate_count": len(ready_by_candidate),
        "route_count": len(route_results),
        "status_counts": dict(sorted(status_counts.items())),
        "all_routes_ready_for_manual_send": all_routes_send_ready,
        "candidate_results": candidate_results,
        "routes": route_results,
        "next_action": next_action,
        "firewall": {
            "creates_new_permission_gate": False,
            "automatic_send_allowed": False,
            "silence_interpreted_as_permission": False,
            "administrative_blocker_is_biological_failure": False,
        },
        "claim_ceiling": (
            "ADMINISTRATIVE_READINESS_SUMMARY_ONLY_NO_CONTACT_EXECUTED_"
            "NO_PERMISSION_NO_FRESH_CONTEXT_NO_P0_RESULT"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit WAVE1 permission outreach readiness without sending anything"
    )
    parser.add_argument(
        "--outreach-ledger-csv",
        type=Path,
        default=DEFAULT_LEDGER,
    )
    parser.add_argument("--followup-policy-json", type=Path)
    parser.add_argument(
        "--ready-messages-json",
        type=Path,
        action="append",
        default=[],
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = _read_csv(args.outreach_ledger_csv)
    followup = (
        json.loads(args.followup_policy_json.read_text(encoding="utf-8"))
        if args.followup_policy_json
        else None
    )
    ready_messages = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in args.ready_messages_json
    ]
    result = audit(
        rows,
        followup_policy=followup,
        ready_message_payloads=ready_messages,
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
