from __future__ import annotations

import argparse
import csv
import importlib.util
from pathlib import Path


FIELDS = [
    "record_type",
    "candidate_site_id",
    "population_id",
    "season_id",
    "screen_window_id",
    "record_id",
    "plant_id",
    "flower_id",
    "planned_observation_minutes",
    "observed_observation_minutes",
    "flowering_plants_censused",
    "population_census_exhausted",
    "legitimate_pollinator_visits",
    "predator_attack_present",
    "predator_evidence_note",
    "water_positive",
    "retained_water_volume_or_proxy",
    "water_state_note",
    "screen_only",
    "confirmatory_eligible",
    "notes",
]


def _load_freeze_validator():
    path = Path(__file__).with_name("adjudicate_pedicularis_context_screen.py")
    spec = importlib.util.spec_from_file_location("ped_context_screen_validator", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.validate_freeze


validate_freeze = _load_freeze_validator()


def _blank() -> dict[str, str]:
    return {field: "" for field in FIELDS}


def generate(freeze: dict) -> list[dict[str, str]]:
    cfg = validate_freeze(freeze)
    ctx = cfg["context"]
    effort = cfg["effort"]
    rows: list[dict[str, str]] = []

    common = {
        "candidate_site_id": ctx["candidate_site_id"],
        "population_id": ctx["population_id"],
        "season_id": ctx["season_id"],
        "screen_window_id": ctx["screen_window_id"],
        "screen_only": "true",
        "confirmatory_eligible": "false",
    }

    census = _blank()
    census.update(common)
    census.update({
        "record_type": "CENSUS",
        "record_id": "CENSUS-001",
        "notes": (
            "Count independent flowering plants until the frozen capacity requirement is reached; "
            "if it is not reached, exhaust the focal population and set population_census_exhausted=true."
        ),
    })
    rows.append(census)

    bouts = effort["minimum_pollinator_observation_bouts"]
    total_minutes = effort["minimum_pollinator_observation_minutes_total"]
    minutes_each = total_minutes / bouts
    for i in range(1, bouts + 1):
        row = _blank()
        row.update(common)
        row.update(
            {
                "record_type": "POLLINATOR_BOUT",
                "record_id": f"POLL-{i:03d}",
                "planned_observation_minutes": f"{minutes_each:.6f}",
            }
        )
        rows.append(row)

    for i in range(1, effort["minimum_predator_screen_flowers"] + 1):
        row = _blank()
        row.update(common)
        row.update({"record_type": "PREDATOR_FLOWER", "record_id": f"PRED-{i:03d}"})
        rows.append(row)

    for i in range(1, effort["minimum_water_state_plants"] + 1):
        row = _blank()
        row.update(common)
        row.update({"record_type": "WATER_PLANT", "record_id": f"WATER-{i:03d}"})
        rows.append(row)

    return rows


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Pedicularis P0 context-screen field packet")
    parser.add_argument("screen_freeze_json", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    import json

    freeze = json.loads(args.screen_freeze_json.read_text(encoding="utf-8"))
    rows = generate(freeze)
    _write_csv(args.output, rows)


if __name__ == "__main__":
    main()
