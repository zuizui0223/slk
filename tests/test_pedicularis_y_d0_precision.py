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
    assert module.n_paired_equivalence(1.0, 0.5) == 35
    assert module.n_two_group_equivalence(1.0, 0.5) == 69
    assert module.n_paired_superiority(1.0, 0.5, 1.0) == 32
    assert module.n_two_group_superiority(1.0, 0.5, 1.0) == 63
    assert module.n_mean_precision(1.0, 0.5) == 16


def test_attrition_inflation_is_prospective_and_conservative():
    assert module.inflate_for_attrition(20, 0.15) == 24
    assert module.inflate_for_attrition(25, 0.15) == 30


def test_manifest_keeps_incompatible_allocation_units_separate():
    manifest = {
        "defaults": {
            "alpha": 0.05,
            "power": 0.80,
            "joint_qualification_power": 0.80,
            "attrition": 0.15,
        },
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
    assert maxima["paired_plants_total"]["inflated_required_n"] == 52
    assert maxima["paired_plants_total"]["driving_endpoints"] == ["paired_eq"]
    assert maxima["plants_per_group"]["inflated_required_n"] == 103
    assert maxima["plants_per_group"]["driving_endpoints"] == ["two_group_eq"]
    minima = result["analysis_minima_by_allocation_unit"]
    assert minima["paired_plants_total"]["raw_required_n"] == 44
    assert minima["plants_per_group"]["raw_required_n"] == 87
    joint = result["joint_qualification_design"]
    assert joint["target_all_pass_power"] == 0.80
    assert joint["power_endpoint_count"] == 2
    assert abs(joint["per_endpoint_power_floor"] - 0.90) < 1e-12
    assert joint["status"] == "JOINT_QUALIFICATION_POWER_TARGET_REGISTERED"
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
    two_sided = module.n_paired_superiority(
        1.0, 0.5, 1.0, directional=False
    )
    directional = module.n_paired_superiority(
        1.0, 0.5, 1.0, directional=True
    )
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


def test_tost_formula_targets_requested_power_at_true_difference_zero():
    n = module.n_paired_equivalence(
        sd_diff=1.0,
        margin=0.5,
        alpha=0.05,
        power=0.80,
    )
    z_alpha = module._z(0.95)
    standardized = 0.5 * (n ** 0.5) / 1.0 - z_alpha
    achieved = 2 * module.NormalDist().cdf(standardized) - 1
    assert n == 35
    assert achieved >= 0.80


def test_joint_all_pass_target_allocates_failure_budget_across_endpoints():
    endpoints = [
        {
            "endpoint_id": f"eq_{i}",
            "kind": "paired_equivalence",
            "sd_diff": 1.0,
            "margin": 0.5,
        }
        for i in range(15)
    ]
    result = module.plan_manifest(
        {
            "defaults": {
                "alpha": 0.05,
                "power": 0.80,
                "joint_qualification_power": 0.80,
                "attrition": 0.0,
            },
            "input_provenance": {
                "confirmatory_outcomes_opened": False,
            },
            "endpoints": endpoints,
        }
    )
    joint = result["joint_qualification_design"]
    expected_floor = 1 - (1 - 0.80) / 15
    assert abs(joint["per_endpoint_power_floor"] - expected_floor) < 1e-12
    assert abs(
        1 - 15 * (1 - joint["per_endpoint_power_floor"]) - 0.80
    ) < 1e-12
    assert all(
        row["power"] >= expected_floor for row in result["results"]
    )


def test_superiority_planning_requires_alternative_above_frozen_threshold():
    with pytest.raises(ValueError, match="planning_effect must exceed"):
        module.n_paired_superiority(
            sd_diff=1.0,
            min_effect=0.5,
            planning_effect=0.5,
        )


def test_fifteen_endpoint_joint_target_gives_reference_n_values():
    joint_floor = 1 - (1 - 0.80) / 15
    paired_n = module.n_paired_equivalence(
        sd_diff=1.0,
        margin=0.5,
        alpha=0.05,
        power=joint_floor,
    )
    two_group_n = module.n_two_group_equivalence(
        sd=1.0,
        margin=0.5,
        alpha=0.05,
        power=joint_floor,
    )
    assert paired_n == 68
    assert two_group_n == 136
    assert (
        module.normal_approx_paired_equivalence_power(
            paired_n, 1.0, 0.5, 0.05
        )
        >= joint_floor
    )
    assert (
        module.normal_approx_two_group_equivalence_power(
            two_group_n, 1.0, 0.5, 0.05
        )
        >= joint_floor
    )
