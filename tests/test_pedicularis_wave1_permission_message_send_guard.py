from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RENDER = ROOT / "scripts" / "render_pedicularis_wave1_permission_messages.py"
GUARD = ROOT / "scripts" / "validate_pedicularis_wave1_permission_messages_for_send.py"

spec = importlib.util.spec_from_file_location("ped_message_render", RENDER)
render = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(render)

spec2 = importlib.util.spec_from_file_location("ped_message_guard", GUARD)
guard = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(guard)


def _filled_payload() -> dict:
    payload = render.render("SONGZANLIN_EIA_2025")
    for message in payload["messages"]:
        message["body_cn"] = message["body_cn"].replace(
            "REQUIRED_BEFORE_SEND",
            "PROJECT_CONTACT",
        )
        message["body_en"] = message["body_en"].replace(
            "REQUIRED_BEFORE_SEND",
            "PROJECT_CONTACT",
        )
    return payload


def test_raw_renderer_output_cannot_become_send_ready() -> None:
    payload = render.render("SONGZANLIN_EIA_2025")
    with pytest.raises(ValueError, match="unfilled body_cn"):
        guard.validate_and_prepare(payload, human_review_approved=True)


def test_filled_but_unreviewed_messages_remain_draft() -> None:
    out = guard.validate_and_prepare(
        _filled_payload(),
        human_review_approved=False,
    )
    assert out["status"] == "DRAFT_NOT_SENT"
    assert out["send_policy"]["automatic_send_allowed"] is False
    assert out["send_policy"]["human_review_approved"] is False
    assert all(m["status"] == "DRAFT_NOT_SENT" for m in out["messages"])


def test_human_review_can_mark_messages_ready_for_manual_send_only() -> None:
    out = guard.validate_and_prepare(
        _filled_payload(),
        human_review_approved=True,
    )
    assert out["status"] == "READY_FOR_MANUAL_SEND"
    assert out["send_policy"] == {
        "manual_send_only": True,
        "automatic_send_allowed": False,
        "human_review_approved": True,
    }
    assert all(m["status"] == "READY_FOR_MANUAL_SEND" for m in out["messages"])
    assert all(
        len(m["message_content_sha256"]) == 64
        for m in out["messages"]
    )
    assert all(
        m["message_content_sha256"] == guard.message_content_sha256(m)
        for m in out["messages"]
    )
    assert all(
        m["send_guard"]["automatic_send_allowed"] is False
        for m in out["messages"]
    )


def test_send_guard_rejects_automatic_send_promotion() -> None:
    payload = _filled_payload()
    payload["messages"][0]["send_guard"]["automatic_send_allowed"] = True
    with pytest.raises(ValueError, match="automatic send must remain disabled"):
        guard.validate_and_prepare(payload, human_review_approved=True)



def test_message_content_hash_changes_when_reviewed_body_changes() -> None:
    out = guard.validate_and_prepare(
        _filled_payload(),
        human_review_approved=True,
    )
    message = out["messages"][0]
    original = message["message_content_sha256"]
    message["body_en"] += "\nAdditional sentence."
    assert guard.message_content_sha256(message) != original
