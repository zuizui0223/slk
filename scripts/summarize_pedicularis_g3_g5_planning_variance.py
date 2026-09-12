from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import stdev


DATASET_ID = "PED_D0_QUAL_CONFIRM_V1"
FITNESS_SCALE_ID = "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER"
D0_RECEIPT_SCHEMA = "SLK_PEDICULARIS_D0_CONFIRMATORY_RECEIPT_V1"
D0_READY = "D0_FULLY_QUALIFIED"


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _num(value: object, label: str) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    _need(math.isfinite(out) and out >= 0, f"{label} must be finite and non-negative")
    return out


def _false(value: object) -> bool:
    return str(value).strip().lower() == "false"


def _true(value: object) -> bool:
    return str(value).strip().lower() == "true"


def summarize(rows: list[dict[str, str]], d0_receipt: dict) -> dict:
    _need(d0_receipt.get("schema_version") == D0_RECEIPT_SCHEMA, "wrong D0 receipt schema")
    _need(d0_receipt.get("status") == D0_READY, "D0 must be fully qualified before G3-G5 variance planning")
    _need(bool(d0_receipt.get("gates")) and all(d0_receipt["gates"].values()), "all D0 Q1-Q6 gates must pass before variance planning")
    dctx = d0_receipt.get("context", {})
    _need(dctx.get("dataset_id") == DATASET_ID, "wrong D0 qualification dataset id")
    _need(dctx.get("fitness_scale_id") == FITNESS_SCALE_ID, "wrong D0 qualification fitness scale")
    _need(d0_receipt.get("firewall", {}).get("d0_qualification_units_g3_g5_ineligible") is True, "D0/G3-G5 firewall missing")
    _need(bool(rows), "D0 qualification rows are empty")

    by_plant: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    contexts = set()
    for row in rows:
        _need(row.get("dataset_id") == DATASET_ID, "wrong row dataset id")
        _need(_true(row.get("d0_qualification_eligible")), "row is not a D0 qualification unit")
        _need(_false(row.get("g3_g5_eligible")), "D0 qualification row cannot be G3-G5 eligible")
        for key in ("context_id", "population_id", "season_id", "fitness_scale_id", "time_horizon_id"):
            _need(row.get(key) == dctx.get(key), f"row/D0 receipt context mismatch: {key}")
        contexts.add((row.get("context_id"), row.get("population_id"), row.get("season_id"), row.get("fitness_scale_id"), row.get("time_horizon_id")))
        plant_id = str(row.get("plant_id", "")).strip()
        treatment = str(row.get("treatment", "")).strip()
        _need(plant_id and treatment, "missing plant/treatment id")
        _need(treatment not in by_plant[plant_id], f"duplicate treatment within plant: {plant_id}/{treatment}")
        by_plant[plant_id][treatment] = row
    _need(len(contexts) == 1, "multiple D0 qualification contexts")

    values = {"S": [], "D0": [], "D": []}
    for plant_id, treatments in by_plant.items():
        for world, treatment in (("S", "S_QUAL"), ("D0", "D0_QUAL"), ("D", "D_QUAL")):
            row = treatments.get(treatment)
            if row is None:
                continue
            raw = str(row.get("mature_viable_undamaged_seeds", "")).strip()
            if raw == "":
                continue
            values[world].append(_num(raw, f"mature seeds {plant_id}/{treatment}"))

    precision = d0_receipt.get("precision_plan", {})
    expected_low = int(precision.get("observed_low_y_plants", 0))
    expected_high = int(precision.get("observed_high_y_plants", 0))
    _need(expected_low > 1 and expected_high > 1, "D0 receipt lacks observed qualification plant counts")

    complete_followup = (
        len(values["S"]) == expected_low
        and len(values["D0"]) == expected_low
        and len(values["D"]) == expected_high
    )
    sds = {}
    for world in ("S", "D0", "D"):
        sds[world] = float(stdev(values[world])) if len(values[world]) >= 2 else None
    nonzero = all(sd is not None and sd > 0 for sd in sds.values())
    ready = complete_followup and nonzero

    return {
        "schema_version": "SLK_PEDICULARIS_G3_G5_PLANNING_VARIANCE_V1",
        "status": "G3_G5_PLANNING_VARIANCE_READY" if ready else "G3_G5_PLANNING_VARIANCE_INCOMPLETE",
        "context": {
            "system": "Pedicularis rex",
            "context_id": dctx["context_id"],
            "population_id": dctx["population_id"],
            "season_id": dctx["season_id"],
            "fitness_scale_id": dctx["fitness_scale_id"],
            "time_horizon_id": dctx["time_horizon_id"],
            "source_dataset_id": DATASET_ID,
        },
        "world_variance": {
            world: {
                "independent_plants": len(values[world]),
                "sd_mature_viable_undamaged_seeds": sds[world],
            }
            for world in ("S", "D0", "D")
        },
        "expected_complete_followup": {
            "low_y_plants": expected_low,
            "high_y_plants": expected_high,
            "all_qualified_plants_have_final_fitness": complete_followup,
        },
        "max_world_sd": max(sds.values()) if nonzero else None,
        "firewall": {
            "all_source_rows_d0_qualification_eligible": True,
            "source_units_planning_only": True,
            "source_units_g3_g5_effect_estimation_ineligible": True,
        },
        "claim_ceiling": "INDEPENDENT_VARIANCE_FOR_SAMPLE_SIZE_PLANNING_ONLY_NO_G3_G5_EFFECT",
    }


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize D0 qualification fitness variance for G3-G5 sample-size planning")
    parser.add_argument("d0_qualification_csv", type=Path)
    parser.add_argument("d0_qualification_receipt_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = summarize(
        _read_csv(args.d0_qualification_csv),
        json.loads(args.d0_qualification_receipt_json.read_text(encoding="utf-8")),
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
