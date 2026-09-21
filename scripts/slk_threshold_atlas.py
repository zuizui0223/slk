"""Deterministic helpers for the SLK unified threshold atlas.

The code mirrors theory/UNIFIED_THRESHOLD_ATLAS_V1.md and exists to prevent
sign drift between the manuscript, theorem ledger, and constructive witnesses.
It does not replace the analytical proofs.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isclose, log


DEFAULT_ABS_TOL = 1e-12
DEFAULT_REL_TOL = 1e-10
DEFAULT_ZERO_TOL = 1e-12


REGISTERED_WITNESS_PARAMETERS = {
    "W1": {"L": 2.0, "k": 2.2},
    "W2": {"k": 1.5},
    "W3": {"k": 0.8, "eta": 1.5},
    "W4": {"k": 2.2, "eta": -1.0},
    "W5": {"k": 2.1, "eta": -0.5},
}
REGISTERED_WITNESS_MORAN_BETA = 0.1
REGISTERED_WITNESS_MORAN_N = 20


def numerically_close(
    a: float,
    b: float,
    *,
    rel_tol: float = DEFAULT_REL_TOL,
    abs_tol: float = DEFAULT_ABS_TOL,
) -> bool:
    """Project-wide floating comparison policy for theoretical quantities."""
    return isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)


def require_numerically_nonzero(
    value: float,
    name: str,
    *,
    zero_tol: float = DEFAULT_ZERO_TOL,
) -> None:
    """Reject numerically singular denominators instead of testing value == 0."""
    if abs(value) <= zero_tol:
        raise ValueError(
            f"{name} is numerically singular: |{name}|={abs(value):.3g} <= {zero_tol:.3g}"
        )


@dataclass(frozen=True)
class SymmetricTwoStrategyGame:
    """Symmetric two-strategy payoff game with S and D strategies."""

    ss: float
    sd: float
    dd: float

    @property
    def self_play_gap(self) -> float:
        """A_DD/2 - A_SS/2."""
        return 0.5 * (self.dd - self.ss)

    @property
    def eta_coordinate(self) -> float:
        """Canonical interaction coordinate when the architecture mapping is valid."""
        return 0.5 * (self.ss + self.dd) - self.sd


@dataclass(frozen=True)
class CanonicalArchitectureGame:
    """Explicit receipt for the registered equal-diagonal-feedback canonical map."""

    phi: float
    eta: float
    baseline: float = 0.0

    def as_game(self) -> SymmetricTwoStrategyGame:
        return SymmetricTwoStrategyGame(
            ss=self.baseline,
            sd=self.baseline + self.phi - self.eta,
            dd=self.baseline + 2.0 * self.phi,
        )


def canonical_architecture_game(
    phi: float,
    eta: float,
    *,
    baseline: float = 0.0,
) -> CanonicalArchitectureGame:
    """Construct the registered canonical pair explicitly."""
    return CanonicalArchitectureGame(phi=phi, eta=eta, baseline=baseline)


def validate_canonical_mapping(
    game: SymmetricTwoStrategyGame,
    *,
    phi: float,
    eta: float,
    rel_tol: float = DEFAULT_REL_TOL,
    abs_tol: float = DEFAULT_ABS_TOL,
) -> None:
    """Require a generic symmetric game to match the registered canonical coordinates."""
    if not numerically_close(
        game.self_play_gap, phi, rel_tol=rel_tol, abs_tol=abs_tol
    ):
        raise ValueError(
            "equal-diagonal-feedback canonical mapping violated: "
            f"self-play gap={game.self_play_gap!r}, expected phi={phi!r}"
        )
    if not numerically_close(
        game.eta_coordinate, eta, rel_tol=rel_tol, abs_tol=abs_tol
    ):
        raise ValueError(
            "canonical interaction coordinate violated: "
            f"eta(game)={game.eta_coordinate!r}, expected eta={eta!r}"
        )


def self_excluding_payoffs(
    game: SymmetricTwoStrategyGame,
    d_count: int,
    n: int,
) -> tuple[float, float]:
    """Return (pi_S, pi_D) for a state with d_count D individuals."""
    if n <= 2:
        raise ValueError("n must exceed 2")
    if not (1 <= d_count <= n - 1):
        raise ValueError("d_count must be between 1 and n-1")
    s_count = n - d_count
    pi_d = (
        (d_count - 1) * game.dd + s_count * game.sd
    ) / (n - 1)
    pi_s = (
        d_count * game.sd + (s_count - 1) * game.ss
    ) / (n - 1)
    return pi_s, pi_d


def moran_transition_probabilities(
    game: SymmetricTwoStrategyGame,
    d_count: int,
    beta: float,
    n: int,
) -> tuple[float, float]:
    """Return (T_plus, T_minus) for the self-excluding exponential Moran process."""
    if beta <= 0:
        raise ValueError("beta must be positive")
    pi_s, pi_d = self_excluding_payoffs(game, d_count, n)
    s_count = n - d_count

    # Stable exponential-fitness reproduction probabilities.  Subtracting the
    # larger log weight prevents overflow without changing the Moran kernel.
    log_weight_d = log(d_count) + beta * pi_d
    log_weight_s = log(s_count) + beta * pi_s
    max_log_weight = max(log_weight_d, log_weight_s)
    weight_d = exp(log_weight_d - max_log_weight)
    weight_s = exp(log_weight_s - max_log_weight)
    birth_d = weight_d / (weight_d + weight_s)
    birth_s = weight_s / (weight_d + weight_s)

    t_plus = birth_d * (s_count / n)
    t_minus = birth_s * (d_count / n)
    return t_plus, t_minus


def _fixation_probability_d_from_game(
    game: SymmetricTwoStrategyGame,
    beta: float,
    n: int,
) -> float:
    """Exact birth-death fixation probability of one D mutant in S."""
    if beta <= 0:
        raise ValueError("beta must be positive")
    if n <= 2:
        raise ValueError("n must exceed 2")

    log_products: list[float] = []
    cumulative_log_gamma = 0.0
    for d_count in range(1, n):
        t_plus, t_minus = moran_transition_probabilities(
            game, d_count, beta, n
        )
        if t_plus <= 0 or t_minus <= 0:
            raise ValueError("interior Moran transition probabilities must be positive")
        cumulative_log_gamma += log(t_minus) - log(t_plus)
        log_products.append(cumulative_log_gamma)

    # Stable evaluation of 1 / (1 + sum(exp(log_products))).
    max_log = max(0.0, *log_products)
    scaled_denom = exp(-max_log) + sum(
        exp(value - max_log) for value in log_products
    )
    return exp(-max_log) / scaled_denom


def fixation_probability_d(
    game: SymmetricTwoStrategyGame,
    beta: float,
    n: int,
) -> float:
    """Fixation probability of one D mutant in an S resident population."""
    return _fixation_probability_d_from_game(game, beta, n)


def swap_strategies(game: SymmetricTwoStrategyGame) -> SymmetricTwoStrategyGame:
    """Relabel S<->D while preserving the underlying biological game."""
    return SymmetricTwoStrategyGame(
        ss=game.dd,
        sd=game.sd,
        dd=game.ss,
    )


def fixation_probability_s(
    game: SymmetricTwoStrategyGame,
    beta: float,
    n: int,
) -> float:
    """Fixation probability of one S mutant in a D resident population."""
    return _fixation_probability_d_from_game(swap_strategies(game), beta, n)


def reciprocal_fixation_ratio_from_process(
    game: SymmetricTwoStrategyGame,
    beta: float,
    n: int,
) -> float:
    """Compute rho_D/rho_S from the Moran birth-death process itself."""
    rho_d = fixation_probability_d(game, beta, n)
    rho_s = fixation_probability_s(game, beta, n)
    return rho_d / rho_s


def symmetric_rare_mutation_stationary_distribution(
    rho_d: float,
    rho_s: float,
) -> tuple[float, float]:
    """Stationary (Pi_S, Pi_D) of the two-state symmetric rare-mutation chain."""
    if rho_d <= 0 or rho_s <= 0:
        raise ValueError("fixation probabilities must be positive")
    total = rho_d + rho_s
    return rho_s / total, rho_d / total


def occupancy_ratio_from_process(
    game: SymmetricTwoStrategyGame,
    beta: float,
    n: int,
) -> float:
    """Compute Pi_D/Pi_S through fixation probabilities and the mutation chain."""
    rho_d = fixation_probability_d(game, beta, n)
    rho_s = fixation_probability_s(game, beta, n)
    pi_s, pi_d = symmetric_rare_mutation_stationary_distribution(rho_d, rho_s)
    return pi_d / pi_s


def canonical_reciprocal_fixation_ratio_closed_form(
    canonical: CanonicalArchitectureGame,
    beta: float,
    n: int,
) -> float:
    """Registered closed form; the canonical-mapping assumption is explicit in the type."""
    if beta <= 0:
        raise ValueError("beta must be positive")
    if n <= 2:
        raise ValueError("n must exceed 2")
    return exp(beta * (n - 2) * canonical.phi)


@dataclass(frozen=True)
class ArchitecturePath:
    """Quadratic witness family R(d)=a*d+b*d^2 on d in [0, dmax]."""

    a: float = 1.0
    b: float = 1.0
    dmax: float = 1.0

    def recovery(self, d: float) -> float:
        return self.a * d + self.b * d * d

    @property
    def k_local(self) -> float:
        return self.a

    @property
    def k_global(self) -> float:
        return self.recovery(self.dmax) / self.dmax

    def phi(self, k: float) -> float:
        return self.recovery(self.dmax) - k * self.dmax

    def local_gradient(self, k: float) -> float:
        return self.k_local - k


def selection_gap(phi: float, eta: float, p: float) -> float:
    """D minus S payoff at D frequency p."""
    return phi + eta * (2.0 * p - 1.0)


def rare_invasion_margin(phi: float, eta: float) -> float:
    return selection_gap(phi, eta, 0.0)


def reverse_invasion_resistance_margin(phi: float, eta: float) -> float:
    return selection_gap(phi, eta, 1.0)


def reciprocal_fixation_ratio(phi: float, beta: float, n: int) -> float:
    """Legacy analytical convenience for the registered canonical pair.

    Prefer canonical_reciprocal_fixation_ratio_closed_form() when the
    equal-diagonal-feedback assumption should be explicit in the API.
    """
    return canonical_reciprocal_fixation_ratio_closed_form(
        canonical_architecture_game(phi, eta=0.0),
        beta,
        n,
    )


def occupancy_ratio(phi: float, beta: float, n: int) -> float:
    """Process-derived symmetric rare-mutation D:S occupancy ratio.

    This intentionally does NOT alias reciprocal_fixation_ratio().
    """
    game = canonical_architecture_game(phi, eta=0.0).as_game()
    return occupancy_ratio_from_process(game, beta, n)


def weak_selection_absolute_fixation_margin(phi: float, eta: float) -> float:
    """Positive iff rho_D > 1/N under the registered weak-selection result."""
    return 3.0 * phi - eta


def environmental_phi(e: float, slope: float, value_threshold: float) -> float:
    """Affine environmental architecture margin Phi(E)=slope*(E-E_V)."""
    if abs(slope) <= DEFAULT_ZERO_TOL:
        raise ValueError("slope must be nonzero")
    return slope * (e - value_threshold)


def rare_invasion_environment(value_threshold: float, slope: float, eta: float) -> float:
    """Environmental E where Phi(E)=eta."""
    if abs(slope) <= DEFAULT_ZERO_TOL:
        raise ValueError("slope must be nonzero")
    return value_threshold + eta / slope


def reverse_invasion_environment(value_threshold: float, slope: float, eta: float) -> float:
    """Environmental E where Phi(E)=-eta."""
    if abs(slope) <= DEFAULT_ZERO_TOL:
        raise ValueError("slope must be nonzero")
    return value_threshold - eta / slope


def rare_invasion_environment_affine_feedback(
    value_threshold: float,
    phi_slope: float,
    eta_at_value: float,
    eta_slope: float,
) -> float:
    """Solve Phi(E)=eta(E) for affine Phi and affine eta."""
    denom = phi_slope - eta_slope
    if abs(denom) <= DEFAULT_ZERO_TOL:
        raise ValueError("phi_slope must differ from eta_slope")
    return value_threshold + eta_at_value / denom


def reverse_invasion_environment_affine_feedback(
    value_threshold: float,
    phi_slope: float,
    eta_at_value: float,
    eta_slope: float,
) -> float:
    """Solve Phi(E)=-eta(E) for affine Phi and affine eta."""
    denom = phi_slope + eta_slope
    if abs(denom) <= DEFAULT_ZERO_TOL:
        raise ValueError("phi_slope must differ from -eta_slope")
    return value_threshold - eta_at_value / denom


def identify_phi_eta_from_symmetric_frequencies(
    delta_minus: float,
    delta_plus: float,
    q: float,
) -> tuple[float, float]:
    """Recover Phi and eta from p=1/2-q and p=1/2+q."""
    if not (0 < q <= 0.5):
        raise ValueError("q must satisfy 0 < q <= 0.5")
    phi = 0.5 * (delta_plus + delta_minus)
    eta = (delta_plus - delta_minus) / (4.0 * q)
    return phi, eta


def selection_gap_quadratic_frequency(
    phi: float,
    h0: float,
    eta: float,
    kappa: float,
    p: float,
) -> float:
    """Centered quadratic frequency map Delta=Phi+h0+eta*x+kappa*x^2."""
    x = 2.0 * p - 1.0
    return phi + h0 + eta * x + kappa * x * x


def identify_quadratic_frequency_components(
    phi: float,
    delta_mid: float,
    delta_minus: float,
    delta_plus: float,
    q: float,
) -> tuple[float, float, float]:
    """Recover h0, eta, kappa from p=1/2 and symmetric p=1/2±q."""
    if not (0 < q <= 0.5):
        raise ValueError("q must satisfy 0 < q <= 0.5")
    h0 = delta_mid - phi
    eta = (delta_plus - delta_minus) / (4.0 * q)
    kappa = (delta_plus + delta_minus - 2.0 * delta_mid) / (8.0 * q * q)
    return h0, eta, kappa


def rare_invasion_margin_quadratic_frequency(
    phi: float,
    h0: float,
    eta: float,
    kappa: float,
) -> float:
    return phi + h0 - eta + kappa


def reverse_invasion_resistance_margin_quadratic_frequency(
    phi: float,
    h0: float,
    eta: float,
    kappa: float,
) -> float:
    return phi + h0 + eta + kappa


def rare_invasion_environment_quadratic_frequency(
    value_threshold: float,
    phi_slope: float,
    h0: float,
    eta: float,
    kappa: float,
) -> float:
    """Solve Phi(E)+h0-eta+kappa=0 for affine Phi(E)."""
    if abs(phi_slope) <= DEFAULT_ZERO_TOL:
        raise ValueError("phi_slope must be nonzero")
    return value_threshold + (eta - kappa - h0) / phi_slope


def reverse_invasion_environment_quadratic_frequency(
    value_threshold: float,
    phi_slope: float,
    h0: float,
    eta: float,
    kappa: float,
) -> float:
    """Solve Phi(E)+h0+eta+kappa=0 for affine Phi(E)."""
    if abs(phi_slope) <= DEFAULT_ZERO_TOL:
        raise ValueError("phi_slope must be nonzero")
    return value_threshold - (eta + kappa + h0) / phi_slope


def rare_invasion_margin_endpoint(phi: float, h_rare: float) -> float:
    """General rare-D invasion margin Phi + endpoint ecological offset."""
    return phi + h_rare


def reverse_invasion_resistance_margin_endpoint(phi: float, h_resident_d: float) -> float:
    """General resistance-to-rare-S margin Phi + D-resident endpoint offset."""
    return phi + h_resident_d


def invasion_environment_from_endpoint_offset(
    value_threshold: float,
    phi_slope: float,
    endpoint_offset: float,
) -> float:
    """Solve Phi(E)+h_endpoint=0 for affine Phi(E)."""
    if abs(phi_slope) <= DEFAULT_ZERO_TOL:
        raise ValueError("phi_slope must be nonzero")
    return value_threshold - endpoint_offset / phi_slope


def endpoint_lipschitz_interval(
    delta_at_epsilon: float,
    epsilon: float,
    lipschitz_bound: float,
) -> tuple[float, float]:
    """Deterministic endpoint interval from one finite-frequency assay."""
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    if lipschitz_bound < 0:
        raise ValueError("lipschitz_bound must be nonnegative")
    radius = lipschitz_bound * epsilon
    return delta_at_epsilon - radius, delta_at_epsilon + radius


def extrapolate_endpoint_two_frequency(
    delta_epsilon: float,
    delta_two_epsilon: float,
) -> float:
    """Linear extrapolation of endpoint value from epsilon and 2*epsilon."""
    return 2.0 * delta_epsilon - delta_two_epsilon


def endpoint_curvature_interval(
    delta_epsilon: float,
    delta_two_epsilon: float,
    epsilon: float,
    curvature_bound: float,
) -> tuple[float, float]:
    """Second-order endpoint interval under |Delta''| <= curvature_bound."""
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    if curvature_bound < 0:
        raise ValueError("curvature_bound must be nonnegative")
    estimate = extrapolate_endpoint_two_frequency(
        delta_epsilon, delta_two_epsilon
    )
    radius = curvature_bound * epsilon * epsilon
    return estimate - radius, estimate + radius


def sign_certificate(interval: tuple[float, float]) -> str:
    """Return positive, negative, or unresolved for a deterministic interval."""
    lower, upper = interval
    if lower > 0:
        return "positive"
    if upper < 0:
        return "negative"
    return "unresolved"


def environmental_threshold_error_bound(
    fitness_margin_error_bound: float,
    phi_environment_slope: float,
) -> float:
    """Convert a fitness-scale endpoint error bound to environmental distance."""
    if fitness_margin_error_bound < 0:
        raise ValueError("fitness_margin_error_bound must be nonnegative")
    require_numerically_nonzero(
        phi_environment_slope, "phi_environment_slope"
    )
    return fitness_margin_error_bound / abs(phi_environment_slope)


def endpoint_lipschitz_interval_with_sampling(
    measured_interval: tuple[float, float],
    epsilon: float,
    lipschitz_bound: float,
) -> tuple[float, float]:
    """Combine sampling interval with one-point endpoint approximation error."""
    lower, upper = measured_interval
    if lower > upper:
        raise ValueError("measured_interval must satisfy lower <= upper")
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    if lipschitz_bound < 0:
        raise ValueError("lipschitz_bound must be nonnegative")
    radius = lipschitz_bound * epsilon
    return lower - radius, upper + radius


def endpoint_curvature_interval_with_sampling(
    interval_epsilon: tuple[float, float],
    interval_two_epsilon: tuple[float, float],
    epsilon: float,
    curvature_bound: float,
) -> tuple[float, float]:
    """Combine two sampling intervals with second-order endpoint remainder."""
    l1, u1 = interval_epsilon
    l2, u2 = interval_two_epsilon
    if l1 > u1 or l2 > u2:
        raise ValueError("sampling intervals must satisfy lower <= upper")
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    if curvature_bound < 0:
        raise ValueError("curvature_bound must be nonnegative")
    radius = curvature_bound * epsilon * epsilon
    return 2.0 * l1 - u2 - radius, 2.0 * u1 - l2 + radius
