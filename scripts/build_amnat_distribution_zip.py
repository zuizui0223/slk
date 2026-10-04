from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

try:
    from scripts.build_anonymous_review_bundle import build as build_bundle
except ImportError:  # direct execution via python scripts/...
    from build_anonymous_review_bundle import build as build_bundle

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GENERATED = ROOT / "submission" / "amnat_review" / "generated"
DEFAULT_BUNDLE = DEFAULT_GENERATED / "reviewer_bundle"
DEFAULT_ZIP = DEFAULT_GENERATED / "SLK_AMNAT_REVIEWER_DATA_CODE_BUNDLE_FINAL.zip"
DEFAULT_RECEIPT = DEFAULT_GENERATED / "DISTRIBUTION_ZIP_BUILD_RECEIPT.json"

# ZIP timestamps cannot predate 1980. A fixed timestamp plus sorted paths and
# fixed file permissions makes the distribution archive byte-reproducible.
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
FILE_MODE = 0o100644 << 16


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_deterministic_zip(bundle_dir: Path, output_zip: Path) -> dict[str, object]:
    if not bundle_dir.is_dir():
        raise FileNotFoundError(bundle_dir)

    files = sorted(
        path for path in bundle_dir.rglob("*")
        if path.is_file()
    )
    if not files:
        raise ValueError("reviewer bundle is empty")

    output_zip.parent.mkdir(parents=True, exist_ok=True)
    if output_zip.exists():
        output_zip.unlink()

    with zipfile.ZipFile(
        output_zip,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for path in files:
            rel = path.relative_to(bundle_dir).as_posix()
            info = zipfile.ZipInfo(rel, date_time=FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = FILE_MODE
            info.flag_bits |= 0x800  # UTF-8 names
            archive.writestr(info, path.read_bytes())

    with zipfile.ZipFile(output_zip, "r") as archive:
        names = archive.namelist()
        if names != sorted(names):
            raise RuntimeError("distribution ZIP paths are not sorted")
        if len(names) != len(set(names)):
            raise RuntimeError("distribution ZIP contains duplicate paths")
        for member in archive.infolist():
            if member.date_time != FIXED_ZIP_TIME:
                raise RuntimeError(f"non-fixed ZIP timestamp: {member.filename}")
            if member.is_dir():
                raise RuntimeError(f"directory member not allowed: {member.filename}")

    return {
        "schema_version": "SLK_AMNAT_DISTRIBUTION_ZIP_BUILD_RECEIPT_V1",
        "status": "DETERMINISTIC_REVIEWER_ZIP_BUILT",
        "reviewer_zip_filename": output_zip.name,
        "reviewer_zip_sha256": sha256(output_zip),
        "reviewer_zip_size_bytes": output_zip.stat().st_size,
        "reviewer_zip_file_count": len(files),
        "fixed_zip_timestamp": "1980-01-01T00:00:00",
        "sorted_paths": True,
        "cache_files_included": any(
            "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}
            for path in files
        ),
        "bundle_identity_audit": (
            bundle_dir / "ANONYMITY_AUDIT.txt"
        ).read_text(encoding="utf-8").splitlines()[0],
    }


def build_distribution(
    *,
    bundle_dir: Path = DEFAULT_BUNDLE,
    output_zip: Path = DEFAULT_ZIP,
    receipt_path: Path = DEFAULT_RECEIPT,
    rebuild_bundle: bool = True,
) -> dict[str, object]:
    if rebuild_bundle:
        build_bundle(bundle_dir)

    receipt = write_deterministic_zip(bundle_dir, output_zip)
    if receipt["cache_files_included"]:
        raise RuntimeError("cache/bytecode files entered reviewer ZIP")
    if receipt["bundle_identity_audit"] != "identity_scan=PASS":
        raise RuntimeError("reviewer bundle anonymity audit did not pass")

    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build byte-reproducible anonymous reviewer distribution ZIP"
    )
    parser.add_argument("--bundle-dir", type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--output-zip", type=Path, default=DEFAULT_ZIP)
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument(
        "--no-rebuild-bundle",
        action="store_true",
        help="Package an already-built reviewer bundle.",
    )
    args = parser.parse_args()

    receipt = build_distribution(
        bundle_dir=args.bundle_dir,
        output_zip=args.output_zip,
        receipt_path=args.receipt,
        rebuild_bundle=not args.no_rebuild_bundle,
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
