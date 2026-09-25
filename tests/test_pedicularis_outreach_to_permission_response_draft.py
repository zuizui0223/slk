from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "compile_pedicularis_outreach_to_permission_response_draft.py"
TEMPLATE = ROOT / "data" / "PEDICULARIS_WAVE1_PERMISSION_OUTREACH_LEDGER_TEMPLATE_V1.csv"

spec = importlib.util.spec_from_file_location("ped_outreach_compile", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def _rows() -> list[dict[str, str]]:
    with TEMPLATE.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _mark_response(rows: list[dict[str, str]], route_id: str) -> None:
    row = next(r for r in rows if r["route_id"] == route_id)
    row["outreach_status"] = "RESPONSE_RECEIVED"
    row["outreach_date"] = "2027-05-01"
    row["outreach_reference"] = f"OUT-{route_id}"
    row["response_status"] = "SUBSTANTIVE_RESPONSE_RECEIVED"
    row["response_date"] = "2027-05-05"
    row["response_reference"] = f"RESP-{route_id}"


def test_response_draft_requires_both_regulatory_and_site_substantive_reply() -> None:
    rows = _rows()
    _mark_response(rows, "SONGZANLIN_FORESTRY_REGULATOR")
    with pytest.raises(ValueError, match="lacks substantive regulatory \+ site"):
        mod.build(rows, "SONGZANLIN_EIA_2025")


def test_ready_candidate_compiles_unresolved_activity_decision_draft() -> None:
    rows = _rows()
    _mark_response(rows, "SONGZANLIN_FORESTRY_REGULATOR")
    _mark_response(rows, "SONGZANLIN_SITE_MANAGEMENT")
    out = mod.build(rows, "SONGZANLIN_EIA_2025")
    assert out["status"] == "DRAFT_AWAITING_ACTIVITY_DECISIONS"
    assert out["candidate_id"] == "SONGZANLIN_EIA_2025"
    assert len(out["responses"]) == 2
    assert {r["route_id"] for r in out["responses"]} == {
        "SONGZANLIN_FORESTRY_REGULATOR",
        "SONGZANLIN_SITE_MANAGEMENT",
    }
    for response in out["responses"]:
        assert [x["activity_id"] for x in response["activity_decisions"]] == list(
            "ABCDEF"
        )
        assert all(
            x["decision"] == "UNRESOLVED"
            for x in response["activity_decisions"]
        )
        assert response["valid_from"] is None
        assert response["valid_through"] is None


def test_routing_only_reply_is_not_copied_as_authorizing_response() -> None:
    rows = _rows()
    _mark_response(rows, "WUFENG_FORESTRY_REGULATOR")
    _mark_response(rows, "WUFENG_JIANTANG_FOREST_FARM")
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
    out = mod.build(rows, "SHANGRILA_WUFENG")
    assert "WUFENG_LOCAL_ROUTING" not in {
        response["route_id"] for response in out["responses"]
    }


def test_draft_cannot_be_mistaken_for_filled_authority_response_bundle() -> None:
    rows = _rows()
    _mark_response(rows, "ALPINE_GARDEN_FORESTRY_REGULATOR")
    _mark_response(rows, "ALPINE_GARDEN_SITE_CONTACT")
    out = mod.build(rows, "SHANGRILA_ALPINE_BOT_GARDEN")
    assert out["status"] != "FILLED_AUTHORITY_RESPONSES"
    assert out["response_bundle_id"] == "REQUIRED_BEFORE_USE"
