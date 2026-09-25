from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate_pedicularis_wave1_permission_inquiry.py"

spec = importlib.util.spec_from_file_location("ped_wave1_permission_inquiry", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def test_songzanlin_permission_packet_is_unsent_and_activity_specific() -> None:
    out = mod.build("SONGZANLIN_EIA_2025")
    assert out["status"] == "DRAFT_NOT_SENT"
    assert out["candidate"]["recovery_wave"] == "WAVE1"
    assert out["scouting_locator_snapshot"]["locator_type"] == "ENVELOPE"
    assert len(out["contact_routes"]) == 2
    assert all(
        route["permission_status"] == "UNRESOLVED"
        for route in out["contact_routes"]
    )
    assert [x["activity_id"] for x in out["activity_questions"]] == list("ABCDEF")
    assert all(
        x["permission_status"] == "UNKNOWN"
        for x in out["activity_questions"]
    )
    assert all(x["valid_from"] is None for x in out["activity_questions"])
    assert all(x["valid_through"] is None for x in out["activity_questions"])
    assert all(
        x["conditions_compatible_with_registered_activity"] is None
        for x in out["activity_questions"]
    )
    assert all(
        x["conditions_review_reference"] is None
        for x in out["activity_questions"]
    )
    assert out["response_requirements"][
        "provide_activity_specific_validity_window_and_conditions"
    ] is True
    assert out["response_requirements"][
        "review_conditions_against_registered_activity"
    ] is True


def test_alpine_garden_packet_keeps_site_and_regulatory_routes_separate() -> None:
    out = mod.build("SHANGRILA_ALPINE_BOT_GARDEN")
    types = {row["route_type"] for row in out["contact_routes"]}
    assert types == {"REGULATORY_ROUTING", "INSTITUTIONAL_SITE_ROUTING"}
    assert out["response_requirements"]["state_allowed_activities_separately"] is True


def test_wufeng_packet_keeps_local_route_non_authorizing() -> None:
    out = mod.build("SHANGRILA_WUFENG")
    local = next(
        row for row in out["contact_routes"]
        if row["route_type"] == "LOCAL_TERRITORIAL_ROUTING"
    )
    site = next(
        row for row in out["contact_routes"]
        if row["route_id"] == "WUFENG_JIANTANG_FOREST_FARM"
    )
    assert local["permission_status"] == "UNRESOLVED"
    assert site["route_type"] == "SITE_MANAGEMENT_ROUTING"
    assert "Jiantang Branch" in site["organization"]
    assert out["promotion_rule"].startswith(
        "This draft cannot set sampling_permission_status=CONFIRMED"
    )
