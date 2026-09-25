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
    target["response_status"] = "ROUTING_RESPONSE_ONLY"
    target["response_date"] = "2027-05-02"
    target["response_reference"] = "EMAIL-WUFENG-LOCAL-RESP-001"
    with pytest.raises(ValueError, match="routing response lacks destination"):
        mod.validate(rows)


def test_candidate_ready_requires_substantive_regulatory_and_site_response() -> None:
    rows = _rows()
    for route_id in ("SONGZANLIN_FORESTRY_REGULATOR", "SONGZANLIN_SITE_MANAGEMENT"):
        target = next(r for r in rows if r["route_id"] == route_id)
        target["outreach_status"] = "RESPONSE_RECEIVED"
        target["outreach_date"] = "2027-05-01"
        target["outreach_reference"] = f"OUT-{route_id}"
        target["response_status"] = "SUBSTANTIVE_RESPONSE_RECEIVED"
        target["response_date"] = "2027-05-05"
        target["response_reference"] = f"RESP-{route_id}"
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
            "response_status": "SUBSTANTIVE_RESPONSE_RECEIVED",
            "response_date": "2027-05-02",
            "response_reference": "RESP-REG",
        }
    )
    local = next(r for r in rows if r["route_id"] == "WUFENG_LOCAL_ROUTING")
    local.update(
        {
            "outreach_status": "ROUTED_TO_ANOTHER_AUTHORITY",
            "outreach_date": "2027-05-01",
            "outreach_reference": "OUT-LOCAL",
            "response_status": "ROUTING_RESPONSE_ONLY",
            "response_date": "2027-05-02",
            "response_reference": "RESP-LOCAL",
            "routed_to_organization": "Shangri-La State-owned Forest Farm, Jiantang Branch",
            "routed_to_contact": "via forestry bureau",
        }
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
