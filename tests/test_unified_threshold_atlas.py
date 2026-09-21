from scripts.slk_threshold_atlas import (
    ArchitecturePath,
    environmental_phi,
    identify_phi_eta_from_symmetric_frequencies,
    identify_quadratic_frequency_components,
    invasion_environment_from_endpoint_offset,
    occupancy_ratio,
    rare_invasion_environment,
    rare_invasion_environment_affine_feedback,
    rare_invasion_environment_quadratic_frequency,
    rare_invasion_margin,
    rare_invasion_margin_endpoint,
    rare_invasion_margin_quadratic_frequency,
    reciprocal_fixation_ratio,
    reverse_invasion_environment,
    reverse_invasion_environment_affine_feedback,
    reverse_invasion_environment_quadratic_frequency,
    reverse_invasion_resistance_margin,
    reverse_invasion_resistance_margin_endpoint,
    reverse_invasion_resistance_margin_quadratic_frequency,
    selection_gap,
    selection_gap_quadratic_frequency,
    weak_selection_absolute_fixation_margin,
)


def test_registered_quadratic_witness_family_has_split_local_and_global_thresholds():
    path = ArchitecturePath()
    assert path.k_local == 1.0
    assert path.k_global == 2.0
    assert path.k_local < path.k_global


def test_w1_conflict_can_persist_without_profitable_endpoint():
    path = ArchitecturePath()
    l_value = 2.0
    phi = path.phi(k=2.2)
    assert l_value > 0
    assert path.recovery(path.dmax) == l_value
    assert phi < 0


def test_w2_global_value_can_be_positive_while_small_release_is_downhill():
    path = ArchitecturePath()
    phi = path.phi(k=1.5)
    assert phi > 0
    assert path.local_gradient(k=1.5) < 0


def test_w3_accessible_positive_endpoint_can_fail_rare_invasion():
    path = ArchitecturePath()
    phi = path.phi(k=0.8)
    eta = 1.5
    assert path.local_gradient(k=0.8) > 0
    assert phi > 0
    assert rare_invasion_margin(phi, eta) < 0


def test_w4_rare_invasion_can_disagree_with_reciprocal_fixation_ordering():
    path = ArchitecturePath()
    phi = path.phi(k=2.2)
    eta = -1.0
    assert rare_invasion_margin(phi, eta) > 0
    assert reciprocal_fixation_ratio(phi, beta=0.1, n=20) < 1


def test_w5_absolute_fixation_advantage_can_disagree_with_occupancy():
    path = ArchitecturePath()
    phi = path.phi(k=2.1)
    eta = -0.5
    assert weak_selection_absolute_fixation_margin(phi, eta) > 0
    assert occupancy_ratio(phi, beta=0.1, n=20) < 1


def test_invasion_surfaces_are_phi_equals_plus_or_minus_eta():
    phi = 0.4
    assert rare_invasion_margin(phi, eta=phi) == 0
    assert reverse_invasion_resistance_margin(phi, eta=-phi) == 0


def test_fixation_and_occupancy_realign_exactly_on_phi_zero():
    for phi in (-0.2, 0.0, 0.2):
        fixation = reciprocal_fixation_ratio(phi, beta=0.1, n=20)
        occupancy = occupancy_ratio(phi, beta=0.1, n=20)
        assert fixation == occupancy
        assert (fixation > 1) == (phi > 0)
        assert (fixation < 1) == (phi < 0)


def test_positive_eta_delays_invasion_beyond_value_threshold():
    e_v = 10.0
    slope = 2.0
    eta = 1.0
    e_i = rare_invasion_environment(e_v, slope, eta)
    e_r = reverse_invasion_environment(e_v, slope, eta)
    assert e_r < e_v < e_i
    assert e_i - e_v == eta / slope
    assert environmental_phi(e_i, slope, e_v) == eta


def test_negative_eta_allows_rare_invasion_before_positive_endpoint_value():
    e_v = 10.0
    slope = 2.0
    eta = -1.0
    e_i = rare_invasion_environment(e_v, slope, eta)
    e_r = reverse_invasion_environment(e_v, slope, eta)
    assert e_i < e_v < e_r
    assert environmental_phi(e_i, slope, e_v) == eta
    midpoint = (e_i + e_v) / 2
    phi_mid = environmental_phi(midpoint, slope, e_v)
    assert phi_mid < 0
    assert rare_invasion_margin(phi_mid, eta) > 0


def test_environmental_invasion_window_width_is_two_abs_eta_over_slope():
    e_v = 3.0
    slope = 0.5
    for eta in (-2.0, 2.0):
        e_i = rare_invasion_environment(e_v, slope, eta)
        e_r = reverse_invasion_environment(e_v, slope, eta)
        assert abs(e_i - e_r) == 2 * abs(eta) / slope


def test_varying_positive_coordination_feedback_delays_invasion_further():
    e_v = 10.0
    a = 2.0
    eta0 = 1.0
    b = 0.5
    e_const = rare_invasion_environment(e_v, a, eta0)
    e_var = rare_invasion_environment_affine_feedback(e_v, a, eta0, b)
    assert e_var > e_const
    assert abs((e_var - e_v) - eta0 / (a - b)) < 1e-12


def test_affine_feedback_gradient_sets_transition_zone_width_and_center():
    e_v = 10.0
    a = 2.0
    eta0 = 1.0
    b = 0.5
    e_i = rare_invasion_environment_affine_feedback(e_v, a, eta0, b)
    e_r = reverse_invasion_environment_affine_feedback(e_v, a, eta0, b)
    expected_width = 2 * a * abs(eta0) / (a * a - b * b)
    expected_center_shift = eta0 * b / (a * a - b * b)
    assert abs((e_i - e_r) - expected_width) < 1e-12
    assert abs(((e_i + e_r) / 2 - e_v) - expected_center_shift) < 1e-12


def test_coordination_feedback_matching_value_slope_removes_forward_crossing():
    e_v = 10.0
    a = 2.0
    eta0 = 1.0
    b = 2.0
    try:
        rare_invasion_environment_affine_feedback(e_v, a, eta0, b)
    except ValueError:
        pass
    else:
        raise AssertionError("equal slopes should not yield a finite affine invasion crossing")


def test_two_symmetric_frequency_treatments_recover_phi_and_eta():
    phi_true = 0.7
    eta_true = -0.4
    q = 0.25
    p_minus = 0.5 - q
    p_plus = 0.5 + q
    delta_minus = selection_gap(phi_true, eta_true, p_minus)
    delta_plus = selection_gap(phi_true, eta_true, p_plus)
    phi_hat, eta_hat = identify_phi_eta_from_symmetric_frequencies(
        delta_minus, delta_plus, q
    )
    assert abs(phi_hat - phi_true) < 1e-12
    assert abs(eta_hat - eta_true) < 1e-12


def test_balanced_frequency_selection_gap_equals_phi():
    phi = -0.3
    eta = 2.0
    assert selection_gap(phi, eta, 0.5) == phi


def test_three_frequency_treatments_recover_quadratic_frequency_components():
    phi = 0.6
    h0 = -0.1
    eta = 0.4
    kappa = 0.25
    q = 0.25
    p_mid = 0.5
    p_minus = 0.5 - q
    p_plus = 0.5 + q

    delta_mid = selection_gap_quadratic_frequency(phi, h0, eta, kappa, p_mid)
    delta_minus = selection_gap_quadratic_frequency(phi, h0, eta, kappa, p_minus)
    delta_plus = selection_gap_quadratic_frequency(phi, h0, eta, kappa, p_plus)

    h0_hat, eta_hat, kappa_hat = identify_quadratic_frequency_components(
        phi, delta_mid, delta_minus, delta_plus, q
    )

    assert abs(h0_hat - h0) < 1e-12
    assert abs(eta_hat - eta) < 1e-12
    assert abs(kappa_hat - kappa) < 1e-12


def test_quadratic_frequency_invasion_thresholds_reduce_to_canonical_when_h0_kappa_zero():
    phi = 0.4
    eta = 0.3
    assert rare_invasion_margin_quadratic_frequency(phi, 0.0, eta, 0.0) == (
        phi - eta
    )
    assert reverse_invasion_resistance_margin_quadratic_frequency(
        phi, 0.0, eta, 0.0
    ) == (phi + eta)


def test_eta_controls_window_width_while_h0_kappa_shift_window_center():
    e_v = 10.0
    slope = 2.0
    h0 = 0.3
    eta = 0.8
    kappa = -0.1

    e_i = rare_invasion_environment_quadratic_frequency(
        e_v, slope, h0, eta, kappa
    )
    e_r = reverse_invasion_environment_quadratic_frequency(
        e_v, slope, h0, eta, kappa
    )

    expected_signed_width = 2.0 * eta / slope
    expected_center_shift = -(h0 + kappa) / slope

    assert abs((e_i - e_r) - expected_signed_width) < 1e-12
    assert abs(((e_i + e_r) / 2.0 - e_v) - expected_center_shift) < 1e-12


def test_nonzero_curvature_rejects_minimal_canonical_frequency_map():
    phi = 0.2
    h0 = 0.0
    eta = 0.5
    kappa = 0.3
    q = 0.2

    delta_mid = selection_gap_quadratic_frequency(phi, h0, eta, kappa, 0.5)
    delta_minus = selection_gap_quadratic_frequency(phi, h0, eta, kappa, 0.5 - q)
    delta_plus = selection_gap_quadratic_frequency(phi, h0, eta, kappa, 0.5 + q)

    _, _, kappa_hat = identify_quadratic_frequency_components(
        phi, delta_mid, delta_minus, delta_plus, q
    )
    assert abs(kappa_hat) > 0


def test_general_endpoint_invasion_recovers_canonical_pair():
    phi = 0.3
    eta = 0.4
    h_rare = -eta
    h_resident_d = eta
    assert rare_invasion_margin_endpoint(phi, h_rare) == phi - eta
    assert reverse_invasion_resistance_margin_endpoint(
        phi, h_resident_d
    ) == phi + eta


def test_general_endpoint_invasion_recovers_quadratic_frequency_extension():
    phi = 0.5
    h0 = -0.2
    eta = 0.6
    kappa = 0.1
    h_rare = h0 - eta + kappa
    h_resident_d = h0 + eta + kappa
    assert abs(
        rare_invasion_margin_endpoint(phi, h_rare)
        - rare_invasion_margin_quadratic_frequency(phi, h0, eta, kappa)
    ) < 1e-12
    assert abs(
        reverse_invasion_resistance_margin_endpoint(phi, h_resident_d)
        - reverse_invasion_resistance_margin_quadratic_frequency(
            phi, h0, eta, kappa
        )
    ) < 1e-12


def test_endpoint_offsets_control_window_width_and_center_without_interior_shape():
    e_v = 7.0
    slope = 1.5
    h_rare = -0.8
    h_resident_d = 0.4
    e_i = invasion_environment_from_endpoint_offset(e_v, slope, h_rare)
    e_r = invasion_environment_from_endpoint_offset(
        e_v, slope, h_resident_d
    )
    expected_width = (h_resident_d - h_rare) / slope
    expected_center_shift = -(h_rare + h_resident_d) / (2 * slope)
    assert abs((e_i - e_r) - expected_width) < 1e-12
    assert abs(((e_i + e_r) / 2 - e_v) - expected_center_shift) < 1e-12
