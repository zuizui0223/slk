from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from pathlib import Path


FIELDS = [
    "dataset_id",
    "record_type",
    "candidate_site_id",
    "population_id",
    "season_id",
    "calibration_window_id",
    "record_id",
    "plant_id",
    "flower_id",
    "observed_minutes",
    "simultaneously_open_focal_flowers",
    "legitimate_pollinator_visits",
    "early_attack_or_oviposition_positive",
    "water_positive",
    "calibration_only",
    "p0_decision_eligible",
    "downstream_confirmatory_eligible",
    "notes",
]


def _load_validator():
    path = Path(__file__).with_name("summarize_pedicularis_p0_natural_history_calibration.py")
    spec = importlib.util.spec_from_file_location("ped_p0_nat_hist_validate", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.validate_freeze


validate_freeze = _load_validator()


def _blank() -> dict[str, str]:
    return {field: "" for field in FIELDS}


def generate(freeze: dict) -> list[dict[str, str]]:
    cfg = validate_freeze(freeze)
    ctx = cfg["context"]
    floors = cfg["floors"]
    rows: list[dict[str, str]] = []

    common = {
        "dataset_id": "PED_P0_NAT_HIST_CAL_V1",
        "candidate_site_id": ctx["candidate_site_id"],
        "population_id": ctx["population_id"],
        "season_id": ctx["season_id"],
        "calibration_window_id": ctx["calibration_window_id"],
        "calibration_only": "true",
        "p0_decision_eligible": "false",
        "downstream_confirmatory_eligible": "false",
    }

    bouts = floors["pollinator_bouts"]
    minutes_each = floors["pollinator_minutes"] / bouts
    for i in range(1, bouts + 1):
        row = _blank()
        row.update(common)
        row.update(
            {
                "record_type": "POLLINATOR_BOUT",
                "record_id": f"CAL-POLL-{i:03d}",
                "observed_minutes": f"{minutes_each:.6f}",
                "notes": "Record simultaneously open focal flowers and legitimate visits for the full registered bout.",
            }
        )
        rows.append(row)

    for i in range(1, floors["predator_flowers"] + 1):
        row = _blank()
        row.update(common)
        row.update(
            {
                "record_type": "PREDATOR_FLOWER",
                "record_id": f"CAL-PRED-{i:03d}",
                "notes": "Use the exact early attack / oviposition-positive definition intended for P0.",
            }
        )
        rows.append(row)

    for i in range(1, floors["water_plants"] + 1):
        row = _blank()
        row.update(common)
        row.update(
            {
                "record_type": "WATER_PLANT",
                "record_id": f"CAL-WATER-{i:03d}",
                "notes": "Score water-positive state under the frozen calibration timing/weather definition.",
            }
        )
        rows.append(row)

    return rows


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate independent Pedicularis P0 natural-history calibration packet")
    parser.add_argument("calibration_freeze_json", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    freeze = json.loads(args.calibration_freeze_json.read_text(encoding="utf-8"))
    rows = generate(freeze)
    _write_csv(args.output, rows)


if __name__ == "__main__":
    main()
