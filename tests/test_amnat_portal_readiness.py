from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_amnat_portal_readiness.py"
TEMPLATE = ROOT / "submission" / "AMNAT_PORTAL_INPUT_TEMPLATE_V1.json"

spec = importlib.util.spec_from_file_location("portal_readiness", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def _template() -> dict:
    return json.loads(TEMPLATE.read_text(encoding="utf-8"))


def _ready_receipt() -> dict:
    return {
        "schema_version": "SLK_AMNAT_REVIEWER_ZIP_RECEIPT_V1",
        "status": "EDITORIAL_MANAGER_ZIP_READY",
        "current_for_submission": True,
        "reviewer_zip_filename": "SLK_AMNAT_REVIEWER_DATA_CODE_BUNDLE_FINAL.zip",
        "reviewer_zip_sha256": "1" * 64,
    }


def _complete_initial() -> dict:
    payload = _template()
    payload["authors"] = [
        {
            "name": "Author One",
            "affiliation": "Institution One",
            "email": "author@example.org",
            "corresponding": True,
            "orcid": "",
        }
    ]
    payload["acknowledgments"] = {"status": "NONE", "text": ""}
    payload["author_contributions"] = "Author One: conceptualization, writing, validation."
    payload["ai_disclosure"]["approved"] = True
    payload["preprint"] = {"status": "NO", "reference": ""}
    payload["data_sharing_policy_agreed"] = True
    payload["reviewer_access"]["zip_sha256"] = "1" * 64
    payload["reviewer_access"]["package_status"] = "CURRENT_VERIFIED_PACKAGE"
    payload["reviewer_access"]["uploaded"] = True
    payload["archive"].update(
        {
            "provider": "ZENODO",
            "deposit_created": True,
            "reference": "ZENODO-DRAFT-123",
            "private_for_review": True,
        }
    )
    payload["portal"].update(
        {
            "manuscript_uploaded": True,
            "anonymous_title_page_uploaded": True,
            "generated_pdf_verified": True,
        }
    )
    payload["all_author_approval"] = True
    return payload


def test_template_is_fail_closed() -> None:
    result = mod.assess(_template())
    assert result["status"] == "BLOCKED"
    assert "author_list" in result["missing"]
    assert "initial_archive_deposit_created" in result["missing"]
    assert "reviewer_zip_uploaded" in result["missing"]
    assert "ai_disclosure_author_approval" in result["missing"]
    assert "all_author_approval" in result["missing"]


def test_stale_receipt_blocks_otherwise_complete_submission() -> None:
    stale = _ready_receipt()
    stale["status"] = "STALE_AFTER_MANUSCRIPT_CHANGE"
    stale["current_for_submission"] = False
    result = mod.assess(
        _complete_initial(), reviewer_zip_receipt=stale
    )
    assert result["status"] == "BLOCKED"
    assert "reviewer_zip_current_receipt" in result["missing"]
    assert result["reviewer_zip_receipt_current"] is False


def test_complete_initial_submission_is_ready_with_current_receipt() -> None:
    result = mod.assess(
        _complete_initial(), reviewer_zip_receipt=_ready_receipt()
    )
    assert result["status"] == "READY_TO_SUBMIT"
    assert result["missing"] == []
    assert result["reviewer_zip_receipt_current"] is True


def test_reviewer_zip_must_match_registered_receipt() -> None:
    payload = _complete_initial()
    payload["reviewer_access"]["zip_sha256"] = "0" * 64
    result = mod.assess(payload, reviewer_zip_receipt=_ready_receipt())
    assert result["status"] == "BLOCKED"
    assert "reviewer_zip_sha256_matches_receipt" in result["missing"]


def test_publication_phase_requires_doi_and_public_release() -> None:
    payload = _complete_initial()
    result = mod.assess(
        payload, phase="publication", reviewer_zip_receipt=_ready_receipt()
    )
    assert result["status"] == "BLOCKED"
    assert "permanent_archive_doi" in result["missing"]
    assert "archive_public_release_ready" in result["missing"]

    payload["archive"]["doi"] = "10.5281/zenodo.1234567"
    payload["archive"]["public_release_ready"] = True
    result = mod.assess(
        payload, phase="publication", reviewer_zip_receipt=_ready_receipt()
    )
    assert result["status"] == "READY_FOR_PUBLICATION"
    assert result["missing"] == []


def test_exactly_one_corresponding_author_is_required() -> None:
    payload = _complete_initial()
    second = copy.deepcopy(payload["authors"][0])
    second["name"] = "Author Two"
    second["email"] = "two@example.org"
    payload["authors"].append(second)
    result = mod.assess(payload)
    assert "exactly_one_corresponding_author" in result["missing"]
