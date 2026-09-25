from __future__ import annotations

import copy
import csv
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
VALIDATE = ROOT / "scripts" / "validate_pedicularis_wave1_permission_followup_policy.py"
PLAN = ROOT / "scripts" / "plan_pedicularis_wave1_permission_followups.py"
TEMPLATE = ROOT / "data" / "PEDICULARIS_WAVE1_PERMISSION_FOLLOWUP_POLICY_TEMPLATE_V1.json"
LEDGER = ROOT / "data" / "PEDICULARIS_WAVE1_PERMISSION_OUTREACH_LEDGER_TEMPLATE_V1.csv"

spec = importlib.util.spec_from_file_location("ped_followup_validate", VALIDATE)
validate = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validate)

spec2 = importlib.util.spec_from_file_location("ped_followup_plan", PLAN)
planner = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(planner)


def _policy() -> dict:
    payload = json.loads(TEMPLATE.read_text())
    payload["status"] = "FROZEN_POLICY"
    payload["production_status"] = (
        "PEDICULARIS_WAVE1_PERMISSION_FOLLOWUP_POLICY_PROSPECTIVELY_FROZEN"
    )
    payload["policy"].update(
        {
            "followup_offsets_days": [7, 14],
            "escalation_review_after_days": 21,
            "frozen_before_first_send": True,
        }
    )
    payload["freeze_metadata"] = {
        "slk_source_commit": "abc123",
        "freeze_commit": "followup-freeze-001",
        "freeze_timestamp": "2027-04-20T00:00:00Z",
        "policy_rationale_reference": "ADMIN-POLICY-001",
    }
    return payload


def _rows() -> list[dict[str, str]]:
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _sent_row(rows: list[dict[str, str]]) -> dict[str, str]:
    row = next(
        r for r in rows
        if r["route_id"] == "SONGZANLIN_FORESTRY_REGULATOR"
    )
    row["outreach_status"] = "SENT_AWAITING_RESPONSE"
    row["outreach_date"] = "2027-05-01"
    row["outreach_reference"] = "SEND-REF-001"
    row["next_action"] = "AWAIT_RESPONSE"
    return row


def test_followup_policy_validates_finite_increasing_schedule() -> None:
    out = validate.validate(_policy())
    assert out["status"] == "FOLLOWUP_POLICY_VALIDATED"
    assert out["followup_offsets_days"] == [7, 14]
    assert out["followup_attempt_count"] == 2
    assert out["escalation_review_after_days"] == 21
    assert out["automatic_close_allowed"] is False


def test_followup_policy_must_be_frozen_before_first_send() -> None:
    payload = _policy()
    payload["policy"]["frozen_before_first_send"] = False
    with pytest.raises(ValueError, match="not frozen before first send"):
        validate.validate(payload)


def test_followup_offsets_must_be_strictly_increasing_and_unique() -> None:
    payload = _policy()
    payload["policy"]["followup_offsets_days"] = [14, 7, 14]
    with pytest.raises(ValueError, match="unique and strictly increasing"):
        validate.validate(payload)


def test_escalation_must_follow_last_followup() -> None:
    payload = _policy()
    payload["policy"]["escalation_review_after_days"] = 14
    with pytest.raises(ValueError, match="after the last follow-up"):
        validate.validate(payload)


def test_followup_policy_cannot_auto_close_no_response_route() -> None:
    payload = _policy()
    payload["policy"]["automatic_close_allowed"] = True
    with pytest.raises(ValueError, match="automatic closure"):
        validate.validate(payload)


def test_unsent_routes_plan_initial_inquiry_not_followup() -> None:
    out = planner.plan(_rows(), _policy(), as_of_date="2027-05-08")
    assert out["action_counts"] == {"SEND_INITIAL_INQUIRY": 7}


def test_initial_send_waits_until_first_frozen_followup_offset() -> None:
    rows = _rows()
    _sent_row(rows)
    out = planner.plan(rows, _policy(), as_of_date="2027-05-05")
    route = next(
        r for r in out["routes"]
        if r["route_id"] == "SONGZANLIN_FORESTRY_REGULATOR"
    )
    assert route["action"] == "WAIT_UNTIL_FOLLOWUP"
    assert route["followup_number"] == 1
    assert route["due_date"] == "2027-05-08"


def test_first_followup_becomes_due_on_frozen_offset() -> None:
    rows = _rows()
    _sent_row(rows)
    out = planner.plan(rows, _policy(), as_of_date="2027-05-08")
    route = next(
        r for r in out["routes"]
        if r["route_id"] == "SONGZANLIN_FORESTRY_REGULATOR"
    )
    assert route["action"] == "FOLLOWUP_DUE"
    assert route["followup_number"] == 1


def test_one_completed_followup_advances_to_second_offset() -> None:
    rows = _rows()
    row = _sent_row(rows)
    row["followup_attempts_completed"] = "1"
    row["last_followup_date"] = "2027-05-08"
    row["last_followup_reference"] = "FOLLOWUP-001"
    out = planner.plan(rows, _policy(), as_of_date="2027-05-10")
    route = next(
        r for r in out["routes"]
        if r["route_id"] == "SONGZANLIN_FORESTRY_REGULATOR"
    )
    assert route["action"] == "WAIT_UNTIL_FOLLOWUP"
    assert route["followup_number"] == 2
    assert route["due_date"] == "2027-05-15"


def test_all_followups_completed_move_to_escalation_review_not_auto_close() -> None:
    rows = _rows()
    row = _sent_row(rows)
    row["followup_attempts_completed"] = "2"
    row["last_followup_date"] = "2027-05-15"
    row["last_followup_reference"] = "FOLLOWUP-002"
    out = planner.plan(rows, _policy(), as_of_date="2027-05-22")
    route = next(
        r for r in out["routes"]
        if r["route_id"] == "SONGZANLIN_FORESTRY_REGULATOR"
    )
    assert route["action"] == "ESCALATION_REVIEW_DUE"
    assert route["due_date"] == "2027-05-22"
    assert out["automatic_close_allowed"] is False


def test_any_recorded_response_preempts_same_route_followup() -> None:
    rows = _rows()
    row = _sent_row(rows)
    row["outreach_status"] = "RESPONSE_RECEIVED"
    row["response_status"] = "SUBSTANTIVE_RESPONSE_RECEIVED"
    row["response_date"] = "2027-05-06"
    row["response_reference"] = "RESPONSE-001"
    out = planner.plan(rows, _policy(), as_of_date="2027-05-20")
    route = next(
        r for r in out["routes"]
        if r["route_id"] == "SONGZANLIN_FORESTRY_REGULATOR"
    )
    assert route["action"] == "RESPONSE_RECORDED_NO_FOLLOWUP"


def test_followup_planner_rejects_future_initial_send_relative_to_as_of() -> None:
    rows = _rows()
    row = _sent_row(rows)
    row["outreach_date"] = "2027-05-10"
    with pytest.raises(ValueError, match="outreach date occurs after"):
        planner.plan(rows, _policy(), as_of_date="2027-05-08")


def test_followup_planner_rejects_future_last_followup_relative_to_as_of() -> None:
    rows = _rows()
    row = _sent_row(rows)
    row["followup_attempts_completed"] = "1"
    row["last_followup_date"] = "2027-05-12"
    row["last_followup_reference"] = "FOLLOWUP-FUTURE"
    with pytest.raises(ValueError, match="last follow-up occurs after"):
        planner.plan(rows, _policy(), as_of_date="2027-05-10")


def test_policy_template_is_deliberately_unfrozen() -> None:
    payload = json.loads(TEMPLATE.read_text())
    assert payload["status"] == "TEMPLATE_ONLY_NOT_FROZEN"
    assert payload["policy"]["followup_offsets_days"] == []
    assert payload["policy"]["frozen_before_first_send"] is False
    assert payload["policy"]["automatic_close_allowed"] is False



def test_followup_policy_freeze_timestamp_requires_timezone() -> None:
    payload = _policy()
    payload["freeze_metadata"]["freeze_timestamp"] = "2027-04-20T00:00:00"
    with pytest.raises(ValueError, match="timezone offset"):
        validate.validate(payload)


def test_followup_attempt_count_cannot_exceed_frozen_schedule() -> None:
    rows = _rows()
    row = _sent_row(rows)
    row["followup_attempts_completed"] = "3"
    row["last_followup_date"] = "2027-05-22"
    row["last_followup_reference"] = "FOLLOWUP-003"
    with pytest.raises(ValueError, match="exceed frozen policy schedule"):
        planner.plan(rows, _policy(), as_of_date="2027-05-23")


def test_followup_attempt_cannot_be_recorded_before_frozen_offset() -> None:
    rows = _rows()
    row = _sent_row(rows)
    row["followup_attempts_completed"] = "1"
    row["last_followup_date"] = "2027-05-06"
    row["last_followup_reference"] = "FOLLOWUP-EARLY"
    with pytest.raises(ValueError, match="precedes frozen attempt offset"):
        planner.plan(rows, _policy(), as_of_date="2027-05-10")
