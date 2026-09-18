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
