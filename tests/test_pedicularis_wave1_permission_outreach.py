from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "manage_pedicularis_wave1_permission_outreach.py"
TEMPLATE = ROOT / "data" / "PEDICULARIS_WAVE1_PERMISSION_OUTREACH_LEDGER_TEMPLATE_V1.csv"

spec = importlib.util.spec_from_file_location("ped_wave1_outreach", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def _rows() -> list[dict[str, str]]:
    with TEMPLATE.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _mark_audited_response(
    row: dict[str, str],
    *,
    status: str,
    response_date: str,
    prefix: str,
    channel: str = "EMAIL",
) -> None:
    row["response_status"] = status
    row["response_date"] = response_date
    row["response_received_at"] = response_date + "T09:00:00+08:00"
    row["response_reference"] = f"{prefix}-REF"
    row["response_event_id"] = f"{prefix}-EVENT"
    row["response_receive_channel"] = channel
    row["response_content_sha256"] = "a" * 64
    row["response_classification_review_reference"] = f"{prefix}-CLASS-REVIEW"


def test_template_matches_generated_canonical_outreach_inventory() -> None:
    generated = mod.generate_rows()
    template = _rows()
    assert {row["route_id"] for row in template} == {
        row["route_id"] for row in generated
    }
    out = mod.validate(template)
    assert out["status"] == "WAVE1_PERMISSION_OUTREACH_LEDGER_VALIDATED"
    assert out["route_count"] == 7
    assert out["candidate_count"] == 3
    assert out["outreach_status_counts"] == {"NOT_SENT": 7}
    assert out["substantive_response_count"] == 0
    assert out["total_followup_attempts"] == 0
    assert all(
        not progress["ready_to_build_permission_response_bundle"]
        for progress in out["candidate_progress"].values()
    )


def test_sent_outreach_requires_date_and_reference() -> None:
    rows = _rows()
    rows[0]["outreach_status"] = "SENT_AWAITING_RESPONSE"
    with pytest.raises(ValueError, match="lacks date/reference"):
        mod.validate(rows)


def test_not_sent_route_cannot_carry_response_evidence() -> None:
    rows = _rows()
    rows[0]["response_status"] = "SUBSTANTIVE_RESPONSE_RECEIVED"
    rows[0]["response_date"] = "2027-05-10"
    rows[0]["response_reference"] = "EMAIL-001"
    with pytest.raises(ValueError, match="NOT_SENT route carries"):
        mod.validate(rows)


def test_routing_only_response_requires_destination() -> None:
    rows = _rows()
    target = next(r for r in rows if r["route_id"] == "WUFENG_LOCAL_ROUTING")
    target["outreach_status"] = "ROUTED_TO_ANOTHER_AUTHORITY"
    target["outreach_date"] = "2027-05-01"
    target["outreach_reference"] = "EMAIL-WUFENG-LOCAL-001"
    _mark_audited_response(
        target,
        status="ROUTING_RESPONSE_ONLY",
        response_date="2027-05-02",
        prefix="EMAIL-WUFENG-LOCAL-RESP-001",
    )
    with pytest.raises(ValueError, match="routing response lacks destination"):
        mod.validate(rows)


def test_candidate_ready_requires_substantive_regulatory_and_site_response() -> None:
    rows = _rows()
    for route_id in ("SONGZANLIN_FORESTRY_REGULATOR", "SONGZANLIN_SITE_MANAGEMENT"):
        target = next(r for r in rows if r["route_id"] == route_id)
        target["outreach_status"] = "RESPONSE_RECEIVED"
        target["outreach_date"] = "2027-05-01"
        target["outreach_reference"] = f"OUT-{route_id}"
        _mark_audited_response(
            target,
            status="SUBSTANTIVE_RESPONSE_RECEIVED",
            response_date="2027-05-05",
            prefix=f"RESP-{route_id}",
        )
    out = mod.validate(rows)
    assert out["candidate_progress"]["SONGZANLIN_EIA_2025"][
        "ready_to_build_permission_response_bundle"
    ] is True
    assert out["candidate_progress"]["SHANGRILA_WUFENG"][
        "ready_to_build_permission_response_bundle"
    ] is False


def test_local_routing_response_does_not_substitute_for_wufeng_site_authority() -> None:
    rows = _rows()
    reg = next(r for r in rows if r["route_id"] == "WUFENG_FORESTRY_REGULATOR")
    reg.update(
        {
            "outreach_status": "RESPONSE_RECEIVED",
            "outreach_date": "2027-05-01",
            "outreach_reference": "OUT-REG",
        }
    )
    _mark_audited_response(
        reg,
        status="SUBSTANTIVE_RESPONSE_RECEIVED",
        response_date="2027-05-02",
        prefix="RESP-REG",
    )
    local = next(r for r in rows if r["route_id"] == "WUFENG_LOCAL_ROUTING")
    local.update(
        {
            "outreach_status": "ROUTED_TO_ANOTHER_AUTHORITY",
            "outreach_date": "2027-05-01",
            "outreach_reference": "OUT-LOCAL",
            "routed_to_organization": "Shangri-La State-owned Forest Farm, Jiantang Branch",
            "routed_to_contact": "via forestry bureau",
        }
    )
    _mark_audited_response(
        local,
        status="ROUTING_RESPONSE_ONLY",
        response_date="2027-05-02",
        prefix="RESP-LOCAL",
    )
    out = mod.validate(rows)
    assert out["candidate_progress"]["SHANGRILA_WUFENG"][
        "substantive_regulatory_response_received"
    ] is True
    assert out["candidate_progress"]["SHANGRILA_WUFENG"][
        "substantive_site_response_received"
    ] is False
    assert out["candidate_progress"]["SHANGRILA_WUFENG"][
        "ready_to_build_permission_response_bundle"
    ] is False
    assert out["candidate_progress"]["SHANGRILA_WUFENG"][
        "canonical_route_update_required"
    ] is True
    routed = out["candidate_progress"]["SHANGRILA_WUFENG"][
        "routing_destinations_pending_canonical_registration"
    ]
    assert routed == [
        {
            "source_route_id": "WUFENG_LOCAL_ROUTING",
            "organization": "Shangri-La State-owned Forest Farm, Jiantang Branch",
            "contact": "via forestry bureau",
        }
    ]



def test_not_sent_route_cannot_claim_followup_attempt() -> None:
    rows = _rows()
    rows[0]["followup_attempts_completed"] = "1"
    rows[0]["last_followup_date"] = "2027-05-08"
    rows[0]["last_followup_reference"] = "FOLLOWUP-001"
    with pytest.raises(ValueError, match="NOT_SENT route carries"):
        mod.validate(rows)


def test_followup_attempt_requires_last_date_and_reference() -> None:
    rows = _rows()
    row = rows[0]
    row["outreach_status"] = "SENT_AWAITING_RESPONSE"
    row["outreach_date"] = "2027-05-01"
    row["outreach_reference"] = "SEND-001"
    row["followup_attempts_completed"] = "1"
    with pytest.raises(ValueError, match="lack last date/reference"):
        mod.validate(rows)


def test_zero_followup_attempts_cannot_carry_last_followup_evidence() -> None:
    rows = _rows()
    row = rows[0]
    row["outreach_status"] = "SENT_AWAITING_RESPONSE"
    row["outreach_date"] = "2027-05-01"
    row["outreach_reference"] = "SEND-001"
    row["last_followup_date"] = "2027-05-08"
    row["last_followup_reference"] = "FOLLOWUP-001"
    with pytest.raises(ValueError, match="zero follow-up attempts"):
        mod.validate(rows)


def test_last_followup_cannot_precede_initial_send() -> None:
    rows = _rows()
    row = rows[0]
    row["outreach_status"] = "SENT_AWAITING_RESPONSE"
    row["outreach_date"] = "2027-05-10"
    row["outreach_reference"] = "SEND-001"
    row["followup_attempts_completed"] = "1"
    row["last_followup_date"] = "2027-05-08"
    row["last_followup_reference"] = "FOLLOWUP-001"
    with pytest.raises(ValueError, match="precedes initial outreach"):
        mod.validate(rows)


def test_valid_followup_attempt_is_counted_in_outreach_receipt() -> None:
    rows = _rows()
    row = rows[0]
    row["outreach_status"] = "SENT_AWAITING_RESPONSE"
    row["outreach_date"] = "2027-05-01"
    row["outreach_reference"] = "SEND-001"
    row["followup_attempts_completed"] = "1"
    row["last_followup_date"] = "2027-05-08"
    row["last_followup_reference"] = "FOLLOWUP-001"
    out = mod.validate(rows)
    assert out["total_followup_attempts"] == 1
    candidate = row["candidate_id"]
    assert out["candidate_progress"][candidate][
        "followup_attempts_completed"
    ] == 1



def test_response_status_requires_audited_response_provenance() -> None:
    rows = _rows()
    row = rows[0]
    row["outreach_status"] = "RESPONSE_RECEIVED"
    row["outreach_date"] = "2027-05-01"
    row["outreach_reference"] = "SEND-001"
    row["response_status"] = "SUBSTANTIVE_RESPONSE_RECEIVED"
    row["response_date"] = "2027-05-02"
    row["response_reference"] = "RESP-001"
    with pytest.raises(ValueError, match="lacks audited response evidence"):
        mod.validate(rows)


def test_response_received_at_date_must_match_response_date() -> None:
    rows = _rows()
    row = rows[0]
    row["outreach_status"] = "RESPONSE_RECEIVED"
    row["outreach_date"] = "2027-05-01"
    row["outreach_reference"] = "SEND-001"
    _mark_audited_response(
        row,
        status="SUBSTANTIVE_RESPONSE_RECEIVED",
        response_date="2027-05-02",
        prefix="RESP-001",
    )
    row["response_received_at"] = "2027-05-03T09:00:00+08:00"
    with pytest.raises(ValueError, match="response_date/received_at mismatch"):
        mod.validate(rows)


def test_response_content_hash_must_be_sha256() -> None:
    rows = _rows()
    row = rows[0]
    row["outreach_status"] = "RESPONSE_RECEIVED"
    row["outreach_date"] = "2027-05-01"
    row["outreach_reference"] = "SEND-001"
    _mark_audited_response(
        row,
        status="SUBSTANTIVE_RESPONSE_RECEIVED",
        response_date="2027-05-02",
        prefix="RESP-001",
    )
    row["response_content_sha256"] = "not-a-hash"
    with pytest.raises(ValueError, match="must be sha256"):
        mod.validate(rows)
