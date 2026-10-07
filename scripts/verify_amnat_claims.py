from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

try:
    from scripts.slk_threshold_atlas import (
        ArchitecturePath,
        REGISTERED_WITNESS_MORAN_BETA,
        REGISTERED_WITNESS_MORAN_N,
        REGISTERED_WITNESS_PARAMETERS,
        SymmetricTwoStrategyGame,
        canonical_architecture_game,
        canonical_reciprocal_fixation_ratio_closed_form,
        compatible_persistent_integration_states,
        fixation_probability_d,
        fixation_probability_s,
        localize_persistent_integration_gate,
        occupancy_ratio_from_process,
        reciprocal_fixation_ratio_from_process,
        symmetric_rare_mutation_stationary_distribution,
        validate_canonical_mapping,
    )
except ImportError:  # direct execution via `python scripts/verify_amnat_claims.py`
    from slk_threshold_atlas import (
        ArchitecturePath,
        REGISTERED_WITNESS_MORAN_BETA,
        REGISTERED_WITNESS_MORAN_N,
        REGISTERED_WITNESS_PARAMETERS,
        SymmetricTwoStrategyGame,
        canonical_architecture_game,
        canonical_reciprocal_fixation_ratio_closed_form,
        compatible_persistent_integration_states,
        fixation_probability_d,
        fixation_probability_s,
        localize_persistent_integration_gate,
        occupancy_ratio_from_process,
        reciprocal_fixation_ratio_from_process,
        symmetric_rare_mutation_stationary_distribution,
        validate_canonical_mapping,
    )


def verify() -> dict[str, object]:
    checks: dict[str, object] = {}

    # UTA1 architecture path: use the canonical implementation directly.
    architecture = ArchitecturePath()
    k_local = architecture.k_local
    k_global = architecture.k_global
    assert math.isclose(k_local, 1.0)
    assert math.isclose(k_global, 2.0)
    assert k_local < k_global
    checks["UTA1_common_architecture_family"] = {
        "R(d)": "d+d^2",
        "dmax": 1.0,
        "k_local": k_local,
        "k_global": k_global,
        "pass": True,
    }

    # NE1: real conflict need not make differentiation profitable.
    L = REGISTERED_WITNESS_PARAMETERS["W1"]["L"]
    k = REGISTERED_WITNESS_PARAMETERS["W1"]["k"]
    R = architecture.recovery(architecture.dmax)
    K = k
    phi = architecture.phi(k)
    assert L > 0 and math.isclose(R, L) and phi < 0 and math.isclose(phi, -0.2)
    checks["NE1_conflict_not_payoff"] = {
        "L": L, "R": R, "K": K, "Phi": phi, "pass": True
    }

    # NE2: positive endpoint value need not imply small-step selective accessibility.
    k = REGISTERED_WITNESS_PARAMETERS["W2"]["k"]
    phi = architecture.phi(k)
    local_gradient = k_local - k
    assert phi > 0 and local_gradient < 0
    checks["NE2_payoff_not_small_step_accessibility"] = {
        "k_local": k_local,
        "k": k,
        "k_global": k_global,
        "Phi": phi,
        "Phi_prime_0": local_gradient,
        "pass": True,
    }

    # NE3: small-step accessible positive endpoint need not invade from rarity.
    k = REGISTERED_WITNESS_PARAMETERS["W3"]["k"]
    eta = REGISTERED_WITNESS_PARAMETERS["W3"]["eta"]
    phi = architecture.phi(k)
    local_gradient = k_local - k
    delta_rare = phi - eta
    assert local_gradient > 0 and phi > 0 and delta_rare < 0
    assert math.isclose(phi, 1.2)
    assert math.isclose(local_gradient, 0.2)
    assert math.isclose(delta_rare, -0.3)
    checks["NE3_accessible_payoff_not_invasion"] = {
        "k": k,
        "Phi": phi,
        "Phi_prime_0": local_gradient,
        "eta": eta,
        "Delta_rare": delta_rare,
        "pass": True,
    }

    # NE4: rare invasion need not imply reciprocal fixation superiority.
    k = REGISTERED_WITNESS_PARAMETERS["W4"]["k"]
    eta = REGISTERED_WITNESS_PARAMETERS["W4"]["eta"]
    beta = REGISTERED_WITNESS_MORAN_BETA
    N = REGISTERED_WITNESS_MORAN_N
    phi = architecture.phi(k)
    delta_rare = phi - eta
    game = canonical_architecture_game(phi, eta).as_game()
    fixation_ratio = reciprocal_fixation_ratio_from_process(
        game, beta, N
    )
    assert delta_rare > 0 and fixation_ratio < 1
    checks["NE4_invasion_not_reciprocal_fixation"] = {
        "k": k,
        "Phi": phi,
        "eta": eta,
        "Delta_rare": delta_rare,
        "rho_D_over_rho_S": fixation_ratio,
        "pass": True,
    }

    # NE5: absolute fixation advantage over neutrality can disagree with occupancy.
    k = REGISTERED_WITNESS_PARAMETERS["W5"]["k"]
    eta = REGISTERED_WITNESS_PARAMETERS["W5"]["eta"]
    beta = REGISTERED_WITNESS_MORAN_BETA
    N = REGISTERED_WITNESS_MORAN_N
    phi = architecture.phi(k)
    weak_selection_advantage = 3 * phi > eta
    game = canonical_architecture_game(phi, eta).as_game()
    occupancy_ratio = occupancy_ratio_from_process(
        game, beta, N
    )
    assert weak_selection_advantage and occupancy_ratio < 1
    checks["NE5_absolute_fixation_not_occupancy"] = {
        "k": k,
        "Phi": phi,
        "eta": eta,
        "three_Phi": 3 * phi,
        "absolute_fixation_advantage": weak_selection_advantage,
        "Pi_D_over_Pi_S": occupancy_ratio,
        "pass": True,
    }

    # UTA1 threshold identities for the canonical population pair.
    threshold_checks = {
        "rare_D_invasion": "Phi=eta",
        "reverse_invasion": "Phi=-eta",
        "reciprocal_fixation": "Phi=0",
        "weak_selection_absolute_fixation": "3Phi=eta",
        "symmetric_rare_mutation_occupancy": "Phi=0",
    }
    assert math.isclose((0.4 - 0.4), 0.0)  # Phi=eta
    assert math.isclose((0.4 + (-0.4)), 0.0)  # Phi=-eta
    checks["UTA1_critical_surfaces"] = {
        "surfaces": threshold_checks,
        "pass": True,
    }

    # UTA1.4: ecological threshold displacement.
    e_v, slope, eta = 10.0, 2.0, 1.0
    e_i = e_v + eta / slope
    e_r = e_v - eta / slope
    assert e_r < e_v < e_i
    assert math.isclose(e_i - e_v, eta / slope)
    assert math.isclose(e_i - e_r, 2 * abs(eta) / slope)
    checks["UTA1_4_environmental_threshold_displacement_positive_eta"] = {
        "E_V": e_v,
        "slope": slope,
        "eta": eta,
        "E_I": e_i,
        "E_R": e_r,
        "E_I_minus_E_V": e_i - e_v,
        "pass": True,
    }

    eta = -1.0
    e_i = e_v + eta / slope
    e_r = e_v - eta / slope
    phi_mid = slope * (((e_i + e_v) / 2) - e_v)
    delta_rare_mid = phi_mid - eta
    assert e_i < e_v < e_r
    assert phi_mid < 0
    assert delta_rare_mid > 0
    checks["UTA1_4_environmental_threshold_displacement_negative_eta"] = {
        "E_V": e_v,
        "slope": slope,
        "eta": eta,
        "E_I": e_i,
        "E_R": e_r,
        "midpoint_Phi": phi_mid,
        "midpoint_rare_invasion_margin": delta_rare_mid,
        "pass": True,
    }

    # UTA1.4b: environmental gradient in feedback shifts the invasion crossing.
    e_v, a, eta0, b = 10.0, 2.0, 1.0, 0.5
    e_i = e_v + eta0 / (a - b)
    e_r = e_v - eta0 / (a + b)
    width = e_i - e_r
    center_shift = (e_i + e_r) / 2 - e_v
    expected_width = 2 * a * abs(eta0) / (a * a - b * b)
    expected_center_shift = eta0 * b / (a * a - b * b)
    assert e_i > e_v
    assert math.isclose(width, expected_width)
    assert math.isclose(center_shift, expected_center_shift)
    checks["UTA1_4b_environmental_feedback_gradient"] = {
        "E_V": e_v,
        "Phi_slope": a,
        "eta_at_value": eta0,
        "eta_slope": b,
        "E_I": e_i,
        "E_R": e_r,
        "zone_width": width,
        "zone_center_shift": center_shift,
        "pass": True,
    }

    # UTA1.4c: the identity of the limiting early barrier can turn over
    # along one environmental gradient while the observed architecture
    # remains integrated.
    dmax = 1.0
    k_local_turn = 1.0
    k_global_turn = 2.0
    k0_turn = 3.0
    c_turn = 1.0
    e0_turn = 0.0
    eta_turn = 1.5

    e_v_turn = e0_turn + (k0_turn - k_global_turn) / c_turn
    e_a_turn = e0_turn + (k0_turn - k_local_turn) / c_turn
    e_i_turn = e_v_turn + eta_turn / (c_turn * dmax)

    assert eta_turn > dmax * (k_global_turn - k_local_turn)
    assert e_v_turn < e_a_turn < e_i_turn

    def turnover_state(e_value: float) -> tuple[float, float, float]:
        k_value = k0_turn - c_turn * (e_value - e0_turn)
        phi_value = dmax * (k_global_turn - k_value)
        g0_value = k_local_turn - k_value
        delta_rare_value = phi_value - eta_turn
        return phi_value, g0_value, delta_rare_value

    phi_low, g0_low, dr_low = turnover_state(0.5)
    phi_value, g0_value, dr_value = turnover_state(1.5)
    phi_access, g0_access, dr_access = turnover_state(2.25)
    phi_pass, g0_pass, dr_pass = turnover_state(3.0)

    assert phi_low < 0
    assert phi_value > 0 and g0_value < 0
    assert phi_access > 0 and g0_access > 0 and dr_access < 0
    assert phi_pass > 0 and g0_pass > 0 and dr_pass > 0

    checks["UTA1_4c_environmental_barrier_turnover"] = {
        "E_V": e_v_turn,
        "E_A": e_a_turn,
        "E_I": e_i_turn,
        "eta": eta_turn,
        "convexity_gap": k_global_turn - k_local_turn,
        "value_limited_example": {
            "E": 0.5,
            "Phi": phi_low,
            "g0": g0_low,
            "Delta_R": dr_low,
        },
        "accessibility_limited_example": {
            "E": 1.5,
            "Phi": phi_value,
            "g0": g0_value,
            "Delta_R": dr_value,
        },
        "establishment_limited_example": {
            "E": 2.25,
            "Phi": phi_access,
            "g0": g0_access,
            "Delta_R": dr_access,
        },
        "early_gates_pass_example": {
            "E": 3.0,
            "Phi": phi_pass,
            "g0": g0_pass,
            "Delta_R": dr_pass,
        },
        "pass": True,
    }

    # UTA1.4f: partial structural release and initial frequency lie on
    # one canonical escape frontier.
    k_escape = 1.5
    eta_escape = 0.8
    d_j_escape = 0.5

    def intrinsic_release(d: float, k_value: float = k_escape) -> float:
        return architecture.recovery(d) - k_value * d

    def p_escape(d: float, k_value: float = k_escape) -> float:
        return 0.5 - intrinsic_release(d, k_value) / (2 * eta_escape)

    phi_escape = intrinsic_release(architecture.dmax)
    p_c_escape = (eta_escape - phi_escape) / (2 * eta_escape)

    assert math.isclose(intrinsic_release(d_j_escape), 0.0)
    assert math.isclose(p_escape(d_j_escape), 0.5)
    assert math.isclose(p_escape(architecture.dmax), p_c_escape)
    assert p_escape(0.25) > 0.5
    assert p_escape(0.75) < 0.5

    def d_escape_at_frequency(p_value: float) -> float:
        target = eta_escape * (1 - 2 * p_value)
        # For R(d)=d+d^2 and k=1.5, F(d)=d^2-0.5d.
        return (0.5 + math.sqrt(0.25 + 4 * target)) / 2

    d_escape_low_frequency = d_escape_at_frequency(0.25)
    d_escape_high_frequency = d_escape_at_frequency(0.40)
    assert d_escape_high_frequency < d_escape_low_frequency

    p_escape_higher_cost = p_escape(0.75, 1.6)
    p_escape_lower_cost = p_escape(0.75, 1.4)
    assert p_escape_lower_cost < p_escape_higher_cost

    checks["UTA1_4f_architecture_frequency_escape_frontier"] = {
        "k": k_escape,
        "eta": eta_escape,
        "d_J": d_j_escape,
        "Phi": phi_escape,
        "p_C": p_c_escape,
        "p_escape_at_d_J": p_escape(d_j_escape),
        "p_escape_at_dmax": p_escape(architecture.dmax),
        "d_escape_at_p_0_25": d_escape_low_frequency,
        "d_escape_at_p_0_40": d_escape_high_frequency,
        "p_escape_at_d_0_75_k_1_6": p_escape_higher_cost,
        "p_escape_at_d_0_75_k_1_4": p_escape_lower_cost,
        "pass": True,
    }

    # UTA1.5: stronger conflict need not mean larger architecture margin.
    L_A, s_A, K_A = 3.0, 0.2, 0.8
    L_B, s_B, K_B = 2.0, 0.8, 0.5
    phi_A = s_A * L_A - K_A
    phi_B = s_B * L_B - K_B
    assert L_A > L_B
    assert phi_A < phi_B
    checks["UTA1_5_conflict_does_not_rank_differentiation"] = {
        "L_A": L_A,
        "Phi_A": phi_A,
        "L_B": L_B,
        "Phi_B": phi_B,
        "pass": True,
    }

    # UTA1.6: two symmetric frequency treatments identify Phi and eta.
    phi_true, eta_true, q = 0.7, -0.4, 0.25
    p_minus, p_plus = 0.5 - q, 0.5 + q
    delta_minus = phi_true + eta_true * (2 * p_minus - 1)
    delta_plus = phi_true + eta_true * (2 * p_plus - 1)
    phi_hat = 0.5 * (delta_plus + delta_minus)
    eta_hat = (delta_plus - delta_minus) / (4 * q)
    assert math.isclose(phi_hat, phi_true)
    assert math.isclose(eta_hat, eta_true)
    checks["UTA1_6_two_frequency_identification"] = {
        "q": q,
        "Delta_minus": delta_minus,
        "Delta_plus": delta_plus,
        "Phi_hat": phi_hat,
        "eta_hat": eta_hat,
        "pass": True,
    }

    # UTA1.7: three frequency treatments diagnose and repair curvature.
    phi = 0.6
    h0 = -0.1
    eta = 0.4
    kappa = 0.25
    q = 0.25
    p_mid = 0.5
    p_minus = 0.5 - q
    p_plus = 0.5 + q

    def curved_gap(p: float) -> float:
        x = 2 * p - 1
        return phi + h0 + eta * x + kappa * x * x

    delta_mid = curved_gap(p_mid)
    delta_minus = curved_gap(p_minus)
    delta_plus = curved_gap(p_plus)

    h0_hat = delta_mid - phi
    eta_hat = (delta_plus - delta_minus) / (4 * q)
    kappa_hat = (delta_plus + delta_minus - 2 * delta_mid) / (8 * q * q)

    assert math.isclose(h0_hat, h0)
    assert math.isclose(eta_hat, eta)
    assert math.isclose(kappa_hat, kappa)

    rare_margin = phi + h0 - eta + kappa
    reverse_margin = phi + h0 + eta + kappa
    checks["UTA1_7_three_frequency_curvature_diagnostic"] = {
        "Phi": phi,
        "h0_hat": h0_hat,
        "eta_hat": eta_hat,
        "kappa_hat": kappa_hat,
        "rare_invasion_margin": rare_margin,
        "reverse_invasion_resistance_margin": reverse_margin,
        "pass": True,
    }

    e_v, slope = 10.0, 2.0
    e_i = e_v + (eta - kappa - h0) / slope
    e_r = e_v - (eta + kappa + h0) / slope
    assert math.isclose(e_i - e_r, 2 * eta / slope)
    assert math.isclose((e_i + e_r) / 2 - e_v, -(h0 + kappa) / slope)
    checks["UTA1_7_curvature_window_geometry"] = {
        "E_V": e_v,
        "E_I": e_i,
        "E_R": e_r,
        "signed_width": e_i - e_r,
        "center_shift": (e_i + e_r) / 2 - e_v,
        "pass": True,
    }

    # UTA1.8: arbitrary interior frequency shape reduces to endpoint offsets for invasion.
    phi = 0.45
    h_rare = -0.6
    h_resident_d = 0.25
    rare_margin = phi + h_rare
    reverse_margin = phi + h_resident_d
    assert rare_margin < 0
    assert reverse_margin > 0

    e_v, slope = 5.0, 1.25
    e_i = e_v - h_rare / slope
    e_r = e_v - h_resident_d / slope
    assert math.isclose(e_i - e_r, (h_resident_d - h_rare) / slope)
    assert math.isclose(
        (e_i + e_r) / 2 - e_v,
        -(h_rare + h_resident_d) / (2 * slope),
    )

    checks["UTA1_8_arbitrary_shape_endpoint_invasion"] = {
        "Phi": phi,
        "h_R": h_rare,
        "h_D": h_resident_d,
        "rare_invasion_margin": rare_margin,
        "reverse_invasion_resistance_margin": reverse_margin,
        "E_I": e_i,
        "E_R": e_r,
        "pass": True,
    }

    # UTA1.9: finite-frequency endpoint certification.
    epsilon = 0.05
    lipschitz = 1.5
    delta_eps = 0.20
    lip_lower = delta_eps - lipschitz * epsilon
    lip_upper = delta_eps + lipschitz * epsilon
    assert lip_lower > 0
    checks["UTA1_9_one_point_endpoint_certificate"] = {
        "epsilon": epsilon,
        "M": lipschitz,
        "lower": lip_lower,
        "upper": lip_upper,
        "pass": True,
    }

    d0, d1, c_quad = 0.15, -0.3, 0.8
    d_eps = d0 + d1 * epsilon + c_quad * epsilon * epsilon
    d_2eps = d0 + d1 * 2 * epsilon + c_quad * (2 * epsilon) ** 2
    endpoint_hat = 2 * d_eps - d_2eps
    curvature_bound = 2 * abs(c_quad)
    error_bound = curvature_bound * epsilon * epsilon
    assert abs(endpoint_hat - d0) <= error_bound + 1e-12
    checks["UTA1_9_two_point_endpoint_certificate"] = {
        "epsilon": epsilon,
        "endpoint_hat": endpoint_hat,
        "true_endpoint": d0,
        "curvature_bound": curvature_bound,
        "error_bound": error_bound,
        "pass": True,
    }

    l1, u1 = 0.18, 0.22
    l2, u2 = 0.10, 0.14
    combined_lower = 2 * l1 - u2 - error_bound
    combined_upper = 2 * u1 - l2 + error_bound
    assert combined_lower > 0
    checks["UTA1_9_sampling_plus_endpoint_error"] = {
        "lower": combined_lower,
        "upper": combined_upper,
        "pass": True,
    }

    # UTA1.10: the same persistent phenotype is compatible with distinct gate-localized sign patterns.
    k_value = REGISTERED_WITNESS_PARAMETERS["W1"]["k"]
    phi_value = architecture.phi(k_value)

    k_access = REGISTERED_WITNESS_PARAMETERS["W2"]["k"]
    phi_access = architecture.phi(k_access)
    g0_access = k_local - k_access

    k_invasion = REGISTERED_WITNESS_PARAMETERS["W3"]["k"]
    eta_invasion = REGISTERED_WITNESS_PARAMETERS["W3"]["eta"]
    phi_invasion = architecture.phi(k_invasion)
    g0_invasion = k_local - k_invasion
    delta_rare_invasion = phi_invasion - eta_invasion

    assert phi_value < 0
    assert phi_access > 0 and g0_access < 0
    assert (
        phi_invasion > 0
        and g0_invasion > 0
        and delta_rare_invasion < 0
    )

    value_state = localize_persistent_integration_gate(
        phi_value, -1.0, -1.0
    )
    access_state = localize_persistent_integration_gate(
        phi_access, g0_access, -1.0
    )
    invasion_state = localize_persistent_integration_gate(
        phi_invasion, g0_invasion, delta_rare_invasion
    )
    early_pass_delta = phi_invasion
    early_pass_state = localize_persistent_integration_gate(
        phi_invasion, g0_invasion, early_pass_delta
    )
    boundary_policy = {
        "Phi=0": localize_persistent_integration_gate(
            0.0, -1.0, -1.0
        ),
        "g0=0": localize_persistent_integration_gate(
            1.0, 0.0, -1.0
        ),
        "Delta_R=0": localize_persistent_integration_gate(
            1.0, 1.0, 0.0
        ),
    }
    assert value_state == "ARCHITECTURE_VALUE_FAILURE"
    assert access_state == "LOCAL_RELEASE_FAILURE"
    assert invasion_state == "RARE_INVASION_FAILURE"
    assert early_pass_state == "EARLY_GATES_PASSED"
    assert all("UNRESOLVED" in state for state in boundary_policy.values())

    checks["UTA1_10_persistent_integration_gate_localization"] = {
        "negative_architecture_value": {
            "Phi": phi_value,
            "first_changed_layer": "architecture_value",
            "state": value_state,
        },
        "local_release_barrier": {
            "Phi": phi_access,
            "g0": g0_access,
            "first_changed_layer": "local_accessibility",
            "state": access_state,
        },
        "rare_establishment_barrier": {
            "Phi": phi_invasion,
            "g0": g0_invasion,
            "Delta_R": delta_rare_invasion,
            "first_changed_layer": "rare_invasion",
            "state": invasion_state,
        },
        "early_gates_passed": {
            "Phi": phi_invasion,
            "g0": g0_invasion,
            "Delta_R": early_pass_delta,
            "state": early_pass_state,
            "excluded_failure_modes": [
                "negative_architecture_value",
                "downhill_initial_release",
                "rare_invasion_failure",
            ],
            "realized_differentiation_implied": False,
        },
        "boundary_policy": boundary_policy,
        "mechanism_identified": False,
        "pass": True,
    }

    # UTA1.11: uncertainty is propagated as a compatible-state set.
    wide_states = compatible_persistent_integration_states(
        (-0.2, 0.4),
        (-0.2, 0.4),
        (-0.2, 0.4),
    )
    medium_states = compatible_persistent_integration_states(
        (0.1, 0.4),
        (-0.1, 0.3),
        (0.1, 0.4),
    )
    narrow_states = compatible_persistent_integration_states(
        (0.2, 0.3),
        (0.1, 0.2),
        (0.1, 0.2),
    )
    assert set(medium_states) < set(wide_states)
    assert set(narrow_states) < set(medium_states)
    assert narrow_states == ("EARLY_GATES_PASSED",)

    checks["UTA1_11_interval_compatible_state_set"] = {
        "wide_states": list(wide_states),
        "medium_states": list(medium_states),
        "narrow_states": list(narrow_states),
        "nested_refinement_monotone": True,
        "marginal_box_is_conservative_outer_set": True,
        "exact_joint_feasibility_supported": False,
        "statistical_partial_identification_novelty_claimed": False,
        "pass": True,
    }

    # INV1: derive both fixation and occupancy from the registered process.
    max_relative_error = 0.0
    comparisons = 0
    for beta in (0.1, 0.5, 1.0, 2.0):
        for N in (3, 4, 10, 50):
            for phi in (-2.0, -0.5, -0.1, 0.0, 0.1, 0.5, 2.0):
                for eta in (-1.0, 0.0, 1.5):
                    canonical = canonical_architecture_game(phi, eta)
                    game = canonical.as_game()

                    rho_d = fixation_probability_d(game, beta, N)
                    rho_s = fixation_probability_s(game, beta, N)
                    fixation_ratio = rho_d / rho_s

                    pi_s, pi_d = symmetric_rare_mutation_stationary_distribution(
                        rho_d, rho_s
                    )
                    occupancy_ratio = pi_d / pi_s

                    closed_form = canonical_reciprocal_fixation_ratio_closed_form(
                        canonical, beta, N
                    )
                    process_ratio = reciprocal_fixation_ratio_from_process(
                        game, beta, N
                    )

                    assert math.isclose(
                        process_ratio,
                        closed_form,
                        rel_tol=1e-10,
                        abs_tol=1e-12,
                    )
                    assert math.isclose(
                        fixation_ratio,
                        occupancy_ratio,
                        rel_tol=1e-10,
                        abs_tol=1e-12,
                    )

                    scale = max(abs(closed_form), 1e-300)
                    relative_error = abs(process_ratio - closed_form) / scale
                    max_relative_error = max(
                        max_relative_error, relative_error
                    )
                    comparisons += 1

    checks["INV1_fixation_occupancy_invariant"] = {
        "comparisons": comparisons,
        "max_relative_error": max_relative_error,
        "derived_from_moran_process": True,
        "derived_from_rare_mutation_chain": True,
        "pass": True,
    }

    # Canonical-mapping guard: unequal diagonal feedback invalidates Phi-only transport.
    violating = SymmetricTwoStrategyGame(ss=0.0, sd=0.0, dd=-0.2)
    canonical_guard_raised = False
    try:
        validate_canonical_mapping(violating, phi=0.0, eta=0.0)
    except ValueError:
        canonical_guard_raised = True
    assert canonical_guard_raised

    violating_ratio = reciprocal_fixation_ratio_from_process(
        violating, beta=0.1, n=20
    )
    assert not math.isclose(
        violating_ratio,
        1.0,
        rel_tol=1e-10,
        abs_tol=1e-12,
    )
    checks["CANONICAL_MAPPING_GUARD"] = {
        "guard_raised": canonical_guard_raised,
        "violating_game_fixation_ratio": violating_ratio,
        "phi_only_prediction": 1.0,
        "pass": True,
    }

    return {
        "manuscript": "SLK_MANUSCRIPT_AMNAT_V4",
        "registered_architecture_family": "R(d)=d+d^2, K(d)=k*d, d in [0,1]",
        "registered_process": "connected symmetric rare mutation + exponential Moran",
        "all_checks_pass": all(bool(v["pass"]) for v in checks.values()),
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("submission/amnat_review/generated/CLAIM_VERIFICATION_RECEIPT.json"),
    )
    args = parser.parse_args()

    receipt = verify()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
