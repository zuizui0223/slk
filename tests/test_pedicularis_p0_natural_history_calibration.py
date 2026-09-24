from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_pedicularis_p0_natural_history_calibration_packet.py"
SUMMARIZER = ROOT / "scripts" / "summarize_pedicularis_p0_natural_history_calibration.py"
COMPILER = ROOT / "scripts" / "compile_pedicularis_p0_fresh_calibration_qualification.py"
QUAL_TEMPLATE = ROOT / "data" / "PEDICULARIS_P0_RELEVANCE_QUALIFICATION_TEMPLATE_V1.json"

spec = importlib.util.spec_from_file_location("ped_p0_cal_gen", GENERATOR)
gen = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(gen)

spec2 = importlib.util.spec_from_file_location("ped_p0_cal_sum", SUMMARIZER)
sum_mod = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(sum_mod)

spec3 = importlib.util.spec_from_file_location("ped_p0_cal_compile", COMPILER)
comp = importlib.util.module_from_spec(spec3)
assert spec3.loader is not None
spec3.loader.exec_module(comp)


def _freeze() -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_P0_NATURAL_HISTORY_CALIBRATION_FREEZE_V1",
        "status": "FROZEN_CANDIDATE",
        "context": {
            "system": "Pedicularis rex",
            "candidate_site_id": "site1",
            "population_id": "pop1",
            "season_id": "2027",
            "calibration_window_id": "cal1",
            "future_p0_screen_window_id": "screen1",
            "dataset_id": "PED_P0_NAT_HIST_CAL_V1",
            "frozen_before_calibration_outcomes": True,
            "p0_outcomes_opened": False,
        },
        "sampling": {
            "minimum_pollinator_bouts": 10,
            "minimum_pollinator_minutes_total": 100,
            "minimum_predator_flowers": 30,
            "minimum_water_state_plants": 20,
            "sampling_floor_source_type": "CALIBRATION_FEASIBILITY_ONLY",
            "sampling_floor_source_reference": "TEST_CAL_FEASIBILITY",
            "sampling_floor_rationale": "test-only independent calibration floor",
        },
        "qualification_rule": {
            "rule": "ONE_SIDED_INDEPENDENT_UNIT_BOOTSTRAP_LOWER_QUANTILE",
            "lower_quantile": 0.10,
            "bootstrap_seed": 1234,
            "bootstrap_reps": 1000,
            "minimum_bootstrap_reps": 1000,
            "minimum_valid_fraction": 0.95,
            "lower_quantile_source_type": "DOWNSTREAM_DESIGN_REQUIREMENT",
            "lower_quantile_source_reference": "TEST_LOWER_BOUND_RULE",
            "lower_quantile_rationale": "use an uncertainty-sensitive lower signal anchor for logistical P0 effort planning",
            "require_all_three_lower_bounds_strictly_positive": True,
        },
        "endpoints": {
            "pollinator": {
                "metric": "LEGITIMATE_VISITS_PER_FLOWER_MINUTE",
                "resampling_unit": "INDEPENDENT_TEMPORAL_BOUT",
                "required_fields": ["observed_minutes", "simultaneously_open_focal_flowers", "legitimate_pollinator_visits"],
            },
            "predator": {
                "metric": "EARLY_ATTACK_OR_OVIPOSITION_POSITIVE_FLOWERS_PER_SCREENED_FLOWERS",
                "resampling_unit": "INDEPENDENT_FOCAL_FLOWER",
                "required_fields": ["early_attack_or_oviposition_positive"],
            },
            "water_state": {
                "metric": "WATER_POSITIVE_FLOWERING_PLANTS_PER_SCREENED_FLOWERING_PLANTS",
                "resampling_unit": "INDEPENDENT_FLOWERING_PLANT",
                "required_fields": ["water_positive"],
            },
        },
        "firewall": {
            "calibration_units_p0_decision_ineligible": True,
            "calibration_units_qz_qp_qg_ineligible": True,
            "calibration_units_g1_g2_ineligible": True,
            "calibration_units_y_d0_ineligible": True,
            "calibration_units_g3_g5_ineligible": True,
            "calibration_values_may_define_p0_effort_only": True,
            "lower_bound_rule_frozen_before_calibration_outcomes": True,
            "failed_or_zero_compatible_calibration_not_rescued_posthoc": True,
        },
        "freeze_metadata": {
            "slk_source_commit": "abc123",
            "freeze_commit": "calfreeze123",
            "freeze_timestamp": "2027-05-01T00:00:00Z",
        },
        "production_status": "PEDICULARIS_P0_NATURAL_HISTORY_CALIBRATION_PROSPECTIVELY_FROZEN",
    }


def _filled_rows(*, rare_predator: bool = False) -> list[dict[str, str]]:
    rows = gen.generate(_freeze())
    pred_index = 0
    water_index = 0
    for row in rows:
        if row["record_type"] == "POLLINATOR_BOUT":
            row["observed_minutes"] = row["planned_minutes"]
            row["simultaneously_open_focal_flowers"] = "5"
            row["legitimate_pollinator_visits"] = "2"
        elif row["record_type"] == "PREDATOR_FLOWER":
            pred_index += 1
            row["plant_id"] = f"PP{pred_index:03d}"
            row["physical_plant_tag"] = f"PHY-P0CAL-PRED-{pred_index:03d}"
            row["flower_id"] = f"PF{pred_index:03d}"
            if rare_predator:
                row["early_attack_or_oviposition_positive"] = "true" if pred_index == 1 else "false"
            else:
                row["early_attack_or_oviposition_positive"] = "true" if pred_index <= 15 else "false"
        elif row["record_type"] == "WATER_PLANT":
            water_index += 1
            row["plant_id"] = f"WP{water_index:03d}"
            row["physical_plant_tag"] = f"PHY-P0CAL-WATER-{water_index:03d}"
            row["water_positive"] = "true" if water_index <= 15 else "false"
    return rows


def _qual_template() -> dict:
    payload = json.loads(QUAL_TEMPLATE.read_text())
    payload["context"].update(
        {
            "candidate_site_id": "site1",
            "population_id": "pop1",
            "season_id": "2027",
            "screen_window_id": "screen1",
            "p0_outcomes_opened": False,
        }
    )
    return payload


def test_generator_creates_disjoint_calibration_packet() -> None:
    rows = gen.generate(_freeze())
    assert sum(r["record_type"] == "POLLINATOR_BOUT" for r in rows) == 10
    assert sum(r["record_type"] == "PREDATOR_FLOWER" for r in rows) == 30
    assert sum(r["record_type"] == "WATER_PLANT" for r in rows) == 20
    assert all(r["calibration_only"] == "true" for r in rows)
    assert all(r["p0_decision_eligible"] == "false" for r in rows)
    assert all(r["downstream_confirmatory_eligible"] == "false" for r in rows)
    assert all(r["observed_minutes"] == "" for r in rows if r["record_type"] == "POLLINATOR_BOUT")
    assert all(float(r["planned_minutes"]) > 0 for r in rows if r["record_type"] == "POLLINATOR_BOUT")


def test_positive_calibration_qualifies_all_three_lower_bounds() -> None:
    receipt = sum_mod.summarize(_filled_rows(), _freeze())
    assert receipt["status"] == "P0_RELEVANCE_FRESH_CALIBRATION_QUALIFIED"
    assert receipt["qualification_ready"] is True
    assert receipt["estimates"]["pollinator"]["point"] == pytest.approx(0.04)
    assert receipt["estimates"]["pollinator"]["lower_bound"] > 0
    assert receipt["estimates"]["predator"]["lower_bound"] > 0
    assert receipt["estimates"]["water_state"]["lower_bound"] > 0
    assert receipt["firewall"]["calibration_units_p0_decision_ineligible"] is True
    handoff = receipt["physical_unit_registry_handoff"]
    assert handoff["current_physical_plant_count"] == 50
    assert handoff["next_stage_firewall_block"]["prior_tag_set_sha256"] == handoff["current_tag_set_sha256"]


def test_rare_predator_signal_can_remain_zero_compatible() -> None:
    receipt = sum_mod.summarize(_filled_rows(rare_predator=True), _freeze())
    assert receipt["status"] == "P0_RELEVANCE_FRESH_CALIBRATION_ZERO_COMPATIBLE_UNRESOLVED"
    assert receipt["qualification_ready"] is False
    assert receipt["estimates"]["predator"]["lower_bound"] == pytest.approx(0.0)
    assert receipt["recommended_minimum_relevance_values"] is None


def test_sampling_floor_failure_is_incomplete_not_negative() -> None:
    rows = _filled_rows()
    rows = [r for r in rows if r["record_id"] != "CAL-WATER-020"]
    receipt = sum_mod.summarize(rows, _freeze())
    assert receipt["status"] == "P0_RELEVANCE_FRESH_CALIBRATION_INCOMPLETE"
    assert receipt["sampling_floor_checks"]["water_plants"] is False


def test_calibration_unit_cannot_be_reused_as_p0_decision_unit() -> None:
    rows = _filled_rows()
    rows[0]["p0_decision_eligible"] = "true"
    with pytest.raises(ValueError, match="cannot be a P0 decision unit"):
        sum_mod.summarize(rows, _freeze())


def test_lower_bound_rule_must_be_frozen_before_calibration() -> None:
    freeze = _freeze()
    freeze["context"]["frozen_before_calibration_outcomes"] = False
    with pytest.raises(ValueError, match="not frozen"):
        sum_mod.summarize(_filled_rows(), freeze)


def test_qualified_calibration_compiles_into_relevance_qualification_candidate() -> None:
    receipt = sum_mod.summarize(_filled_rows(), _freeze())
    out = comp.compile_qualification(receipt, _qual_template())
    assert out["status"] == "CALIBRATION_VALUES_COMPILED_AWAITING_QUALIFICATION_METADATA"
    rows = {r["input_id"]: r for r in out["inputs"]}
    assert rows["P0_POLLINATOR_MIN_RATE"]["qualification_route"] == "FRESH_INDEPENDENT_CALIBRATION"
    assert rows["P0_POLLINATOR_MIN_RATE"]["numeric_units"] == "LEGITIMATE_VISITS_PER_FLOWER_MINUTE"
    assert rows["P0_PREDATOR_MIN_PREVALENCE"]["numeric_value"] > 0
    assert rows["P0_WATER_POSITIVE_PREVALENCE"]["numeric_value"] > 0
    assert rows["P0_WATER_POSITIVE_PREVALENCE"]["fresh_calibration_units_downstream_confirmatory_ineligible"] is True


def test_unresolved_calibration_cannot_compile_qualification() -> None:
    receipt = sum_mod.summarize(_filled_rows(rare_predator=True), _freeze())
    with pytest.raises(ValueError, match="not qualified"):
        comp.compile_qualification(receipt, _qual_template())


def test_missing_calibration_measurement_is_reported_and_blocks_qualification() -> None:
    rows = _filled_rows()
    # Add one extra valid water row so the numerical floor can still pass after
    # one registered row becomes incomplete.
    extra = dict(next(r for r in rows if r["record_type"] == "WATER_PLANT"))
    extra["record_id"] = "CAL-WATER-EXTRA"
    extra["plant_id"] = "WP-EXTRA"
    extra["physical_plant_tag"] = "PHY-P0CAL-WATER-EXTRA"
    extra["water_positive"] = "true"
    rows.append(extra)

    target = next(r for r in rows if r["record_id"] == "CAL-WATER-020")
    target["water_positive"] = ""

    receipt = sum_mod.summarize(rows, _freeze())
    assert receipt["sampling_floors_pass"] is True
    assert receipt["completion_audit"]["registered_rows_complete"] is False
    assert receipt["completion_audit"]["incomplete_records"] == 1
    assert receipt["completion_audit"]["incomplete_record_details"][0][
        "record_id"
    ] == "CAL-WATER-020"
    assert receipt["completion_audit"]["sensitivity_required"] is True
    assert receipt["status"] == "P0_RELEVANCE_FRESH_CALIBRATION_INCOMPLETE"
    assert receipt["qualification_ready"] is False


def test_calibration_receipt_reports_frozen_bootstrap_valid_fraction() -> None:
    receipt = sum_mod.summarize(_filled_rows(), _freeze())
    assert receipt["qualification_rule"]["minimum_valid_fraction"] == 0.95



def test_p0_calibration_requires_permanent_tags_for_plant_based_units() -> None:
    rows = _filled_rows()
    target = next(r for r in rows if r["record_type"] == "WATER_PLANT")
    target["physical_plant_tag"] = ""
    with pytest.raises(ValueError, match="physical_plant_tag"):
        sum_mod.summarize(rows, _freeze())


def test_p0_calibration_rejects_same_physical_plant_hidden_by_two_ids() -> None:
    rows = _filled_rows()
    water = [r for r in rows if r["record_type"] == "WATER_PLANT"]
    water[1]["physical_plant_tag"] = water[0]["physical_plant_tag"]
    with pytest.raises(ValueError, match="reused across assignment IDs"):
        sum_mod.summarize(rows, _freeze())
