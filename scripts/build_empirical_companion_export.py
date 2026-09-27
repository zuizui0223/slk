from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_REL = Path("data/EMPIRICAL_COMPANION_MIGRATION_MANIFEST_V1.json")
SUPPORT_FILES = ("pytest.ini",)

COMPANION_CI = """name: test

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  pytest:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install test dependency
        run: python -m pip install --upgrade pip pytest
      - name: Run empirical companion tests
        run: python -m pytest -q
"""


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_relative(path_text: str) -> Path:
    path = Path(path_text)
    _need(not path.is_absolute(), f"absolute manifest path is forbidden: {path_text}")
    _need(".." not in path.parts, f"parent traversal is forbidden: {path_text}")
    return path


def build_export(source_root: Path, output_dir: Path) -> dict:
    source_root = source_root.resolve()
    output_dir = output_dir.resolve()
    manifest_path = source_root / MANIFEST_REL
    _need(manifest_path.is_file(), "migration manifest is missing")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    _need(
        manifest.get("schema_version")
        == "SLK_EMPIRICAL_COMPANION_MIGRATION_MANIFEST_V1",
        "wrong migration manifest schema",
    )
    files = manifest.get("files")
    _need(isinstance(files, list) and files, "migration manifest files missing")
    _need(len(files) == manifest.get("file_count"), "manifest file count mismatch")
    _need(len(files) == len(set(files)), "manifest contains duplicate paths")

    if output_dir.exists():
        _need(
            not any(output_dir.iterdir()),
            f"output directory is not empty: {output_dir}",
        )
    else:
        output_dir.mkdir(parents=True)

    copied_files: list[str] = []
    checksum_rows: list[str] = []
    for rel_text in files:
        rel = _safe_relative(rel_text)
        src = source_root / rel
        _need(src.is_file(), f"manifest source file is missing: {rel_text}")
        dst = output_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied_files.append(rel_text)
        checksum_rows.append(f"{_sha256(dst)}  {rel_text}")

    support_files: list[str] = []
    for rel_text in SUPPORT_FILES:
        rel = _safe_relative(rel_text)
        src = source_root / rel
        _need(src.is_file(), f"support file is missing: {rel_text}")
        dst = output_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        support_files.append(rel_text)
        checksum_rows.append(f"{_sha256(dst)}  {rel_text}")

    workflow = output_dir / ".github" / "workflows" / "test.yml"
    workflow.parent.mkdir(parents=True, exist_ok=True)
    workflow.write_text(COMPANION_CI, encoding="utf-8")

    export_manifest = {
        "schema_version": "SLK_EMPIRICAL_COMPANION_EXPORT_V1",
        "status": "TRANSFER_PACKAGE_BUILT",
        "source_repository": manifest["source_repository"],
        "source_commit": manifest["source_commit"],
        "archive_branch": manifest["archive_branch"],
        "migration_manifest": MANIFEST_REL.as_posix(),
        "migration_manifest_sha256": _sha256(manifest_path),
        "copied_file_count": len(copied_files),
        "copied_files": copied_files,
        "support_files": support_files,
        "generated_files": [
            ".github/workflows/test.yml",
            "COMPANION_EXPORT_MANIFEST.json",
            "README.md",
            "SHA256SUMS.txt",
        ],
        "destination_receipt_rule": (
            "record only copied_files in the SLK destination receipt; "
            "support/generated files are companion infrastructure"
        ),
    }
    (output_dir / "COMPANION_EXPORT_MANIFEST.json").write_text(
        json.dumps(export_manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    readme = f"""# Pedicularis empirical companion transfer package

This directory was built mechanically from the frozen SLK empirical-companion
migration manifest.

- source repository: {manifest["source_repository"]}
- source commit: {manifest["source_commit"]}
- frozen operational files: {len(copied_files)}
- archive branch: {manifest["archive_branch"]}

The copied scientific/operational inventory is exactly the 160 paths listed in
`COMPANION_EXPORT_MANIFEST.json`. Root support files and the generated GitHub
Actions workflow are transfer infrastructure and are not part of the 160-file
destination-receipt inventory.

Before SLK pruning is authorized:

1. create the destination repository;
2. copy this package into it;
3. run the included CI successfully;
4. record the destination full commit SHA and the exact 160 copied paths in the
   SLK destination receipt;
5. validate that receipt with
   `scripts/check_empirical_companion_destination.py` in SLK.

This package does not change any scientific claim ceiling.
"""
    (output_dir / "README.md").write_text(readme, encoding="utf-8")
    (output_dir / "SHA256SUMS.txt").write_text(
        "\n".join(checksum_rows) + "\n",
        encoding="utf-8",
    )

    return export_manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build a transfer-ready empirical companion from the frozen "
            "SLK migration manifest."
        )
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        default=ROOT,
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
    )
    args = parser.parse_args()
    result = build_export(args.source_root, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
