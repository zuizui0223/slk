from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZIP_RECEIPT = ROOT / "submission" / "AMNAT_REVIEWER_ZIP_RECEIPT_V1.json"

SCHEMA = "SLK_AMNAT_PORTAL_INPUT_V1"
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _text(value: object) -> str:
    return "" if value is None else str(value).strip()


def _filled(value: object) -> bool:
    text = _text(value)
    if not text:
        return False
    upper = text.upper()
    return not any(token in upper for token in ("[REQUIRED", "[PENDING", "TBD", "REQUIRED_BEFORE_USE"))


def assess(payload: dict, phase: str = "initial_submission") -> dict:
    if phase not in {"initial_submission", "publication"}:
        raise ValueError("phase must be initial_submission or publication")

    missing: list[str] = []
    warnings: list[str] = []

    if payload.get("schema_version") != SCHEMA:
        missing.append("valid_schema_version")

    authors = payload.get("authors")
    if not isinstance(authors, list) or not authors:
        missing.append("author_list")
        authors = []
    else:
        corresponding = 0
        for index, author in enumerate(authors, start=1):
            if not isinstance(author, dict):
                missing.append(f"author_{index}_record")
                continue
            if not _filled(author.get("name")):
                missing.append(f"author_{index}_name")
            if not _filled(author.get("affiliation")):
                missing.append(f"author_{index}_affiliation")
            email = _text(author.get("email"))
            if not EMAIL_RE.fullmatch(email):
                missing.append(f"author_{index}_email")
            if author.get("corresponding") is True:
                corresponding += 1
        if corresponding != 1:
            missing.append("exactly_one_corresponding_author")

    acknowledgments = payload.get("acknowledgments")
    if not isinstance(acknowledgments, dict):
        missing.append("acknowledgments_status")
    else:
        status = acknowledgments.get("status")
        if status not in {"NONE", "PROVIDED"}:
            missing.append("acknowledgments_status_NONE_or_PROVIDED")
        elif status == "PROVIDED" and not _filled(acknowledgments.get("text")):
            missing.append("acknowledgments_text")

    if not _filled(payload.get("author_contributions")):
        missing.append("author_contributions")

    ai = payload.get("ai_disclosure")
    if not isinstance(ai, dict):
        missing.append("ai_disclosure")
    else:
        if ai.get("approved") is not True:
            missing.append("ai_disclosure_author_approval")
        if not _filled(ai.get("text")):
            missing.append("ai_disclosure_text")

    preprint = payload.get("preprint")
    if not isinstance(preprint, dict):
        missing.append("preprint_status")
    else:
        status = preprint.get("status")
        if status not in {"NO", "YES"}:
            missing.append("preprint_status_NO_or_YES")
        elif status == "YES" and not _filled(preprint.get("reference")):
            missing.append("preprint_reference")

    if payload.get("data_sharing_policy_agreed") is not True:
        missing.append("data_sharing_policy_agreement")

    receipt = json.loads(ZIP_RECEIPT.read_text(encoding="utf-8"))
    access = payload.get("reviewer_access")
    if not isinstance(access, dict):
        missing.append("reviewer_access")
    else:
        if access.get("route") != "EDITORIAL_MANAGER_ZIP":
            missing.append("reviewer_access_route_EDITORIAL_MANAGER_ZIP")
        if access.get("zip_filename") != receipt["reviewer_zip_filename"]:
            missing.append("reviewer_zip_filename_matches_receipt")
        if access.get("zip_sha256") != receipt["reviewer_zip_sha256"]:
            missing.append("reviewer_zip_sha256_matches_receipt")
        if access.get("uploaded") is not True:
            missing.append("reviewer_zip_uploaded")

    archive = payload.get("archive")
    if not isinstance(archive, dict):
        missing.append("archive_deposit")
    else:
        if not _filled(archive.get("provider")):
            missing.append("archive_provider")
        if archive.get("deposit_created") is not True:
            missing.append("initial_archive_deposit_created")
        if not _filled(archive.get("reference")):
            missing.append("initial_archive_reference")
        if phase == "publication":
            doi = _text(archive.get("doi"))
            if not doi:
                missing.append("permanent_archive_doi")
            elif not doi.lower().startswith("10."):
                warnings.append("archive_doi_does_not_start_with_10")
            if archive.get("public_release_ready") is not True:
                missing.append("archive_public_release_ready")

    portal = payload.get("portal")
    if not isinstance(portal, dict):
        missing.append("portal_upload_state")
    else:
        if portal.get("manuscript_uploaded") is not True:
            missing.append("anonymous_manuscript_uploaded")
        if portal.get("anonymous_title_page_uploaded") is not True:
            missing.append("anonymous_title_page_uploaded")
        if portal.get("generated_pdf_verified") is not True:
            missing.append("editorial_manager_generated_pdf_verified")

    if payload.get("all_author_approval") is not True:
        missing.append("all_author_approval")

    status = "READY_TO_SUBMIT" if not missing and phase == "initial_submission" else (
        "READY_FOR_PUBLICATION" if not missing else "BLOCKED"
    )
    return {
        "schema_version": "SLK_AMNAT_PORTAL_READINESS_V1",
        "phase": phase,
        "status": status,
        "missing": sorted(set(missing)),
        "warnings": sorted(set(warnings)),
        "reviewer_zip_sha256": receipt["reviewer_zip_sha256"],
        "claim_ceiling": "SUBMISSION_READINESS_ONLY_NO_SCIENTIFIC_CLAIM_CHANGE",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Assess the minimal human-controlled Am Nat submission gate."
    )
    parser.add_argument("portal_input_json", type=Path)
    parser.add_argument(
        "--phase",
        choices=("initial_submission", "publication"),
        default="initial_submission",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--allow-blocked",
        action="store_true",
        help="Exit successfully even when required fields are still missing.",
    )
    args = parser.parse_args()

    payload = json.loads(args.portal_input_json.read_text(encoding="utf-8"))
    result = assess(payload, phase=args.phase)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")

    if result["status"] == "BLOCKED" and not args.allow_blocked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
