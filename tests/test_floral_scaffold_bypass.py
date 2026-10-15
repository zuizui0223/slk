"""A filament-only functional benefit cannot by itself maintain anther dimorphism."""

from math import isclose
from pathlib import Path

import pytest

from scripts.floral_scaffold_bypass import (
    DIMORPHIC_WITH_SCAFFOLD,
    GENERALIZED,
    SCAFFOLD_ONLY,
    DIMORPHIC_UNSUPPORTED,
    FloralContext,
    witness_cases,
)


ROOT = Path(__file__).resolve().parents[1]


def params(*, pollen=0.0, scaffold=1.2, joint=0.0, anther_cost=0.3, support_cost=0.1):
    return FloralContext(pollen, scaffold, joint, anther_cost, support_cost)


def test_fitness_table_and_mechanically_supported_bypass() -> None:
    context = params()
    assert context.scores() == pytest.approx(
        {"G": 0.0, "F": 1.1, "H": 0.8, "U": -0.3}
    )
    assert context.fitness(*DIMORPHIC_WITH_SCAFFOLD) > context.fitness(*GENERALIZED)
    assert context.fitness(*SCAFFOLD_ONLY) > context.fitness(*DIMORPHIC_WITH_SCAFFOLD)
    assert context.best_in_accessible_set((GENERALIZED, DIMORPHIC_WITH_SCAFFOLD)) == (
        DIMORPHIC_WITH_SCAFFOLD,
    )
    assert context.best_in_accessible_set((GENERALIZED, DIMORPHIC_WITH_SCAFFOLD, SCAFFOLD_ONLY)) == (
        SCAFFOLD_ONLY,
    )


@pytest.mark.parametrize("support", [0.0, 0.1, 1.2, 10.0, 100.0])
@pytest.mark.parametrize("pollen", [-0.2, 0.0, 0.2, 0.8])
@pytest.mark.parametrize("joint", [-0.5, 0.0, 0.1, 0.5])
def test_mechanical_main_effect_cancels_from_heteranthery_versus_bypass(
    support: float, pollen: float, joint: float
) -> None:
    context = params(scaffold=support, pollen=pollen, joint=joint)
    expected = pollen + joint - 0.3
    assert isclose(context.retained_scaffold_dimorphism_increment(), expected, abs_tol=1e-12)


@pytest.mark.parametrize("joint", [-0.5, 0.0, 0.2, 0.3, 0.5, 1.0])
def test_cross_function_interaction_requires_a_full_four_architecture_contrast(
    joint: float,
) -> None:
    context = params(joint=joint)
    assert isclose(context.scaffold_dimorphism_interaction(), joint, abs_tol=1e-12)
    if joint > 0.3:
        assert context.fitness(*DIMORPHIC_WITH_SCAFFOLD) > context.fitness(
            *SCAFFOLD_ONLY
        )
    elif joint < 0.3:
        assert context.fitness(*DIMORPHIC_WITH_SCAFFOLD) < context.fitness(
            *SCAFFOLD_ONLY
        )
    else:
        assert isclose(
            context.fitness(*DIMORPHIC_WITH_SCAFFOLD),
            context.fitness(*SCAFFOLD_ONLY),
            abs_tol=1e-12,
        )


def test_explicit_positive_joint_gain_can_keep_anther_dimorphism_in_witness() -> None:
    no_interaction = params(joint=0.0)
    positive_interaction = params(joint=0.5)
    assert positive_interaction.scores() == pytest.approx(
        {"G": 0.0, "F": 1.1, "H": 1.3, "U": -0.3}
    )
    assert no_interaction.retained_scaffold_dimorphism_increment() < 0.0
    assert positive_interaction.retained_scaffold_dimorphism_increment() > 0.0
    assert positive_interaction.best_in_accessible_set(
        (GENERALIZED, SCAFFOLD_ONLY, DIMORPHIC_WITH_SCAFFOLD, DIMORPHIC_UNSUPPORTED)
    ) == (DIMORPHIC_WITH_SCAFFOLD,)


def test_pollinator_replacement_can_reverse_which_anther_architecture_is_favored() -> None:
    selective = params(pollen=0.8)
    indiscriminate = params(pollen=0.0)
    # In both contexts a scaffold remains useful.
    for context in (selective, indiscriminate):
        assert context.fitness(*SCAFFOLD_ONLY) > context.fitness(*GENERALIZED)
    # But dimorphic pollen-bearing anthers need not be maintained.
    assert selective.retained_scaffold_dimorphism_increment() > 0.0
    assert indiscriminate.retained_scaffold_dimorphism_increment() < 0.0


def test_accessibility_is_not_confused_with_lifetime_fitness_ranking() -> None:
    context = params()
    assert context.best_in_accessible_set((GENERALIZED, DIMORPHIC_WITH_SCAFFOLD)) == (
        DIMORPHIC_WITH_SCAFFOLD,
    )
    assert context.best_in_accessible_set((GENERALIZED, SCAFFOLD_ONLY, DIMORPHIC_WITH_SCAFFOLD)) == (
        SCAFFOLD_ONLY,
    )
    with pytest.raises(ValueError, match="empty"):
        context.best_in_accessible_set(())
    with pytest.raises(ValueError, match="binary"):
        context.fitness(2, 0)
    with pytest.raises(ValueError, match="nonnegative"):
        params(anther_cost=-0.3)


def test_claim_ceiling_keeps_bredia_acutely_manipulated_and_derived_model_conditional() -> None:
    theory = (ROOT / "theory" / "FLORAL_SCAFFOLD_BYPASS_V1.md").read_text(
        encoding="utf-8"
    )
    for statement in (
        "treatment D is not an evolved uniform-anther flower",
        "The stand-alone mechanical gain",
        "W(H)-W(F)=pi_z+gamma_z-c_a",
        "C_z = [W_z(1,1)-W_z(0,1)]",
        "without selecting to preserve dimorphic anthers",
        "not a new general theory",
    ):
        assert statement.lower() in theory.lower()
    assert witness_cases()["mechanical_only"]["F"] > witness_cases()["mechanical_only"]["H"]


def test_manuscript_does_not_infer_dimorphism_retention_from_scaffold_behavior() -> None:
    p = ROOT / "manuscript" / "SLK_MANUSCRIPT_AMNAT_V4.md"
    if not p.exists():
        p = ROOT / "MANUSCRIPT_SOURCE.md"
    text = p.read_text(encoding="utf-8")
    assert "Supporting filaments may persist without dimorphic anthers" in text
    assert "maintenance of dimorphism remains untested" in text
