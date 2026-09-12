from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


RECEIPT_SCHEMA = "SLK_PEDICULARIS_CONTEXT_SCREEN_RECEIPT_V1"


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _bool(value: object, label: str) -> bool:
    text = str(value).strip().lower()
    _need(text in {"true", "false", "1", "0", "yes", "no"}, f"{label} must be boolean-like")
    return text in {"true", "1", "yes"}


def _optional_bool(value: object, label: str) -> bool | None:
    text = str(value).strip()
    if text == "":
        return None
    return _bool(text, label)


def _num(value: object, label: str, *, minimum: float = 0) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    _need(math.isfinite(out) and out >= minimum, f"{label} must be finite and >= {minimum}")
    return out


def _one_context(rows: list[dict[str, str]]) -> dict[str, str]:
    keys = ("candidate_site_id", "population_id", "season_id", "screen_window_id")
    contexts = {tuple(str(row.get(k, "")).strip() for k in keys) for row in rows}
    _need(len(contexts) == 1, "context screen packet contains multiple contexts")
    values = next(iter(contexts))
    _need(all(values), "context screen packet has blank context identifiers")
    return dict(zip(keys, values))


def summarize(rows: list[dict[str, str]]) -> dict:
    _need(bool(rows), "context screen packet is empty")
    ids = [str(row.get("record_id", "")).strip() for row in rows]
    _need(all(ids) and len(ids) == len(set(ids)), "record_id must be non-empty and unique")
    ctx = _one_context(rows)

    for row in rows:
        _need(_bool(row.get("screen_only", ""), f"screen_only/{row.get('record_id')}") is True, "every P0 row must remain screen-only")
        _need(_bool(row.get("confirmatory_eligible", ""), f"confirmatory_eligible/{row.get('record_id')}") is False, "P0 row cannot be confirmatory eligible")

    census_rows = [row for row in rows if row.get("record_type") == "CENSUS"]
    poll_rows = [row for row in rows if row.get("record_type") == "POLLINATOR_BOUT"]
    pred_rows = [row for row in rows if row.get("record_type") == "PREDATOR_FLOWER"]
    water_rows = [row for row in rows if row.get("record_type") == "WATER_PLANT"]
    _need(len(census_rows) == 1, "context screen packet must contain exactly one CENSUS row")
    _need(bool(poll_rows) and bool(pred_rows) and bool(water_rows), "context screen packet is missing a registered screen block")

    census_row = census_rows[0]
    census_raw = str(census_row.get("flowering_plants_censused", "")).strip()
    census = _num(census_raw, "flowering_plants_censused") if census_raw else 0.0
    census_exhausted = _optional_bool(
        census_row.get("population_census_exhausted", ""),
        "population_census_exhausted",
    )

    completed_poll = []
    total_minutes = 0.0
    visits = 0.0
    for row in poll_rows:
        minutes_raw = str(row.get("observed_observation_minutes", "")).strip()
        visits_raw = str(row.get("legitimate_pollinator_visits", "")).strip()
        if not minutes_raw or not visits_raw:
            continue
        minutes = _num(minutes_raw, f"observed minutes/{row['record_id']}")
        visit = _num(visits_raw, f"legitimate visits/{row['record_id']}")
        total_minutes += minutes
        visits += visit
        completed_poll.append(row)

    completed_pred = []
    attacked = 0
    pred_notes = []
    for row in pred_rows:
        raw = str(row.get("predator_attack_present", "")).strip()
        if raw == "":
            continue
        _need(str(row.get("plant_id", "")).strip(), f"predator row missing plant_id: {row['record_id']}")
        _need(str(row.get("flower_id", "")).strip(), f"predator row missing flower_id: {row['record_id']}")
        present = _bool(raw, f"predator_attack_present/{row['record_id']}")
        attacked += int(present)
        note = str(row.get("predator_evidence_note", "")).strip()
        if note:
            pred_notes.append(note)
        completed_pred.append(row)

    completed_water = []
    water_positive = 0
    water_notes = []
    for row in water_rows:
        raw = str(row.get("water_positive", "")).strip()
        if raw == "":
            continue
        _need(str(row.get("plant_id", "")).strip(), f"water row missing plant_id: {row['record_id']}")
        present = _bool(raw, f"water_positive/{row['record_id']}")
        water_positive += int(present)
        note = str(row.get("water_state_note", "")).strip()
        if note:
            water_notes.append(note)
        completed_water.append(row)

    return {
        "schema_version": RECEIPT_SCHEMA,
        "status": "FILLED_SCREEN_DATA",
        "context": {
            "system": "Pedicularis rex",
            **ctx,
        },
        "effort": {
            "independent_flowering_plants_censused": census,
            "population_census_exhausted": census_exhausted,
            "pollinator_observation_minutes_total": total_minutes,
            "pollinator_observation_bouts": len(completed_poll),
            "predator_screen_flowers": len(completed_pred),
            "water_state_plants": len(completed_water),
        },
        "observations": {
            "legitimate_pollinator_visits": visits,
            "predator_attacked_flowers": attacked,
            "water_positive_plants": water_positive,
            "notes_on_predator_evidence": (
                "; ".join(sorted(set(pred_notes))) if pred_notes else f"completed predator screen: {attacked}/{len(completed_pred)} attack-positive flowers"
            ),
            "notes_on_water_state": (
                "; ".join(sorted(set(water_notes))) if water_notes else f"completed water screen: {water_positive}/{len(completed_water)} water-positive plants"
            ),
        },
        "pollen_limitation": {
            "status": "UNRESOLVED_UNTIL_QP_CALIBRATION",
            "used_as_context_screen_pass_gate": False,
        },
        "firewall": {
            "screen_units_confirmatory_eligible": False,
            "screen_used_for_treatment_effect_estimation": False,
            "zero_detection_interpreted_as_biological_absence": False,
        },
        "packet_completion": {
            "registered_pollinator_rows": len(poll_rows),
            "completed_pollinator_rows": len(completed_poll),
            "registered_predator_rows": len(pred_rows),
            "completed_predator_rows": len(completed_pred),
            "registered_water_rows": len(water_rows),
            "completed_water_rows": len(completed_water),
            "capacity_census_exhaustion_recorded": census_exhausted is not None,
        },
        "final_adjudication": "NOT_YET_EXECUTED",
    }


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize a completed Pedicularis P0 context-screen field packet")
    parser.add_argument("context_screen_csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = summarize(_read_csv(args.context_screen_csv))
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
