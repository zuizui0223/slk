from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "PEDICULARIS_CONTEXT_CANDIDATE_LEDGER_V1.csv"
QUEUE = ROOT / "data" / "PEDICULARIS_CONTEXT_RECOVERY_QUEUE_V1.csv"
LOCATORS = ROOT / "data" / "PEDICULARIS_CONTEXT_RECOVERY_SCOUTING_LOCATORS_V1.csv"


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _num(raw: str, label: str) -> float:
    try:
        x = float(str(raw).strip())
    except ValueError as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not math.isfinite(x):
        raise ValueError(f"{label} must be finite")
    return x


def validate() -> dict:
    ledger = {r["candidate_id"].strip(): r for r in _read(LEDGER)}
    queue = {r["candidate_id"].strip(): r for r in _read(QUEUE)}
    rows = _read(LOCATORS)
    ids = [r["candidate_id"].strip() for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate scouting candidate_id")

    for row in rows:
        candidate_id = row["candidate_id"].strip()
        if candidate_id not in ledger:
            raise ValueError(f"scouting candidate absent from ledger: {candidate_id}")
        if candidate_id not in queue:
            raise ValueError(f"scouting candidate absent from recovery queue: {candidate_id}")
        if row["recovery_wave"].strip() != queue[candidate_id]["recovery_wave"].strip():
            raise ValueError(f"scouting wave mismatch: {candidate_id}")
        if not row["source_reference"].strip() or not row["locator_claim"].strip():
            raise ValueError(f"scouting source/claim missing: {candidate_id}")

        kind = row["locator_type"].strip()
        if kind == "POINT":
            lat = _num(row["latitude_deg"], f"latitude/{candidate_id}")
            lon = _num(row["longitude_deg"], f"longitude/{candidate_id}")
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                raise ValueError(f"invalid point coordinates: {candidate_id}")
            if any(row[k].strip() for k in ("lat_min_deg","lat_max_deg","lon_min_deg","lon_max_deg")):
                raise ValueError(f"point row unexpectedly has envelope coordinates: {candidate_id}")
        elif kind == "ENVELOPE":
            lat_min = _num(row["lat_min_deg"], f"lat_min/{candidate_id}")
            lat_max = _num(row["lat_max_deg"], f"lat_max/{candidate_id}")
            lon_min = _num(row["lon_min_deg"], f"lon_min/{candidate_id}")
            lon_max = _num(row["lon_max_deg"], f"lon_max/{candidate_id}")
            if not (-90 <= lat_min <= lat_max <= 90):
                raise ValueError(f"invalid latitude envelope: {candidate_id}")
            if not (-180 <= lon_min <= lon_max <= 180):
                raise ValueError(f"invalid longitude envelope: {candidate_id}")
            if row["latitude_deg"].strip() or row["longitude_deg"].strip():
                raise ValueError(f"envelope row unexpectedly has point coordinates: {candidate_id}")
        else:
            raise ValueError(f"unsupported locator_type: {candidate_id}/{kind}")

    return {
        "schema_version": "SLK_PEDICULARIS_CONTEXT_RECOVERY_SCOUTING_LOCATORS_RECEIPT_V1",
        "status": "SCOUTING_LOCATORS_VALIDATED",
        "locator_count": len(rows),
        "wave1_locator_count": sum(r["recovery_wave"].strip() == "WAVE1" for r in rows),
        "candidate_ids": ids,
        "claim_ceiling": "SCOUTING_LOCATORS_ONLY_NO_FRESH_CONTEXT_OR_BIOLOGICAL_RESULT",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Pedicularis context-recovery scouting locators")
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
