from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "scripts" / "generate_pedicularis_context_recovery_packet.py"
ADJ = ROOT / "scripts" / "adjudicate_pedicularis_context_recovery.py"

spec = importlib.util.spec_from_file_location("ped_context_packet_gen", GEN)
gen = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(gen)

spec2 = importlib.util.spec_from_file_location("ped_context_recovery_adj_for_packet", ADJ)
adj = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(adj)


def _packet() -> dict:
    return gen.build_packet(
        candidate_id="SHANGRILA_WUFENG",
        candidate_site_id="site-wufeng",
        population_id="pop-wufeng-2027",
        season_id="2027",
        recovery_window_id="recovery-2027-a",
        p0_relevance_calibration_window_id="p0-cal-2027-a",
        p0_screen_window_id="p0-screen-2027-a",
    )


def test_packet_uses_canonical_candidate_ledger_snapshot() -> None:
    packet = _packet()
    snap = packet["candidate_ledger_snapshot"]
    assert snap["candidate_id"] == "SHANGRILA_WUFENG"
    assert snap["source_type"] == "DIRECT_INTERACTION_FIELD_SITE"
    assert snap["source_reference"] == "10.1098/rsbl.2013.0387"
    assert snap["current_status"] == "HISTORICAL_CANDIDATE_ONLY"
    freeze = packet["freeze_draft"]
    assert freeze["historical_anchor"]["source_reference"] == snap["source_reference"]
    assert freeze["historical_anchor"]["candidate_status_before_recovery"] == snap["current_status"]
    assert packet["recovery_queue_snapshot"]["recovery_wave"] == "WAVE1"
    locator = packet["scouting_locator_snapshot"]
    assert locator["locator_type"] == "POINT"
    assert locator["point"]["latitude_deg"] == pytest.approx(27.796111)
    assert locator["point"]["longitude_deg"] == pytest.approx(99.709722)
    assert packet["observation_template"]["scouting_locator_snapshot"] == locator


def test_generated_draft_cannot_be_adjudicated_before_freeze() -> None:
    packet = _packet()
    freeze = packet["freeze_draft"]
    obs = packet["observation_template"]
    obs["status"] = "FRESH_CONTEXT_RECOVERY_DATA"
    with pytest.raises(ValueError, match="must be FROZEN_CANDIDATE"):
        adj.adjudicate(obs, freeze)


def test_unknown_candidate_is_rejected() -> None:
    with pytest.raises(ValueError, match="not uniquely registered"):
        gen.build_packet(
            candidate_id="NOT_IN_LEDGER",
            candidate_site_id="site-x",
            population_id="pop-x",
            season_id="2027",
            recovery_window_id="rec-x",
            p0_relevance_calibration_window_id="cal-x",
            p0_screen_window_id="screen-x",
        )


def test_frozen_generated_packet_flows_into_recovery_adjudicator() -> None:
    packet = _packet()
    freeze = packet["freeze_draft"]
    freeze["status"] = "FROZEN_CANDIDATE"
    freeze["context"]["frozen_before_recovery_observations"] = True
    freeze["freeze_metadata"] = {
        "slk_source_commit": "abc123",
        "freeze_commit": "freeze123",
        "freeze_timestamp": "2027-05-01T00:00:00Z",
    }

    obs = packet["observation_template"]
    obs["status"] = "FRESH_CONTEXT_RECOVERY_DATA"
    obs["fresh_verification"].update(
        {
            "verification_date": "2027-06-15",
            "verification_source_reference": "FIELD_RECOVERY_LOG_001",
            "taxon_identity_confirmed": True,
            "taxon_verification_method": "FIELD_MORPHOLOGY_PHOTO",
            "taxon_evidence_reference": "PHOTO_SET_TAXON_001",
            "flowering_population_present": True,
            "flowering_population_evidence_reference": "PHOTO_SET_FLOWERING_001",
            "independent_flowering_plants_seen": 8,
            "site_access_confirmed": True,
            "access_evidence_reference": "FIELD_ACCESS_LOG_001",
            "sampling_permission_status": "CONFIRMED",
            "sampling_permission_reference": "PERMIT_001",
            "same_season_revisit_feasible": True,
            "revisit_plan_reference": "REVISIT_PLAN_001",
        }
    )

    out = adj.adjudicate(obs, freeze)
    assert out["status"] == "CONTEXT_RECOVERY_READY_FOR_P0_RELEVANCE_CALIBRATION"
    assert out["context"]["candidate_id"] == "SHANGRILA_WUFENG"



def test_new_daocheng_seed_dna_anchor_is_recovery_only() -> None:
    packet = gen.build_packet(
        candidate_id="DAOCHENG_IFLORA_2011",
        candidate_site_id="site-daocheng",
        population_id="pop-daocheng-2027",
        season_id="2027",
        recovery_window_id="recovery-daocheng-2027",
        p0_relevance_calibration_window_id="cal-daocheng-2027",
        p0_screen_window_id="screen-daocheng-2027",
    )
    snap = packet["candidate_ledger_snapshot"]
    assert snap["source_type"] == "SEED_DNA_COLLECTION"
    assert snap["source_reference"] == "iFlora.cn:SunH-07ZX-3605"
    assert snap["current_status"] == "HISTORICAL_OCCURRENCE_ONLY"
    assert packet["freeze_draft"]["historical_anchor"]["use"] == (
        "PRIORITIZATION_ONLY_NOT_FRESH_CONTEXT_PASS"
    )
    assert packet["recovery_queue_snapshot"]["recovery_wave"] == "WAVE2"
    assert packet["scouting_locator_snapshot"] is None



def test_songzanlin_2025_assessment_anchor_stays_occurrence_only() -> None:
    packet = gen.build_packet(
        candidate_id="SONGZANLIN_EIA_2025",
        candidate_site_id="site-songzanlin-2027",
        population_id="pop-songzanlin-2027",
        season_id="2027",
        recovery_window_id="recovery-songzanlin-2027",
        p0_relevance_calibration_window_id="cal-songzanlin-2027",
        p0_screen_window_id="screen-songzanlin-2027",
    )
    snap = packet["candidate_ledger_snapshot"]
    assert snap["source_type"] == "RECENT_ENVIRONMENTAL_ASSESSMENT"
    assert snap["current_status"] == "RECENT_ASSESSMENT_OCCURRENCE_ONLY"
    assert snap["priority_for_fresh_p0"] == "HIGH"
    freeze = packet["freeze_draft"]
    assert freeze["historical_anchor"]["candidate_status_before_recovery"] == (
        "RECENT_ASSESSMENT_OCCURRENCE_ONLY"
    )
    assert freeze["historical_anchor"]["use"] == (
        "PRIORITIZATION_ONLY_NOT_FRESH_CONTEXT_PASS"
    )



def test_songzanlin_packet_embeds_project_evaluation_envelope_not_point() -> None:
    packet = gen.build_packet(
        candidate_id="SONGZANLIN_EIA_2025",
        candidate_site_id="site-songzanlin-2027",
        population_id="pop-songzanlin-2027",
        season_id="2027",
        recovery_window_id="recovery-songzanlin-2027",
        p0_relevance_calibration_window_id="cal-songzanlin-2027",
        p0_screen_window_id="screen-songzanlin-2027",
    )
    locator = packet["scouting_locator_snapshot"]
    assert locator["locator_type"] == "ENVELOPE"
    assert locator["locator_claim"] == "RECENT_OFFICIAL_PROJECT_EVALUATION_AREA_ENVELOPE"
    assert locator["envelope"]["lat_min_deg"] == pytest.approx(27.850706)
    assert locator["envelope"]["lat_max_deg"] == pytest.approx(27.871333)
    assert locator["envelope"]["lon_min_deg"] == pytest.approx(99.688308)
    assert locator["envelope"]["lon_max_deg"] == pytest.approx(99.709172)
    assert "not an exact plant locality" in locator["notes"]
