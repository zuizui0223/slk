from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ROOT / "data" / "PEDICULARIS_WAVE1_PERMISSION_CONTACT_ROUTES_V1.csv"
QUEUE = ROOT / "data" / "PEDICULARIS_CONTEXT_RECOVERY_QUEUE_V1.csv"

OUTREACH_STATUSES = {
    "NOT_SENT",
    "SENT_AWAITING_RESPONSE",
    "ROUTED_TO_ANOTHER_AUTHORITY",
    "RESPONSE_RECEIVED",
    "CLOSED_NO_ACTION",
}
RESPONSE_STATUSES = {
    "NO_RESPONSE",
    "ROUTING_RESPONSE_ONLY",
    "SUBSTANTIVE_RESPONSE_RECEIVED",
    "CLOSED_NO_RESPONSE_EXPECTED",
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def generate_rows() -> list[dict[str, str]]:
    wave1 = {
        row["candidate_id"].strip()
        for row in _read(QUEUE)
        if row["recovery_wave"].strip() == "WAVE1"
    }
    rows = []
    for route in _read(ROUTES):
        candidate_id = route["candidate_id"].strip()
        if candidate_id not in wave1:
            continue
        rows.append(
            {
                "candidate_id": candidate_id,
                "recovery_wave": "WAVE1",
                "route_id": route["route_id"].strip(),
                "route_type": route["route_type"].strip(),
                "organization": route["organization"].strip(),
                "public_contact": route["public_contact"].strip(),
                "outreach_status": "NOT_SENT",
                "outreach_date": "",
                "outreach_reference": "",
                "response_status": "NO_RESPONSE",
                "response_date": "",
                "response_reference": "",
                "routed_to_organization": "",
                "routed_to_contact": "",
                "next_action": "SEND_REGISTERED_PERMISSION_INQUIRY",
                "notes": "",
            }
        )
    return rows


def validate(rows: list[dict[str, str]]) -> dict:
    canonical = {
        row["route_id"].strip(): row
        for row in _read(ROUTES)
        if row["recovery_wave"].strip() == "WAVE1"
    }
    wave1 = {
        row["candidate_id"].strip()
        for row in _read(QUEUE)
        if row["recovery_wave"].strip() == "WAVE1"
    }

    route_ids = [str(row.get("route_id", "")).strip() for row in rows]
    if len(route_ids) != len(set(route_ids)):
        raise ValueError("duplicate outreach ledger route_id")
    if set(route_ids) != set(canonical):
        missing = sorted(set(canonical) - set(route_ids))
        extra = sorted(set(route_ids) - set(canonical))
        raise ValueError(
            f"outreach ledger route inventory mismatch: missing={missing}; extra={extra}"
        )

    by_candidate: dict[str, list[dict[str, str]]] = defaultdict(list)
    status_counts: Counter[str] = Counter()
    substantive_responses = 0

    for row in rows:
        route_id = str(row.get("route_id", "")).strip()
        source = canonical[route_id]
        candidate_id = str(row.get("candidate_id", "")).strip()
        if candidate_id != source["candidate_id"].strip():
            raise ValueError(f"outreach candidate/route mismatch: {route_id}")
        if candidate_id not in wave1:
            raise ValueError(f"outreach candidate is not WAVE1: {candidate_id}")
        if str(row.get("recovery_wave", "")).strip() != "WAVE1":
            raise ValueError(f"outreach recovery wave changed: {route_id}")
        for field in ("route_type", "organization", "public_contact"):
            if str(row.get(field, "")).strip() != source[field].strip():
                raise ValueError(f"outreach canonical route field changed: {route_id}/{field}")

        outreach = str(row.get("outreach_status", "")).strip()
        response = str(row.get("response_status", "")).strip()
        if outreach not in OUTREACH_STATUSES:
            raise ValueError(f"unregistered outreach_status: {route_id}/{outreach}")
        if response not in RESPONSE_STATUSES:
            raise ValueError(f"unregistered response_status: {route_id}/{response}")

        outreach_date = str(row.get("outreach_date", "")).strip()
        outreach_ref = str(row.get("outreach_reference", "")).strip()
        response_date = str(row.get("response_date", "")).strip()
        response_ref = str(row.get("response_reference", "")).strip()

        if outreach == "NOT_SENT":
            if outreach_date or outreach_ref or response != "NO_RESPONSE":
                raise ValueError(f"NOT_SENT route carries outreach/response evidence: {route_id}")
        else:
            if not outreach_date or not outreach_ref:
                raise ValueError(f"sent outreach lacks date/reference: {route_id}")

        if response == "NO_RESPONSE":
            if response_date or response_ref:
                raise ValueError(f"NO_RESPONSE route carries response evidence: {route_id}")
        else:
            if not response_date or not response_ref:
                raise ValueError(f"response status lacks date/reference: {route_id}")

        if response == "ROUTING_RESPONSE_ONLY":
            if (
                not str(row.get("routed_to_organization", "")).strip()
                or not str(row.get("routed_to_contact", "")).strip()
            ):
                raise ValueError(f"routing response lacks destination: {route_id}")
            if outreach not in {"ROUTED_TO_ANOTHER_AUTHORITY", "RESPONSE_RECEIVED"}:
                raise ValueError(f"routing response/outreach status mismatch: {route_id}")

        if response == "SUBSTANTIVE_RESPONSE_RECEIVED":
            substantive_responses += 1
            if outreach != "RESPONSE_RECEIVED":
                raise ValueError(f"substantive response/outreach status mismatch: {route_id}")

        by_candidate[candidate_id].append(row)
        status_counts[outreach] += 1

    if set(by_candidate) != wave1:
        raise ValueError("not all WAVE1 candidates are represented in outreach ledger")

    candidate_progress = {}
    for candidate_id in sorted(wave1):
        candidate_rows = by_candidate[candidate_id]
        regulatory = [
            row for row in candidate_rows
            if row["route_type"].strip() == "REGULATORY_ROUTING"
        ]
        site = [
            row for row in candidate_rows
            if row["route_type"].strip()
            in {"SITE_MANAGEMENT_ROUTING", "INSTITUTIONAL_SITE_ROUTING"}
        ]
        routing_destinations = [
            {
                "source_route_id": row["route_id"].strip(),
                "organization": row["routed_to_organization"].strip(),
                "contact": row["routed_to_contact"].strip(),
            }
            for row in candidate_rows
            if row["response_status"].strip() == "ROUTING_RESPONSE_ONLY"
        ]
        candidate_progress[candidate_id] = {
            "registered_routes": len(candidate_rows),
            "regulatory_routes": len(regulatory),
            "site_authorizing_routes": len(site),
            "routing_destinations_pending_canonical_registration": routing_destinations,
            "canonical_route_update_required": bool(routing_destinations),
            "substantive_regulatory_response_received": any(
                row["response_status"].strip() == "SUBSTANTIVE_RESPONSE_RECEIVED"
                for row in regulatory
            ),
            "substantive_site_response_received": any(
                row["response_status"].strip() == "SUBSTANTIVE_RESPONSE_RECEIVED"
                for row in site
            ),
            "ready_to_build_permission_response_bundle": (
                any(
                    row["response_status"].strip() == "SUBSTANTIVE_RESPONSE_RECEIVED"
                    for row in regulatory
                )
                and any(
                    row["response_status"].strip() == "SUBSTANTIVE_RESPONSE_RECEIVED"
                    for row in site
                )
            ),
        }

    return {
        "schema_version": "SLK_PEDICULARIS_WAVE1_PERMISSION_OUTREACH_LEDGER_RECEIPT_V1",
        "status": "WAVE1_PERMISSION_OUTREACH_LEDGER_VALIDATED",
        "route_count": len(rows),
        "candidate_count": len(wave1),
        "outreach_status_counts": dict(sorted(status_counts.items())),
        "substantive_response_count": substantive_responses,
        "candidate_progress": candidate_progress,
        "claim_ceiling": (
            "OUTREACH_TRACKING_ONLY_NO_PERMISSION_GRANTED_"
            "NO_FRESH_CONTEXT_NO_P0_SIGNAL_NO_G1_G5_RESULT"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate or validate the Pedicularis WAVE1 permission outreach ledger"
    )
    parser.add_argument("--generate", type=Path)
    parser.add_argument("--validate", dest="validate_path", type=Path)
    parser.add_argument("--receipt-output", type=Path)
    args = parser.parse_args()

    if bool(args.generate) == bool(args.validate_path):
        raise SystemExit("choose exactly one of --generate or --validate")

    if args.generate:
        rows = generate_rows()
        fieldnames = list(rows[0].keys())
        with args.generate.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        result = validate(rows)
    else:
        rows = _read(args.validate_path)
        result = validate(rows)

    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.receipt_output:
        args.receipt_output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
