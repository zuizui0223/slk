from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

FREEZE_SCHEMA = "SLK_PEDICULARIS_CONTEXT_RECOVERY_FREEZE_V1"
OBS_SCHEMA = "SLK_PEDICULARIS_CONTEXT_RECOVERY_OBSERVATION_V1"
PRODUCTION_STATUS = "PEDICULARIS_CONTEXT_RECOVERY_PROSPECTIVELY_FROZEN"
ALLOWED_PRIOR_STATUSES = {
    "HISTORICAL_CANDIDATE_ONLY",
    "HISTORICAL_OCCURRENCE_ONLY",
    "RECENT_ASSESSMENT_OCCURRENCE_ONLY",
}
ALLOWED_PERMISSION = {"CONFIRMED"}
REQUIRED_PERMISSION_SCOPE = "RECOVERY_PLUS_P0A_NONDESTRUCTIVE"
PERMISSION_RECEIPT_SCHEMA = "SLK_PEDICULARIS_WAVE1_PERMISSION_SCOPE_RECEIPT_V1"
PERMISSION_RECEIPT_STATUS = "RECOVERY_P0A_PERMISSION_SCOPE_CONFIRMED"
ALLOWED_TAXON_VERIFICATION_METHODS = {
    "FIELD_MORPHOLOGY_PHOTO",
    "VOUCHER_OR_SPECIMEN",
    "EXPERT_CONFIRMATION",
    "COMBINED",
}
FIELD_MORPHOLOGY_METHODS = {"FIELD_MORPHOLOGY_PHOTO", "COMBINED"}
TAXON_KEY_SOURCE = "FLORA_OF_CHINA_PEDICULARIS_SERIES_REGES_KEY"
CANDIDATE_LEDGER_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "PEDICULARIS_CONTEXT_CANDIDATE_LEDGER_V1.csv"
)


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _filled(value: object, label: str) -> str:
    out = str(value).strip()
    _need(bool(out) and "REQUIRED_BEFORE_USE" not in out, f"unfrozen {label}")
    return out


def _optional_text(value: object) -> str | None:
    text = str(value).strip()
    if not text or "REQUIRED_BEFORE_USE" in text:
        return None
    return text


def _optional_bool(value: object, label: str) -> bool | None:
    if value is None or str(value).strip() == "":
        return None
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    _need(text in {"true", "false", "1", "0", "yes", "no"}, f"{label} must be boolean-like")
    return text in {"true", "1", "yes"}


def _optional_nonnegative_int(value: object, label: str) -> int | None:
    if value is None or str(value).strip() == "":
        return None
    _need(not isinstance(value, bool), f"{label} must be an integer")
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be an integer") from exc
    _need(math.isfinite(out) and out >= 0 and out.is_integer(), f"{label} must be a nonnegative integer")
    return int(out)


def _candidate_ledger_row(candidate_id: str) -> dict[str, str]:
    with CANDIDATE_LEDGER_PATH.open(newline="", encoding="utf-8") as handle:
        rows = [
            row for row in csv.DictReader(handle)
            if str(row.get("candidate_id", "")).strip() == candidate_id
        ]
    _need(len(rows) == 1, f"candidate_id not uniquely registered in candidate ledger: {candidate_id}")
    return rows[0]


def validate_freeze(freeze: dict) -> dict:
    _need(freeze.get("schema_version") == FREEZE_SCHEMA, "wrong context-recovery freeze schema")
    _need(freeze.get("status") == "FROZEN_CANDIDATE", "context recovery freeze must be FROZEN_CANDIDATE")
    _need(freeze.get("production_status") == PRODUCTION_STATUS, "wrong context-recovery production status")

    ctx = freeze.get("context", {})
    _need(ctx.get("system") == "Pedicularis rex", "wrong context-recovery system")
    for key in ("candidate_id", "candidate_site_id", "population_id", "season_id", "recovery_window_id"):
        _filled(ctx.get(key), f"context.{key}")
    _need(ctx.get("frozen_before_recovery_observations") is True, "context recovery was not frozen before observations")

    anchor = freeze.get("historical_anchor", {})
    _filled(anchor.get("source_type"), "historical source_type")
    _filled(anchor.get("source_reference"), "historical source_reference")
    ledger_row = _candidate_ledger_row(ctx["candidate_id"])
    _need(
        anchor.get("source_type") == ledger_row.get("source_type"),
        "historical source_type does not match candidate ledger",
    )
    _need(
        anchor.get("source_reference") == ledger_row.get("source_reference"),
        "historical source_reference does not match candidate ledger",
    )
    _need(
        anchor.get("candidate_status_before_recovery")
        == ledger_row.get("current_status"),
        "candidate prior status does not match candidate ledger",
    )
    _need(
        anchor.get("candidate_status_before_recovery") in ALLOWED_PRIOR_STATUSES,
        "candidate must begin as a historical-only candidate",
    )
    _need(anchor.get("use") == "PRIORITIZATION_ONLY_NOT_FRESH_CONTEXT_PASS", "historical anchor use changed")

    downstream = freeze.get("downstream_windows", {})
    for key in ("p0_relevance_calibration_window_id", "p0_screen_window_id"):
        _filled(downstream.get(key), f"downstream_windows.{key}")

    rules = freeze.get("decision_rules", {})
    for key in (
        "require_fresh_taxon_confirmation",
        "require_current_flowering_population",
        "require_current_site_access",
        "require_sampling_permission_resolved",
        "require_same_season_revisit_feasible",
        "require_at_least_one_independent_flowering_plant_seen",
        "interaction_signal_not_required_at_recovery",
        "capacity_pass_not_inferred_at_recovery",
    ):
        _need(rules.get(key) is True, f"context recovery decision rule disabled: {key}")

    firewall = freeze.get("firewall", {})
    for key in (
        "historical_record_cannot_count_as_fresh_recovery",
        "recovery_does_not_test_pollinator_predator_or_water_signal",
        "recovery_does_not_establish_p0_capacity",
        "failed_recovery_is_not_species_absence",
        "p0_relevance_calibration_remains_next_biological_signal_gate",
    ):
        _need(firewall.get(key) is True, f"context recovery firewall disabled: {key}")

    metadata = freeze.get("freeze_metadata", {})
    for key in ("slk_source_commit", "freeze_commit", "freeze_timestamp"):
        _filled(metadata.get(key), f"freeze_metadata.{key}")

    return {
        "context": ctx,
        "historical_anchor": anchor,
        "downstream_windows": downstream,
        "freeze_commit": metadata["freeze_commit"],
    }


def adjudicate(observation: dict, freeze: dict) -> dict:
    cfg = validate_freeze(freeze)
    _need(observation.get("schema_version") == OBS_SCHEMA, "wrong context-recovery observation schema")
    _need(observation.get("status") == "FRESH_CONTEXT_RECOVERY_DATA", "context recovery observation is not filled data")

    octx = observation.get("context", {})
    fctx = cfg["context"]
    for key in ("system", "candidate_id", "candidate_site_id", "population_id", "season_id", "recovery_window_id"):
        _need(octx.get(key) == fctx.get(key), f"recovery observation/freeze context mismatch: {key}")

    prohibited = observation.get("prohibited_recovery_inferences", {})
    for key in (
        "pollinator_signal_scored",
        "predator_signal_scored",
        "water_state_signal_scored",
        "p0_capacity_pass_scored",
    ):
        _need(prohibited.get(key) is False, f"recovery illegally scored downstream endpoint: {key}")

    fresh = observation.get("fresh_verification", {})
    verification_date = str(fresh.get("verification_date", "")).strip()
    source_reference = str(fresh.get("verification_source_reference", "")).strip()
    taxon = _optional_bool(fresh.get("taxon_identity_confirmed"), "taxon_identity_confirmed")
    flowering = _optional_bool(fresh.get("flowering_population_present"), "flowering_population_present")
    plants_seen = _optional_nonnegative_int(fresh.get("independent_flowering_plants_seen"), "independent_flowering_plants_seen")
    access = _optional_bool(fresh.get("site_access_confirmed"), "site_access_confirmed")
    permission_raw = str(fresh.get("sampling_permission_status", "")).strip()
    permission_scope = _optional_text(fresh.get("sampling_permission_scope"))
    revisit = _optional_bool(fresh.get("same_season_revisit_feasible"), "same_season_revisit_feasible")

    permission_receipt = observation.get("permission_scope_receipt")
    permission_receipt_valid = False
    if permission_raw in ALLOWED_PERMISSION:
        _need(
            permission_scope == REQUIRED_PERMISSION_SCOPE,
            "confirmed recovery permission has wrong scope",
        )
        _need(
            isinstance(permission_receipt, dict),
            "confirmed recovery permission scope receipt missing",
        )
        _need(
            permission_receipt.get("schema_version") == PERMISSION_RECEIPT_SCHEMA,
            "wrong recovery permission scope receipt schema",
        )
        _need(
            permission_receipt.get("status") == PERMISSION_RECEIPT_STATUS,
            "recovery permission scope receipt is not confirmed",
        )
        _need(
            permission_receipt.get("candidate_id") == fctx["candidate_id"],
            "recovery permission scope receipt candidate mismatch",
        )
        _need(
            permission_receipt.get("required_scope") == REQUIRED_PERMISSION_SCOPE,
            "recovery permission scope receipt scope changed",
        )
        matrix = permission_receipt.get("required_activity_matrix")
        _need(
            isinstance(matrix, dict) and set(matrix) == {"A", "B", "C"},
            "recovery permission scope receipt activity matrix changed",
        )
        for activity_id in ("A", "B", "C"):
            cell = matrix[activity_id]
            _need(
                isinstance(cell, dict)
                and cell.get("regulatory") == "PASS"
                and cell.get("site") == "PASS",
                f"recovery permission scope not passed for activity {activity_id}",
            )
        permission_receipt_valid = True

    taxon_method = _optional_text(fresh.get("taxon_verification_method"))
    if taxon_method is not None:
        _need(
            taxon_method in ALLOWED_TAXON_VERIFICATION_METHODS,
            "unregistered taxon verification method",
        )
    diagnostic_checklist = None
    if taxon_method in FIELD_MORPHOLOGY_METHODS:
        raw_diag = fresh.get("taxon_diagnostic_checklist")
        if isinstance(raw_diag, dict):
            _need(
                raw_diag.get("source_reference") == TAXON_KEY_SOURCE,
                "field morphology taxon checklist source changed",
            )
            leaves_four = _optional_bool(
                raw_diag.get("leaves_mostly_whorls_of_4_documented"),
                "leaves_mostly_whorls_of_4_documented",
            )
            cupular = _optional_bool(
                raw_diag.get(
                    "petiole_and_bract_bases_enlarged_connate_cupular_documented"
                ),
                "petiole_and_bract_bases_enlarged_connate_cupular_documented",
            )
            whole_ref = _optional_text(raw_diag.get("whole_plant_photo_reference"))
            whorl_ref = _optional_text(raw_diag.get("leaf_whorl_photo_reference"))
            cup_ref = _optional_text(raw_diag.get("cupular_base_photo_reference"))
            color_required = _optional_bool(
                raw_diag.get("flower_color_used_as_required_diagnostic"),
                "flower_color_used_as_required_diagnostic",
            )
            diagnostic_checklist = {
                "source_reference": TAXON_KEY_SOURCE,
                "leaves_mostly_whorls_of_4_documented": leaves_four,
                "petiole_and_bract_bases_enlarged_connate_cupular_documented": cupular,
                "whole_plant_photo_reference": whole_ref,
                "leaf_whorl_photo_reference": whorl_ref,
                "cupular_base_photo_reference": cup_ref,
                "flower_color_used_as_required_diagnostic": color_required,
            }
            if (
                leaves_four is None
                or cupular is None
                or whole_ref is None
                or whorl_ref is None
                or cup_ref is None
                or color_required is None
            ):
                diagnostic_checklist = None
            elif taxon is True:
                _need(
                    leaves_four is True and cupular is True,
                    "positive field-morphology taxon confirmation requires both registered diagnostic features",
                )
                _need(
                    color_required is False,
                    "flower color cannot be a required P. rex diagnostic",
                )

    evidence = {
        "taxon": _optional_text(fresh.get("taxon_evidence_reference")),
        "flowering_population": _optional_text(
            fresh.get("flowering_population_evidence_reference")
        ),
        "access": _optional_text(fresh.get("access_evidence_reference")),
        "sampling_permission": _optional_text(
            fresh.get("sampling_permission_reference")
        ),
        "revisit_plan": _optional_text(fresh.get("revisit_plan_reference")),
    }

    complete = (
        bool(verification_date)
        and "REQUIRED_BEFORE_USE" not in verification_date
        and bool(source_reference)
        and "REQUIRED_BEFORE_USE" not in source_reference
        and taxon is not None
        and flowering is not None
        and plants_seen is not None
        and access is not None
        and permission_raw not in {"", "REQUIRED_BEFORE_USE"}
        and permission_scope is not None
        and revisit is not None
        and taxon_method is not None
        and all(value is not None for value in evidence.values())
        and (
            taxon_method not in FIELD_MORPHOLOGY_METHODS
            or diagnostic_checklist is not None
        )
    )

    if not complete:
        status = "CONTEXT_RECOVERY_INCOMPLETE"
    elif not taxon:
        status = "CONTEXT_RECOVERY_TAXON_UNCONFIRMED"
    elif not flowering:
        _need(plants_seen == 0, "no flowering population cannot have flowering plants seen")
        status = "CONTEXT_RECOVERY_NO_FLOWERING_POPULATION"
    else:
        _need(plants_seen >= 1, "flowering population requires at least one independent flowering plant seen")
        if not access or permission_raw not in ALLOWED_PERMISSION:
            status = "CONTEXT_RECOVERY_ACCESS_BLOCKED"
        elif not revisit:
            status = "CONTEXT_RECOVERY_CURRENT_SEASON_NOT_FEASIBLE"
        else:
            status = "CONTEXT_RECOVERY_READY_FOR_P0_RELEVANCE_CALIBRATION"

    ready = status == "CONTEXT_RECOVERY_READY_FOR_P0_RELEVANCE_CALIBRATION"
    return {
        "schema_version": "SLK_PEDICULARIS_CONTEXT_RECOVERY_RECEIPT_V1",
        "status": status,
        "context": {
            "system": "Pedicularis rex",
            "candidate_id": fctx["candidate_id"],
            "candidate_site_id": fctx["candidate_site_id"],
            "population_id": fctx["population_id"],
            "season_id": fctx["season_id"],
            "recovery_window_id": fctx["recovery_window_id"],
        },
        "fresh_verification": {
            "verification_date": verification_date or None,
            "verification_source_reference": source_reference or None,
            "taxon_identity_confirmed": taxon,
            "taxon_verification_method": taxon_method,
            "taxon_evidence_reference": evidence["taxon"],
            "taxon_diagnostic_checklist": diagnostic_checklist,
            "flowering_population_present": flowering,
            "flowering_population_evidence_reference": evidence[
                "flowering_population"
            ],
            "independent_flowering_plants_seen": plants_seen,
            "site_access_confirmed": access,
            "access_evidence_reference": evidence["access"],
            "sampling_permission_status": permission_raw or None,
            "sampling_permission_scope": permission_scope,
            "sampling_permission_reference": evidence["sampling_permission"],
            "permission_scope_receipt_validated": permission_receipt_valid,
            "same_season_revisit_feasible": revisit,
            "revisit_plan_reference": evidence["revisit_plan"],
        },
        "historical_anchor": cfg["historical_anchor"],
        "downstream_handoff": {
            "p0_relevance_calibration_authorized": ready,
            "p0_relevance_calibration_window_id": cfg["downstream_windows"]["p0_relevance_calibration_window_id"],
            "p0_screen_window_id": cfg["downstream_windows"]["p0_screen_window_id"],
        },
        "firewall": {
            "historical_anchor_used_for_priority_not_pass": True,
            "no_pollinator_predator_water_signal_claim": True,
            "no_p0_capacity_claim": True,
            "failed_recovery_is_not_species_absence": True,
        },
        "next_action": (
            "FREEZE_AND_EXECUTE_P0_RELEVANCE_NATURAL_HISTORY_CALIBRATION"
            if ready
            else "COMPLETE_RECOVERY_OR_TRY_NEXT_CANDIDATE"
        ),
        "freeze_commit": cfg["freeze_commit"],
        "claim_ceiling": "FRESH_CONTEXT_EXISTENCE_AND_LOGISTICAL_FEASIBILITY_ONLY_NO_P0_SIGNAL_NO_G1_G5_RESULT",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Adjudicate fresh Pedicularis candidate-context recovery")
    parser.add_argument("observation_json", type=Path)
    parser.add_argument("freeze_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = adjudicate(
        json.loads(args.observation_json.read_text(encoding="utf-8")),
        json.loads(args.freeze_json.read_text(encoding="utf-8")),
    )
    text_out = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text_out, encoding="utf-8")
    else:
        print(text_out, end="")


if __name__ == "__main__":
    main()
