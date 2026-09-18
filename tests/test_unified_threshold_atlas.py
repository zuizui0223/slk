from scripts.slk_threshold_atlas import (
    ArchitecturePath,
    occupancy_ratio,
    rare_invasion_margin,
    reciprocal_fixation_ratio,
    reverse_invasion_resistance_margin,
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
