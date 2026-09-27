from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "EMPIRICAL_COMPANION_MIGRATION_MANIFEST_V1.json"
PATTERN = re.compile(
    r"^(?:docs|data|scripts|tests)/.*pedicularis.*",
    re.IGNORECASE,
)


def _manifest() -> dict:
    return json.loads(PATH.read_text())


def test_migration_manifest_freezes_complete_operational_inventory() -> None:
    payload = _manifest()
    assert payload["schema_version"] == (
        "SLK_EMPIRICAL_COMPANION_MIGRATION_MANIFEST_V1"
    )
    assert payload["source_repository"] == "zuizui0223/slk"
    assert payload["source_commit"] == (
        "0f632f7cfce12f04cb2106c24753ca976f30d677"
    )
    assert payload["archive_branch"] == (
        "archive/pedicularis-operations-2026-09-27"
    )

    files = payload["files"]
    assert len(files) == payload["file_count"] == 160
    assert len(files) == len(set(files))
    assert files == sorted(files)
    assert all(PATTERN.search(path) for path in files)

    assert payload["counts"] == {
        "docs": 30,
        "data": 39,
        "scripts": 50,
        "tests": 41,
    }


def test_migration_manifest_does_not_authorize_deletion_without_destination() -> None:
    payload = _manifest()
    assert payload["status"] == (
        "SOURCE_SNAPSHOT_FROZEN_DESTINATION_NOT_YET_RECORDED"
    )
    assert payload["destination_repository"] is None
    assert payload["destination_commit"] is None
    assert payload["destination_ci_verified"] is False
    assert payload["slk_deletion_authorized"] is False


def test_manifest_count_matches_root_breakdown() -> None:
    payload = _manifest()
    files = payload["files"]
    observed = {
        root: sum(path.startswith(root + "/") for path in files)
        for root in ("docs", "data", "scripts", "tests")
    }
    assert observed == payload["counts"]
    assert sum(observed.values()) == payload["file_count"]
