import pytest

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ROADMAP = ROOT / "docs" / "PAPER_ROADMAP.md"
MANUSCRIPT = ROOT / "manuscript" / "SLK_MANUSCRIPT_AMNAT_V4.md"
THEORY = ROOT / "theory" / "UNIFIED_THRESHOLD_ATLAS_V1.md"
FIG1 = ROOT / "figures" / "FIG1_LOGIC_DIAGRAM.svg"
FIG2 = ROOT / "figures" / "FIG2_PHASE_MAP.svg"
FIG3 = ROOT / "figures" / "FIG3_EMPIRICAL_LADDER.svg"
LEDGER = ROOT / "docs" / "THEOREM_CLAIM_LEDGER_V1.md"
SECTION_MAP = ROOT / "docs" / "SECTION_CLAIM_MAP_V1.md"
EMPIRICAL_BRIDGE = ROOT / "docs" / "EMPIRICAL_BRIDGE_EVIDENCE_V1.md"

pytestmark = pytest.mark.document_sync


def test_environmental_threshold_displacement_is_retained_in_supporting_theory() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    figure = FIG3.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")

    for token in ("E_I=E_V+eta/a", "eta/a"):
        assert token in theory

    assert "UTA1.4" in theory
    assert "UTA1.4" in ledger
    assert "E_I" in manuscript
    assert "E_V" in manuscript
    assert "E_I" in figure
    assert "E_V" in figure

def test_ecological_prediction_distinguishes_frequency_feedback_signs() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    assert "Positive frequency dependence" in manuscript
    assert "negative frequency dependence" in manuscript
    assert "fail when uncommon" in manuscript
    assert "generate coexistence" in manuscript


def test_conflict_strength_is_not_promoted_to_differentiation_rank() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "incidence of division of labor need not increase monotonically" in manuscript
    assert "UTA1.5" in theory
    assert "UTA1.5" in ledger


def test_downstream_population_processes_are_demoted_to_supporting_theory() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8").lower()
    assert "finite-population fixation and long-run occupancy are retained in the supporting theory" in manuscript
    assert "rather than additional explanations for multifunctionality" in manuscript

def test_persistent_multifunctionality_three_selective_states_are_registered() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "UTA1.10" in theory
    assert "UTA1.10" in ledger
    assert "Three evolutionary bottlenecks behind one persistent phenotype" in manuscript
    assert "Adaptive integration." in manuscript
    assert "Historical or developmental trapping." in manuscript
    assert "Ecological stabilization of integration." in manuscript
    assert "Phi > 0 and g0 < 0" in manuscript
    assert "Phi > 0, g0 > 0, Delta_R < 0" in manuscript
    assert "does not guarantee fixation or historical realization" in manuscript
    assert "same morphology can consequently have different evolutionary meanings" in manuscript

def test_feedback_gradient_generalization_is_retained_in_supporting_theory() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "eta_0/(a-b)" in theory
    assert "UTA1.4b" in theory
    assert "UTA1.4b" in ledger
    assert "Community turnover can therefore change whether an innovation spreads" in manuscript

def test_two_frequency_identification_is_retained_in_supporting_theory() -> None:
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "UTA1.6" in theory
    assert "UTA1.6" in ledger


def test_three_frequency_curvature_diagnostic_is_retained_in_supporting_theory() -> None:
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "UTA1.7" in theory
    assert "UTA1.7" in ledger
    assert "does not inherit the canonical exponential-Moran fixation" in theory


def test_arbitrary_shape_endpoint_invasion_is_retained_in_supporting_theory() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "UTA1.8" in theory
    assert "UTA1.8" in ledger
    assert "Delta_R" in manuscript


def test_finite_frequency_endpoint_certification_is_retained_in_supporting_theory() -> None:
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "UTA1.9" in theory
    assert "UTA1.9" in ledger



def test_environmental_barrier_turnover_is_registered() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "UTA1.4c" in theory
    assert "UTA1.4c" in ledger
    assert "E_V<E_A<E_I" in theory
    assert "limiting explanation" in theory
    assert "same integrated phenotype" in theory
    assert "The same phenotype can change evolutionary meaning before it changes form" in manuscript
    assert "E_A" in manuscript
    assert "E_I" in manuscript


def test_natural_systems_anchor_multiple_conflict_resolutions() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    figure = FIG2.read_text(encoding="utf-8")
    for token in (
        "Natural systems show multiple resolutions of functional conflict",
        "Solanum rostratum",
        "Clarkia",
        "Penstemon",
        "Pedicularis rex",
        "Ipomoea purpurea",
        "Primula farinosa",
        "cichlid",
        "structural partitioning",
        "temporal partitioning",
        "ecological coupling",
    ):
        assert token in manuscript
    for token in (
        "Solanum rostratum",
        "Clarkia",
        "Penstemon + Keckiella",
        "Pedicularis rex",
        "Ipomoea + Primula",
        "Multifunctional fish skulls",
        "cichlids split capture from processing",
    ):
        assert token in figure


def test_ecology_only_phase_has_general_rare_type_criterion() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    figure = FIG3.read_text(encoding="utf-8")

    for text in (manuscript, theory):
        assert "Delta_R(E_A)<0" in text
        assert "B_A = Phi(E_A)" in text

    assert "ΔR(E_A)" in figure
    assert "ecological stabilization" in figure


def test_architecture_path_hysteresis_is_registered() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")

    assert "UTA1.4d" in theory
    assert "UTA1.4d" in ledger
    assert "k_S < k_V < k_D" in theory
    assert "E_H < E_V < E_A" in theory
    assert "architecture-path hysteresis" in theory
    assert "evolutionary legacy" in manuscript.lower()
    assert "frequency-dependent priority effects" in manuscript.lower()


def test_persistence_erosion_thresholds_are_registered() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")

    assert "UTA1.4e" in theory
    assert "UTA1.4e" in ledger
    assert "R(d_J)/d_J=k" in theory
    assert "p_C" in theory
    assert "(eta-Phi)/(2eta)" in theory
    assert "easier to overturn before morphology changes" in manuscript
    assert "p_C=(eta-Phi)/(2eta)" in manuscript


def test_structural_resolution_claims_are_candidate_relative() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    assert "given one integrated architecture and one specified structurally divided alternative" in manuscript
    assert "candidate-relative statement" in manuscript
    assert "does not show that integration is globally optimal" in manuscript
    assert "1.36% to 27.42%" in manuscript
    assert "integration can be the best architecture" not in manuscript.lower()


def test_environment_changes_the_evolutionary_bottleneck() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    assert "path limited" in manuscript
    assert "establishment limited" in manuscript
    assert "switch the limiting process from architecture economics" in manuscript


def test_hidden_bottleneck_turnover_is_the_reader_facing_spine() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    figure = FIG1.read_text(encoding="utf-8")
    for token in (
        "Persistent phenotypes can conceal change in their genetic or developmental underpinnings",
        "can the selective bottleneck preventing reorganization change while a multifunctional architecture remains visibly unchanged",
        "phenotypic stasis can conceal loss of evolutionary resistance",
    ):
        assert token in manuscript
    for token in (
        "One persistent phenotype can hide different evolutionary bottlenecks",
        "Same visible phenotype",
        "Unchanged morphology does not imply an unchanged evolutionary bottleneck or unchanged resistance",
    ):
        assert token in figure


def test_system_drift_is_not_confused_with_selective_bottleneck_turnover() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    assert "Developmental/system drift already shows" in manuscript
    assert "The natural systems reviewed above show structural, temporal, and integrated resolutions of conflict" in manuscript
    assert "separates three decision criteria" in manuscript
    assert "one integrated architecture and one specified divided alternative fixed" in manuscript


def test_section_claim_map_matches_current_manuscript_structure() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    section_map = SECTION_MAP.read_text(encoding="utf-8")
    headings = [
        "## 2. Functional conflict creates the problem, not its resolution",
        "## 3. Natural systems show multiple resolutions of functional conflict",
        "## 4. When is retaining multifunctionality favored over a structural alternative?",
        "## 5. When can evolutionary history preserve multifunctionality?",
        "## 6. How can ecology stabilize multifunctionality?",
        "## 7. Three evolutionary bottlenecks behind one persistent phenotype",
        "## 8. Formal backbone",
        "## 9. Ecological and evolutionary consequences",
        "## 10. Discussion",
    ]
    for heading in headings:
        assert heading in manuscript
        assert heading.removeprefix("## ") in section_map
    assert "full architecture -> path -> ecology sequence is a conditional biological prediction" in section_map


def test_hidden_resistance_is_not_promoted_to_generic_evolvability() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    assert "This is not generic resilience, propagule-pressure, or evolvability theory" in manuscript
    assert "d_J` and `p_C` slice identities" in manuscript


def test_pseudomonas_is_registered_only_as_positive_control() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    bridge = EMPIRICAL_BRIDGE.read_text(encoding="utf-8")
    assert "Experimental controls separate value, access, and ecological maintenance" in manuscript
    assert "the study does not estimate `Phi`, `g0`, or `Delta_R`" in manuscript
    assert "EMPIRICAL ANALOGUE / POSITIVE CONTROL" in bridge
    assert "not a DIRECT TEST OF STRUCTURAL SLK TURNOVER" in bridge
    assert "Resident-density Allee effect is therefore not Delta_R" in bridge


def test_direct_specialist_experiments_separate_value_from_coexistence() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    bridge = EMPIRICAL_BRIDGE.read_text(encoding="utf-8")
    assert "Bacillus subtilis" in manuscript
    assert "Pseudomonas aeruginosa" in manuscript
    assert "Stable specialist coexistence therefore does not itself imply positive net value of division of labour" in manuscript
    assert "not `Delta_R` of a divided collective invading a generalist resident" in manuscript
    assert "Empirical coverage matrix" in bridge
    assert "specialist-specialist negative frequency dependence" in bridge
    assert "no system that simultaneously measures" in bridge


def test_volvocine_system_is_path_anchor_not_g0_measurement() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    bridge = EMPIRICAL_BRIDGE.read_text(encoding="utf-8")
    assert "Volvocine algae make that last possibility concrete" in manuscript
    assert "PATH-ACCESSIBILITY EMPIRICAL ANCHOR" in bridge
    assert "do not estimate the SLK local path gradient `g0`" in bridge
    assert "Twenty-one of 48 lines (44%)" in bridge


def test_volvocine_path_bridge_is_scope_bounded() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    bridge = EMPIRICAL_BRIDGE.read_text(encoding="utf-8")
    assert "Volvocine algae make that last possibility concrete" in manuscript
    assert "21 of 48 lines evolved more differentiated colonies" in manuscript
    assert "These studies do not estimate `g_0`" in manuscript
    assert "STRUCTURAL EMPIRICAL BRIDGE FOR VALUE + DEVELOPMENTAL ACCESS" in bridge
    assert "not a full SLK gate closure" in bridge
    assert "2026 result is a preprint" in bridge


def test_stutzeri_is_rare_establishment_analogue_not_structural_delta() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    bridge = EMPIRICAL_BRIDGE.read_text(encoding="utf-8")
    assert "Pseudomonas stutzeri" in manuscript
    assert "weak-toxicity trend was non-significant and therefore unresolved rather than evidence of invasion failure" in manuscript
    assert "This is not a structurally divided alternative invading an integrated resident" in manuscript
    assert "RARE-ESTABLISHMENT EMPIRICAL ANCHOR / GENERALIST-SPECIALIST ANALOGUE" in bridge
    assert "not an estimate of structural `Delta_R`" in bridge
    assert "tau=1, P=0.042" in bridge
    assert "tau=0.67, P=0.31" in bridge
    assert "This treatment is **unresolved**, not evidence that the rare specialist had negative invasion fitness" in bridge


def test_gate_hierarchy_is_conditional_not_dynamically_independent() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    assert "conditional diagnostics, not dynamically independent mechanisms" in manuscript
    assert "must be re-evaluated in the new context rather than treated as fixed labels" in manuscript
    assert "The gate coordinates are conditional on the measured context" in theory
    assert "does not assume that architecture, path geometry, and ecology evolve independently" in theory


def test_empirical_bridge_is_on_canonical_reader_path() -> None:
    readme = README.read_text(encoding="utf-8")
    roadmap = ROADMAP.read_text(encoding="utf-8")
    section_map = SECTION_MAP.read_text(encoding="utf-8")
    bridge = EMPIRICAL_BRIDGE.read_text(encoding="utf-8")

    assert "docs/EMPIRICAL_BRIDGE_EVIDENCE_V1.md" in readme
    assert "EMPIRICAL_BRIDGE_EVIDENCE_LEDGER_REGISTERED" in readme
    assert "Canonical empirical evidence ledger" in roadmap
    assert "docs/EMPIRICAL_BRIDGE_EVIDENCE_V1.md" in section_map
    assert "no system that simultaneously measures" in bridge
    assert "unresolved" in bridge


def test_environmental_tradeoff_shifts_are_prior_art_not_slk_novelty() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    prior = (ROOT / "docs" / "PRIOR_ART_BOUNDARY_V1.md").read_text(encoding="utf-8")
    assert "Siepielski et al. 2026" in manuscript
    assert "does not claim that environmental change generically shifts constraints or trade-offs" in manuscript
    assert "strict convexity forces the architecture-value crossing to precede local accessibility" in manuscript
    assert "Environmentally reshaped trade-offs" in prior
    assert "must **not** claim that environmental change reshaping a trade-off" in prior
    assert "Delta_R(E_A)<0" in prior


def test_value_context_separation_is_not_promoted_as_new() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    prior = (ROOT / "docs" / "PRIOR_ART_BOUNDARY_V1.md").read_text(encoding="utf-8")
    assert "Wahl 2002" in manuscript
    assert "high divided-state value need not imply ecological success in every population context" in manuscript
    assert "Divided-state performance versus population context" in prior
    assert "must **not** claim that a high-value divided organization being disadvantaged" in prior


def test_changing_tradeoff_invasion_landscapes_are_prior_art() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    prior = (ROOT / "docs" / "PRIOR_ART_BOUNDARY_V1.md").read_text(encoding="utf-8")
    assert "Rueffler, Van Dooren, and Metz 2004" in manuscript
    assert "trade-off–invasion integration" in manuscript
    assert "changing-fitness-landscape treatment of trade-offs" in prior
    assert "three-surface relation" not in prior
    assert "completed divided-state value, a local release criterion" in prior


def test_architecture_frequency_escape_frontier_unifies_thresholds() -> None:
    eta = 0.8
    k = 1.5

    def recovery(d: float) -> float:
        return d + d * d

    dmax = 1.0

    def intrinsic(d: float, kk: float = k) -> float:
        return recovery(d) - kk * d

    def secant(d: float) -> float:
        return recovery(d) / d

    def p_escape(d: float, kk: float = k) -> float:
        return 0.5 - (dmax / (2 * eta)) * (secant(d) - kk)

    d_j = 0.5
    phi = intrinsic(dmax)
    p_c = (eta - phi) / (2 * eta)

    assert p_escape(d_j) == pytest.approx(0.5)
    assert p_escape(dmax) == pytest.approx(p_c)
    assert p_escape(0.25) == pytest.approx(0.65625)
    assert p_escape(0.75) == pytest.approx(0.34375)

    # Higher initial frequency lowers the release required on the favorable branch.
    def d_escape(p: float) -> float:
        return 0.5 + eta * (1 - 2 * p) / dmax

    assert d_escape(0.25) == pytest.approx(0.9)
    assert d_escape(0.40) == pytest.approx(0.66)
    assert d_escape(0.40) < d_escape(0.25)

    # Lower architecture cost shifts the frequency frontier downward.
    assert p_escape(0.75, 1.4) == pytest.approx(0.28125)
    assert p_escape(0.75, 1.6) == pytest.approx(0.40625)
    assert p_escape(0.75, 1.4) < p_escape(0.75, 1.6)

    # Cost-only environmental change is a parallel frontier translation
    # under proportional feedback scaling.
    shift_at_small_release = p_escape(0.25, 1.4) - p_escape(0.25, 1.6)
    shift_at_large_release = p_escape(0.75, 1.4) - p_escape(0.75, 1.6)
    assert shift_at_small_release == pytest.approx(-0.125)
    assert shift_at_large_release == pytest.approx(-0.125)


def test_escape_frontier_is_scope_bounded_against_allee_prior_art() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    prior = (ROOT / "docs" / "PRIOR_ART_BOUNDARY_V1.md").read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")

    assert "p_escape(d)" in manuscript
    assert "UTA1.4f" in theory
    assert "UTA1.4f" in ledger
    assert "eta (d/dmax)(2p-1)" in theory
    assert "dmax/(2eta)" in theory
    assert "Trait-dependent establishment, Allee thresholds, and propagule pressure" in prior
    assert "must **not** claim a first interaction between phenotype and initial abundance" in prior


def test_escape_frontier_slice_identities_survive_identity_preserving_rescaling() -> None:
    eta = 0.8
    k = 1.5
    dmax = 1.0

    def recovery(d: float) -> float:
        return d + d * d

    def intrinsic(d: float) -> float:
        return recovery(d) - k * d

    def p_escape_w(d: float) -> float:
        w = (d / dmax) ** 2
        return 0.5 - intrinsic(d) / (2 * eta * w)

    d_j = 0.5
    phi = intrinsic(dmax)
    p_c = (eta - phi) / (2 * eta)

    assert p_escape_w(d_j) == pytest.approx(0.5)
    assert p_escape_w(dmax) == pytest.approx(p_c)

    # Lowering architecture cost shifts the generalized frontier downward
    # at every positive release size, independent of the proportional choice.
    d = 0.75
    w = (d / dmax) ** 2

    def p_at_cost(kk: float) -> float:
        f = recovery(d) - kk * d
        return 0.5 - f / (2 * eta * w)

    assert p_at_cost(1.4) < p_at_cost(1.6)


def test_partial_division_can_invade_when_complete_division_fails() -> None:
    # Identity-preserving nonlinear ecological feedback can reverse
    # monotone novelty-versus-abundance compensation.
    eta = 0.8
    k = 1.5
    p_initial = 0.15

    def intrinsic(d: float) -> float:
        return d + d**2 - k * d

    def weight(d: float) -> float:
        return d**4

    def p_escape(d: float) -> float:
        return 0.5 - intrinsic(d) / (2 * eta * weight(d))

    def selection(d: float, p: float) -> float:
        return intrinsic(d) + eta * weight(d) * (2 * p - 1)

    assert weight(0) == 0
    assert weight(1) == 1
    assert intrinsic(1) > intrinsic(0.75)
    assert p_escape(0.5) == pytest.approx(0.5)
    assert p_escape(1) == pytest.approx(0.1875)
    assert p_escape(0.75) == pytest.approx(0.12962962962962962)
    assert p_escape(0.75) < p_initial < p_escape(1)
    assert selection(0.75, p_initial) == pytest.approx(0.0103125)
    assert selection(1, p_initial) == pytest.approx(-0.06)

    # Ecological feedback must grow faster than intrinsic value for
    # a more divided form to need a greater initial frequency.
    def intrinsic_elasticity(d: float) -> float:
        return (2 * d - 0.5) / (d - 0.5)

    ecological_elasticity = 4.0
    assert intrinsic_elasticity(0.7) > ecological_elasticity
    assert intrinsic_elasticity(0.75) == pytest.approx(ecological_elasticity)
    assert intrinsic_elasticity(0.8) < ecological_elasticity
    assert p_escape(0.75) < p_escape(0.7)
    assert p_escape(0.75) < p_escape(0.8)

    theory = THEORY.read_text(encoding="utf-8")
    assert "epsilon_w(d)>epsilon_F(d)" in theory
    assert "more divided can be intrinsically fitter but less invadable" in theory
    assert "Delta_w(0.75,0.15)=+0.0103125" in theory


def test_feedback_steepness_threshold_for_interior_establishment_optimum() -> None:
    # R(d)=a*d+b*d*d with J=(k-a)/b, positive eta, w=(d/D)**m.
    # An interior minimum of required founding frequency exists
    # iff m > (2*D-J)/(D-J).
    D = 1.0
    eta = 0.8

    def critical_power(J: float) -> float:
        return (2 * D - J) / (D - J)

    def optimum(J: float, m: float) -> float:
        return (m - 1) * J / (m - 2)

    def frontier(d: float, m: float, J: float) -> float:
        return 0.5 - (D**m / (2 * eta)) * (d - J) * d**(1 - m)

    J = 0.5
    assert critical_power(J) == pytest.approx(3.0)
    assert optimum(J, 3.0) == pytest.approx(1.0)
    assert optimum(J, 4.0) == pytest.approx(0.75)
    assert frontier(0.75, 4, J) == pytest.approx(0.12962962962962962)
    assert frontier(1.0, 4, J) == pytest.approx(0.1875)

    # The threshold steepens as the minimum viable intrinsic jump grows.
    assert critical_power(0.25) == pytest.approx(7 / 3)
    assert critical_power(0.75) == pytest.approx(5.0)

    # For m=4, lowering k past 5/3 takes J below 2/3:
    # the most invadable degree shifts inside the release interval.
    assert critical_power(0.7) > 4
    assert critical_power(0.5) < 4
    assert frontier(0.75, 4, 0.7) > frontier(1.0, 4, 0.7)
    assert frontier(0.75, 4, 0.5) < frontier(1.0, 4, 0.5)

    theory = THEORY.read_text(encoding="utf-8")
    assert "Critical ecological steepness for an interior establishment optimum" in theory
    assert "m_crit(x)=(2-x)/(1-x)" in theory
    assert "k(E)<a+bD[(m-2)/(m-1)]" in theory


def test_viable_partial_division_is_a_bounded_introduction_window() -> None:
    # A positive band of partial releases can be flanked on BOTH sides
    # by negative invasion selection, even with strictly convex recovery.
    eta = 0.8
    p = 0.15
    b = eta * (1 - 2 * p)

    def selection(d: float, frequency: float = p) -> float:
        return d * (d - 0.5 - eta * (1 - 2 * frequency) * d**3)

    assert 0.5 < b < 16 / 27
    assert 7 / 54 < p < 3 / 16
    d_peak = (1 / (3 * b)) ** 0.5
    assert d_peak == pytest.approx(0.77151674981046)
    assert selection(0.6) < 0
    assert selection(d_peak) > 0
    assert selection(1.0) < 0

    def crossing(lo: float, hi: float) -> float:
        sign_at_lo = selection(lo)
        assert sign_at_lo * selection(hi) < 0
        for _ in range(70):
            mid = (lo + hi) / 2
            if sign_at_lo * selection(mid) > 0:
                lo = mid
                sign_at_lo = selection(lo)
            else:
                hi = mid
        return (lo + hi) / 2

    d_min = crossing(0.6, d_peak)
    d_max = crossing(d_peak, 1.0)
    assert d_min == pytest.approx(0.6637794898247931)
    assert d_max == pytest.approx(0.8744526100516654)
    assert selection(d_min) == pytest.approx(0, abs=1e-12)
    assert selection(d_max) == pytest.approx(0, abs=1e-12)
    assert selection(0.75) == pytest.approx(0.0103125)
    # Below the lower frequency boundary, not even the optimal partial
    # release establishes; above the upper, full division establishes.
    assert selection(d_peak, 0.10) < 0
    assert selection(1.0, 0.20) > 0

    theory = THEORY.read_text(encoding="utf-8")
    assert "A bounded window of selectively viable partial differentiation" in theory
    assert "7/54 < p < 3/16" in theory
    assert "does not establish that an interior" in theory


def test_empirical_bridge_registers_escape_frontier_gap() -> None:
    bridge = EMPIRICAL_BRIDGE.read_text(encoding="utf-8")
    assert "Escape-frontier evidence gap" in bridge
    assert "partial structural release x initial frequency" in bridge
    assert "translate in parallel across environments" in bridge
    assert "A change in frontier shape would reject that mechanism" in bridge
