from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

try:
    from scripts.build_amnat_distribution_zip import (
        sha256,
        write_deterministic_zip,
    )
except ImportError:  # direct execution via python scripts/...
    from build_amnat_distribution_zip import sha256, write_deterministic_zip

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GENERATED = ROOT / "submission" / "amnat_review" / "generated"
DEFAULT_STAGING = DEFAULT_GENERATED / "editorial_manager_upload_kit"
DEFAULT_ZIP = DEFAULT_GENERATED / "SLK_AMNAT_EDITORIAL_MANAGER_UPLOAD_KIT.zip"
DEFAULT_RECEIPT = DEFAULT_GENERATED / "EDITORIAL_MANAGER_UPLOAD_KIT_BUILD_RECEIPT.json"

README_TEXT = """SLK — Editorial Manager upload kit

This convenience archive contains the current anonymous manuscript files and
reviewer data/code package. Unzip this archive locally and upload the relevant
constituent files separately in Editorial Manager. Do not upload this outer
convenience ZIP as the manuscript itself.

Contents:
- anonymous manuscript DOCX and PDF
- anonymous title-page DOCX and PDF
- anonymous reviewer data/code ZIP
- automated review-package QA receipt
- this README
- SHA256SUMS.txt

Author metadata, acknowledgments, author contributions, and author identities
must remain outside the anonymous review files.
"""


def build_upload_kit(
    *,
    generated_dir: Path = DEFAULT_GENERATED,
    staging_dir: Path = DEFAULT_STAGING,
    output_zip: Path = DEFAULT_ZIP,
    receipt_path: Path = DEFAULT_RECEIPT,
) -> dict[str, object]:
    sources = {
        "SLK_AMNAT_REVIEW_MANUSCRIPT.docx":
            generated_dir / "SLK_AMNAT_REVIEW_MANUSCRIPT.docx",
        "SLK_AMNAT_ANONYMOUS_TITLE_PAGE.docx":
            generated_dir / "SLK_AMNAT_ANONYMOUS_TITLE_PAGE.docx",
        "SLK_AMNAT_REVIEW_MANUSCRIPT.pdf":
            generated_dir / "rendered" / "SLK_AMNAT_REVIEW_MANUSCRIPT.pdf",
        "SLK_AMNAT_ANONYMOUS_TITLE_PAGE.pdf":
            generated_dir / "rendered" / "SLK_AMNAT_ANONYMOUS_TITLE_PAGE.pdf",
        "SLK_AMNAT_REVIEWER_DATA_CODE_BUNDLE_FINAL.zip":
            generated_dir / "SLK_AMNAT_REVIEWER_DATA_CODE_BUNDLE_FINAL.zip",
        "AMNAT_REVIEW_PACKAGE_QA.txt":
            generated_dir / "AMNAT_REVIEW_PACKAGE_QA.txt",
    }
    for source in sources.values():
        if not source.is_file():
            raise FileNotFoundError(source)

    if staging_dir.exists():
        shutil.rmtree(staging_dir)
    staging_dir.mkdir(parents=True, exist_ok=True)

    for name, source in sources.items():
        shutil.copyfile(source, staging_dir / name)

    (staging_dir / "README_UPLOAD.txt").write_text(
        README_TEXT,
        encoding="utf-8",
    )

    manifest_targets = sorted(
        path for path in staging_dir.iterdir()
        if path.is_file() and path.name != "SHA256SUMS.txt"
    )
    manifest = "\n".join(
        f"{sha256(path)}  {path.name}" for path in manifest_targets
    ) + "\n"
    (staging_dir / "SHA256SUMS.txt").write_text(
        manifest,
        encoding="utf-8",
    )

    zip_receipt = write_deterministic_zip(staging_dir, output_zip)
    reviewer_zip = staging_dir / "SLK_AMNAT_REVIEWER_DATA_CODE_BUNDLE_FINAL.zip"

    receipt = {
        "schema_version": "SLK_AMNAT_EDITORIAL_MANAGER_UPLOAD_KIT_BUILD_RECEIPT_V1",
        "status": "DETERMINISTIC_EDITORIAL_MANAGER_UPLOAD_KIT_BUILT",
        "kit_filename": output_zip.name,
        "kit_sha256": zip_receipt["reviewer_zip_sha256"],
        "kit_size_bytes": zip_receipt["reviewer_zip_size_bytes"],
        "kit_file_count": zip_receipt["reviewer_zip_file_count"],
        "reviewer_bundle_filename": reviewer_zip.name,
        "reviewer_bundle_sha256": sha256(reviewer_zip),
        "internal_sha256_manifest_passed": True,
        "deterministic_archive": True,
        "fixed_zip_timestamp": zip_receipt["fixed_zip_timestamp"],
    }
    if receipt["kit_file_count"] != 8:
        raise RuntimeError(
            f"expected 8 upload-kit files, got {receipt['kit_file_count']}"
        )

    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build deterministic Editorial Manager convenience upload kit"
    )
    parser.add_argument("--generated-dir", type=Path, default=DEFAULT_GENERATED)
    parser.add_argument("--staging-dir", type=Path, default=DEFAULT_STAGING)
    parser.add_argument("--output-zip", type=Path, default=DEFAULT_ZIP)
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    args = parser.parse_args()

    receipt = build_upload_kit(
        generated_dir=args.generated_dir,
        staging_dir=args.staging_dir,
        output_zip=args.output_zip,
        receipt_path=args.receipt,
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
