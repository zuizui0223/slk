from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_empirical_companion_export.py"
MANIFEST = ROOT / "data" / "EMPIRICAL_COMPANION_MIGRATION_MANIFEST_V1.json"

spec = importlib.util.spec_from_file_location("companion_export", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_export_copies_exact_frozen_operational_inventory(tmp_path: Path) -> None:
    out = tmp_path / "companion"
    result = mod.build_export(ROOT, out)
    manifest = json.loads(MANIFEST.read_text())

    assert result["status"] == "TRANSFER_PACKAGE_BUILT"
    assert result["copied_file_count"] == manifest["file_count"] == 160
    assert result["copied_files"] == manifest["files"]

    for rel in manifest["files"]:
        assert (out / rel).is_file()
        assert (out / rel).read_bytes() == (ROOT / rel).read_bytes()

    assert not (out / "theory").exists()
    assert not (out / "manuscript").exists()
    assert not (out / "figures").exists()


def test_export_contains_only_declared_support_and_generated_infrastructure(
    tmp_path: Path,
) -> None:
    out = tmp_path / "companion"
    result = mod.build_export(ROOT, out)

    assert result["support_files"] == ["pytest.ini"]
    assert (out / "pytest.ini").is_file()
    assert (out / ".github" / "workflows" / "test.yml").is_file()
    assert (out / "README.md").is_file()
    assert (out / "COMPANION_EXPORT_MANIFEST.json").is_file()
    assert (out / "SHA256SUMS.txt").is_file()

    payload = json.loads((out / "COMPANION_EXPORT_MANIFEST.json").read_text())
    assert payload["copied_files"] == result["copied_files"]
    assert payload["copied_file_count"] == 160


def test_export_checksum_ledger_matches_all_source_copies(tmp_path: Path) -> None:
    out = tmp_path / "companion"
    result = mod.build_export(ROOT, out)
    rows = (out / "SHA256SUMS.txt").read_text().splitlines()
    observed = {}
    for row in rows:
        digest, rel = row.split("  ", 1)
        observed[rel] = digest

    expected_paths = result["copied_files"] + result["support_files"]
    assert set(observed) == set(expected_paths)
    for rel in expected_paths:
        assert observed[rel] == _sha256(out / rel)


def test_export_refuses_nonempty_destination(tmp_path: Path) -> None:
    out = tmp_path / "companion"
    out.mkdir()
    (out / "existing.txt").write_text("occupied")
    try:
        mod.build_export(ROOT, out)
    except ValueError as exc:
        assert "output directory is not empty" in str(exc)
    else:
        raise AssertionError("nonempty destination should fail closed")
