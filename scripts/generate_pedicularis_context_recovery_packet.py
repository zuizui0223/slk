from __future__ import annotations

import argparse
import copy
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "PEDICULARIS_CONTEXT_CANDIDATE_LEDGER_V1.csv"
QUEUE = ROOT / "data" / "PEDICULARIS_CONTEXT_RECOVERY_QUEUE_V1.csv"
LOCATORS = ROOT / "data" / "PEDICULARIS_CONTEXT_RECOVERY_SCOUTING_LOCATORS_V1.csv"
FREEZE_TEMPLATE = ROOT / "data" / "PEDICULARIS_CONTEXT_RECOVERY_FREEZE_TEMPLATE_V1.json"
OBS_TEMPLATE = ROOT / "data" / "PEDICULARIS_CONTEXT_RECOVERY_OBSERVATION_TEMPLATE_V1.json"


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _filled(value: str, label: str) -> str:
    out = str(value).strip()
    _need(bool(out), f"{label} must be non-empty")
    return out


def _candidate(candidate_id: str) -> dict[str, str]:
    candidate_id = _filled(candidate_id, "candidate_id")
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if str(row.get("candidate_id", "")).strip() == candidate_id
        ]
    _need(
        len(rows) == 1,
        f"candidate_id not uniquely registered in candidate ledger: {candidate_id}",
    )
    return rows[0]


def _one_csv_row(path: Path, candidate_id: str, *, required: bool) -> dict[str, str] | None:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if str(row.get("candidate_id", "")).strip() == candidate_id
        ]
    if required:
        _need(
            len(rows) == 1,
            f"candidate_id not uniquely registered in {path.name}: {candidate_id}",
        )
    else:
        _need(
            len(rows) <= 1,
            f"candidate_id duplicated in {path.name}: {candidate_id}",
        )
    return rows[0] if rows else None


def _clean_locator(row: dict[str, str] | None) -> dict | None:
    if row is None:
        return None
    out = {
        "candidate_id": row["candidate_id"],
        "recovery_wave": row["recovery_wave"],
        "locator_type": row["locator_type"],
        "source_reference": row["source_reference"],
        "locator_claim": row["locator_claim"],
        "elevation_m_or_range": row["elevation_m_or_range"] or None,
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


def build_packet(
    *,
    candidate_id: str,
    candidate_site_id: str,
    population_id: str,
    season_id: str,
    recovery_window_id: str,
    p0_relevance_calibration_window_id: str,
    p0_screen_window_id: str,
) -> dict:
    row = _candidate(candidate_id)
    queue_row = _one_csv_row(QUEUE, candidate_id, required=True)
    locator_row = _one_csv_row(LOCATORS, candidate_id, required=False)
    locator_snapshot = _clean_locator(locator_row)
    freeze = json.loads(FREEZE_TEMPLATE.read_text(encoding="utf-8"))
    observation = json.loads(OBS_TEMPLATE.read_text(encoding="utf-8"))

    values = {
        "candidate_id": candidate_id,
        "candidate_site_id": _filled(candidate_site_id, "candidate_site_id"),
        "population_id": _filled(population_id, "population_id"),
        "season_id": _filled(season_id, "season_id"),
        "recovery_window_id": _filled(recovery_window_id, "recovery_window_id"),
    }

    freeze = copy.deepcopy(freeze)
    freeze["status"] = "CONTEXT_RECOVERY_DRAFT_AWAITING_FREEZE_METADATA"
    freeze["context"].update(values)
    freeze["context"]["frozen_before_recovery_observations"] = False
    freeze["historical_anchor"].update(
        {
            "source_type": row["source_type"],
            "source_reference": row["source_reference"],
            "candidate_status_before_recovery": row["current_status"],
            "use": "PRIORITIZATION_ONLY_NOT_FRESH_CONTEXT_PASS",
        }
    )
    freeze["downstream_windows"].update(
        {
            "p0_relevance_calibration_window_id": _filled(
                p0_relevance_calibration_window_id,
                "p0_relevance_calibration_window_id",
            ),
            "p0_screen_window_id": _filled(
                p0_screen_window_id,
                "p0_screen_window_id",
            ),
        }
    )
    freeze["freeze_metadata"] = {
        "slk_source_commit": "REQUIRED_BEFORE_USE",
        "freeze_commit": "REQUIRED_BEFORE_USE",
        "freeze_timestamp": "REQUIRED_BEFORE_USE",
    }

    observation = copy.deepcopy(observation)
    observation["context"].update(values)
    observation["status"] = "TEMPLATE_ONLY_NOT_DATA"
    observation["recovery_queue_snapshot"] = {
        "recovery_wave": queue_row["recovery_wave"],
        "selection_basis": queue_row["selection_basis"],
        "reason": queue_row["reason"],
    }
    observation["scouting_locator_snapshot"] = locator_snapshot

    return {
        "schema_version": "SLK_PEDICULARIS_CONTEXT_RECOVERY_PACKET_V1",
        "status": "DRAFT_PACKET_REQUIRES_PROSPECTIVE_FREEZE",
        "candidate_ledger_snapshot": {
            "candidate_id": row["candidate_id"],
            "region_or_site": row["region_or_site"],
            "historical_year": row["historical_year"],
            "source_type": row["source_type"],
            "source_reference": row["source_reference"],
            "priority_for_fresh_p0": row["priority_for_fresh_p0"],
            "current_status": row["current_status"],
        },
        "recovery_queue_snapshot": {
            "recovery_wave": queue_row["recovery_wave"],
            "selection_basis": queue_row["selection_basis"],
            "reason": queue_row["reason"],
        },
        "scouting_locator_snapshot": locator_snapshot,
        "freeze_draft": freeze,
        "observation_template": observation,
        "next_action": (
            "Review the draft; fill freeze_metadata; commit/freeze it; set "
            "status=FROZEN_CANDIDATE and frozen_before_recovery_observations=true "
            "before collecting fresh recovery observations."
        ),
        "claim_ceiling": "PACKET_GENERATION_ONLY_NO_FRESH_CONTEXT_RESULT",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a Pedicularis fresh-context recovery draft packet from the canonical candidate ledger"
    )
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--candidate-site-id", required=True)
    parser.add_argument("--population-id", required=True)
    parser.add_argument("--season-id", required=True)
    parser.add_argument("--recovery-window-id", required=True)
    parser.add_argument("--p0-calibration-window-id", required=True)
    parser.add_argument("--p0-screen-window-id", required=True)
    parser.add_argument("--packet-output", required=True, type=Path)
    parser.add_argument("--freeze-output", type=Path)
    parser.add_argument("--observation-output", type=Path)
    args = parser.parse_args()

    packet = build_packet(
        candidate_id=args.candidate_id,
        candidate_site_id=args.candidate_site_id,
        population_id=args.population_id,
        season_id=args.season_id,
        recovery_window_id=args.recovery_window_id,
        p0_relevance_calibration_window_id=args.p0_calibration_window_id,
        p0_screen_window_id=args.p0_screen_window_id,
    )
    args.packet_output.write_text(
        json.dumps(packet, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if args.freeze_output:
        args.freeze_output.write_text(
            json.dumps(packet["freeze_draft"], indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.observation_output:
        args.observation_output.write_text(
            json.dumps(packet["observation_template"], indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
