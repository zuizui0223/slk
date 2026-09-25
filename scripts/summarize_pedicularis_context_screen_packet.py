from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import date
from pathlib import Path

try:
    from scripts.pedicularis_physical_units import (
        canonical_tag_hash,
        validate_physical_plant_mapping,
    )
except ImportError:
    from pedicularis_physical_units import (
        canonical_tag_hash,
        validate_physical_plant_mapping,
    )


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


def _iso_date(value: object, label: str) -> date:
    text = str(value).strip()
    _need(bool(text), f"{label} missing")
    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{label} must be ISO YYYY-MM-DD") from exc


def _num(value: object, label: str, *, minimum: float = 0) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    _need(math.isfinite(out) and out >= minimum, f"{label} must be finite and >= {minimum}")
    return out


def _one_context(rows: list[dict[str, str]]) -> dict[str, str]:
    keys = ("candidate_id", "candidate_site_id", "population_id", "season_id", "screen_window_id")
    contexts = {tuple(str(row.get(k, "")).strip() for k in keys) for row in rows}
    _need(len(contexts) == 1, "context screen packet contains multiple contexts")
    values = next(iter(contexts))
    _need(all(values), "context screen packet has blank context identifiers")
    return dict(zip(keys, values))


def summarize(rows: list[dict[str, str]]) -> dict:
    _need(bool(rows), "context screen packet is empty")
    ids = [str(row.get("record_id", "")).strip() for row in rows]
    _need(all(ids) and len(ids) == len(set(ids)), "record_id must be non-empty and unique")
    allowed_record_types = {
        "CENSUS",
        "POLLINATOR_BOUT",
        "PREDATOR_FLOWER",
        "WATER_PLANT",
    }
    unknown_types = {
        str(row.get("record_type", "")).strip()
        for row in rows
        if str(row.get("record_type", "")).strip()
        not in allowed_record_types
    }
    _need(
        not unknown_types,
        f"unregistered context-screen record types: {sorted(unknown_types)}",
    )
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

    for row in pred_rows:
        _need(
            str(row.get("plant_id", "")).strip(),
            f"predator row missing plant_id: {row['record_id']}",
        )
    for row in water_rows:
        _need(
            str(row.get("plant_id", "")).strip(),
            f"water row missing plant_id: {row['record_id']}",
        )
    physical_rows = pred_rows + water_rows
    physical_mapping = validate_physical_plant_mapping(physical_rows)
    physical_tags = sorted(set(physical_mapping.values()))

    census_row = census_rows[0]
    census_date_raw = str(census_row.get("observation_date", "")).strip()
    census_raw = str(census_row.get("flowering_plants_censused", "")).strip()
    census = _num(census_raw, "flowering_plants_censused") if census_raw else 0.0
    _need(
        census.is_integer(),
        "flowering_plants_censused must be an integer count",
    )
    census_exhausted = _optional_bool(
        census_row.get("population_census_exhausted", ""),
        "population_census_exhausted",
    )

    observed_dates: list[date] = []
    completed_poll = []
    poll_bout_details: list[dict] = []
    total_minutes = 0.0
    total_flower_minutes = 0.0
    visits = 0.0
    incomplete_records: list[dict[str, str]] = []
    for row in poll_rows:
        date_raw = str(row.get("observation_date", "")).strip()
        minutes_raw = str(row.get("observed_observation_minutes", "")).strip()
        flowers_raw = str(row.get("simultaneously_open_focal_flowers", "")).strip()
        visits_raw = str(row.get("legitimate_pollinator_visits", "")).strip()
        if not date_raw or not minutes_raw or not flowers_raw or not visits_raw:
            missing_fields = [
                field
                for field, value in (
                    ("observation_date", date_raw),
                    ("observed_observation_minutes", minutes_raw),
                    (
                        "simultaneously_open_focal_flowers",
                        flowers_raw,
                    ),
                    ("legitimate_pollinator_visits", visits_raw),
                )
                if not value
            ]
            incomplete_records.append(
                {
                    "record_id": row["record_id"],
                    "record_type": "POLLINATOR_BOUT",
                    "reason": "MISSING_REQUIRED_MEASUREMENT",
                    "detail": ",".join(missing_fields),
                }
            )
            continue
        observation_date = _iso_date(
            date_raw,
            f"observation_date/{row['record_id']}",
        )
        observed_dates.append(observation_date)
        minutes = _num(minutes_raw, f"observed minutes/{row['record_id']}", minimum=0.000001)
        flowers = _num(flowers_raw, f"simultaneously open focal flowers/{row['record_id']}", minimum=1)
        _need(flowers.is_integer(), f"simultaneously open focal flowers must be an integer: {row['record_id']}")
        visit = _num(visits_raw, f"legitimate visits/{row['record_id']}")
        _need(
            visit.is_integer(),
            f"legitimate visits must be an integer count: {row['record_id']}",
        )
        planned_raw = str(
            row.get("planned_observation_minutes", "")
        ).strip()
        _need(
            planned_raw != "",
            f"planned observation minutes missing: {row['record_id']}",
        )
        planned_minutes = _num(
            planned_raw,
            f"planned observation minutes/{row['record_id']}",
            minimum=0.000001,
        )
        total_minutes += minutes
        total_flower_minutes += minutes * flowers
        visits += visit
        completed_poll.append(row)
        poll_bout_details.append(
            {
                "record_id": row["record_id"],
                "observation_date": observation_date.isoformat(),
                "planned_minutes": planned_minutes,
                "observed_minutes": minutes,
                "simultaneously_open_focal_flowers": int(flowers),
                "legitimate_visits": int(visit),
            }
        )

    completed_pred = []
    attacked = 0
    pred_notes = []
    pred_units: set[tuple[str, str]] = set()
    for row in pred_rows:
        date_raw = str(row.get("observation_date", "")).strip()
        raw = str(row.get("predator_attack_present", "")).strip()
        if not date_raw or raw == "":
            incomplete_records.append(
                {
                    "record_id": row["record_id"],
                    "record_type": "PREDATOR_FLOWER",
                    "reason": "MISSING_REQUIRED_MEASUREMENT",
                    "detail": ",".join(
                        field
                        for field, value in (
                            ("observation_date", date_raw),
                            ("predator_attack_present", raw),
                        )
                        if not value
                    ),
                }
            )
            continue
        observation_date = _iso_date(
            date_raw,
            f"observation_date/{row['record_id']}",
        )
        observed_dates.append(observation_date)
        observation_date = _iso_date(
            date_raw,
            f"observation_date/{row['record_id']}",
        )
        observed_dates.append(observation_date)
        plant_id = str(row.get("plant_id", "")).strip()
        flower_id = str(row.get("flower_id", "")).strip()
        _need(
            plant_id,
            f"predator row missing plant_id: {row['record_id']}",
        )
        _need(
            flower_id,
            f"predator row missing flower_id: {row['record_id']}",
        )
        unit = (plant_id, flower_id)
        _need(
            unit not in pred_units,
            f"duplicate predator flower unit: {plant_id}/{flower_id}",
        )
        pred_units.add(unit)
        present = _bool(raw, f"predator_attack_present/{row['record_id']}")
        attacked += int(present)
        note = str(row.get("predator_evidence_note", "")).strip()
        if note:
            pred_notes.append(note)
        completed_pred.append(row)

    completed_water = []
    water_positive = 0
    water_notes = []
    water_units: set[str] = set()
    for row in water_rows:
        date_raw = str(row.get("observation_date", "")).strip()
        raw = str(row.get("water_positive", "")).strip()
        if not date_raw or raw == "":
            incomplete_records.append(
                {
                    "record_id": row["record_id"],
                    "record_type": "WATER_PLANT",
                    "reason": "MISSING_REQUIRED_MEASUREMENT",
                    "detail": ",".join(
                        field
                        for field, value in (
                            ("observation_date", date_raw),
                            ("water_positive", raw),
                        )
                        if not value
                    ),
                }
            )
            continue
        plant_id = str(row.get("plant_id", "")).strip()
        _need(
            plant_id,
            f"water row missing plant_id: {row['record_id']}",
        )
        _need(
            plant_id not in water_units,
            f"duplicate water-state plant unit: {plant_id}",
        )
        water_units.add(plant_id)
        present = _bool(raw, f"water_positive/{row['record_id']}")
        water_positive += int(present)
        note = str(row.get("water_state_note", "")).strip()
        if note:
            water_notes.append(note)
        completed_water.append(row)

    census_dated = False
    if census_raw and census_exhausted is not None:
        if census_date_raw:
            observed_dates.append(
                _iso_date(census_date_raw, "observation_date/CENSUS-001")
            )
            census_dated = True
        else:
            incomplete_records.append(
                {
                    "record_id": census_row["record_id"],
                    "record_type": "CENSUS",
                    "reason": "MISSING_CAPACITY_CENSUS_DATE",
                    "detail": "observation_date",
                }
            )

    if not census_raw:
        incomplete_records.append(
            {
                "record_id": census_row["record_id"],
                "record_type": "CENSUS",
                "reason": "MISSING_CAPACITY_CENSUS_COUNT",
                "detail": "flowering_plants_censused",
            }
        )
    if census_exhausted is None:
        incomplete_records.append(
            {
                "record_id": census_row["record_id"],
                "record_type": "CENSUS",
                "reason": "MISSING_CAPACITY_EXHAUSTION_STATUS",
                "detail": "population_census_exhausted",
            }
        )

    reason_counts: dict[str, int] = {}
    for item in incomplete_records:
        reason = item["reason"]
        reason_counts[reason] = reason_counts.get(reason, 0) + 1

    poll_rate = (
        visits / total_flower_minutes
        if total_flower_minutes > 0
        else None
    )
    return {
        "schema_version": RECEIPT_SCHEMA,
        "status": "FILLED_SCREEN_DATA",
        "context": {
            "system": "Pedicularis rex",
            **ctx,
        },
        "field_timing_audit": {
            "capacity_census_dated": census_dated,
            "observed_date_min": (
                min(observed_dates).isoformat() if observed_dates else None
            ),
            "observed_date_max": (
                max(observed_dates).isoformat() if observed_dates else None
            ),
            "completed_dated_record_count": len(observed_dates),
        },
        "physical_unit_audit": {
            "status": "P0_SCREEN_PLANT_TAGS_VALIDATED",
            "assignment_to_physical_tag": physical_mapping,
            "current_physical_plant_count": len(physical_tags),
            "current_physical_plant_tags": physical_tags,
            "current_tag_set_sha256": canonical_tag_hash(physical_tags),
            "scope_note": (
                "Permanent-tag firewall covers plant/flower-based predator and water screen units. "
                "Pollinator screen independence remains temporal at the observation-bout level."
            ),
        },
        "effort": {
            "independent_flowering_plants_censused": census,
            "population_census_exhausted": census_exhausted,
            "pollinator_observation_minutes_total": total_minutes,
            "pollinator_flower_minutes_total": total_flower_minutes,
            "pollinator_observation_bouts": len(completed_poll),
            "pollinator_bout_details": poll_bout_details,
            "minimum_observed_pollinator_bout_minutes": (
                min(
                    detail["observed_minutes"]
                    for detail in poll_bout_details
                )
                if poll_bout_details
                else None
            ),
            "predator_screen_flowers": len(completed_pred),
            "water_state_plants": len(completed_water),
        },
        "observations": {
            "legitimate_pollinator_visits": visits,
            "legitimate_visit_rate_per_flower_min": poll_rate,
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
            "pollinator_exposure_unit": "FLOWER_MINUTES",
        },
        "packet_completion": {
            "registered_pollinator_rows": len(poll_rows),
            "completed_pollinator_rows": len(completed_poll),
            "registered_predator_rows": len(pred_rows),
            "completed_predator_rows": len(completed_pred),
            "registered_water_rows": len(water_rows),
            "completed_water_rows": len(completed_water),
            "capacity_census_exhaustion_recorded": (
                census_exhausted is not None
            ),
            "incomplete_records": len(incomplete_records),
            "incomplete_reason_counts": reason_counts,
            "incomplete_record_details": incomplete_records,
            "missingness_sensitivity_required": bool(
                incomplete_records
            ),
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
