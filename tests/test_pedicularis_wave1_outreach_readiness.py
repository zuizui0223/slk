from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "scripts" / "audit_pedicularis_wave1_outreach_readiness.py"
RENDER = ROOT / "scripts" / "render_pedicularis_wave1_permission_messages.py"
GUARD = ROOT / "scripts" / "validate_pedicularis_wave1_permission_messages_for_send.py"
FOLLOWUP_TEMPLATE = (
    ROOT / "data"
    / "PEDICULARIS_WAVE1_PERMISSION_FOLLOWUP_POLICY_TEMPLATE_V1.json"
)
LEDGER = (
    ROOT / "data"
    / "PEDICULARIS_WAVE1_PERMISSION_OUTREACH_LEDGER_TEMPLATE_V1.csv"
)

spec = importlib.util.spec_from_file_location("ped_wave1_readiness", AUDIT)
audit_mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(audit_mod)

spec2 = importlib.util.spec_from_file_location("ped_wave1_render", RENDER)
render = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(render)

spec3 = importlib.util.spec_from_file_location("ped_wave1_guard", GUARD)
guard = importlib.util.module_from_spec(spec3)
assert spec3.loader is not None
spec3.loader.exec_module(guard)


def _rows() -> list[dict[str, str]]:
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _policy() -> dict:
    payload = json.loads(FOLLOWUP_TEMPLATE.read_text())
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
        "slk_source_commit": "test-source",
        "freeze_commit": "test-followup-freeze",
        "freeze_timestamp": "2027-04-20T00:00:00+09:00",
        "policy_rationale_reference": "TEST-ADMIN-POLICY",
    }
    return payload


def _ready_messages(candidate_id: str) -> dict:
    payload = render.render(candidate_id)
    for message in payload["messages"]:
        message["body_cn"] = message["body_cn"].replace(
            "REQUIRED_BEFORE_SEND",
            "PROJECT_CONTACT",
        )
        message["body_en"] = message["body_en"].replace(
            "REQUIRED_BEFORE_SEND",
            "PROJECT_CONTACT",
        )
    return guard.validate_and_prepare(
        payload,
        human_review_approved=True,
    )


def test_current_canonical_state_reports_administrative_not_biological_blockers() -> None:
    out = audit_mod.audit(_rows())
    assert out["status"] == "OUTREACH_READINESS_AUDITED"
    assert out["followup_policy_state"] == "NOT_PROVIDED"
    assert out["route_count"] == 7
    assert out["status_counts"] == {"BLOCKED_BEFORE_FIRST_SEND": 7}
    assert out["next_action"] == "FREEZE_FOLLOWUP_POLICY_BEFORE_FIRST_SEND"
    assert out["firewall"]["creates_new_permission_gate"] is False
    assert out["firewall"]["administrative_blocker_is_biological_failure"] is False
    assert all(
        "FOLLOWUP_POLICY_NOT_FROZEN" in route["blockers"]
        and "HUMAN_REVIEWED_MESSAGE_NOT_READY" in route["blockers"]
        for route in out["routes"]
    )


def test_frozen_policy_plus_one_candidate_messages_makes_only_that_candidate_send_ready() -> None:
    out = audit_mod.audit(
        _rows(),
        followup_policy=_policy(),
        ready_message_payloads=[_ready_messages("SONGZANLIN_EIA_2025")],
    )
    assert out["followup_policy_state"] == "FROZEN_AND_VALIDATED"
    assert out["status_counts"] == {
        "BLOCKED_BEFORE_FIRST_SEND": 5,
        "READY_FOR_MANUAL_SEND": 2,
    }
    assert out["candidate_results"]["SONGZANLIN_EIA_2025"][
        "ready_for_manual_send_count"
    ] == 2
    assert out["candidate_results"]["SHANGRILA_WUFENG"][
        "blocked_before_first_send_count"
    ] == 3
    assert out["next_action"] == "MANUALLY_SEND_READY_ROUTES"
    assert out["all_routes_ready_for_manual_send"] is False


def test_all_wave1_routes_can_become_manual_send_ready_without_automatic_send() -> None:
    ready = [
        _ready_messages("SONGZANLIN_EIA_2025"),
        _ready_messages("SHANGRILA_WUFENG"),
        _ready_messages("SHANGRILA_ALPINE_BOT_GARDEN"),
    ]
    out = audit_mod.audit(
        _rows(),
        followup_policy=_policy(),
        ready_message_payloads=ready,
    )
    assert out["status_counts"] == {"READY_FOR_MANUAL_SEND": 7}
    assert out["all_routes_ready_for_manual_send"] is True
    assert out["next_action"] == "MANUALLY_SEND_READY_ROUTES"
    assert all(route["manual_send_only"] is True for route in out["routes"])
    assert all(
        route["automatic_send_allowed"] is False
        for route in out["routes"]
    )


def test_tampered_reviewed_message_hash_is_rejected() -> None:
    ready = _ready_messages("SONGZANLIN_EIA_2025")
    ready["messages"][0]["body_en"] += "\nChanged after review."
    with pytest.raises(
        ValueError,
        match=r"reviewed-message (?:CN|EN|bilingual )?hash mismatch",
    ):
        audit_mod.audit(
            _rows(),
            followup_policy=_policy(),
            ready_message_payloads=[ready],
        )


def test_sent_route_is_awaiting_response_not_blocked_for_missing_message_bundle() -> None:
    rows = _rows()
    route = next(
        row for row in rows
        if row["route_id"] == "SONGZANLIN_FORESTRY_REGULATOR"
    )
    route["outreach_status"] = "SENT_AWAITING_RESPONSE"
    route["outreach_date"] = "2027-05-01"
    route["outreach_reference"] = "SEND-001"
    route["next_action"] = "AWAIT_RESPONSE"

    out = audit_mod.audit(rows)
    route_out = next(
        row for row in out["routes"]
        if row["route_id"] == "SONGZANLIN_FORESTRY_REGULATOR"
    )
    assert route_out["administrative_state"] == "AWAITING_RESPONSE_OR_FOLLOWUP"
    assert route_out["blockers"] == []
