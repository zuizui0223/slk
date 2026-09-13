# SLK Am Nat theorem/formula consistency audit V1

## Scope

Cross-check the current journal-facing manuscript, internal audit manuscript, core theory, non-equivalence theorem, Figures 1–3, claim ledger, section map, provenance, and frozen programme ownership contract.

## Material inconsistency found and repaired

The audit found a real legacy inconsistency: several internal theory/provenance surfaces still used

```text
Phi=sL-K
```

as though it were the general architecture-margin definition, despite the frozen programme closure defining

```text
Phi=R-K
```

and retaining

```text
R=sL
```

only as the registered quadratic partial-release bridge.

Repaired surfaces:

1. `theory/SLK_CORE_THEORY_V1.md`
2. `theory/NON_EQUIVALENCE_THEOREM_V1.md`
3. `figures/FIG1_CAPTION_AND_SPEC.md`
4. `figures/FIG1_LOGIC_DIAGRAM.svg`
5. `docs/CLAIM_PROVENANCE_PINNED_V1.md`
6. `docs/SECTION_CLAIM_MAP_V1.md`

No theorem conclusion changes under the quadratic witness cases; the repair changes the generality statement and ownership/provenance boundary.

## Cross-surface formula checks

### Architecture value

```text
GENERAL:             Phi=R-K
QUADRATIC BRIDGE:    R=sL -> Phi=sL-K
```

Status: **PASS after repair**.

### Population feedback

```text
Delta(p)=Phi+eta(2p-1)
Delta(0)=Phi-eta
Delta(1)=Phi+eta
rare-invasion boundaries: Phi=+eta and Phi=-eta
```

Status: **PASS** across manuscript/core/non-equivalence/Figure 2–3 logic.

### Reciprocal fixation

Registered exponential Moran pair:

```text
rho_D/rho_S = exp[beta(N-2)Phi]
```

Status: **PASS** across manuscript and non-equivalence theorem.

### Absolute fixation advantage under weak selection

```text
rho_D > 1/N iff 3Phi > eta
```

Status: **PASS** where invoked; explicitly process/approximation specific.

### Weak-mutation occupancy and invariant

```text
u_i=A_ii/2
Pi_i proportional to exp[beta(N-2)u_i]

rho(j|i)/rho(i|j)
= exp[beta(N-2)(u_j-u_i)]

Pi_j/Pi_i
= exp[beta(N-2)(u_j-u_i)]
```

Therefore

```text
rho(j|i)>rho(i|j) iff Pi_j>Pi_i.
```

Status: **PASS**, with symmetric game, connected symmetric rare mutation, and registered exponential-Moran assumptions retained.

## Independent witness arithmetic

The registered constructive witnesses were recalculated independently:

```text
NE1: L=1, R=0.5, K=1
     Phi=R-K=-0.5                         PASS

NE2: s0=0.5, Delta=2
     k_local=s0^2 Delta^2=1
     k_global=s0 Delta^2=2
     k=1.5 lies strictly between them     PASS

NE3: Phi=0.2, eta=0.5
     Delta(0)=Phi-eta=-0.3                PASS

NE4: Phi=-0.2, eta=-1
     Delta(0)=Phi-eta=0.8
     beta>0,N>2 -> rho_D/rho_S<1          PASS

NE5: Phi=-0.1, eta=-0.5
     3Phi=-0.3 > -0.5=eta
     Phi<0 -> Pi_D<Pi_S in registered pair PASS
```

## Manuscript-surface check

The internal audit manuscript remains the C/G/INV-labelled traceability surface. The current journal-facing surface is `manuscript/SLK_MANUSCRIPT_AMNAT_V2.md`; `docs/SECTION_CLAIM_MAP_V1.md` now explicitly maps both surfaces and prevents journal prose from exceeding the audit claim ceiling.

Figure 3 already used the general `Phi=R-K` gate and required no formula repair.

## Result

```text
GENERAL_ARCHITECTURE_MARGIN     PASS_AFTER_REPAIR
QUADRATIC_BRIDGE_SCOPE          PASS_AFTER_REPAIR
POPULATION_FEEDBACK             PASS
RECIPROCAL_FIXATION             PASS
ABSOLUTE_FIXATION_WEAK_SELECTION PASS
WEAK_MUTATION_OCCUPANCY         PASS
FIXATION_OCCUPANCY_INVARIANT    PASS
WITNESS_ARITHMETIC              PASS
MANUSCRIPT_LEDGER_SYNC          PASS_AFTER_REPAIR
```

No remaining theorem/formula contradiction was found in the audited flagship surfaces. This audit does not establish biological G1–G9 closure and does not generalize the registered population-process results beyond their stated assumptions.
