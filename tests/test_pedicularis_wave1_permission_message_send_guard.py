from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RENDER = ROOT / "scripts" / "render_pedicularis_wave1_permission_messages.py"
GUARD = ROOT / "scripts" / "validate_pedicularis_wave1_permission_messages_for_send.py"
REVIEW = ROOT / "scripts" / "generate_pedicularis_permission_message_review.py"

spec = importlib.util.spec_from_file_location("ped_message_render", RENDER)
render = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(render)

spec2 = importlib.util.spec_from_file_location("ped_message_guard", GUARD)
guard = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(guard)


spec3 = importlib.util.spec_from_file_location("ped_message_review", REVIEW)
review = importlib.util.module_from_spec(spec3)
assert spec3.loader is not None
spec3.loader.exec_module(review)


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


def _approved_review(payload: dict) -> dict:
    out = review.build_review_draft(payload)
    out["status"] = "HUMAN_REVIEW_APPROVED"
    out["review_bundle_id"] = "TEST-REVIEW-BUNDLE-001"
    out["reviewer_name"] = "TEST REVIEWER"
    out["reviewer_reference"] = "TEST-REVIEWER-REF-001"
    out["reviewed_at"] = "2027-04-20T10:00:00+09:00"
    for route in out["route_reviews"]:
        route["checks"] = {
            key: True
            for key in route["checks"]
        }
        route["approved_for_manual_send"] = True
    return out


def test_raw_renderer_output_cannot_become_send_ready() -> None:
    payload = render.render("SONGZANLIN_EIA_2025")
    with pytest.raises(ValueError, match="unfilled body_cn"):
        guard.validate_and_prepare(
            payload,
            human_review_approved=False,
        )


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
    payload = _filled_payload()
    out = guard.validate_and_prepare(
        payload,
        human_review_approved=True,
        review_receipt=_approved_review(payload),
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
        and len(m["message_content_sha256_cn"]) == 64
        and len(m["message_content_sha256_en"]) == 64
        and len(m["message_content_sha256_bilingual"]) == 64
        for m in out["messages"]
    )
    assert all(
        m["message_content_sha256_cn"]
        == guard.message_content_sha256(m, language="CN")
        and m["message_content_sha256_en"]
        == guard.message_content_sha256(m, language="EN")
        and m["message_content_sha256_bilingual"]
        == guard.message_content_sha256(m, language="BILINGUAL")
        and m["message_content_sha256"]
        == m["message_content_sha256_bilingual"]
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
        guard.validate_and_prepare(
            payload,
            human_review_approved=True,
            review_receipt=_approved_review(payload),
        )



def test_message_content_hash_changes_when_reviewed_body_changes() -> None:
    payload = _filled_payload()
    out = guard.validate_and_prepare(
        payload,
        human_review_approved=True,
        review_receipt=_approved_review(payload),
    )
    message = out["messages"][0]
    original = message["message_content_sha256"]
    message["body_en"] += "\nAdditional sentence."
    assert guard.message_content_sha256(message) != original



def test_language_specific_hashes_are_distinct_for_bilingual_draft() -> None:
    payload = _filled_payload()
    out = guard.validate_and_prepare(
        payload,
        human_review_approved=True,
        review_receipt=_approved_review(payload),
    )
    message = out["messages"][0]
    assert len(
        {
            message["message_content_sha256_cn"],
            message["message_content_sha256_en"],
            message["message_content_sha256_bilingual"],
        }
    ) == 3



def test_human_review_approval_requires_review_receipt() -> None:
    payload = _filled_payload()
    with pytest.raises(ValueError, match="requires review receipt"):
        guard.validate_and_prepare(
            payload,
            human_review_approved=True,
        )


def test_human_review_hash_must_match_exact_message_content() -> None:
    payload = _filled_payload()
    receipt = _approved_review(payload)
    payload["messages"][0]["body_en"] += "\nChanged after review draft."
    with pytest.raises(ValueError, match="human review bilingual hash mismatch"):
        guard.validate_and_prepare(
            payload,
            human_review_approved=True,
            review_receipt=receipt,
        )


def test_human_review_requires_all_route_checks() -> None:
    payload = _filled_payload()
    receipt = _approved_review(payload)
    first = receipt["route_reviews"][0]
    first["checks"]["activity_A_F_wording_verified"] = False
    with pytest.raises(ValueError, match="checks not all passed"):
        guard.validate_and_prepare(
            payload,
            human_review_approved=True,
            review_receipt=receipt,
        )


def test_human_review_receipt_is_retained_in_send_ready_output() -> None:
    payload = _filled_payload()
    receipt = _approved_review(payload)
    out = guard.validate_and_prepare(
        payload,
        human_review_approved=True,
        review_receipt=receipt,
    )
    assert out["human_review_receipt"]["review_bundle_id"] == (
        "TEST-REVIEW-BUNDLE-001"
    )
    assert out["human_review_receipt"]["reviewer_name"] == "TEST REVIEWER"
    assert all(
        message["send_guard"]["human_review_bundle_id"]
        == "TEST-REVIEW-BUNDLE-001"
        for message in out["messages"]
    )
