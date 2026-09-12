from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


SCHEMA = "SLK_PEDICULARIS_D0_MARGIN_FREEZE_V1"
ALLOWED_Q5_ROUTES = {
    "NEGLIGIBLE_BURDEN_EQUIVALENCE",
    "MEASURED_BURDEN_ADJUSTMENT",
}
NUMERIC_CRITERIA = {
    "EQUIVALENCE",
    "CONTAMINATION_BOUND",
    "MINIMUM_USEFUL_EFFECT",
    "MAX_CI_HALF_WIDTH",
}
REQUIRED_ENDPOINT_IDS = {
    "D0_Q1_Z",
    "D0_Q1_OPENING",
    "D0_Q1_STIGMA",
    "D0_Q1_ORIENTATION",
    "D0_Q1_DAMAGE",
    "D0_Q2_VOLUME",
    "D0_Q2_DURATION",
    "D0_Q2_COVERAGE",
    "D0_Q2_PROTECTION",
    "D0_Q3_VISIT",
    "D0_Q3_POLLEN",
    "D0_Q3_INITIAL_SEED",
    "D0_Q4_WET_EFFECT",
    "D0_Q4_DRY_RESIDUAL",
    "D0_Q5_BURDEN_EQ",
    "D0_Q5_BURDEN_PRECISION",
    "D0_Q6_HORIZON",
}
EXPECTED_COMPARISONS = {
    "D0_Q1_Z": "D0_MINUS_SHAM",
    "D0_Q1_OPENING": "D0_MINUS_SHAM",
    "D0_Q1_STIGMA": "D0_MINUS_SHAM",
    "D0_Q1_ORIENTATION": "D0_MINUS_SHAM",
    "D0_Q1_DAMAGE": "D0_MINUS_SHAM",
    "D0_Q2_VOLUME": "D0_MINUS_D",
    "D0_Q2_DURATION": "D0_MINUS_D",
    "D0_Q2_COVERAGE": "D0_MINUS_D",
    "D0_Q2_PROTECTION": "D0_MINUS_D",
    "D0_Q3_VISIT": "D0_MINUS_SHAM",
    "D0_Q3_POLLEN": "D0_MINUS_SHAM",
    "D0_Q3_INITIAL_SEED": "D0_MINUS_SHAM",
    "D0_Q4_WET_EFFECT": "WET_D0_MINUS_DRY_OR_SHAM",
    "D0_Q4_DRY_RESIDUAL": "SHAM_MINUS_S",
    "D0_Q5_BURDEN_EQ": "S_MINUS_SHAM",
    "D0_Q5_BURDEN_PRECISION": "S_MINUS_SHAM",
    "D0_Q6_HORIZON": "S_EQ_D0_EQ_D",
}


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _filled_text(value: object) -> bool:
    return (
        isinstance(value, str)
        and bool(value.strip())
        and "REQUIRED_BEFORE_USE" not in value
    )


def _positive_number(value: object) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
        and float(value) > 0
    )


def _required_for_route(endpoint: dict, q5_route: str) -> bool:
    if endpoint.get("required_for_production") is True:
        return True
    return endpoint.get("required_if_q5_route") == q5_route


def validate(manifest: dict) -> dict:
    _need(manifest.get("schema_version") == SCHEMA, "wrong schema_version")

    context = manifest.get("context", {})
    _need(context.get("system") == "Pedicularis rex", "wrong system")
    for key in (
        "population_id",
        "season_id",
        "protocol_version",
        "fitness_scale_id",
        "time_horizon_id",
        "y_cal_dataset_id",
        "d0_cal_dataset_id",
        "confirmatory_dataset_id",
    ):
        _need(_filled_text(context.get(key)), f"unfrozen context field: {key}")

    _need(
        context.get("confirmatory_outcomes_opened") is False,
        "confirmatory outcomes already opened",
    )
    q5_route = context.get("q5_route")
    _need(q5_route in ALLOWED_Q5_ROUTES, "invalid or unfrozen q5_route")

    confirmatory_id = context["confirmatory_dataset_id"]
    for calibration_key in ("y_cal_dataset_id", "d0_cal_dataset_id"):
        _need(
            context[calibration_key] != confirmatory_id,
            f"{calibration_key} cannot equal confirmatory_dataset_id",
        )

    firewall = manifest.get("firewall", {})
    for key in (
        "variance_only_margin_basis_forbidden",
        "confirmatory_outcome_derived_margin_forbidden",
        "nonsignificant_pvalue_as_equivalence_forbidden",
        "pilot_units_excluded_from_confirmatory_g3_g5",
    ):
        _need(firewall.get(key) is True, f"firewall not active: {key}")

    allowed_sources = set(manifest.get("allowed_source_types", []))
    forbidden_sources = set(manifest.get("forbidden_source_types", []))
    _need(bool(allowed_sources), "allowed_source_types empty")
    _need(bool(forbidden_sources), "forbidden_source_types empty")
    _need(not (allowed_sources & forbidden_sources), "source-type allow/forbid overlap")

    endpoints = manifest.get("endpoints", [])
    _need(isinstance(endpoints, list) and endpoints, "endpoints missing")
    ids = [x.get("endpoint_id") for x in endpoints]
    _need(len(ids) == len(set(ids)), "duplicate endpoint_id")
    _need(set(ids) == REQUIRED_ENDPOINT_IDS, "endpoint inventory mismatch")

    validated: list[str] = []
    skipped: list[str] = []

    for endpoint in endpoints:
        endpoint_id = endpoint["endpoint_id"]
        _need(
            endpoint.get("comparison") == EXPECTED_COMPARISONS[endpoint_id],
            f"comparison identity mismatch: {endpoint_id}",
        )
        required = _required_for_route(endpoint, q5_route)
        if not required:
            skipped.append(endpoint_id)
            continue

        criterion = endpoint.get("criterion_type")
        value = endpoint.get("value")
        if criterion in NUMERIC_CRITERIA:
            _need(_positive_number(value), f"missing/invalid numeric value: {endpoint_id}")
        elif criterion == "EXACT_IDENTITY":
            _need(
                value == "SAME_REGISTERED_HORIZON",
                f"invalid exact identity: {endpoint_id}",
            )
        else:
            raise ValueError(f"unsupported criterion_type for {endpoint_id}: {criterion}")

        source_type = endpoint.get("source_type")
        _need(source_type in allowed_sources, f"unapproved source_type: {endpoint_id}")
        _need(source_type not in forbidden_sources, f"forbidden source_type: {endpoint_id}")
        _need(
            isinstance(endpoint.get("source_reference"), list)
            and len(endpoint["source_reference"]) > 0,
            f"source_reference missing: {endpoint_id}",
        )
        _need(_filled_text(endpoint.get("margin_basis")), f"margin_basis missing: {endpoint_id}")
        _need(
            _filled_text(endpoint.get("biological_rationale")),
            f"biological_rationale missing: {endpoint_id}",
        )
        _need(
            endpoint.get("variance_only_basis") is False,
            f"variance-only margin forbidden: {endpoint_id}",
        )
        _need(
            endpoint.get("derived_from_confirmatory_outcome") is False,
            f"confirmatory-outcome-derived margin forbidden: {endpoint_id}",
        )
        _need(
            endpoint.get("frozen_before_confirmatory_outcomes") is True,
            f"endpoint not prospectively frozen: {endpoint_id}",
        )

        calibration_id = endpoint.get("calibration_dataset_id")
        if calibration_id is not None:
            _need(_filled_text(calibration_id), f"bad calibration_dataset_id: {endpoint_id}")
            _need(
                calibration_id != confirmatory_id,
                f"calibration/confirmatory dataset reuse: {endpoint_id}",
            )

        if endpoint_id == "D0_Q4_WET_EFFECT":
            _need(
                source_type == "BIOLOGICAL_RELEVANCE_PLUS_CALIBRATION",
                "D0_Q4_WET_EFFECT requires biological relevance plus calibration",
            )
        if endpoint_id == "D0_Q5_BURDEN_PRECISION":
            _need(
                source_type == "DOWNSTREAM_DECISION_INVARIANCE",
                "burden precision target must come from downstream decision invariance",
            )
        if endpoint_id == "D0_Q6_HORIZON":
            _need(source_type == "DESIGN_INVARIANCE", "Q6 horizon must be design invariance")

        validated.append(endpoint_id)

    metadata = manifest.get("freeze_metadata", {})
    for key in ("slk_source_commit", "freeze_commit", "freeze_timestamp"):
        _need(_filled_text(metadata.get(key)), f"freeze metadata missing: {key}")

    return {
        "schema_version": SCHEMA,
        "status": "FROZEN_FOR_CONFIRMATORY_USE",
        "q5_route": q5_route,
        "validated_endpoints": validated,
        "route_skipped_endpoints": skipped,
        "confirmatory_outcomes_opened": False,
        "claim_ceiling": (
            "MARGINS_FROZEN_ONLY_NO_D0_OR_G3_G5_BIOLOGICAL_RESULT"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a prospective Pedicularis D0 biological margin freeze"
    )
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text())
    result = validate(manifest)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
