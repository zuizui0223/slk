from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "data" / "EMPIRICAL_COMPANION_EXPORT_RECEIPT_V1.json"
MANIFEST = ROOT / "data" / "EMPIRICAL_COMPANION_MIGRATION_MANIFEST_V1.json"


def test_transfer_package_receipt_closes_export_stage_without_authorizing_pruning() -> None:
    receipt = json.loads(RECEIPT.read_text())
    manifest = json.loads(MANIFEST.read_text())

    assert receipt["schema_version"] == "SLK_EMPIRICAL_COMPANION_EXPORT_RECEIPT_V1"
    assert receipt["status"] == "TRANSFER_PACKAGE_STANDALONE_VERIFIED"
    assert receipt["frozen_source_commit"] == manifest["source_commit"]
    assert receipt["copied_file_count"] == manifest["file_count"] == 160
    assert receipt["standalone_pytest_passed"] == 446
    assert receipt["standalone_pytest_failed"] == 0
    assert len(receipt["artifact_zip_sha256"]) == 64
    assert receipt["artifact_size_bytes"] > 0

    assert receipt["destination_repository"] is None
    assert receipt["destination_commit"] is None
    assert receipt["destination_ci_verified"] is False
    assert receipt["slk_deletion_authorized"] is False
