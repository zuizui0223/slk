from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "PEDICULARIS_CONTEXT_CANDIDATE_LEDGER_V1.csv"
QUEUE = ROOT / "data" / "PEDICULARIS_CONTEXT_RECOVERY_QUEUE_V1.csv"
WAVES = {"WAVE1", "WAVE2", "WAVE3"}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validate() -> dict:
    ledger = _read(LEDGER)
    queue = _read(QUEUE)
    ledger_ids = [row["candidate_id"].strip() for row in ledger]
    queue_ids = [row["candidate_id"].strip() for row in queue]

    if len(ledger_ids) != len(set(ledger_ids)):
        raise ValueError("duplicate candidate_id in candidate ledger")
    if len(queue_ids) != len(set(queue_ids)):
        raise ValueError("duplicate candidate_id in recovery queue")
    if set(queue_ids) != set(ledger_ids):
        missing = sorted(set(ledger_ids) - set(queue_ids))
        extra = sorted(set(queue_ids) - set(ledger_ids))
        raise ValueError(f"recovery queue inventory mismatch: missing={missing}; extra={extra}")

    by_id = {row["candidate_id"].strip(): row for row in ledger}
    wave_counts = {wave: 0 for wave in WAVES}
    for row in queue:
        candidate_id = row["candidate_id"].strip()
        wave = row["recovery_wave"].strip()
        basis = row["selection_basis"].strip()
        reason = row["reason"].strip()
        if wave not in WAVES:
            raise ValueError(f"invalid recovery wave: {candidate_id}/{wave}")
        if not basis or not reason:
            raise ValueError(f"incomplete recovery queue rationale: {candidate_id}")
        wave_counts[wave] += 1

        priority = by_id[candidate_id]["priority_for_fresh_p0"].strip()
        if wave == "WAVE1" and priority != "HIGH":
            raise ValueError(f"WAVE1 candidate must be HIGH priority: {candidate_id}")
        if priority == "LOW" and wave != "WAVE3":
            raise ValueError(f"LOW-priority candidate must remain WAVE3: {candidate_id}")

    return {
        "schema_version": "SLK_PEDICULARIS_CONTEXT_RECOVERY_QUEUE_RECEIPT_V1",
        "status": "RECOVERY_QUEUE_VALIDATED",
        "candidate_count": len(queue),
        "wave_counts": wave_counts,
        "wave1_candidates": [
            row["candidate_id"].strip()
            for row in queue
            if row["recovery_wave"].strip() == "WAVE1"
        ],
        "claim_ceiling": "RECOVERY_ORDER_ONLY_NO_FRESH_CONTEXT_OR_BIOLOGICAL_RESULT",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the Pedicularis context-recovery queue against the candidate ledger")
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
