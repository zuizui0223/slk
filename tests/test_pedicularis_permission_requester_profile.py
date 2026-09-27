from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RENDER = ROOT / "scripts" / "render_pedicularis_wave1_permission_messages.py"
COMPILE = ROOT / "scripts" / "compile_pedicularis_permission_requester_profile.py"
GUARD = ROOT / "scripts" / "validate_pedicularis_wave1_permission_messages_for_send.py"
REVIEW = ROOT / "scripts" / "generate_pedicularis_permission_message_review.py"
PROFILE_TEMPLATE = (
    ROOT / "data" / "PEDICULARIS_PERMISSION_REQUESTER_PROFILE_TEMPLATE_V1.json"
)

spec = importlib.util.spec_from_file_location("ped_requester_render", RENDER)
render = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(render)

spec2 = importlib.util.spec_from_file_location("ped_requester_compile", COMPILE)
compiler = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(compiler)

spec3 = importlib.util.spec_from_file_location("ped_requester_guard", GUARD)
guard = importlib.util.module_from_spec(spec3)
assert spec3.loader is not None
spec3.loader.exec_module(guard)


spec4 = importlib.util.spec_from_file_location("ped_requester_review", REVIEW)
review = importlib.util.module_from_spec(spec4)
assert spec4.loader is not None
spec4.loader.exec_module(review)


def _profile() -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_PERMISSION_REQUESTER_PROFILE_V1",
        "status": "LOCAL_PROFILE_FILLED",
        "requester_name": "TEST REQUESTER",
        "institution": "TEST INSTITUTION",
        "contact_email": "test.requester@example.org",
        "profile_reference": "LOCAL-PROFILE-TEST-001",
        "privacy_policy": "FILLED_PROFILE_LOCAL_GITIGNORED_DO_NOT_COMMIT",
    }


def _approved_review(payload: dict) -> dict:
    receipt = review.build_review_draft(payload)
    receipt["status"] = "HUMAN_REVIEW_APPROVED"
    receipt["review_bundle_id"] = "TEST-REQUESTER-REVIEW-001"
    receipt["reviewer_name"] = "TEST REVIEWER"
    receipt["reviewer_reference"] = "TEST-REQUESTER-REVIEWER-REF"
    receipt["reviewed_at"] = "2027-04-20T10:00:00+09:00"
    for route in receipt["route_reviews"]:
        route["checks"] = {key: True for key in route["checks"]}
        route["approved_for_manual_send"] = True
    return receipt


def test_profile_template_is_explicitly_not_filled() -> None:
    payload = json.loads(PROFILE_TEMPLATE.read_text())
    assert payload["schema_version"] == (
        "SLK_PEDICULARIS_PERMISSION_REQUESTER_PROFILE_V1"
    )
    assert payload["status"] == "TEMPLATE_ONLY_NOT_DATA"
    assert payload["privacy_policy"] == (
        "FILLED_PROFILE_LOCAL_GITIGNORED_DO_NOT_COMMIT"
    )


def test_local_profile_fills_unique_requester_placeholders_only() -> None:
    draft = render.render("SONGZANLIN_EIA_2025")
    out = compiler.compile_profile(draft, _profile())

    assert out["status"] == (
        "DRAFT_REQUESTER_FILLED_AWAITING_HUMAN_REVIEW"
    )
    assert out["requester_profile_reference"] == "LOCAL-PROFILE-TEST-001"
    assert out["send_policy"]["human_review_approved"] is False
    assert out["send_policy"]["automatic_send_allowed"] is False

    for message in out["messages"]:
        assert message["status"] == (
            "DRAFT_REQUESTER_FILLED_AWAITING_HUMAN_REVIEW"
        )
        assert "REQUIRED_BEFORE_SEND" not in message["body_cn"]
        assert "REQUIRED_BEFORE_SEND" not in message["body_en"]
        assert "TEST REQUESTER" in message["body_cn"]
        assert "TEST INSTITUTION" in message["body_cn"]
        assert "test.requester@example.org" in message["body_cn"]
        assert "TEST REQUESTER" in message["body_en"]
        assert message["send_guard"]["requester_identity_filled"] is True
        assert message["send_guard"]["institution_filled"] is True
        assert message["send_guard"]["reply_contact_filled"] is True
        assert message["send_guard"]["human_review_approved"] is False


def test_requester_filled_draft_can_only_become_ready_after_human_review() -> None:
    filled = compiler.compile_profile(
        render.render("SONGZANLIN_EIA_2025"),
        _profile(),
    )
    ready = guard.validate_and_prepare(
        filled,
        human_review_approved=True,
        review_receipt=_approved_review(filled),
    )
    assert ready["status"] == "READY_FOR_MANUAL_SEND"
    assert ready["send_policy"]["manual_send_only"] is True
    assert ready["send_policy"]["automatic_send_allowed"] is False
    assert ready["send_policy"]["human_review_approved"] is True
    assert all(
        len(message["message_content_sha256_cn"]) == 64
        and len(message["message_content_sha256_en"]) == 64
        and len(message["message_content_sha256_bilingual"]) == 64
        for message in ready["messages"]
    )


def test_unreviewed_requester_filled_draft_does_not_become_send_ready() -> None:
    filled = compiler.compile_profile(
        render.render("SONGZANLIN_EIA_2025"),
        _profile(),
    )
    out = guard.validate_and_prepare(
        filled,
        human_review_approved=False,
    )
    assert out["status"] == "DRAFT_NOT_SENT"
    assert out["send_policy"]["human_review_approved"] is False
    assert all(
        message["status"] == "DRAFT_NOT_SENT"
        for message in out["messages"]
    )


def test_profile_must_be_local_filled_status() -> None:
    profile = _profile()
    profile["status"] = "TEMPLATE_ONLY_NOT_DATA"
    with pytest.raises(ValueError, match="not LOCAL_PROFILE_FILLED"):
        compiler.compile_profile(
            render.render("SONGZANLIN_EIA_2025"),
            profile,
        )


def test_profile_email_must_be_valid() -> None:
    profile = _profile()
    profile["contact_email"] = "not-an-email"
    with pytest.raises(ValueError, match="valid email address"):
        compiler.compile_profile(
            render.render("SONGZANLIN_EIA_2025"),
            profile,
        )


def test_profile_compiler_rejects_missing_field_specific_placeholder() -> None:
    draft = render.render("SONGZANLIN_EIA_2025")
    draft["messages"][0]["body_en"] = draft["messages"][0][
        "body_en"
    ].replace("REQUIRED_BEFORE_SEND_EMAIL", "MISSING")
    with pytest.raises(ValueError, match="must contain exactly one"):
        compiler.compile_profile(draft, _profile())


def test_profile_compiler_does_not_accept_already_reviewed_messages() -> None:
    draft = render.render("SONGZANLIN_EIA_2025")
    for message in draft["messages"]:
        message["body_cn"] = message["body_cn"].replace(
            "REQUIRED_BEFORE_SEND",
            "PROJECT_CONTACT",
        )
        message["body_en"] = message["body_en"].replace(
            "REQUIRED_BEFORE_SEND",
            "PROJECT_CONTACT",
        )
    ready = guard.validate_and_prepare(
        draft,
        human_review_approved=True,
        review_receipt=_approved_review(draft),
    )
    with pytest.raises(ValueError, match="requires DRAFT_NOT_SENT"):
        compiler.compile_profile(ready, _profile())



def test_review_draft_binds_to_requester_filled_bilingual_hash() -> None:
    filled = compiler.compile_profile(
        render.render("SONGZANLIN_EIA_2025"),
        _profile(),
    )
    receipt = review.build_review_draft(filled)
    assert receipt["status"] == "DRAFT_REVIEW_NOT_APPROVED"
    assert receipt["candidate_id"] == "SONGZANLIN_EIA_2025"
    assert len(receipt["route_reviews"]) == len(filled["messages"])
    for route in receipt["route_reviews"]:
        assert len(route["reviewed_message_sha256_bilingual"]) == 64
        assert all(value is False for value in route["checks"].values())
        assert route["approved_for_manual_send"] is False
