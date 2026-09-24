from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ADJ = ROOT / "scripts" / "adjudicate_pedicularis_context_recovery.py"
COMP = ROOT / "scripts" / "compile_pedicularis_context_recovery_to_p0_calibration.py"
CAL_TEMPLATE = ROOT / "data" / "PEDICULARIS_P0_NATURAL_HISTORY_CALIBRATION_FREEZE_TEMPLATE_V1.json"

spec = importlib.util.spec_from_file_location("ped_context_recovery", ADJ)
adj = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(adj)

spec2 = importlib.util.spec_from_file_location("ped_context_recovery_compile", COMP)
comp = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(comp)


def _freeze() -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_CONTEXT_RECOVERY_FREEZE_V1",
        "status": "FROZEN_CANDIDATE",
        "context": {
            "system": "Pedicularis rex",
            "candidate_id": "SHANGRILA_WUFENG",
            "candidate_site_id": "site-wufeng",
            "population_id": "pop-wufeng-2027",
            "season_id": "2027",
            "recovery_window_id": "recovery-2027-a",
            "frozen_before_recovery_observations": True,
        },
        "historical_anchor": {
            "source_type": "DIRECT_INTERACTION_FIELD_SITE",
            "source_reference": "10.1098/rsbl.2013.0387",
            "candidate_status_before_recovery": "HISTORICAL_CANDIDATE_ONLY",
            "use": "PRIORITIZATION_ONLY_NOT_FRESH_CONTEXT_PASS",
        },
        "downstream_windows": {
            "p0_relevance_calibration_window_id": "p0-cal-2027-a",
            "p0_screen_window_id": "p0-screen-2027-a",
        },
        "decision_rules": {
            "require_fresh_taxon_confirmation": True,
            "require_current_flowering_population": True,
            "require_current_site_access": True,
            "require_sampling_permission_resolved": True,
            "require_same_season_revisit_feasible": True,
            "require_at_least_one_independent_flowering_plant_seen": True,
            "interaction_signal_not_required_at_recovery": True,
            "capacity_pass_not_inferred_at_recovery": True,
        },
        "firewall": {
            "historical_record_cannot_count_as_fresh_recovery": True,
            "recovery_does_not_test_pollinator_predator_or_water_signal": True,
            "recovery_does_not_establish_p0_capacity": True,
            "failed_recovery_is_not_species_absence": True,
            "p0_relevance_calibration_remains_next_biological_signal_gate": True,
        },
        "freeze_metadata": {
            "slk_source_commit": "abc123",
            "freeze_commit": "recovery-freeze-1",
            "freeze_timestamp": "2027-05-01T00:00:00Z",
        },
        "production_status": "PEDICULARIS_CONTEXT_RECOVERY_PROSPECTIVELY_FROZEN",
    }


def _obs() -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_CONTEXT_RECOVERY_OBSERVATION_V1",
        "status": "FRESH_CONTEXT_RECOVERY_DATA",
        "context": {
            "system": "Pedicularis rex",
            "candidate_id": "SHANGRILA_WUFENG",
            "candidate_site_id": "site-wufeng",
            "population_id": "pop-wufeng-2027",
            "season_id": "2027",
            "recovery_window_id": "recovery-2027-a",
        },
        "fresh_verification": {
            "verification_date": "2027-06-15",
            "verification_source_reference": "FIELD_RECOVERY_LOG_2027_001",
            "taxon_identity_confirmed": True,
            "taxon_verification_method": "FIELD_MORPHOLOGY_PHOTO",
            "taxon_evidence_reference": "PHOTO_SET_TAXON_001",
            "taxon_diagnostic_checklist": {
                "source_reference": "FLORA_OF_CHINA_PEDICULARIS_SERIES_REGES_KEY",
                "leaves_mostly_whorls_of_4_documented": True,
                "petiole_and_bract_bases_enlarged_connate_cupular_documented": True,
                "whole_plant_photo_reference": "PHOTO_WHOLE_001",
                "leaf_whorl_photo_reference": "PHOTO_WHORL_001",
                "cupular_base_photo_reference": "PHOTO_CUPULAR_001",
                "flower_color_used_as_required_diagnostic": False,
            },
            "flowering_population_present": True,
            "flowering_population_evidence_reference": "PHOTO_SET_FLOWERING_001",
            "independent_flowering_plants_seen": 12,
            "site_access_confirmed": True,
            "access_evidence_reference": "FIELD_ACCESS_LOG_001",
            "sampling_permission_status": "CONFIRMED",
            "sampling_permission_reference": "PERMIT_001",
            "same_season_revisit_feasible": True,
            "revisit_plan_reference": "REVISIT_PLAN_001",
            "notes": "fresh context only",
        },
        "prohibited_recovery_inferences": {
            "pollinator_signal_scored": False,
            "predator_signal_scored": False,
            "water_state_signal_scored": False,
            "p0_capacity_pass_scored": False,
        },
    }


def test_positive_recovery_unlocks_only_p0_relevance_calibration() -> None:
    out = adj.adjudicate(_obs(), _freeze())
    assert out["status"] == "CONTEXT_RECOVERY_READY_FOR_P0_RELEVANCE_CALIBRATION"
    assert out["downstream_handoff"]["p0_relevance_calibration_authorized"] is True
    assert out["firewall"]["no_pollinator_predator_water_signal_claim"] is True
    assert out["firewall"]["no_p0_capacity_claim"] is True


def test_historical_candidate_without_fresh_observations_is_incomplete() -> None:
    obs = _obs()
    obs["fresh_verification"]["verification_date"] = ""
    obs["fresh_verification"]["taxon_identity_confirmed"] = None
    out = adj.adjudicate(obs, _freeze())
    assert out["status"] == "CONTEXT_RECOVERY_INCOMPLETE"
    assert out["downstream_handoff"]["p0_relevance_calibration_authorized"] is False


def test_no_current_flowering_population_is_not_species_absence() -> None:
    obs = _obs()
    obs["fresh_verification"]["flowering_population_present"] = False
    obs["fresh_verification"]["independent_flowering_plants_seen"] = 0
    out = adj.adjudicate(obs, _freeze())
    assert out["status"] == "CONTEXT_RECOVERY_NO_FLOWERING_POPULATION"
    assert out["firewall"]["failed_recovery_is_not_species_absence"] is True


def test_access_or_permission_failure_blocks_current_context() -> None:
    obs = _obs()
    obs["fresh_verification"]["sampling_permission_status"] = "PENDING"
    out = adj.adjudicate(obs, _freeze())
    assert out["status"] == "CONTEXT_RECOVERY_ACCESS_BLOCKED"


def test_recovery_must_not_score_downstream_signals() -> None:
    obs = _obs()
    obs["prohibited_recovery_inferences"]["predator_signal_scored"] = True
    with pytest.raises(ValueError, match="illegally scored downstream endpoint"):
        adj.adjudicate(obs, _freeze())


def test_positive_recovery_compiles_context_into_p0_calibration_template() -> None:
    receipt = adj.adjudicate(_obs(), _freeze())
    template = json.loads(CAL_TEMPLATE.read_text())
    out = comp.compile_recovery(receipt, template)
    assert out["status"] == "CONTEXT_RECOVERY_COMPILED_AWAITING_P0_CALIBRATION_DESIGN"
    assert out["context"]["candidate_site_id"] == "site-wufeng"
    assert out["context"]["population_id"] == "pop-wufeng-2027"
    assert out["context"]["season_id"] == "2027"
    assert out["context"]["calibration_window_id"] == "p0-cal-2027-a"
    assert out["context"]["future_p0_screen_window_id"] == "p0-screen-2027-a"
    assert out["sampling"]["minimum_pollinator_bouts"] is None
    assert out["context"]["frozen_before_calibration_outcomes"] is False


def test_nonready_recovery_cannot_compile_p0_calibration() -> None:
    obs = _obs()
    obs["fresh_verification"]["same_season_revisit_feasible"] = False
    receipt = adj.adjudicate(obs, _freeze())
    template = json.loads(CAL_TEMPLATE.read_text())
    with pytest.raises(ValueError, match="not ready"):
        comp.compile_recovery(receipt, template)


def test_freeze_must_be_prospective() -> None:
    freeze = copy.deepcopy(_freeze())
    freeze["context"]["frozen_before_recovery_observations"] = False
    with pytest.raises(ValueError, match="not frozen before observations"):
        adj.adjudicate(_obs(), freeze)



def test_unregistered_candidate_cannot_be_frozen() -> None:
    freeze = _freeze()
    freeze["context"]["candidate_id"] = "MADE_UP_SITE"
    with pytest.raises(ValueError, match="not uniquely registered"):
        adj.adjudicate(_obs(), freeze)


def test_historical_source_must_match_candidate_ledger() -> None:
    freeze = _freeze()
    freeze["historical_anchor"]["source_reference"] = "WRONG_SOURCE"
    with pytest.raises(ValueError, match="source_reference does not match"):
        adj.adjudicate(_obs(), freeze)



def test_recent_assessment_candidate_can_enter_fresh_recovery_gate() -> None:
    freeze = _freeze()
    freeze["context"].update(
        {
            "candidate_id": "SONGZANLIN_EIA_2025",
            "candidate_site_id": "site-songzanlin",
            "population_id": "pop-songzanlin-2027",
            "recovery_window_id": "recovery-songzanlin-2027",
        }
    )
    freeze["historical_anchor"].update(
        {
            "source_type": "RECENT_ENVIRONMENTAL_ASSESSMENT",
            "source_reference": "XGLL_EIA_2025",
            "candidate_status_before_recovery": "RECENT_ASSESSMENT_OCCURRENCE_ONLY",
        }
    )

    obs = _obs()
    obs["context"].update(
        {
            "candidate_id": "SONGZANLIN_EIA_2025",
            "candidate_site_id": "site-songzanlin",
            "population_id": "pop-songzanlin-2027",
            "recovery_window_id": "recovery-songzanlin-2027",
        }
    )
    out = adj.adjudicate(obs, freeze)
    assert out["status"] == "CONTEXT_RECOVERY_READY_FOR_P0_RELEVANCE_CALIBRATION"
    assert out["historical_anchor"]["candidate_status_before_recovery"] == (
        "RECENT_ASSESSMENT_OCCURRENCE_ONLY"
    )



def test_recovery_without_evidence_references_is_incomplete() -> None:
    obs = _obs()
    obs["fresh_verification"]["taxon_evidence_reference"] = ""
    out = adj.adjudicate(obs, _freeze())
    assert out["status"] == "CONTEXT_RECOVERY_INCOMPLETE"
    assert out["downstream_handoff"]["p0_relevance_calibration_authorized"] is False


def test_unregistered_taxon_verification_method_is_rejected() -> None:
    obs = _obs()
    obs["fresh_verification"]["taxon_verification_method"] = "GUESS"
    with pytest.raises(ValueError, match="unregistered taxon verification method"):
        adj.adjudicate(obs, _freeze())


def test_positive_receipt_preserves_recovery_evidence_references() -> None:
    out = adj.adjudicate(_obs(), _freeze())
    fresh = out["fresh_verification"]
    assert fresh["taxon_evidence_reference"] == "PHOTO_SET_TAXON_001"
    assert fresh["flowering_population_evidence_reference"] == "PHOTO_SET_FLOWERING_001"
    assert fresh["access_evidence_reference"] == "FIELD_ACCESS_LOG_001"
    assert fresh["sampling_permission_reference"] == "PERMIT_001"
    assert fresh["revisit_plan_reference"] == "REVISIT_PLAN_001"



def test_field_morphology_confirmation_requires_diagnostic_checklist() -> None:
    obs = _obs()
    obs["fresh_verification"].pop("taxon_diagnostic_checklist")
    out = adj.adjudicate(obs, _freeze())
    assert out["status"] == "CONTEXT_RECOVERY_INCOMPLETE"


def test_positive_field_morphology_requires_both_registered_features() -> None:
    obs = _obs()
    obs["fresh_verification"]["taxon_diagnostic_checklist"][
        "leaves_mostly_whorls_of_4_documented"
    ] = False
    with pytest.raises(ValueError, match="requires both registered diagnostic features"):
        adj.adjudicate(obs, _freeze())


def test_flower_color_cannot_be_required_for_p_rex_confirmation() -> None:
    obs = _obs()
    obs["fresh_verification"]["taxon_diagnostic_checklist"][
        "flower_color_used_as_required_diagnostic"
    ] = True
    with pytest.raises(ValueError, match="flower color cannot be a required"):
        adj.adjudicate(obs, _freeze())


def test_taxon_unconfirmed_can_record_failed_morphology_without_false_pass() -> None:
    obs = _obs()
    obs["fresh_verification"]["taxon_identity_confirmed"] = False
    obs["fresh_verification"]["taxon_diagnostic_checklist"][
        "leaves_mostly_whorls_of_4_documented"
    ] = False
    out = adj.adjudicate(obs, _freeze())
    assert out["status"] == "CONTEXT_RECOVERY_TAXON_UNCONFIRMED"
    assert out["downstream_handoff"]["p0_relevance_calibration_authorized"] is False
