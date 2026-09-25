from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "PEDICULARIS_CONTEXT_CANDIDATE_LEDGER_V1.csv"
QUEUE = ROOT / "data" / "PEDICULARIS_CONTEXT_RECOVERY_QUEUE_V1.csv"
LOCATORS = ROOT / "data" / "PEDICULARIS_CONTEXT_RECOVERY_SCOUTING_LOCATORS_V1.csv"
ROUTES = ROOT / "data" / "PEDICULARIS_WAVE1_PERMISSION_CONTACT_ROUTES_V1.csv"

ACTIVITIES = [
    ("A", "VISUAL_OBSERVATION"),
    ("B", "PHOTOGRAPHY_MORPHOLOGY_DOCUMENTATION"),
    ("C", "NON_DESTRUCTIVE_MEASUREMENT"),
    ("D", "VOUCHER_SPECIMEN_COLLECTION"),
    ("E", "LEAF_OR_TISSUE_SAMPLING"),
    ("F", "SEED_OR_FRUIT_COLLECTION"),
]


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _one(rows: list[dict[str, str]], candidate_id: str, label: str) -> dict[str, str]:
    keep = [r for r in rows if r["candidate_id"].strip() == candidate_id]
    if len(keep) != 1:
        raise ValueError(f"candidate_id not uniquely registered in {label}: {candidate_id}")
    return keep[0]


def _locator_snapshot(candidate_id: str) -> dict | None:
    rows = [r for r in _read(LOCATORS) if r["candidate_id"].strip() == candidate_id]
    if len(rows) > 1:
        raise ValueError(f"duplicate scouting locator: {candidate_id}")
    if not rows:
        return None
    row = rows[0]
    out = {
        "locator_type": row["locator_type"],
        "source_reference": row["source_reference"],
        "locator_claim": row["locator_claim"],
        "notes": row["notes"],
    }
    if row["locator_type"] == "POINT":
        out["point"] = {
            "latitude_deg": float(row["latitude_deg"]),
            "longitude_deg": float(row["longitude_deg"]),
        }
    else:
        out["envelope"] = {
            "lat_min_deg": float(row["lat_min_deg"]),
            "lat_max_deg": float(row["lat_max_deg"]),
            "lon_min_deg": float(row["lon_min_deg"]),
            "lon_max_deg": float(row["lon_max_deg"]),
        }
    return out


def build(candidate_id: str) -> dict:
    ledger = _one(_read(LEDGER), candidate_id, "candidate ledger")
    queue = _one(_read(QUEUE), candidate_id, "recovery queue")
    if queue["recovery_wave"].strip() != "WAVE1":
        raise ValueError("permission inquiry packets are registered only for WAVE1")

    contacts = [
        {
            "route_id": row["route_id"],
            "route_type": row["route_type"],
            "organization": row["organization"],
            "public_contact": row["public_contact"],
            "source_reference": row["source_reference"],
            "source_url": row["source_url"],
            "question_to_resolve": row["question_to_resolve"],
            "permission_status": row["permission_status"],
            "route_status": row["route_status"],
        }
        for row in _read(ROUTES)
        if row["candidate_id"].strip() == candidate_id
    ]
    if not contacts:
        raise ValueError(f"no permission contact routes registered: {candidate_id}")

    return {
        "schema_version": "SLK_PEDICULARIS_WAVE1_PERMISSION_INQUIRY_PACKET_V1",
        "status": "DRAFT_NOT_SENT",
        "candidate": {
            "candidate_id": candidate_id,
            "region_or_site": ledger["region_or_site"],
            "recovery_wave": queue["recovery_wave"],
            "selection_basis": queue["selection_basis"],
            "candidate_prior_status": ledger["current_status"],
        },
        "scouting_locator_snapshot": _locator_snapshot(candidate_id),
        "requester": {
            "name": "REQUIRED_BEFORE_SEND",
            "institution": "REQUIRED_BEFORE_SEND",
            "contact_email": "REQUIRED_BEFORE_SEND",
        },
        "project": {
            "title": "SLK Pedicularis rex fresh-context recovery",
            "purpose": (
                "Verify a current flowering P. rex population and resolve whether the site "
                "can support the prospectively registered P0 natural-history calibration path."
            ),
            "fresh_recovery_is_not_p0_signal_test": True,
        },
        "activity_questions": [
            {
                "activity_id": activity_id,
                "activity": activity,
                "permission_status": "UNKNOWN",
                "correct_authority_confirmed": False,
                "permit_or_response_reference": None,
                "valid_from": None,
                "valid_through": None,
                "conditions": None,
            }
            for activity_id, activity in ACTIVITIES
        ],
        "contact_routes": contacts,
        "response_requirements": {
            "identify_correct_authority": True,
            "identify_current_site_manager": True,
            "state_allowed_activities_separately": True,
            "state_prohibited_activities_separately": True,
            "provide_written_permission_or_response_reference": True,
            "provide_activity_specific_validity_window_and_conditions": True,
        },
        "promotion_rule": (
            "This draft cannot set sampling_permission_status=CONFIRMED. "
            "Only an auditable authority/site response covering the activity needed by "
            "the prospective recovery/P0 path may be cited in the fresh recovery observation."
        ),
        "claim_ceiling": (
            "PERMISSION_INQUIRY_DRAFT_ONLY_NO_PERMISSION_GRANTED_"
            "NO_FRESH_CONTEXT_NO_P0_SIGNAL_NO_G1_G5_RESULT"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate an unsent permission-inquiry packet for a Pedicularis WAVE1 candidate"
    )
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = build(args.candidate_id)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
