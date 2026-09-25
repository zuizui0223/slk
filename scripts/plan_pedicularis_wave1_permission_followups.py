from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANAGER_PATH = ROOT / "scripts" / "manage_pedicularis_wave1_permission_outreach.py"
POLICY_VALIDATOR_PATH = ROOT / "scripts" / "validate_pedicularis_wave1_permission_followup_policy.py"

_spec_manager = importlib.util.spec_from_file_location("ped_outreach_manager", MANAGER_PATH)
manager = importlib.util.module_from_spec(_spec_manager)
assert _spec_manager.loader is not None
_spec_manager.loader.exec_module(manager)

_spec_policy = importlib.util.spec_from_file_location("ped_followup_policy", POLICY_VALIDATOR_PATH)
policy_validator = importlib.util.module_from_spec(_spec_policy)
assert _spec_policy.loader is not None
_spec_policy.loader.exec_module(policy_validator)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _date(value: str, label: str) -> date:
    try:
        return date.fromisoformat(str(value).strip())
    except ValueError as exc:
        raise ValueError(f"{label} must be ISO YYYY-MM-DD") from exc


def plan(
    rows: list[dict[str, str]],
    policy_payload: dict,
    *,
    as_of_date: str,
) -> dict:
    manager_receipt = manager.validate(rows)
    policy = policy_validator.validate(policy_payload)
    as_of = _date(as_of_date, "as_of_date")
    offsets = policy["followup_offsets_days"]
    escalation_after = policy["escalation_review_after_days"]

    route_plans = []
    for row in rows:
        route_id = row["route_id"].strip()
        candidate_id = row["candidate_id"].strip()
        outreach = row["outreach_status"].strip()
        response = row["response_status"].strip()
        attempts = int(row["followup_attempts_completed"])

        if outreach == "NOT_SENT":
            action = "SEND_INITIAL_INQUIRY"
            due_date = None
            followup_number = None
        else:
            outreach_day = _date(
                row["outreach_date"],
                f"outreach_date/{route_id}",
            )
            if outreach_day > as_of:
                raise ValueError(
                    f"outreach date occurs after as_of_date: {route_id}"
                )
            if attempts > 0:
                last_followup_day = _date(
                    row["last_followup_date"],
                    f"last_followup_date/{route_id}",
                )
                if last_followup_day > as_of:
                    raise ValueError(
                        f"last follow-up occurs after as_of_date: {route_id}"
                    )

            if response != "NO_RESPONSE":
                response_day = _date(
                    row["response_date"],
                    f"response_date/{route_id}",
                )
                if response_day > as_of:
                    raise ValueError(
                        f"response date occurs after as_of_date: {route_id}"
                    )
                action = "RESPONSE_RECORDED_NO_FOLLOWUP"
                due_date = None
                followup_number = None
            elif outreach != "SENT_AWAITING_RESPONSE":
                action = "NO_FOLLOWUP_ROUTE_NOT_AWAITING_RESPONSE"
                due_date = None
                followup_number = None
            elif attempts < len(offsets):
                followup_number = attempts + 1
                due = outreach_day + timedelta(days=offsets[attempts])
                due_date = due.isoformat()
                action = (
                    "FOLLOWUP_DUE"
                    if as_of >= due
                    else "WAIT_UNTIL_FOLLOWUP"
                )
            else:
                followup_number = None
                due = outreach_day + timedelta(days=escalation_after)
                due_date = due.isoformat()
                action = (
                    "ESCALATION_REVIEW_DUE"
                    if as_of >= due
                    else "WAIT_UNTIL_ESCALATION_REVIEW"
                )

        route_plans.append(
            {
                "candidate_id": candidate_id,
                "route_id": route_id,
                "route_type": row["route_type"].strip(),
                "outreach_status": outreach,
                "response_status": response,
                "followup_attempts_completed": attempts,
                "action": action,
                "followup_number": followup_number,
                "due_date": due_date,
            }
        )

    action_counts: dict[str, int] = {}
    for route in route_plans:
        action_counts[route["action"]] = action_counts.get(route["action"], 0) + 1

    return {
        "schema_version": "SLK_PEDICULARIS_WAVE1_PERMISSION_FOLLOWUP_PLAN_V1",
        "status": "FOLLOWUP_PLAN_COMPUTED",
        "as_of_date": as_of.isoformat(),
        "policy_freeze_commit": policy["freeze_commit"],
        "followup_offsets_days": offsets,
        "escalation_review_after_days": escalation_after,
        "automatic_close_allowed": False,
        "manager_receipt_status": manager_receipt["status"],
        "action_counts": dict(sorted(action_counts.items())),
        "routes": route_plans,
        "claim_ceiling": (
            "ADMINISTRATIVE_FOLLOWUP_PLAN_ONLY_NO_CONTACT_EXECUTED_"
            "NO_PERMISSION_NO_FRESH_CONTEXT_NO_P0_SIGNAL"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Plan WAVE1 permission follow-ups from a frozen administrative policy"
    )
    parser.add_argument("outreach_ledger_csv", type=Path)
    parser.add_argument("followup_policy_json", type=Path)
    parser.add_argument("--as-of-date", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = plan(
        _read(args.outreach_ledger_csv),
        json.loads(args.followup_policy_json.read_text(encoding="utf-8")),
        as_of_date=args.as_of_date,
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
