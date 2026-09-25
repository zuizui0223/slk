from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data" / "PEDICULARIS_CONTEXT_RECOVERY_QUEUE_V1.csv"
ANCHORS = ROOT / "data" / "PEDICULARIS_WAVE1_RECOVERY_ACCESS_ANCHORS_V1.csv"


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validate() -> dict:
    queue = _read(QUEUE)
    anchors = _read(ANCHORS)
    wave1 = {
        row["candidate_id"].strip()
        for row in queue
        if row["recovery_wave"].strip() == "WAVE1"
    }
    ids = [row["candidate_id"].strip() for row in anchors]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate WAVE1 access anchor candidate_id")
    if set(ids) != wave1:
        raise ValueError(
            "WAVE1 access-anchor inventory mismatch: "
            f"expected={sorted(wave1)} observed={sorted(set(ids))}"
        )

    for row in anchors:
        candidate_id = row["candidate_id"].strip()
        if row["recovery_wave"].strip() != "WAVE1":
            raise ValueError(f"access anchor must remain WAVE1: {candidate_id}")
        if not row["evidence_date"].strip():
            raise ValueError(f"missing access-anchor date: {candidate_id}")
        if not row["evidence_type"].strip():
            raise ValueError(f"missing access-anchor type: {candidate_id}")
        if not row["source_reference"].strip() or not row["source_url"].strip():
            raise ValueError(f"missing access-anchor source: {candidate_id}")
        if not row["current_access_signal"].strip():
            raise ValueError(f"missing current access signal: {candidate_id}")
        if row["sampling_permission_status"].strip() != "UNRESOLVED":
            raise ValueError(
                f"preflight anchor cannot resolve sampling permission: {candidate_id}"
            )
        if row["permitted_use"].strip() != "RECOVERY_PREFLIGHT_ONLY":
            raise ValueError(f"access anchor use changed: {candidate_id}")

    return {
        "schema_version": "SLK_PEDICULARIS_WAVE1_ACCESS_ANCHORS_RECEIPT_V1",
        "status": "WAVE1_ACCESS_PREFLIGHT_ANCHORS_VALIDATED",
        "candidate_count": len(anchors),
        "candidate_ids": ids,
        "sampling_permission_status": "UNRESOLVED_FOR_ALL",
        "claim_ceiling": (
            "CURRENT_OPERATIONAL_ACCESS_PREFLIGHT_ONLY_NO_SAMPLING_PERMISSION_"
            "NO_FRESH_CONTEXT_NO_BIOLOGICAL_RESULT"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate current operational access anchors for Pedicularis WAVE1"
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = validate()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
