from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANAGER_PATH = ROOT / "scripts" / "manage_pedicularis_wave1_permission_outreach.py"
ROUTES = ROOT / "data" / "PEDICULARIS_WAVE1_PERMISSION_CONTACT_ROUTES_V1.csv"

_spec = importlib.util.spec_from_file_location("ped_wave1_outreach_manager", MANAGER_PATH)
manager = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(manager)

ACTIVITIES = {
    "A": "VISUAL_OBSERVATION",
    "B": "PHOTOGRAPHY_MORPHOLOGY_DOCUMENTATION",
    "C": "NON_DESTRUCTIVE_MEASUREMENT",
    "D": "VOUCHER_SPECIMEN_COLLECTION",
    "E": "LEAF_OR_TISSUE_SAMPLING",
    "F": "SEED_OR_FRUIT_COLLECTION",
}
AUTHORIZING_ROUTE_TYPES = {
    "REGULATORY_ROUTING",
    "SITE_MANAGEMENT_ROUTING",
    "INSTITUTIONAL_SITE_ROUTING",
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build(rows: list[dict[str, str]], candidate_id: str) -> dict:
    receipt = manager.validate(rows)
    progress = receipt["candidate_progress"].get(candidate_id)
    if progress is None:
        raise ValueError(f"candidate absent from WAVE1 outreach ledger: {candidate_id}")
    if not progress["ready_to_build_permission_response_bundle"]:
        raise ValueError(
            f"candidate lacks substantive regulatory + site responses: {candidate_id}"
        )

    canonical = {
        row["route_id"].strip(): row
        for row in _read(ROUTES)
        if row["candidate_id"].strip() == candidate_id
    }

    selected = []
    for row in rows:
        if row["candidate_id"].strip() != candidate_id:
            continue
        if row["response_status"].strip() != "SUBSTANTIVE_RESPONSE_RECEIVED":
            continue
        route_id = row["route_id"].strip()
        route = canonical[route_id]
        if route["route_type"].strip() not in AUTHORIZING_ROUTE_TYPES:
            continue
        selected.append(
            {
                "response_id": f"DRAFT-{route_id}",
                "route_id": route_id,
                "responding_organization": route["organization"].strip(),
                "response_date": row["response_date"].strip(),
                "response_reference": row["response_reference"].strip(),
                "activity_decisions": [
                    {
                        "activity_id": activity_id,
                        "activity": activity,
                        "decision": "UNRESOLVED",
                        "response_reference": None,
                        "valid_from": None,
                        "valid_through": None,
                        "conditions": None,
                        "conditions_compatible_with_registered_activity": None,
                        "conditions_review_reference": None,
                    }
                    for activity_id, activity in ACTIVITIES.items()
                ],
                "conditions": None,
            }
        )

    route_classes = {canonical[x["route_id"]]["route_type"].strip() for x in selected}
    if "REGULATORY_ROUTING" not in route_classes:
        raise ValueError("response draft lost substantive regulatory response")
    if not (
        {"SITE_MANAGEMENT_ROUTING", "INSTITUTIONAL_SITE_ROUTING"}
        & route_classes
    ):
        raise ValueError("response draft lost substantive site-authorizing response")

    return {
        "schema_version": "SLK_PEDICULARIS_WAVE1_PERMISSION_RESPONSE_BUNDLE_V1",
        "status": "DRAFT_AWAITING_ACTIVITY_DECISIONS",
        "candidate_id": candidate_id,
        "response_bundle_id": "REQUIRED_BEFORE_USE",
        "responses": selected,
        "adjudication_metadata": {
            "slk_source_commit": "REQUIRED_BEFORE_USE",
            "adjudication_commit": "REQUIRED_BEFORE_USE",
            "adjudication_timestamp": "REQUIRED_BEFORE_USE",
        },
        "draft_source": {
            "schema_version": receipt["schema_version"],
            "outreach_status": receipt["status"],
            "substantive_response_count_for_candidate": len(selected),
        },
        "next_action": (
            "Read each returned authority/site response; set A-F decisions separately; "
            "fill activity-level response references, validity dates and conditions; "
            "review whether each positive condition is compatible with the registered "
            "activity and record the review reference; then set "
            "status=FILLED_AUTHORITY_RESPONSES before adjudication."
        ),
        "claim_ceiling": (
            "RESPONSE_BUNDLE_DRAFT_ONLY_NO_ACTIVITY_DECISION_"
            "NO_PERMISSION_GRANTED_NO_FRESH_CONTEXT_NO_P0_RESULT"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compile a WAVE1 outreach ledger into an unresolved permission-response bundle draft"
    )
    parser.add_argument("outreach_ledger_csv", type=Path)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = build(_read(args.outreach_ledger_csv), args.candidate_id)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
