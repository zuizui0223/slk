"""Four-architecture floral counterfactual; illustrative biological payoffs only.

Not an empirical fit, a population-dynamic model or a proof of evolutionary
retention. a=0 means reduced anther dimorphism, NOT absence of pollen-bearing
anthers; h=1 means a mechanically functional filament scaffold.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


ArchitecturalType = tuple[int, int]

GENERALIZED: ArchitecturalType = (0, 0)
SCAFFOLD_ONLY: ArchitecturalType = (0, 1)
DIMORPHIC_WITH_SCAFFOLD: ArchitecturalType = (1, 1)
DIMORPHIC_UNSUPPORTED: ArchitecturalType = (1, 0)


@dataclass(frozen=True)
class FloralContext:
    """Complete-cycle reproductive payoff increments relative to generalized G."""

    pollen_gain: float
    scaffold_gain: float
    joint_gain: float
    incremental_dimorphism_cost: float
    scaffold_cost: float

    def __post_init__(self) -> None:
        if self.incremental_dimorphism_cost < 0 or self.scaffold_cost < 0:
            raise ValueError("architecture costs must be nonnegative")

    def fitness(self, anther_dimorphism: int, scaffold: int) -> float:
        """Common additive fitness scale; this is not measured pollen deposition."""
        if anther_dimorphism not in (0, 1) or scaffold not in (0, 1):
            raise ValueError("both architectural traits are binary")
        a, h = anther_dimorphism, scaffold
        return (
            self.pollen_gain * a
            + self.scaffold_gain * h
            + self.joint_gain * a * h
            - self.incremental_dimorphism_cost * a
            - self.scaffold_cost * h
        )

    def scores(self) -> dict[str, float]:
        return {
            "G": self.fitness(*GENERALIZED),
            "F": self.fitness(*SCAFFOLD_ONLY),
            "H": self.fitness(*DIMORPHIC_WITH_SCAFFOLD),
            "U": self.fitness(*DIMORPHIC_UNSUPPORTED),
        }

    def retained_scaffold_dimorphism_increment(self) -> float:
        """H-F: reward for anther dimorphism after preserving support."""
        return self.fitness(*DIMORPHIC_WITH_SCAFFOLD) - self.fitness(
            *SCAFFOLD_ONLY
        )

    def scaffold_dimorphism_interaction(self) -> float:
        """Four-cell interaction, not identified by Bredia slip counts."""
        return (
            self.fitness(*DIMORPHIC_WITH_SCAFFOLD)
            - self.fitness(*SCAFFOLD_ONLY)
            - self.fitness(*DIMORPHIC_UNSUPPORTED)
            + self.fitness(*GENERALIZED)
        )

    def best_in_accessible_set(
        self, accessible: Iterable[ArchitecturalType]
    ) -> tuple[ArchitecturalType, ...]:
        """Best *payoff* candidates; does not infer their mutational appearance."""
        candidates = tuple(dict.fromkeys(accessible))
        if not candidates:
            raise ValueError("accessible architecture set cannot be empty")
        measured = [(type_, self.fitness(*type_)) for type_ in candidates]
        maximum = max(value for _, value in measured)
        return tuple(type_ for type_, value in measured if abs(value - maximum) < 1e-12)


def witness_cases() -> dict[str, dict[str, float]]:
    """Two explicitly hypothetical ecologies with and without a joint effect."""
    common = dict(
        pollen_gain=0.0,
        scaffold_gain=1.2,
        incremental_dimorphism_cost=0.3,
        scaffold_cost=0.1,
    )
    return {
        "mechanical_only": FloralContext(**common, joint_gain=0.0).scores(),
        "synergistic": FloralContext(**common, joint_gain=0.5).scores(),
    }


if __name__ == "__main__":
    for label, scores in witness_cases().items():
        print(label, scores)
