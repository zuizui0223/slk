from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_empirical_companion_destination.py"
MANIFEST = ROOT / "data" / "EMPIRICAL_COMPANION_MIGRATION_MANIFEST_V1.json"
TEMPLATE = ROOT / "data" / "EMPIRICAL_COMPANION_DESTINATION_RECEIPT_TEMPLATE_V1.json"

spec = importlib.util.spec_from_file_location("companion_destination", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def _receipt() -> dict:
    files = json.loads(MANIFEST.read_text())["files"]
    return {
        "schema_version": "SLK_EMPIRICAL_COMPANION_DESTINATION_RECEIPT_V1",
        "status": "DESTINATION_COPY_VERIFIED",
        "destination_repository": "zuizui0223/pedicularis-empirical",
        "destination_commit": "a" * 40,
        "destination_ci_verified": True,
        "copied_files": list(files),
        "verification_reference": "COMPANION-CI-001",
    }


def test_complete_verified_destination_authorizes_slk_pruning() -> None:
    out = mod.validate_destination(_receipt())
    assert out["status"] == "READY_TO_PRUNE_SLK"
    assert out["file_count"] == 160
    assert out["destination_ci_verified"] is True
    assert out["slk_deletion_authorized"] is True
    assert out["destination_repository"] == "zuizui0223/pedicularis-empirical"


def test_missing_destination_file_blocks_pruning() -> None:
    receipt = _receipt()
    receipt["copied_files"].pop()
    with pytest.raises(ValueError, match="destination file inventory mismatch"):
        mod.validate_destination(receipt)


def test_extra_destination_file_blocks_pruning() -> None:
    receipt = _receipt()
    receipt["copied_files"].append("extra/file.txt")
    with pytest.raises(ValueError, match="destination file inventory mismatch"):
        mod.validate_destination(receipt)


def test_duplicate_destination_file_blocks_pruning() -> None:
    receipt = _receipt()
    receipt["copied_files"].append(receipt["copied_files"][0])
    with pytest.raises(ValueError, match="contains duplicates"):
        mod.validate_destination(receipt)


def test_unverified_destination_ci_blocks_pruning() -> None:
    receipt = _receipt()
    receipt["destination_ci_verified"] = False
    with pytest.raises(ValueError, match="destination CI is not verified"):
        mod.validate_destination(receipt)


def test_short_destination_commit_blocks_pruning() -> None:
    receipt = _receipt()
    receipt["destination_commit"] = "abc123"
    with pytest.raises(ValueError, match="full 40-character Git SHA"):
        mod.validate_destination(receipt)


def test_unverified_receipt_status_blocks_pruning() -> None:
    receipt = _receipt()
    receipt["status"] = "TEMPLATE_ONLY_NOT_VERIFIED"
    with pytest.raises(ValueError, match="destination receipt is not verified"):
        mod.validate_destination(receipt)


def test_destination_template_cannot_authorize_pruning() -> None:
    template = json.loads(TEMPLATE.read_text())
    assert template["status"] == "TEMPLATE_ONLY_NOT_VERIFIED"
    assert template["destination_ci_verified"] is False
    with pytest.raises(ValueError, match="destination receipt is not verified"):
        mod.validate_destination(template)
