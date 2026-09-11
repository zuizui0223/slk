"""Validate a prospectively frozen Pedicularis field-threshold manifest.

This validator does not choose thresholds. It only verifies that every decision
criterion required by the SLK Qz/Qp/Qg execution policy has been assigned a
prospectively justified value before confirmatory treatment outcomes are opened.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


SCHEMA = "SLK_PEDICULARIS_THRESHOLD_FREEZE_V1"
FROZEN_STATUS = "THRESHOLDS_PROSPECTIVELY_FROZEN"
PLACEHOLDER = "REQUIRED_BEFORE_USE"

ALLOWED_SOURCE_TYPES = {
    "published_primary_source",
    "independent_calibration",
    "measurement_repeatability",
    "biological_relevance",
    "prospective_power",
    "prospective_precision",
    "combined_predeclared",
}

QZ = {
    "min_z_levels": "design_floor",
    "min_flowers_per_level": "design_floor",
    "min_plants": "design_floor",
    "min_adjacent_exsertion_gap": "target_effect",
    "max_opening_width_relative_change": "equivalence_tolerance",
    "max_tube_diameter_relative_change": "equivalence_tolerance",
    "max_bract_height_relative_change": "equivalence_tolerance",
    "max_lower_lip_angle_change_deg": "equivalence_tolerance",
    "max_water_depth_change": "equivalence_tolerance",
    "max_flower_orientation_change_deg": "equivalence_tolerance",
    "max_mechanical_damage_rate": "equivalence_tolerance",
}

QP = {
    "min_paired_plants": "design_floor",
    "min_flowers_per_treatment": "design_floor",
    "min_pollen_grain_delta": "target_effect",
    "min_initial_seed_set_delta": "target_effect",
    "max_early_predator_attack_difference": "equivalence_tolerance",
    "max_z_relative_change": "equivalence_tolerance",
    "max_bract_height_relative_change": "equivalence_tolerance",
    "max_opening_width_relative_change": "equivalence_tolerance",
    "max_water_depth_change": "equivalence_tolerance",
    "max_mechanical_damage_rate": "equivalence_tolerance",
}

QG = {
    "method_min_paired_plants": "design_floor",
    "method_min_flowers_per_treatment": "design_floor",
    "min_hours_after_anthesis_before_barrier": "natural_history_timing",
    "max_hours_after_anthesis_before_barrier": "natural_history_timing",
    "predator_min_paired_plants": "design_floor",
    "predator_min_flowers_per_treatment": "design_floor",
    "min_early_attack_reduction": "target_effect",
    "min_predation_fraction_reduction": "target_effect",
    "min_final_seed_set_gain": "target_effect",
    "max_initial_seed_set_difference": "equivalence_tolerance",
    "max_pollen_grain_relative_change": "equivalence_tolerance",
    "max_pollinator_visit_relative_change": "equivalence_tolerance",
    "max_z_relative_change": "equivalence_tolerance",
    "max_water_depth_change": "equivalence_tolerance",
    "max_damage_rate_difference": "equivalence_tolerance",
}

REQUIRED_QG_BOOLEANS = {
    "require_pollination_window_complete": True,
    "require_ovary_not_swollen": True,
    "require_barrier_not_cover_pollinator_entry": True,
    "require_sham_on_exposed": True,
}


def _text(value: object, name: str) -> str:
    out = str(value).strip()
    if not out or out == PLACEHOLDER:
        raise ValueError(f"{name} must be frozen")
    return out


def _number(value: object, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be numeric, not boolean")
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if not math.isfinite(out):
        raise ValueError(f"{name} must be finite")
    return out


def _validate_parameter(entry: dict, name: str, expected_class: str) -> float:
    if not isinstance(entry, dict):
        raise ValueError(f"{name} must be an object")
    if entry.get("threshold_class") != expected_class:
        raise ValueError(f"{name} threshold_class must be {expected_class}")
    source_type = _text(entry.get("source_type"), f"{name}.source_type")
    if source_type not in ALLOWED_SOURCE_TYPES:
        raise ValueError(f"{name}.source_type is not registered")
    _text(entry.get("source_reference"), f"{name}.source_reference")
    _text(entry.get("biological_rationale"), f"{name}.biological_rationale")
    _text(entry.get("units"), f"{name}.units")
    if entry.get("frozen_before_confirmatory_outcomes") is not True:
        raise ValueError(f"{name} was not prospectively frozen")

    value = _number(entry.get("value"), f"{name}.value")
    if expected_class == "design_floor":
        if value < 1 or not value.is_integer():
            raise ValueError(f"{name} design floor must be a positive integer")
    elif value < 0:
        raise ValueError(f"{name} must be non-negative")
    return value


def _validate_block(manifest: dict, block: str, expected: dict[str, str]) -> dict[str, float]:
    raw = manifest.get(block)
    if not isinstance(raw, dict):
        raise ValueError(f"missing {block} block")
    params = raw.get("parameters")
    if not isinstance(params, dict):
        raise ValueError(f"missing {block}.parameters")
    if set(params) != set(expected):
        missing = sorted(set(expected) - set(params))
        extra = sorted(set(params) - set(expected))
        raise ValueError(f"{block} parameter mismatch; missing={missing}, extra={extra}")
    return {
        name: _validate_parameter(params[name], f"{block}.{name}", threshold_class)
        for name, threshold_class in expected.items()
    }


def validate(manifest: dict) -> dict:
    if manifest.get("manifest_schema_version") != SCHEMA:
        raise ValueError(f"manifest_schema_version must be {SCHEMA}")
    if manifest.get("status") != FROZEN_STATUS:
        raise ValueError(f"status must be {FROZEN_STATUS}")

    context = manifest.get("context")
    if not isinstance(context, dict):
        raise ValueError("missing context block")
    if _text(context.get("system"), "context.system") != "Pedicularis rex":
        raise ValueError("context.system must be Pedicularis rex")
    _text(context.get("population_id"), "context.population_id")
    _text(context.get("season_id"), "context.season_id")
    calibration_id = _text(context.get("calibration_dataset_id"), "context.calibration_dataset_id")
    qualification_id = _text(context.get("qualification_dataset_id"), "context.qualification_dataset_id")
    if calibration_id == qualification_id:
        raise ValueError("calibration and qualification datasets must be distinct")

    provenance = manifest.get("provenance")
    if not isinstance(provenance, dict):
        raise ValueError("missing provenance block")
    for field in ("sch_source_commit", "slk_source_commit", "freeze_commit", "freeze_timestamp"):
        _text(provenance.get(field), f"provenance.{field}")
    if provenance.get("confirmatory_outcomes_opened_before_freeze") is not False:
        raise ValueError("confirmatory outcomes must remain unopened before freeze")

    qz = _validate_block(manifest, "qz", QZ)
    qp = _validate_block(manifest, "qp", QP)
    qg = _validate_block(manifest, "qg", QG)

    qg_block = manifest["qg"]
    fixed = qg_block.get("fixed_boolean_requirements")
    if fixed != REQUIRED_QG_BOOLEANS:
        raise ValueError("Qg fixed boolean requirements must remain all true under v1")

    if qg["min_hours_after_anthesis_before_barrier"] >= qg["max_hours_after_anthesis_before_barrier"]:
        raise ValueError("Qg barrier timing window must have min < max")

    # Design floors are allowed to differ between method and effect blocks, but
    # the final confirmatory collection must satisfy the stricter of the two.
    effective_qg_min_plants = int(max(qg["method_min_paired_plants"], qg["predator_min_paired_plants"]))
    effective_qg_min_flowers = int(
        max(qg["method_min_flowers_per_treatment"], qg["predator_min_flowers_per_treatment"])
    )

    return {
        "manifest_schema_version": SCHEMA,
        "status": "THRESHOLD_FREEZE_VALIDATED",
        "context": {
            "system": "Pedicularis rex",
            "population_id": context["population_id"],
            "season_id": context["season_id"],
        },
        "parameter_counts": {"qz": len(qz), "qp": len(qp), "qg": len(qg)},
        "effective_qg_design_floor": {
            "min_paired_plants": effective_qg_min_plants,
            "min_flowers_per_treatment": effective_qg_min_flowers,
        },
        "claim_ceiling": (
            "prospective decision criteria frozen only; no Qz/Qp/Qg biological gate, "
            "G1 conflict, G2 conflict budget, or downstream architecture claim is identified"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a frozen Pedicularis threshold manifest")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = validate(json.loads(args.manifest.read_text(encoding="utf-8")))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
