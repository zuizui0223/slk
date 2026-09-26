from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

try:
    from scripts.pedicularis_permission_scope import (
        validate_confirmed_permission_scope,
    )
    from scripts.pedicularis_physical_units import validate_firewall_block
except ImportError:
    from pedicularis_permission_scope import (
        validate_confirmed_permission_scope,
    )
    from pedicularis_physical_units import validate_firewall_block


SCHEMA = "SLK_PEDICULARIS_P0_RELEVANCE_QUALIFICATION_V1"
REQUIRED_IDS = {
    "P0_POLLINATOR_MIN_RATE",
    "P0_PREDATOR_MIN_PREVALENCE",
    "P0_WATER_POSITIVE_PREVALENCE",
}
TARGET_METRICS = {
    "P0_POLLINATOR_MIN_RATE": "LEGITIMATE_VISITS_PER_FLOWER_MINUTE",
    "P0_PREDATOR_MIN_PREVALENCE": "EARLY_ATTACK_OR_OVIPOSITION_POSITIVE_FLOWERS_PER_SCREENED_FLOWERS",
    "P0_WATER_POSITIVE_PREVALENCE": "WATER_POSITIVE_FLOWERING_PLANTS_PER_SCREENED_FLOWERING_PLANTS",
}
ROUTES = {
    "EXTERNAL_NUMERIC_TRANSPORT": (
        "EXTERNAL_MATCHED_PRIMARY_SOURCE",
        "NUMERIC_TRANSPORT_QUALIFIED",
    ),
    "FRESH_INDEPENDENT_CALIBRATION": (
        "INDEPENDENT_NATURAL_HISTORY_CALIBRATION",
        "FRESH_CALIBRATION_QUALIFIED",
    ),
}


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _filled(value: object, label: str) -> str:
    out = str(value).strip()
    _need(bool(out) and "REQUIRED_BEFORE_USE" not in out, f"unfrozen {label}")
    return out


def _positive(value: object, label: str) -> float:
    _need(isinstance(value, (int, float)) and not isinstance(value, bool), f"{label} must be numeric")
    out = float(value)
    _need(math.isfinite(out) and out > 0, f"{label} must be finite and > 0")
    return out


def validate(payload: dict) -> dict:
    _need(payload.get("schema_version") == SCHEMA, "wrong P0 relevance qualification schema")
    _need(payload.get("status") == "QUALIFICATION_CANDIDATE", "qualification payload must be QUALIFICATION_CANDIDATE")

    ctx = payload.get("context", {})
    _need(ctx.get("system") == "Pedicularis rex", "wrong system")
    for key in ("candidate_id", "candidate_site_id", "population_id", "season_id", "screen_window_id"):
        _filled(ctx.get(key), f"context.{key}")
    _need(ctx.get("p0_outcomes_opened") is False, "P0 outcomes already opened")

    permission = payload.get("permission_scope_receipt")
    _need(
        isinstance(permission, dict),
        "P0 qualification permission scope receipt missing",
    )
    validate_confirmed_permission_scope(
        permission,
        expected_candidate_id=ctx["candidate_id"],
    )

    _need(set(payload.get("allowed_routes", [])) == set(ROUTES), "allowed qualification routes changed")
    firewall = payload.get("firewall", {})
    for key in (
        "figure_read_off_without_exact_source_forbidden",
        "endpoint_substitution_forbidden",
        "historical_sample_size_as_numeric_source_forbidden",
        "fresh_calibration_units_p0_decision_reuse_forbidden",
        "fresh_calibration_units_downstream_confirmatory_reuse_forbidden",
        "qualification_must_precede_p0_outcomes",
    ):
        _need(firewall.get(key) is True, f"qualification firewall disabled: {key}")

    inputs = payload.get("inputs", [])
    _need(isinstance(inputs, list) and inputs, "qualification inputs missing")
    ids = [row.get("input_id") for row in inputs]
    _need(len(ids) == len(set(ids)), "duplicate relevance input_id")
    _need(set(ids) == REQUIRED_IDS, "relevance input inventory mismatch")

    qualified = []
    values = {}
    plant_based_fresh_route_used = any(
        row.get("input_id") in {
            "P0_PREDATOR_MIN_PREVALENCE",
            "P0_WATER_POSITIVE_PREVALENCE",
        }
        and row.get("qualification_route") == "FRESH_INDEPENDENT_CALIBRATION"
        for row in inputs
    )
    physical_handoff = None
    if plant_based_fresh_route_used:
        raw_handoff = payload.get("physical_unit_firewall_handoff")
        _need(
            isinstance(raw_handoff, dict),
            "fresh calibration physical-unit firewall handoff missing",
        )
        physical_handoff = validate_firewall_block(raw_handoff)

    for row in inputs:
        input_id = row["input_id"]
        _need(row.get("target_metric") == TARGET_METRICS[input_id], f"target metric changed: {input_id}")
        route = row.get("qualification_route")
        _need(route in ROUTES, f"invalid qualification route: {input_id}")
        expected_source, expected_status = ROUTES[route]
        _need(row.get("source_type") == expected_source, f"source type/route mismatch: {input_id}")
        _need(row.get("qualification_status") == expected_status, f"qualification status/route mismatch: {input_id}")
        _filled(row.get("source_reference"), f"source_reference/{input_id}")
        _filled(row.get("source_metric"), f"source_metric/{input_id}")
        _filled(row.get("biological_rationale"), f"biological_rationale/{input_id}")
        _need(row.get("endpoint_match") is True, f"endpoint mismatch: {input_id}")
        _need(row.get("unit_or_denominator_match") is True, f"unit/denominator mismatch: {input_id}")
        _need(row.get("frozen_before_p0_outcomes") is True, f"input not frozen before P0 outcomes: {input_id}")

        value = _positive(row.get("numeric_value"), f"numeric_value/{input_id}")
        if input_id != "P0_POLLINATOR_MIN_RATE":
            _need(value <= 1, f"prevalence must be <=1: {input_id}")
            _need(row.get("numeric_units") == "PROPORTION_0_1", f"wrong prevalence units: {input_id}")
        else:
            _need(
                row.get("numeric_units") == "LEGITIMATE_VISITS_PER_FLOWER_MINUTE",
                "pollinator numeric units must be flower-minute based",
            )

        if route == "EXTERNAL_NUMERIC_TRANSPORT":
            _need(row.get("context_transport_justified") is True, f"external context transport not justified: {input_id}")
            _need(
                row.get("fresh_calibration_units_independent_of_p0") is False,
                f"external route should not claim fresh calibration units: {input_id}",
            )
        else:
            _need(
                row.get("fresh_calibration_units_independent_of_p0") is True,
                f"fresh calibration not independent of P0: {input_id}",
            )
            _need(
                row.get("fresh_calibration_units_downstream_confirmatory_ineligible") is True,
                f"fresh calibration units not firewalled from downstream confirmatory use: {input_id}",
            )

        qualified.append(input_id)
        values[input_id] = {
            "value": value,
            "units": row["numeric_units"],
            "source_type": expected_source,
            "qualification_status": expected_status,
            "source_reference": row["source_reference"],
            "qualification_route": route,
        }

    metadata = payload.get("qualification_metadata", {})
    for key in ("slk_source_commit", "qualification_commit", "qualification_timestamp"):
        _filled(metadata.get(key), f"qualification_metadata.{key}")

    return {
        "schema_version": "SLK_PEDICULARIS_P0_RELEVANCE_QUALIFICATION_RECEIPT_V1",
        "status": "P0_MINIMUM_RELEVANCE_INPUTS_QUALIFIED",
        "context": {
            "system": "Pedicularis rex",
            "candidate_id": ctx["candidate_id"],
            "candidate_site_id": ctx["candidate_site_id"],
            "population_id": ctx["population_id"],
            "season_id": ctx["season_id"],
            "screen_window_id": ctx["screen_window_id"],
            "p0_outcomes_opened": False,
        },
        "qualified_inputs": qualified,
        "values": values,
        "permission_scope_receipt": permission,
        "physical_unit_firewall_handoff": (
            {
                "schema_version": "SLK_PEDICULARIS_PHYSICAL_PLANT_FIREWALL_V1",
                "require_nonempty_physical_plant_tag": True,
                "prior_physical_plant_tags_forbidden": sorted(
                    physical_handoff["forbidden_tags"]
                ),
                "prior_tag_source_references": physical_handoff[
                    "source_references"
                ],
                "prior_tag_set_sha256": physical_handoff[
                    "prior_tag_set_sha256"
                ],
                "frozen_before_outcomes": True,
            }
            if physical_handoff is not None
            else None
        ),
        "qualification_commit": metadata["qualification_commit"],
        "claim_ceiling": "MINIMUM_RELEVANCE_SOURCE_QUALIFICATION_ONLY_NO_P0_OR_G1_G5_RESULT",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Pedicularis P0 minimum-relevance numeric sources")
    parser.add_argument("qualification_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = validate(json.loads(args.qualification_json.read_text(encoding="utf-8")))
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
