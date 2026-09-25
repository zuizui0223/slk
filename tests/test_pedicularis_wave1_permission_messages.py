from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_pedicularis_wave1_permission_messages.py"

spec = importlib.util.spec_from_file_location("ped_wave1_message_renderer", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def test_songzanlin_message_drafts_remain_unsent_and_activity_specific() -> None:
    out = mod.render("SONGZANLIN_EIA_2025")
    assert out["status"] == "DRAFT_NOT_SENT"
    assert len(out["messages"]) == 2
    for message in out["messages"]:
        assert message["status"] == "DRAFT_NOT_SENT"
        assert message["send_guard"]["automatic_send_allowed"] is False
        assert message["send_guard"]["human_review_required"] is True
        for activity_id in "ABCDEF":
            assert f"{activity_id}." in message["body_cn"]
            assert f"{activity_id}." in message["body_en"]
        assert "REQUIRED_BEFORE_SEND" in message["body_cn"]


def test_songzanlin_envelope_is_not_described_as_current_plant_location() -> None:
    out = mod.render("SONGZANLIN_EIA_2025")
    body = out["messages"][0]["body_cn"]
    assert "该范围不是具体植株位置" in body
    assert "确认本季是否仍存在" in body


def test_wufeng_point_is_labeled_as_scouting_only() -> None:
    out = mod.render("SHANGRILA_WUFENG")
    assert len(out["messages"]) == 3
    body = out["messages"][0]["body_en"]
    assert "scouting locator only" in body
    assert "not a current population coordinate" in body


def test_renderer_never_claims_permission_or_executes_contact() -> None:
    out = mod.render("SHANGRILA_WUFENG")
    assert "NO_PERMISSION_GRANTED" in out["claim_ceiling"]
    assert all(
        message["send_guard"]["requester_identity_filled"] is False
        and message["send_guard"]["institution_filled"] is False
        and message["send_guard"]["reply_contact_filled"] is False
        for message in out["messages"]
    )
