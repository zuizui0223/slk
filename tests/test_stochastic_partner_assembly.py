"""Exact birth-death founder survival under an explicitly assumed partner-assembly switch.

These synthetic demographic parameters are not estimates of empirical systems.
"""

from math import exp, isclose
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
A = 117.0 / 98.0
B = 711.0 / 490.0
G_PRE = A - B
G_POST = A - 0.6 * B
B_POST = 1.2
D_POST = B_POST - G_POST


def pre_switch_pgf(s: float, t: float, b: float, d: float) -> float:
    assert 0.0 <= s <= 1.0
    assert t >= 0.0 and 0.0 <= b < d
    z = exp(-(d - b) * t)
    numerator = d * (1.0 - s) * z - (d - b * s)
    denominator = b * (1.0 - s) * z - (d - b * s)
    return numerator / denominator


def eventual_survival(n0: int, t: float, b_pre: float) -> float:
    assert n0 >= 1
    d_pre = b_pre - G_PRE
    q_post = D_POST / B_POST
    assert 0.0 < q_post < 1.0
    q = pre_switch_pgf(q_post, t, b_pre, d_pre)
    return 1.0 - q**n0


def alive_at_switch(n0: int, t: float, b_pre: float) -> float:
    d_pre = b_pre - G_PRE
    return 1.0 - pre_switch_pgf(0.0, t, b_pre, d_pre) ** n0


@pytest.mark.parametrize("b_pre", [0.0, 0.4, 1.4, 5.0])
def test_pgf_limits_and_absorbing_certificates(b_pre: float) -> None:
    d_pre = b_pre - G_PRE
    for s in (0.0, 0.1, 0.5, D_POST / B_POST, 1.0):
        assert isclose(pre_switch_pgf(s, 0.0, b_pre, d_pre), s, abs_tol=1e-14)
        assert isclose(pre_switch_pgf(1.0, 3.0, b_pre, d_pre), 1.0)
        assert 0.0 <= pre_switch_pgf(s, 3.0, b_pre, d_pre) <= 1.0
        assert isclose(pre_switch_pgf(s, 100.0, b_pre, d_pre), 1.0, abs_tol=1e-11)


def test_pure_death_special_case() -> None:
    d = -G_PRE
    survival_post_one = 1.0 - D_POST / B_POST
    for t in (0.0, 1.0, 3.0):
        analytic = survival_post_one * exp(-d * t)
        assert isclose(eventual_survival(1, t, 0.0), analytic, abs_tol=1e-13)
        assert isclose(alive_at_switch(1, t, 0.0), exp(-d * t), abs_tol=1e-13)


def test_two_absolute_turnover_regimes_share_mean_decline_but_not_survival() -> None:
    assert isclose(G_PRE, -9.0 / 35.0)
    assert isclose(G_POST, 0.3232653061224491, abs_tol=1e-14)
    assert isclose(exp(G_PRE * 3.0), 0.4623520933081964, abs_tol=1e-14)
    for pre_birth in (0.4, 1.4):
        assert isclose(pre_birth - (pre_birth - G_PRE), G_PRE)
        assert alive_at_switch(5, 3.0, pre_birth) > eventual_survival(5, 3.0, pre_birth)
    assert isclose(alive_at_switch(5, 3.0, 0.4), 0.7654963793636065, abs_tol=1e-12)
    assert isclose(alive_at_switch(5, 3.0, 1.4), 0.4654290538690993, abs_tol=1e-12)
    assert isclose(eventual_survival(5, 3.0, 0.4), 0.4149036517572605, abs_tol=1e-12)
    assert isclose(eventual_survival(5, 3.0, 1.4), 0.30295854840211167, abs_tol=1e-12)


def test_survival_decreases_with_delay_increases_with_founder_count() -> None:
    for pre_birth in (0.4, 1.4):
        assert eventual_survival(5, 0.0, pre_birth) > eventual_survival(5, 1.0, pre_birth)
        assert eventual_survival(5, 1.0, pre_birth) > eventual_survival(5, 3.0, pre_birth)
        assert eventual_survival(5, 3.0, pre_birth) > eventual_survival(5, 5.0, pre_birth)
        assert eventual_survival(5, 3.0, pre_birth) > eventual_survival(1, 3.0, pre_birth)
        assert eventual_survival(20, 3.0, pre_birth) > eventual_survival(5, 3.0, pre_birth)


def test_pgf_solution_agrees_with_independent_forward_kolmogorov_ode() -> None:
    # An independently derived generating-function evolution ODE:
    # dG/dt=b*G**2-(b+d)*G+d, G(s,0)=s.
    b, d, t = 0.4, 0.4 - G_PRE, 3.0
    s = D_POST / B_POST
    y = s
    steps = 2000
    h = t / steps

    def rhs(g: float) -> float:
        return b * g * g - (b + d) * g + d

    for _ in range(steps):
        k1 = rhs(y)
        k2 = rhs(y + h * k1 / 2.0)
        k3 = rhs(y + h * k2 / 2.0)
        k4 = rhs(y + h * k3)
        y += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0

    assert isclose(y, pre_switch_pgf(s, t, b, d), abs_tol=1e-10)


def test_scientific_claims_require_separate_absolute_demography_and_prior_art() -> None:
    theory = (ROOT / "theory" / "STOCHASTIC_PARTNER_ASSEMBLY_V1.md").read_text(
        encoding="utf-8"
    )
    for phrase in (
        "relative",
        "absolute",
        "birth",
        "death",
        "P_eventual_persistence",
        "P_alive_at_switch",
        "Goldberg & Friedman (2021",
        "not a novel result in birth–death theory",
        "two-phase approximation",
        "both",
    ):
        assert phrase in theory, phrase
