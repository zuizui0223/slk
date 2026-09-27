from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "EMPIRICAL_COMPANION_MIGRATION_MANIFEST_V1.json"

RECEIPT_SCHEMA = "SLK_EMPIRICAL_COMPANION_DESTINATION_RECEIPT_V1"
READY_STATUS = "DESTINATION_COPY_VERIFIED"


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _filled(value: object, label: str) -> str:
    if value is None:
        raise ValueError(f"unresolved {label}")
    text = str(value).strip()
    _need(
        bool(text)
        and "REQUIRED_BEFORE_USE" not in text
        and text.lower() not in {"none", "null"},
        f"unresolved {label}",
    )
    return text


def validate_destination(receipt: dict) -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    _need(
        manifest.get("schema_version")
        == "SLK_EMPIRICAL_COMPANION_MIGRATION_MANIFEST_V1",
        "wrong migration manifest schema",
    )
    _need(
        manifest.get("status")
        == "SOURCE_SNAPSHOT_FROZEN_DESTINATION_NOT_YET_RECORDED",
        "migration manifest source state changed",
    )
    expected = manifest.get("files")
    _need(isinstance(expected, list) and expected, "migration manifest files missing")
    _need(
        len(expected) == manifest.get("file_count"),
        "migration manifest file count mismatch",
    )
    _need(
        len(expected) == len(set(expected)),
        "migration manifest contains duplicate paths",
    )

    _need(
        receipt.get("schema_version") == RECEIPT_SCHEMA,
        "wrong destination receipt schema",
    )
    _need(
        receipt.get("status") == READY_STATUS,
        "destination receipt is not verified",
    )
    destination_repository = _filled(
        receipt.get("destination_repository"),
        "destination_repository",
    )
    _need(
        re.fullmatch(r"[^/\s]+/[^/\s]+", destination_repository) is not None,
        "destination_repository must be owner/name",
    )
    destination_commit = _filled(
        receipt.get("destination_commit"),
        "destination_commit",
    )
    _need(
        re.fullmatch(r"[0-9a-fA-F]{40}", destination_commit) is not None,
        "destination_commit must be a full 40-character Git SHA",
    )
    _need(
        receipt.get("destination_ci_verified") is True,
        "destination CI is not verified",
    )
    _filled(
        receipt.get("verification_reference"),
        "verification_reference",
    )

    copied = receipt.get("copied_files")
    _need(
        isinstance(copied, list),
        "destination copied_files must be a list",
    )
    _need(
        len(copied) == len(set(copied)),
        "destination copied_files contains duplicates",
    )
    expected_set = set(expected)
    copied_set = set(copied)
    missing = sorted(expected_set - copied_set)
    extra = sorted(copied_set - expected_set)
    _need(
        not missing and not extra,
        f"destination file inventory mismatch: missing={missing}; extra={extra}",
    )

    return {
        "schema_version": "SLK_EMPIRICAL_COMPANION_MIGRATION_READINESS_V1",
        "status": "READY_TO_PRUNE_SLK",
        "source_repository": manifest["source_repository"],
        "source_commit": manifest["source_commit"],
        "archive_branch": manifest["archive_branch"],
        "destination_repository": destination_repository,
        "destination_commit": destination_commit.lower(),
        "file_count": len(expected),
        "destination_ci_verified": True,
        "slk_deletion_authorized": True,
        "claim_ceiling": (
            "REPOSITORY_MIGRATION_READINESS_ONLY_NO_SCIENTIFIC_CLAIM_CHANGE"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a Pedicularis empirical-companion destination receipt "
            "against the frozen SLK migration manifest."
        )
    )
    parser.add_argument("destination_receipt_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = json.loads(
        args.destination_receipt_json.read_text(encoding="utf-8")
    )
    result = validate_destination(receipt)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
