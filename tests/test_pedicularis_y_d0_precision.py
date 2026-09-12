from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "plan_pedicularis_y_d0_precision.py"
spec = importlib.util.spec_from_file_location("ped_y_d0_precision", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_reference_normal_approximation_values():
    assert module.n_paired_equivalence(1.0, 0.5) == 25
    assert module.n_two_group_equivalence(1.0, 0.5) == 50
    assert module.n_paired_superiority(1.0, 0.5) == 32
    assert module.n_two_group_superiority(1.0, 0.5) == 63
    assert module.n_mean_precision(1.0, 0.5) == 16


def test_attrition_inflation_is_prospective_and_conservative():
    assert module.inflate_for_attrition(20, 0.15) == 24
    assert module.inflate_for_attrition(25, 0.15) == 30


def test_manifest_keeps_incompatible_allocation_units_separate():
    manifest = {
        "defaults": {"alpha": 0.05, "power": 0.80, "attrition": 0.15},
        "input_provenance": {
            "population_id": "pop1",
            "season_id": "2027",
            "fitness_scale_id": "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER",
            "time_horizon_id": "FLOWER_TO_MATURE_VIABLE_SEED",
            "confirmatory_dataset_id": "PED_D0_QUAL_CONFIRM_V1",
            "confirmatory_outcomes_opened": False,
            "margin_freeze_commit": "abc123",
            "q5_route": "NEGLIGIBLE_BURDEN_EQUIVALENCE",
        },
        "endpoints": [
            {
                "endpoint_id": "paired_eq",
                "kind": "paired_equivalence",
                "sd_diff": 1.0,
                "margin": 0.5,
            },
            {
                "endpoint_id": "two_group_eq",
                "kind": "two_group_equivalence",
                "sd": 1.0,
                "margin": 0.5,
            },
        ],
    }
    result = module.plan_manifest(manifest)
    assert result["status"] == "PLANNING_ONLY_NOT_A_BIOLOGICAL_RECEIPT"
    assert result["input_provenance"] == manifest["input_provenance"]
    maxima = result["maxima_by_allocation_unit"]
    assert maxima["paired_plants_total"]["inflated_required_n"] == 30
    assert maxima["paired_plants_total"]["driving_endpoints"] == ["paired_eq"]
    assert maxima["plants_per_group"]["inflated_required_n"] == 59
    assert maxima["plants_per_group"]["driving_endpoints"] == ["two_group_eq"]
    assert "Do not take one numeric maximum" in result["allocation_rule"]


def test_precision_planner_rejects_opened_confirmatory_provenance():
    manifest = {
        "input_provenance": {"confirmatory_outcomes_opened": True},
        "endpoints": [
            {
                "endpoint_id": "paired_eq",
                "kind": "paired_equivalence",
                "sd_diff": 1.0,
                "margin": 0.5,
            }
        ],
    }
    with pytest.raises(ValueError, match="opened confirmatory outcomes"):
        module.plan_manifest(manifest)


def test_directional_gate_uses_one_sided_alpha_only_when_declared():
    two_sided = module.n_paired_superiority(1.0, 0.5, directional=False)
    directional = module.n_paired_superiority(1.0, 0.5, directional=True)
    assert directional < two_sided


def test_invalid_or_missing_design_inputs_fail_closed():
    with pytest.raises(ValueError):
        module.n_paired_equivalence(0.0, 0.5)
    with pytest.raises(ValueError):
        module.n_two_group_equivalence(1.0, 0.0)
    with pytest.raises(ValueError, match="unsupported kind"):
        module.plan_endpoint({"endpoint_id": "bad", "kind": "magic"})
    with pytest.raises(ValueError, match="no endpoints"):
        module.plan_manifest({"endpoints": []})
