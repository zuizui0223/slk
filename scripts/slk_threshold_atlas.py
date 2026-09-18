"""Deterministic helpers for the SLK unified threshold atlas.

The code mirrors theory/UNIFIED_THRESHOLD_ATLAS_V1.md and exists to prevent
sign drift between the manuscript, theorem ledger, and constructive witnesses.
It does not replace the analytical proofs.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp


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
    if beta <= 0:
        raise ValueError("beta must be positive")
    if n <= 2:
        raise ValueError("n must exceed 2")
    return exp(beta * (n - 2) * phi)


def occupancy_ratio(phi: float, beta: float, n: int) -> float:
    """Symmetric rare-mutation D:S monomorphic occupancy ratio."""
    return reciprocal_fixation_ratio(phi, beta, n)


def weak_selection_absolute_fixation_margin(phi: float, eta: float) -> float:
    """Positive iff rho_D > 1/N under the registered weak-selection result."""
    return 3.0 * phi - eta


def environmental_phi(e: float, slope: float, value_threshold: float) -> float:
    """Affine environmental architecture margin Phi(E)=slope*(E-E_V)."""
    if slope == 0:
        raise ValueError("slope must be nonzero")
    return slope * (e - value_threshold)


def rare_invasion_environment(value_threshold: float, slope: float, eta: float) -> float:
    """Environmental E where Phi(E)=eta."""
    if slope == 0:
        raise ValueError("slope must be nonzero")
    return value_threshold + eta / slope


def reverse_invasion_environment(value_threshold: float, slope: float, eta: float) -> float:
    """Environmental E where Phi(E)=-eta."""
    if slope == 0:
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
    if denom == 0:
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
    if denom == 0:
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
    if phi_slope == 0:
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
    if phi_slope == 0:
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
    if phi_slope == 0:
        raise ValueError("phi_slope must be nonzero")
    return value_threshold - endpoint_offset / phi_slope
