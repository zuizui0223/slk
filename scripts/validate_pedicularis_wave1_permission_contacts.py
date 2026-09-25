from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data" / "PEDICULARIS_CONTEXT_RECOVERY_QUEUE_V1.csv"
ROUTES = ROOT / "data" / "PEDICULARIS_WAVE1_PERMISSION_CONTACT_ROUTES_V1.csv"

ALLOWED_ROUTE_TYPES = {
    "REGULATORY_ROUTING",
    "SITE_MANAGEMENT_ROUTING",
    "LOCAL_TERRITORIAL_ROUTING",
    "INSTITUTIONAL_SITE_ROUTING",
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validate() -> dict:
    queue = _read(QUEUE)
    routes = _read(ROUTES)
    wave1 = {
        row["candidate_id"].strip()
        for row in queue
        if row["recovery_wave"].strip() == "WAVE1"
    }

    route_ids = [row["route_id"].strip() for row in routes]
    if len(route_ids) != len(set(route_ids)):
        raise ValueError("duplicate permission-contact route_id")

    by_candidate: dict[str, list[dict[str, str]]] = defaultdict(list)
    route_type_counts: Counter[str] = Counter()

    for row in routes:
        candidate_id = row["candidate_id"].strip()
        if candidate_id not in wave1:
            raise ValueError(f"permission route candidate is not WAVE1: {candidate_id}")
        if row["recovery_wave"].strip() != "WAVE1":
            raise ValueError(f"permission route wave changed: {candidate_id}")
        route_type = row["route_type"].strip()
        if route_type not in ALLOWED_ROUTE_TYPES:
            raise ValueError(f"unregistered permission route type: {candidate_id}/{route_type}")
        for field in (
            "organization",
            "public_contact",
            "source_reference",
            "source_url",
            "question_to_resolve",
        ):
            if not row[field].strip():
                raise ValueError(f"missing permission route field {field}: {candidate_id}")
        if not row["source_url"].strip().startswith("https://"):
            raise ValueError(f"permission route source_url must be https: {candidate_id}")
        if row["permission_status"].strip() != "UNRESOLVED":
            raise ValueError(
                f"contact route cannot pre-resolve sampling permission: {candidate_id}"
            )
        if row["route_status"].strip() != "CONTACT_ROUTE_IDENTIFIED":
            raise ValueError(f"permission contact route status changed: {candidate_id}")
        by_candidate[candidate_id].append(row)
        route_type_counts[route_type] += 1

    if set(by_candidate) != wave1:
        missing = sorted(wave1 - set(by_candidate))
        raise ValueError(f"WAVE1 candidates missing permission contact routes: {missing}")

    for candidate_id in sorted(wave1):
        types = {row["route_type"].strip() for row in by_candidate[candidate_id]}
        if "REGULATORY_ROUTING" not in types:
            raise ValueError(
                f"WAVE1 candidate lacks regulatory routing contact: {candidate_id}"
            )

    return {
        "schema_version": "SLK_PEDICULARIS_WAVE1_PERMISSION_CONTACT_ROUTES_RECEIPT_V1",
        "status": "WAVE1_PERMISSION_CONTACT_ROUTES_VALIDATED",
        "candidate_count": len(wave1),
        "route_count": len(routes),
        "route_type_counts": dict(sorted(route_type_counts.items())),
        "permission_status": "UNRESOLVED_FOR_ALL",
        "candidate_route_counts": {
            candidate_id: len(by_candidate[candidate_id])
            for candidate_id in sorted(by_candidate)
        },
        "claim_ceiling": (
            "CONTACT_ROUTING_ONLY_NO_PERMISSION_GRANTED_NO_FRESH_CONTEXT_"
            "NO_P0_SIGNAL_NO_G1_G5_RESULT"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate official contact routes for Pedicularis WAVE1 permission inquiries"
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
