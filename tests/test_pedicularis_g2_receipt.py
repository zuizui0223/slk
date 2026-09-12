from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "adjudicate_pedicularis_g2_receipt.py"

spec = importlib.util.spec_from_file_location("pedicularis_g2", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)
adjudicate = module.adjudicate


def _receipt() -> dict:
    return {
        "receipt_schema_version": "SLK_PEDICULARIS_G2_RECEIPT_V1",
        "context": {
            "context_id": "ped-rex-pop1-2027",
            "system": "Pedicularis rex",
            "population_id": "pop1",
            "season_id": "2027",
            "fitness_scale_id": "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER",
        },
        "canonical_sch_path": {
            "readiness_schema": "SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3",
            "surface_wrapper_schema": "SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2",
            "core_surface_schema": "SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1",
            "predator_method_schema": "SCH_PEDICULARIS_PREDATOR_METHOD_V3",
            "water_y": "HELD_FIXED_ACROSS_ALL_SCH_CELLS",
            "predator_method_requirement": (
                "TIMED_POST_POLLINATION_OR_LOCAL_BARRIER_QUALIFIED_WITH_"
                "POLLINATOR_ACCESS_PRESERVED"
            ),
        },
        "g1_surface": {
            "status": "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE",
            "opposing_geometry_identified": True,
            "interior_combined_optimum_supported": True,
        },
        "component_upgrade": {
            "status": "CONTEXT_STABLE_COMPONENT_OPTIMA_IDENTIFIED"
        },
        "conflict_budget": {
            "receipt_schema_version": "SCH_COMPONENT_CONFLICT_BUDGET_V1",
            "status": "FITNESS_SCALE_SHARED_CONFLICT_BUDGET_IDENTIFIED",
            "fitness_scale_id": "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER",
            "L_S_component": 2.0,
            "L_S_component_95_ci": [1.0, 3.0],
        },
        "three_world_handoff": {
            "receipt_schema_version": "THREE_WORLD_CONFLICT_HANDOFF_V1",
            "status": "THREE_WORLD_CONFLICT_CONTEXT_IDENTIFIED",
            "context_id": "ped-rex-pop1-2027",
            "system": "Pedicularis rex",
            "population_id": "pop1",
            "season_id": "2027",
            "fitness_scale_id": "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER",
            "conflict_load": {
                "point": 2.0,
                "lower_95": 1.0,
                "upper_95": 3.0,
            },
        },
        "anti_circularity": {
            "water_used_as_sch_antagonist_G": False,
            "independent_predator_exposure_used": True,
            "water_y_held_fixed_during_sch_surface": True,
        },
    }


def test_positive_non_circular_receipt_closes_g2() -> None:
    result = adjudicate(_receipt())
    assert result["g1"] == "DIRECT_PASS"
    assert result["g2"] == "DIRECT_PASS"
    assert result["g2_detail"] == "G2_DIRECT_PASS_POSITIVE"
    assert result["context"] == {
        "context_id": "ped-rex-pop1-2027",
        "system": "Pedicularis rex",
        "population_id": "pop1",
        "season_id": "2027",
        "fitness_scale_id": "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER",
    }
    assert result["downstream_balance_eligible"] is True
    assert result["downstream_bita_non_circular_eligible"] is True


def test_zero_compatible_interval_is_measured_but_not_balance_eligible() -> None:
    receipt = json.loads(json.dumps(_receipt()))
    receipt["conflict_budget"]["L_S_component_95_ci"][0] = 0.0
    receipt["three_world_handoff"]["conflict_load"]["lower_95"] = 0.0
    result = adjudicate(receipt)
    assert result["g1"] == "DIRECT_PASS"
    assert result["g2"] == "PARTIAL_SUPPORT"
    assert result["g2_detail"] == "G2_MEASURED_BUT_ZERO_COMPATIBLE"
    assert result["context"]["context_id"] == "ped-rex-pop1-2027"
    assert result["downstream_balance_eligible"] is False


def test_legacy_water_as_g_is_rejected() -> None:
    receipt = _receipt()
    receipt["anti_circularity"]["water_used_as_sch_antagonist_G"] = True
    with pytest.raises(ValueError, match="water-as-G"):
        adjudicate(receipt)
