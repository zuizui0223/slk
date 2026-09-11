"""Fail-closed adjudication for the SLK Pedicularis G2 composite receipt.

This script does not estimate L. SCH owns that estimation. It checks whether a
filled composite receipt carries the non-circular V2 provenance and compatible
context required before SLK may promote Pedicularis from partial support to a
biological G2 result.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


SCHEMA = "SLK_PEDICULARIS_G2_RECEIPT_V1"
SYSTEM = "Pedicularis rex"
FITNESS_BUDGET_SCHEMA = "SCH_COMPONENT_CONFLICT_BUDGET_V1"
HANDOFF_SCHEMA = "THREE_WORLD_CONFLICT_HANDOFF_V1"
V2_WRAPPER = "SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2"
READINESS_V3 = "SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3"
PREDATOR_V3 = "SCH_PEDICULARIS_PREDATOR_METHOD_V3"
CORE_SURFACE = "SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1"
POSITIVE_G1 = "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE"
POSITIVE_COMPONENT = "CONTEXT_STABLE_COMPONENT_OPTIMA_IDENTIFIED"
POSITIVE_BUDGET = "FITNESS_SCALE_SHARED_CONFLICT_BUDGET_IDENTIFIED"
POSITIVE_HANDOFF = "THREE_WORLD_CONFLICT_CONTEXT_IDENTIFIED"
WATER_FIXED = "HELD_FIXED_ACROSS_ALL_SCH_CELLS"


def _text(value: Any, name: str) -> str:
    out = str(value).strip()
    if not out or out == "REQUIRED_BEFORE_USE":
        raise ValueError(f"{name} must be frozen before positive adjudication")
    return out


def _nonnegative(value: Any, name: str) -> float:
    out = float(value)
    if not math.isfinite(out) or out < 0:
        raise ValueError(f"{name} must be finite and non-negative")
    return out


def _context_tuple(obj: dict[str, Any]) -> tuple[str, str, str, str, str]:
    return (
        _text(obj.get("context_id"), "context_id"),
        _text(obj.get("system"), "system"),
        _text(obj.get("population_id"), "population_id"),
        _text(obj.get("season_id"), "season_id"),
        _text(obj.get("fitness_scale_id"), "fitness_scale_id"),
    )


def adjudicate(receipt: dict[str, Any]) -> dict[str, Any]:
    if receipt.get("receipt_schema_version") != SCHEMA:
        raise ValueError(f"receipt must use {SCHEMA}")

    context = receipt.get("context") or {}
    canonical = receipt.get("canonical_sch_path") or {}
    anti = receipt.get("anti_circularity") or {}
    g1_surface = receipt.get("g1_surface") or {}
    component = receipt.get("component_upgrade") or {}
    budget = receipt.get("conflict_budget") or {}
    handoff = receipt.get("three_world_handoff") or {}

    # Canonical path is structural provenance, not optional prose.
    if canonical.get("readiness_schema") != READINESS_V3:
        raise ValueError("Pedicularis G2 requires SCH readiness V3")
    if canonical.get("surface_wrapper_schema") != V2_WRAPPER:
        raise ValueError("Pedicularis G2 requires the non-circular V2 full-surface wrapper")
    if canonical.get("core_surface_schema") != CORE_SURFACE:
        raise ValueError("unexpected SCH core surface schema")
    if canonical.get("predator_method_schema") != PREDATOR_V3:
        raise ValueError("Pedicularis G2 requires independent predator method V3")
    if canonical.get("water_y") != WATER_FIXED:
        raise ValueError("water-y must be held fixed during the SCH surface")
    if "POLLINATOR_ACCESS_PRESERVED" not in str(canonical.get("predator_method_requirement", "")):
        raise ValueError("predator method must preserve pollinator access")

    if anti.get("water_used_as_sch_antagonist_G") is not False:
        raise ValueError("deprecated water-as-G SCH reference is forbidden")
    if anti.get("independent_predator_exposure_used") is not True:
        raise ValueError("independent predator exposure is required")
    if anti.get("water_y_held_fixed_during_sch_surface") is not True:
        raise ValueError("water-y must be fixed across the SCH surface")

    # An incomplete prospective receipt is allowed to remain explicitly open.
    g1_positive = (
        g1_surface.get("status") == POSITIVE_G1
        and g1_surface.get("opposing_geometry_identified") is True
        and g1_surface.get("interior_combined_optimum_supported") is True
    )
    if not g1_positive:
        return {
            "g1": "PARTIAL_SUPPORT",
            "g2": "NOT_IDENTIFIED",
            "g2_detail": "G1_CAUSAL_SURFACE_NOT_YET_POSITIVE",
            "downstream_balance_eligible": False,
            "downstream_bita_non_circular_eligible": False,
        }

    component_positive = component.get("status") == POSITIVE_COMPONENT
    if not component_positive:
        return {
            "g1": "DIRECT_PASS",
            "g2": "NOT_IDENTIFIED",
            "g2_detail": "COMPONENT_OPTIMUM_UPGRADE_NOT_IDENTIFIED",
            "downstream_balance_eligible": False,
            "downstream_bita_non_circular_eligible": False,
        }

    if budget.get("receipt_schema_version") != FITNESS_BUDGET_SCHEMA:
        raise ValueError("unexpected SCH conflict-budget schema")
    if budget.get("status") != POSITIVE_BUDGET:
        return {
            "g1": "DIRECT_PASS",
            "g2": "NOT_IDENTIFIED",
            "g2_detail": "FITNESS_SCALE_CONFLICT_BUDGET_NOT_IDENTIFIED",
            "downstream_balance_eligible": False,
            "downstream_bita_non_circular_eligible": False,
        }

    if handoff.get("receipt_schema_version") != HANDOFF_SCHEMA:
        raise ValueError("unexpected three-world handoff schema")
    if handoff.get("status") != POSITIVE_HANDOFF:
        return {
            "g1": "DIRECT_PASS",
            "g2": "NOT_IDENTIFIED",
            "g2_detail": "THREE_WORLD_HANDOFF_NOT_IDENTIFIED",
            "downstream_balance_eligible": False,
            "downstream_bita_non_circular_eligible": False,
        }

    ctx = _context_tuple(context)
    hctx = _context_tuple(handoff)
    if ctx != hctx:
        raise ValueError("context/system/population/season/fitness scale must match exactly")
    if ctx[1] != SYSTEM:
        raise ValueError(f"system must be {SYSTEM}")
    if _text(budget.get("fitness_scale_id"), "budget fitness_scale_id") != ctx[4]:
        raise ValueError("budget fitness scale must match frozen context")

    point = _nonnegative(budget.get("L_S_component"), "budget L point")
    raw_ci = budget.get("L_S_component_95_ci")
    if not isinstance(raw_ci, list) or len(raw_ci) != 2:
        raise ValueError("budget L_S_component_95_ci must have two elements")
    blo = _nonnegative(raw_ci[0], "budget L lower")
    bhi = _nonnegative(raw_ci[1], "budget L upper")
    if not blo <= point <= bhi:
        raise ValueError("budget L point must lie inside its 95% interval")

    hload = handoff.get("conflict_load") or {}
    hpoint = _nonnegative(hload.get("point"), "handoff L point")
    hlo = _nonnegative(hload.get("lower_95"), "handoff L lower")
    hhi = _nonnegative(hload.get("upper_95"), "handoff L upper")
    if not hlo <= hpoint <= hhi:
        raise ValueError("handoff L point must lie inside its 95% interval")
    if (point, blo, bhi) != (hpoint, hlo, hhi):
        raise ValueError("handoff L values must exactly match the SCH conflict-budget export")

    if hlo > 0:
        return {
            "g1": "DIRECT_PASS",
            "g2": "DIRECT_PASS",
            "g2_detail": "G2_DIRECT_PASS_POSITIVE",
            "conflict_load": {"point": hpoint, "lower_95": hlo, "upper_95": hhi},
            "downstream_balance_eligible": True,
            "downstream_bita_non_circular_eligible": True,
        }

    return {
        "g1": "DIRECT_PASS",
        "g2": "PARTIAL_SUPPORT",
        "g2_detail": "G2_MEASURED_BUT_ZERO_COMPATIBLE",
        "conflict_load": {"point": hpoint, "lower_95": hlo, "upper_95": hhi},
        "downstream_balance_eligible": False,
        "downstream_bita_non_circular_eligible": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    result = adjudicate(receipt)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
