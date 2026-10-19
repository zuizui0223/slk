"""Model witnesses: invasion from integration does not decide partial-resident stability."""

from math import exp, isclose, log, sqrt
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
ETA = 1.5
ALPHA = 0.1
D_STAR = 1.0 / 7.0


def intrinsic(d: float) -> float:
    return 0.25 * d + d * d


def dependence(d: float) -> float:
    return ALPHA * d + (1.0 - ALPHA) * d * d


def payoff(u: float, v: float, interaction_strength: float = 0.0) -> float:
    return (
        intrinsic(u)
        - ETA * abs(dependence(u) - dependence(v))
        + interaction_strength * u * v * (u - v)
    )


def rare_invasion(u: float, resident: float, interaction_strength: float = 0.0) -> float:
    return payoff(u, resident, interaction_strength) - payoff(
        resident, resident, interaction_strength
    )


def s_vs_d_selection(d: float, mutant_frequency: float, strength: float) -> float:
    p = mutant_frequency
    w_d = p * payoff(d, d, strength) + (1.0 - p) * payoff(d, 0.0, strength)
    w_s = p * payoff(0.0, d, strength) + (1.0 - p) * payoff(
        0.0, 0.0, strength
    )
    return w_d - w_s


@pytest.mark.parametrize("strength", [0.0, 1.0, 3.0, 10.0])
def test_every_s_vs_d_frequency_curve_is_identical_to_registered_model(
    strength: float,
) -> None:
    for d in (0.02, 0.1, D_STAR, 0.25, 0.5, 0.75, 1.0):
        for p in (0.0, 0.01, 0.1, 0.3, 0.5, 0.9, 1.0):
            expected = intrinsic(d) + ETA * dependence(d) * (2.0 * p - 1.0)
            assert isclose(
                s_vs_d_selection(d, p, strength), expected, abs_tol=1e-12
            )


def test_partial_only_invasion_and_best_initial_founder() -> None:
    assert rare_invasion(0.1, 0.0) > 0
    assert isclose(rare_invasion(D_STAR, 0.0), 1.0 / 140.0, abs_tol=1e-12)
    assert isclose(rare_invasion(2.0 / 7.0, 0.0), 0.0, abs_tol=1e-12)
    assert rare_invasion(0.5, 0.0) < 0
    assert isclose(rare_invasion(1.0, 0.0), -0.25, abs_tol=1e-12)
    # H(d)=0.1d-0.35d^2 is strictly concave, with vertex at 1/7.
    for d in (0.001, 0.05, 0.11, 0.19, 0.25, 0.75, 1.0):
        assert rare_invasion(d, 0.0) < rare_invasion(D_STAR, 0.0)


def test_symmetric_mismatch_model_stabilizes_many_partial_residents() -> None:
    # H(d) decreases for d>1/7 and J(d) increases throughout [0,1].
    for resident in (D_STAR, 0.2, 0.35, 0.5, 0.8, 1.0):
        for n in range(201):
            mutant = n / 200.0
            if isclose(mutant, resident, abs_tol=1e-12):
                continue
            assert rare_invasion(mutant, resident) < 1e-12


def test_one_partial_resident_can_replace_integration_when_rare() -> None:
    for p in (0.0, 0.1, 0.5, 0.9, 1.0):
        assert s_vs_d_selection(D_STAR, p, 0.0) > 0


def test_advanced_mutant_invasion_is_not_identified_by_s_comparisons() -> None:
    # Both models have full division losing against integrated S.
    for strength in (0.0, 2.1, 3.0):
        assert isclose(rare_invasion(1.0, 0.0, strength), -0.25)
        assert isclose(rare_invasion(D_STAR, 0.0, strength), 1.0 / 140.0)
    # But changing specialist-specialist interactions flips later invasion.
    assert rare_invasion(1.0, D_STAR, 0.0) < 0
    assert isclose(rare_invasion(1.0, D_STAR, 2.1), 0.0, abs_tol=1e-12)
    assert isclose(
        rare_invasion(1.0, D_STAR, 3.0), 27.0 / 245.0, abs_tol=1e-12
    )
    assert rare_invasion(D_STAR, 1.0, 3.0) < 0


def test_directional_resident_interaction_allows_small_step_continuation() -> None:
    # H'(v)+lambda*v^2 >= 0.1-0.49/12 > 0 at lambda=3.
    minimum_upward_slope = 0.1 - 0.49 / 12.0
    assert minimum_upward_slope > 0
    for index in range(100):
        resident = index / 100.0
        mutant = resident + 1e-5
        assert rare_invasion(mutant, resident, 3.0) > 0
        if resident >= 1e-5:
            assert rare_invasion(resident - 1e-5, resident, 3.0) < 0



def smooth_mismatch(u: float, v: float, exponent: float) -> float:
    left = dependence(u)
    right = dependence(v)
    if isclose(left + right, 0.0, abs_tol=0.0):
        return 0.0
    return abs(left - right) ** exponent / (left + right) ** (exponent - 1.0)


def smooth_payoff(u: float, v: float, exponent: float) -> float:
    return intrinsic(u) - ETA * smooth_mismatch(u, v, exponent)


def smooth_invasion(u: float, resident: float, exponent: float) -> float:
    return smooth_payoff(u, resident, exponent) - smooth_payoff(
        resident, resident, exponent
    )


@pytest.mark.parametrize("exponent", [1.0, 1.5, 2.0, 4.0])
def test_symmetric_mismatch_models_preserve_all_s_vs_d_assays(
    exponent: float,
) -> None:
    for d in (0.01, D_STAR, 0.25, 0.5, 1.0):
        assert isclose(smooth_mismatch(d, 0.0, exponent), dependence(d))
        assert isclose(smooth_mismatch(d, d, exponent), 0.0)
        for p in (0.0, 0.1, 0.5, 0.9, 1.0):
            test_w_d = p * smooth_payoff(d, d, exponent) + (1-p) * smooth_payoff(d, 0.0, exponent)
            test_w_s = p * smooth_payoff(0.0, d, exponent) + (1-p) * smooth_payoff(0.0, 0.0, exponent)
            expected = intrinsic(d) + ETA * dependence(d) * (2*p-1)
            assert isclose(test_w_d - test_w_s, expected, abs_tol=1e-12)


def test_smooth_symmetric_mismatch_allows_continued_small_step_specialization() -> None:
    step = 1e-6
    for resident in (0.001, 0.01, 0.05, D_STAR, 0.2, 0.5, 0.9, 0.99):
        assert smooth_invasion(resident + step, resident, 2.0) > 0
        assert smooth_invasion(resident - step, resident, 2.0) < 0
        observed_gradient = smooth_invasion(resident + step, resident, 2.0) / step
        assert isclose(observed_gradient, 0.25 + 2.0 * resident, abs_tol=0.001)



def test_smooth_mismatch_has_a_stepping_stone_threshold_for_full_division() -> None:
    # New full D cannot invade S or the first partial founder, but can
    # invade a sufficiently advanced partial resident.
    assert smooth_invasion(1.0, 0.0, 2.0) < 0
    assert smooth_invasion(1.0, D_STAR, 2.0) < 0
    left, right = 0.2, 0.5
    assert smooth_invasion(1.0, left, 2.0) < 0
    assert smooth_invasion(1.0, right, 2.0) > 0
    for _ in range(65):
        mid = (left + right) / 2.0
        if smooth_invasion(1.0, mid, 2.0) > 0:
            right = mid
        else:
            left = mid
    threshold = (left + right) / 2.0
    assert isclose(threshold, 0.28615302603084614, abs_tol=1e-12)
    assert threshold > 2.0 / 7.0
    assert threshold < 0.3
    assert smooth_invasion(1.0, 0.3, 2.0) > 0
    assert smooth_invasion(0.3, 0.0, 2.0) < 0
    assert smooth_invasion(0.3, 0.25, 2.0) > 0

def test_cusp_and_smooth_payoffs_disagree_after_partial_becomes_resident() -> None:
    assert smooth_invasion(D_STAR, 0.0, 2.0) > 0
    assert smooth_invasion(1.0, 0.0, 2.0) < 0
    assert smooth_invasion(D_STAR + 1e-5, D_STAR, 1.0) < 0
    assert smooth_invasion(D_STAR + 1e-5, D_STAR, 2.0) > 0
    assert smooth_invasion(1.0, D_STAR, 2.0) < 0


def mutant_frequency_threshold(u: float, v: float, exponent: float = 1.0) -> float:
    mismatch = smooth_mismatch(u, v, exponent)
    assert mismatch > 0.0
    return 0.5 - (intrinsic(u) - intrinsic(v)) / (2.0 * ETA * mismatch)


def s_vs_partial_pair_selection(u: float, v: float, p: float, exponent: float = 1.0) -> float:
    return intrinsic(u) - intrinsic(v) + ETA * smooth_mismatch(u, v, exponent) * (2.0*p - 1.0)


def test_exact_finite_introduction_overcomes_rare_resistance_of_partial_resident() -> None:
    u, v = 1.0, D_STAR
    assert isclose(intrinsic(u)-intrinsic(v), 117.0/98.0, abs_tol=1e-12)
    assert isclose(ETA*smooth_mismatch(u, v, 1.0), 711.0/490.0, abs_tol=1e-12)
    assert isclose(smooth_invasion(u, v, 1.0), -9.0/35.0, abs_tol=1e-12)
    p_critical = mutant_frequency_threshold(u, v, 1.0)
    assert isclose(p_critical, 7.0/79.0, abs_tol=1e-12)
    assert s_vs_partial_pair_selection(u, v, 0.05) < 0.0
    assert isclose(s_vs_partial_pair_selection(u, v, p_critical), 0.0, abs_tol=1e-12)
    assert s_vs_partial_pair_selection(u, v, 0.10) > 0.0


def test_uninvadable_partial_degree_has_no_uniform_founding_frequency_margin() -> None:
    for delta in (0.5, 0.1, 0.01, 1e-3, 1e-5):
        u = D_STAR + delta
        expected_rare = -(7.0/20.0)*delta*delta
        expected_frequency = 49.0*delta/(150.0+378.0*delta)
        assert isclose(smooth_invasion(u, D_STAR, 1.0), expected_rare, abs_tol=1e-12)
        assert isclose(mutant_frequency_threshold(u, D_STAR, 1.0), expected_frequency, abs_tol=2e-11)
        assert expected_frequency > 0.0
        assert s_vs_partial_pair_selection(u, D_STAR, expected_frequency*1.5) > 0.0
    assert mutant_frequency_threshold(D_STAR+1e-5, D_STAR) < 0.000004


def test_fixed_finite_coalition_does_not_increase_arbitrarily_close_to_rarity() -> None:
    resident = D_STAR
    types = (0.25, 0.50)
    proportions = (0.4, 0.6)
    assert all(smooth_invasion(u, resident, 1.0) < 0.0 for u in types)

    def average_payoff(focal: float, epsilon: float) -> float:
        return (1.0-epsilon)*payoff(focal, resident) + epsilon*sum(
            q*payoff(focal, u) for q, u in zip(proportions, types)
        )

    for epsilon in (1e-8, 1e-6, 1e-4):
        for u in types:
            assert average_payoff(u, epsilon) < average_payoff(resident, epsilon)

def test_theory_documents_explicit_conditional_scope() -> None:
    source = (
        ROOT / "theory" / "PARTIAL_DIVISION_RESIDENT_STABILITY_V1.md"
    ).read_text(encoding="utf-8")
    for term in (
        "A_0(u,v)",
        "M_q(d,0)=w(d)",
        "q=2",
        "p_escape(1|1/7) = 7/79",
        "49 delta/(150+378 delta)",
        "I_lambda(1|d_*)",
        "lambda=21/10=2.1",
        "not stability conclusions",
        "exactly identical",
        "established partial resident",
    ):
        assert term in source


def test_main_manuscript_preserves_partial_arrest_vs_completion_fork() -> None:
    """Check the same integration assays lead to opposite downstream outcomes."""
    source = ROOT / "manuscript" / "SLK_MANUSCRIPT_AMNAT_V4.md"
    if not source.exists():
        source = ROOT / "MANUSCRIPT_SOURCE.md"
    manuscript = source.read_text(encoding="utf-8")
    for statement in (
        "Partial division can alter the ecological fate of further specialization",
        "identical fitness differences for every integrated-versus-divided pair",
        "partial division may arrest evolution",
        "−0.24850",
        "+0.01796",
        "not simulated or observed long-term lineage outcomes",
        "Wahl 2002; Uchiumi and Sasaki 2020",
    ):
        assert statement in manuscript, statement
    # The numerical witness is conditional, not a fitted natural-system estimate.
    assert isclose(smooth_invasion(D_STAR, 0.0, 1.0), 1.0 / 140.0, abs_tol=1e-12)
    for shape in (1.0, 2.0):
        assert isclose(smooth_invasion(1.0, 0.0, shape), -0.25, abs_tol=1e-12)
        assert smooth_invasion(0.30, 0.0, shape) < 0.0
    assert isclose(smooth_invasion(1.0, 0.30, 1.0), -0.24850, abs_tol=1e-12)
    assert isclose(smooth_invasion(1.0, 0.30, 2.0), 0.017959946, abs_tol=1e-8)
    assert smooth_invasion(D_STAR + 1e-5, D_STAR, 1.0) < 0.0
    assert smooth_invasion(D_STAR + 1e-5, D_STAR, 2.0) > 0.0


def test_first_partial_founder_has_exact_direct_completion_curvature_boundary() -> None:
    """Closed-form comparison changes only specialist–specialist mismatch."""
    assert isclose(dependence(D_STAR), 8.0 / 245.0, abs_tol=1e-14)
    assert isclose(intrinsic(1.0) - intrinsic(D_STAR), 117.0 / 98.0, abs_tol=1e-14)
    q_critical = 1.0 + log(65.0 / 79.0) / log(237.0 / 253.0)
    assert isclose(q_critical, 3.98580331443734, abs_tol=1e-12)

    def closed_form(q: float) -> float:
        return 117.0 / 98.0 - (711.0 / 490.0) * (237.0 / 253.0) ** (q - 1.0)

    assert isclose(closed_form(q_critical), 0.0, abs_tol=1e-12)
    for q in (1.0, 1.05, 1.1, 1.5, 2.0, 3.0, q_critical, 4.0, 5.0):
        assert isclose(
            smooth_invasion(1.0, D_STAR, q), closed_form(q), abs_tol=1e-12
        )
        assert isclose(smooth_invasion(D_STAR, 0.0, q), 1.0 / 140.0, abs_tol=1e-12)
        assert isclose(smooth_invasion(1.0, 0.0, q), -0.25, abs_tol=1e-12)
        # More than just endpoints: every S–d selection curve is identical.
        for d in (0.05, D_STAR, 0.24, 0.6, 1.0):
            for p in (0.0, 0.1, 0.5, 0.9, 1.0):
                observed = (
                    p * smooth_payoff(d, d, q)
                    + (1.0 - p) * smooth_payoff(d, 0.0, q)
                    - p * smooth_payoff(0.0, d, q)
                    - (1.0 - p) * smooth_payoff(0.0, 0.0, q)
                )
                expected = intrinsic(d) + ETA * dependence(d) * (2.0 * p - 1.0)
                assert isclose(observed, expected, abs_tol=1e-12)

    assert smooth_invasion(1.0, D_STAR, q_critical - 0.001) < 0
    assert smooth_invasion(1.0, D_STAR, q_critical + 0.001) > 0


def test_mismatch_curvature_changes_founder_threshold_then_allows_two_step_route() -> None:
    """Early founder success is invariant; completion is conditional on resident ecology."""
    assert isclose(smooth_invasion(1.0, D_STAR, 1.0), -9.0 / 35.0, abs_tol=1e-12)
    for q, expected_p in (
        (1.0, 7.0 / 79.0),
        (2.0, 0.060834268012604824),
        (3.0, 0.031185948553540163),
    ):
        assert smooth_invasion(1.0, D_STAR, q) < 0.0
        critical_p = mutant_frequency_threshold(1.0, D_STAR, q)
        assert isclose(critical_p, expected_p, abs_tol=1e-12)
        assert s_vs_partial_pair_selection(1.0, D_STAR, critical_p * 0.5, q) < 0
        assert s_vs_partial_pair_selection(1.0, D_STAR, critical_p + 0.05, q) > 0

    for q in (4.0, 5.0):
        # Both separate pairwise substitutions have positive relative fitness
        # at all tested frequencies if first partial and later full mutants appear.
        assert mutant_frequency_threshold(1.0, D_STAR, q) < 0
        for p in (0.0, 0.001, 0.01, 0.1, 0.5, 0.99, 1.0):
            assert s_vs_partial_pair_selection(D_STAR, 0.0, p, q) > 0
            assert s_vs_partial_pair_selection(1.0, D_STAR, p, q) > 0
        assert smooth_invasion(1.0, 0.0, q) < 0

    assert isclose(smooth_invasion(1.0, D_STAR, 4.0), 0.0011067606016059717, abs_tol=1e-12)
    assert isclose(smooth_invasion(1.0, D_STAR, 5.0), 0.0765389054502259, abs_tol=1e-12)


def test_curvature_dependence_of_minimum_resident_degree_enabling_completion() -> None:
    """Numeric first crossing v(q), not a general monotonicity theorem."""
    expected = (
        (1.1, 0.9025056150614044),
        (1.5, 0.43146179809559637),
        (2.0, 0.28615302603084614),
        (3.0, 0.18556385618903565),
        (4.0, 0.1424076082307703),
        (5.0, 0.11731821627431274),
    )
    thresholds = []
    for q, witness_v in expected:
        low, high = 0.00000001, 1.0 - 1e-9
        assert smooth_invasion(1.0, low, q) < 0
        assert smooth_invasion(1.0, high, q) > 0
        for _ in range(75):
            mid = (low + high) / 2.0
            if smooth_invasion(1.0, mid, q) > 0:
                high = mid
            else:
                low = mid
        root = (low + high) / 2.0
        thresholds.append(root)
        assert isclose(root, witness_v, abs_tol=1e-10)
        assert smooth_invasion(1.0, max(0.0, root - 1e-4), q) < 0
        assert smooth_invasion(1.0, min(1.0, root + 1e-4), q) > 0
    assert all(a > b for a, b in zip(thresholds, thresholds[1:]))


def test_theory_qualifies_direct_completion_threshold_and_its_prior_art() -> None:
    source = (ROOT / "theory" / "PARTIAL_DIVISION_RESIDENT_STABILITY_V1.md").read_text(encoding="utf-8")
    for token in (
        "log(65/79)/log(237/253)",
        "3.98580331443734",
        "q > q_critical",
        "M_q(d,0)=w(d)",
        "0.060834268",
        "sequential",
        "10.1007/s00285-013-0725-z",
        "not a general new theorem",
    ):
        if token == "not a general new theorem":
            assert "**not** the first discovery" in source.lower()
        else:
            assert token in source, token


def finite_mismatch_pair_fixation_from_closed_sum(
    mutant: float, resident: float, exponent: float, n: int, beta: float
) -> float:
    """Exact one-mutant exponential Moran fixation, excluding self encounters."""
    assert n >= 3 and beta > 0 and exponent >= 1
    gap = intrinsic(mutant) - intrinsic(resident)
    mismatch = ETA * smooth_mismatch(mutant, resident, exponent)
    terms = [
        -beta * (j * gap + mismatch * j * (j + 1 - n) / (n - 1))
        for j in range(n)
    ]
    peak = max(terms)
    return exp(-peak) / sum(exp(t - peak) for t in terms)


def finite_mismatch_pair_fixation_from_transitions(
    mutant: float, resident: float, exponent: float, n: int, beta: float
) -> float:
    """Independent exact birth/death ratio implementation of the 4-payoff game."""
    gap = intrinsic(mutant) - intrinsic(resident)
    mismatch = ETA * smooth_mismatch(mutant, resident, exponent)
    products_log = [0.0]
    cumulative = 0.0
    for i in range(1, n):
        # Pi are expected encounter payoffs, not raw fitness observations.
        pi_mutant = intrinsic(mutant) - mismatch * (n - i) / (n - 1)
        pi_resident = intrinsic(resident) - mismatch * i / (n - 1)
        weight_m = i * exp(beta * pi_mutant)
        weight_r = (n - i) * exp(beta * pi_resident)
        t_plus = weight_m / (weight_m + weight_r) * (n - i) / n
        t_minus = weight_r / (weight_m + weight_r) * i / n
        assert t_plus > 0 and t_minus > 0
        # The self-exclusion correction survives; do not use Delta(0).
        assert isclose(pi_mutant - pi_resident,
                       gap + mismatch * (2*i-n)/(n-1), abs_tol=1e-12)
        cumulative += log(t_minus / t_plus)
        products_log.append(cumulative)
    peak = max(products_log)
    return exp(-peak) / sum(exp(x - peak) for x in products_log)


@pytest.mark.parametrize("exponent", (1.0, 2.0, 3.0, 4.0, 5.0))
@pytest.mark.parametrize("n", (20, 100))
@pytest.mark.parametrize("beta", (0.1, 1.0))
def test_finite_four_payoff_moran_replays_independent_fixation_formula(
    exponent: float, n: int, beta: float
) -> None:
    for mutant, resident in ((D_STAR, 0.0), (1.0, 0.0),
                             (1.0, D_STAR), (D_STAR, 1.0)):
        expected = finite_mismatch_pair_fixation_from_closed_sum(
            mutant, resident, exponent, n, beta
        )
        observed = finite_mismatch_pair_fixation_from_transitions(
            mutant, resident, exponent, n, beta
        )
        assert isclose(expected, observed, rel_tol=1e-11, abs_tol=1e-12)


def test_finite_moran_fixation_is_continuous_at_direct_completion_boundary() -> None:
    n, beta = 100, 0.1
    q_star = 1.0 + log(65.0 / 79.0) / log(237.0 / 253.0)
    q_values = (1.0, 2.0, 3.0, q_star - 0.001,
                q_star, q_star + 0.001, 4.0, 5.0)
    fixation_values = [
        finite_mismatch_pair_fixation_from_closed_sum(
            1.0, D_STAR, q, n, beta
        ) for q in q_values
    ]
    assert all(x < y for x, y in zip(fixation_values, fixation_values[1:]))
    assert fixation_values[0] > 1.0 / n  # opposed when rare, but fixation is possible
    assert smooth_invasion(1.0, D_STAR, 1.0) < 0
    assert smooth_invasion(1.0, D_STAR, 4.0) > 0
    assert isclose(fixation_values[0], 0.027876352004896413, abs_tol=1e-12)
    assert isclose(fixation_values[-2], 0.03848215517968246, abs_tol=1e-12)
    assert isclose(fixation_values[-1], 0.04200871838101656, abs_tol=1e-12)
    assert fixation_values[4] > fixation_values[3]
    assert fixation_values[5] > fixation_values[4]


def test_all_integration_assays_keep_same_finite_moran_probabilities() -> None:
    """The initial S-vs-d tests are invariant, even for finite population fixation."""
    n, beta = 100, 0.1
    for mutant in (D_STAR, 1.0):
        base = finite_mismatch_pair_fixation_from_closed_sum(mutant, 0.0, 1.0, n, beta)
        for exponent in (1.0, 1.5, 2.0, 3.0, 4.0, 7.0):
            observed = finite_mismatch_pair_fixation_from_closed_sum(
                mutant, 0.0, exponent, n, beta
            )
            assert isclose(observed, base, abs_tol=1e-12)
    assert isclose(
        finite_mismatch_pair_fixation_from_closed_sum(D_STAR, 0.0, 1.0, n, beta),
        0.012025785305009848,
        abs_tol=1e-12,
    )
    assert isclose(
        finite_mismatch_pair_fixation_from_closed_sum(1.0, 0.0, 1.0, n, beta),
        0.028918435811972974,
        abs_tol=1e-12,
    )


@pytest.mark.parametrize("exponent", (1.0, 2.0, 4.0, 5.0))
@pytest.mark.parametrize("n", (20, 100))
def test_symmetric_mismatch_retains_stationary_odds_but_changes_turnover(
    exponent: float, n: int
) -> None:
    beta = 0.1
    forward = finite_mismatch_pair_fixation_from_closed_sum(
        1.0, D_STAR, exponent, n, beta
    )
    backward = finite_mismatch_pair_fixation_from_closed_sum(
        D_STAR, 1.0, exponent, n, beta
    )
    gap = intrinsic(1.0) - intrinsic(D_STAR)
    assert isclose(forward / backward, exp(beta*(n-1)*gap), rel_tol=1e-10)
    assert 0 < backward < forward < 1
    # The 4-entry asymmetric focal payoff is not the canonical 3-entry game.
    x = ETA * smooth_mismatch(1.0, D_STAR, exponent)
    assert not isclose(intrinsic(1.0)-x, intrinsic(D_STAR)-x)


def test_finite_stochastic_fitness_receipt_preserves_known_prior_art() -> None:
    source = (
        ROOT / "theory" / "PARTIAL_DIVISION_RESIDENT_STABILITY_V1.md"
    ).read_text(encoding="utf-8")
    for marker in (
        "10.1016/j.jtbi.2007.07.005",
        "not a fixation threshold",
        "rho_u|v / rho_v|u",
        "strictly increases",
        "0.027876352",
        "0.038482155",
        "do not form the equal-off-diagonal three-entry canonical game",
        "rate of turnover",
    ):
        assert marker in source, marker


def _partial_history_rates(exponent: float, n: int, beta: float,
                           *, direct: bool = False) -> tuple[float, float, float, float]:
    """Successful substitution coefficients before common rare rate mu."""
    partial = D_STAR
    a = finite_mismatch_pair_fixation_from_closed_sum(partial, 0.0, exponent, n, beta)
    b = (finite_mismatch_pair_fixation_from_closed_sum(1.0, 0.0, exponent, n, beta)
         if direct else 0.0)
    c = finite_mismatch_pair_fixation_from_closed_sum(0.0, partial, exponent, n, beta)
    d = finite_mismatch_pair_fixation_from_closed_sum(1.0, partial, exponent, n, beta)
    return a, b, c, d


def _first_hit_scaled_mean(a: float, b: float, c: float, d: float) -> float:
    """Closed two-transient-state first-passage time, in 1/mu units."""
    return (a + c + d) / (a*d + b*(c+d))


def _first_hit_closed_probability(a: float, b: float, c: float, d: float,
                                  normalized_horizon: float) -> float:
    """Exact CDF of first entry to D; later return substitutions are irrelevant."""
    g = sqrt((a+b-c-d)**2 + 4*a*c)
    assert g > 0
    r_slow = (a+b+c+d-g)/2
    r_fast = (a+b+c+d+g)/2
    surviving = ((r_fast-b)/g)*exp(-r_slow*normalized_horizon) + (
        (b-r_slow)/g
    )*exp(-r_fast*normalized_horizon)
    return 1.0 - surviving


def _first_hit_independent_poisson_uniformization(
    a: float, b: float, c: float, d: float, normalized_horizon: float
) -> float:
    """Independent forward CTMC calculation using the substochastic matrix."""
    rate = max(a+b, c+d)
    if rate <= 0:
        return 0.0
    p_ss, p_sp = 1-(a+b)/rate, a/rate
    p_ps, p_pp = c/rate, 1-(c+d)/rate
    p0, p1 = 1.0, 0.0  # initial integrated state
    poisson = exp(-rate*normalized_horizon)
    survival = poisson*(p0+p1)
    for k in range(1, 201):
        p0, p1 = p0*p_ss+p1*p_ps, p0*p_sp+p1*p_pp
        poisson *= (rate*normalized_horizon)/k
        survival += poisson*(p0+p1)
    return 1.0 - survival


@pytest.mark.parametrize("exponent", (1.0, 2.0, 3.0, 4.0, 5.0))
@pytest.mark.parametrize("direct", (False, True))
def test_first_arrival_matches_independent_transient_ctmc(
    exponent: float, direct: bool
) -> None:
    a, b, c, d = _partial_history_rates(exponent, 100, 1.0, direct=direct)
    assert a > 0 and c > 0 and d > 0
    assert (b > 0) == direct
    for horizon in (0.0, 2.0, 20.0, 40.0, 80.0, 200.0):
        closed = _first_hit_closed_probability(a, b, c, d, horizon)
        independent = _first_hit_independent_poisson_uniformization(a,b,c,d,horizon)
        assert 0 <= closed <= 1
        assert isclose(closed, independent, rel_tol=1e-10, abs_tol=1e-12)


def test_three_state_history_distinguishes_stationarity_from_first_arrival() -> None:
    """Identical initial and equilibrium states do not identify evolutionary timing."""
    N, beta = 100, 1.0
    a1, b1, c1, d1 = _partial_history_rates(1.0, N, beta)
    a4, b4, c4, d4 = _partial_history_rates(4.0, N, beta)
    assert b1 == b4 == 0
    assert isclose(a1, a4, abs_tol=1e-12)
    assert isclose(c1, c4, abs_tol=1e-12)
    assert isclose(a1, 0.029404746476, abs_tol=1e-12)
    assert isclose(c1, 0.000113611977, abs_tol=1e-12)
    assert isclose(d1, 0.023423120313, abs_tol=1e-12)
    assert isclose(d4, 0.117256955418, abs_tol=1e-12)

    tau1 = _first_hit_scaled_mean(a1,b1,c1,d1)
    tau4 = _first_hit_scaled_mean(a4,b4,c4,d4)
    assert isclose(tau1, 76.86592881951795, abs_tol=1e-9)
    assert isclose(tau4, 42.569344710067, abs_tol=1e-9)
    assert tau1 > 1.8*tau4

    hit1 = _first_hit_closed_probability(a1,b1,c1,d1,40.0)
    hit4 = _first_hit_closed_probability(a4,b4,c4,d4,40.0)
    assert isclose(hit1, 0.2813787530564026, abs_tol=1e-9)
    assert isclose(hit4, 0.5910823833300526, abs_tol=1e-9)
    assert hit4 > 2*hit1

    # The finite-time route changes, but the equilibrium occupancy does not.
    vals = [0.0, intrinsic(D_STAR), intrinsic(1.0)]
    scores = [exp(beta*(N-1)*(z-max(vals))) for z in vals]
    equilibrium = [z/sum(scores) for z in scores]
    for q in (1.0, 2.0, 4.0, 6.0):
        S_to_P, _, P_to_S, P_to_D = _partial_history_rates(q,N,beta)
        D_to_P = finite_mismatch_pair_fixation_from_closed_sum(
            D_STAR, 1.0, q, N, beta
        )
        # Connected symmetric mutation graph: S<->P<->D.
        assert isclose(equilibrium[0]*S_to_P,
                       equilibrium[1]*P_to_S, rel_tol=1e-10, abs_tol=1e-12)
        assert isclose(equilibrium[1]*P_to_D,
                       equilibrium[2]*D_to_P, rel_tol=1e-10, abs_tol=1e-12)


def test_direct_large_mutation_changes_first_passage_but_not_q_independence_of_S_assays() -> None:
    """Mutation topology is an additional *declared* developmental hypothesis."""
    t = {}
    for q in (1.0, 4.0):
        a,b,c,d = _partial_history_rates(q,100,1.0,direct=True)
        assert b > 0
        t[q] = _first_hit_scaled_mean(a,b,c,d)
    assert isclose(t[1.0], 40.37744336884948, abs_tol=1e-9)
    assert isclose(t[4.0], 22.402628919964393, abs_tol=1e-9)
    assert t[1.0] > t[4.0]


def test_three_state_finite_history_has_prior_art_and_clear_time_units() -> None:
    source = (ROOT/"theory"/"PARTIAL_DIVISION_RESIDENT_STABILITY_V1.md").read_text(encoding="utf-8")
    for statement in (
        "10.1111/j.1558-5646.2011.01236.x",
        "stationary probabilities from approach-to-equilibrium",
        "mu * E[T_(S->D)]",
        "76.86592882",
        "42.56934471",
        "0.28137875",
        "0.59108238",
        "strong-mutation-weak-selection is NOT required",
        "not a fourth universal SLK gate",
    ):
        if statement == "stationary probabilities from approach-to-equilibrium":
            assert "stationary probabilities from approach-to-equilibrium" not in source
            assert "distinguishes stationary probabilities" in source
        else:
            assert statement in source, statement
