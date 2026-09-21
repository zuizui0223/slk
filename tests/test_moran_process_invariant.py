from math import exp, isclose

import pytest

from scripts.slk_threshold_atlas import (
    SymmetricTwoStrategyGame,
    canonical_architecture_game,
    canonical_reciprocal_fixation_ratio_closed_form,
    fixation_probability_d,
    fixation_probability_s,
    moran_transition_probabilities,
    occupancy_ratio_from_process,
    reciprocal_fixation_ratio_from_process,
    symmetric_rare_mutation_stationary_distribution,
    validate_canonical_mapping,
)


@pytest.mark.theory_process
@pytest.mark.parametrize("phi", (-0.2, 0.0, 0.2))
@pytest.mark.parametrize("eta", (-1.0, 0.0, 1.5))
def test_moran_process_reproduces_canonical_reciprocal_fixation_ratio(phi, eta):
    n = 20
    beta = 0.1
    canonical = canonical_architecture_game(phi, eta)
    game = canonical.as_game()

    rho_d = fixation_probability_d(game, beta, n)
    rho_s = fixation_probability_s(game, beta, n)
    process_ratio = rho_d / rho_s
    closed_form = canonical_reciprocal_fixation_ratio_closed_form(
        canonical, beta, n
    )

    assert isclose(
        process_ratio,
        closed_form,
        rel_tol=1e-10,
        abs_tol=1e-12,
    )
    assert isclose(
        process_ratio,
        exp(beta * (n - 2) * phi),
        rel_tol=1e-10,
        abs_tol=1e-12,
    )


@pytest.mark.theory_process
def test_eta_changes_statewise_moran_transitions_even_when_fixation_ratio_cancels_it():
    n = 20
    beta = 0.1
    phi = 0.2
    state = 1

    game_a = canonical_architecture_game(phi, eta=-1.0).as_game()
    game_b = canonical_architecture_game(phi, eta=1.5).as_game()

    transitions_a = moran_transition_probabilities(game_a, state, beta, n)
    transitions_b = moran_transition_probabilities(game_b, state, beta, n)

    assert transitions_a != transitions_b

    ratio_a = reciprocal_fixation_ratio_from_process(game_a, beta, n)
    ratio_b = reciprocal_fixation_ratio_from_process(game_b, beta, n)
    assert isclose(ratio_a, ratio_b, rel_tol=1e-10, abs_tol=1e-12)


@pytest.mark.theory_process
def test_inv1_stationary_occupancy_is_computed_from_fixations_not_aliased():
    n = 20
    beta = 0.1
    canonical = canonical_architecture_game(phi=0.2, eta=1.5)
    game = canonical.as_game()

    rho_d = fixation_probability_d(game, beta, n)
    rho_s = fixation_probability_s(game, beta, n)
    pi_s, pi_d = symmetric_rare_mutation_stationary_distribution(rho_d, rho_s)

    fixation_ratio = rho_d / rho_s
    occupancy_ratio = pi_d / pi_s

    assert isclose(
        fixation_ratio,
        occupancy_ratio,
        rel_tol=1e-10,
        abs_tol=1e-12,
    )
    assert isclose(
        occupancy_ratio_from_process(game, beta, n),
        occupancy_ratio,
        rel_tol=1e-10,
        abs_tol=1e-12,
    )


@pytest.mark.theory_process
def test_noncanonical_diagonal_feedback_breaks_phi_only_closed_form():
    n = 20
    beta = 0.1
    phi = 0.0
    eta = 0.0

    # Same declared architecture coordinates, but an unequal D:D diagonal shift.
    violating = SymmetricTwoStrategyGame(
        ss=0.0,
        sd=0.0,
        dd=-0.2,
    )

    with pytest.raises(ValueError, match="equal-diagonal-feedback"):
        validate_canonical_mapping(violating, phi=phi, eta=eta)

    process_ratio = reciprocal_fixation_ratio_from_process(
        violating, beta, n
    )
    phi_only_prediction = exp(beta * (n - 2) * phi)

    assert not isclose(
        process_ratio,
        phi_only_prediction,
        rel_tol=1e-10,
        abs_tol=1e-12,
    )


@pytest.mark.theory_process
def test_canonical_builder_declares_and_validates_required_mapping():
    canonical = canonical_architecture_game(
        phi=0.2,
        eta=-0.4,
        baseline=3.0,
    )
    game = canonical.as_game()

    # A common payoff baseline is allowed because it does not alter selection.
    validate_canonical_mapping(
        game,
        phi=canonical.phi,
        eta=canonical.eta,
    )
    assert isclose(game.self_play_gap, canonical.phi)
    assert isclose(game.eta_coordinate, canonical.eta)
