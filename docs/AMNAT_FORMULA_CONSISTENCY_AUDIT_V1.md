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

## Unified critical-surface check

The current flagship now registers one composite theorem surface:

```text
small-step selective release       k=k_local
global endpoint value              Phi=0 <=> k=k_global
rare D invasion                    Phi=eta
reverse invasion                   Phi=-eta
reciprocal fixation ordering       Phi=0
absolute fixation vs neutrality    3Phi=eta [weak selection]
rare-mutation occupancy ordering   Phi=0
```

Status: **PASS** across `theory/UNIFIED_THRESHOLD_ATLAS_V1.md`, core theory, claim ledger, AMNAT V4, and the redesigned Figure 1.

## Cross-level compatibility check

The registered composite mapping preserves the endpoint architecture contrast:

```text
Phi = W_D-W_S
A_DD/2-A_SS/2 = Phi
log(rho_D/rho_S) / [beta(N-2)] = Phi
log(Pi_D/Pi_S) / [beta(N-2)] = Phi
```

Status: **PASS** under the registered equal-diagonal-feedback canonical mapping, exponential-Moran process, and connected symmetric rare mutation.

This check is essential: the threshold atlas transports one endpoint contrast rather than replacing it with unrelated downstream payoff coordinates.

## Ecological threshold-displacement check

For the registered affine environmental slice,

```text
Phi(E)=a(E-E_V), a>0
```

the value crossing is `E_V`. Substituting the invasion surfaces gives

```text
Phi(E_I)=eta
-> E_I=E_V+eta/a

Phi(E_R)=-eta
-> E_R=E_V-eta/a.
```

Therefore

```text
E_I-E_V=eta/a
|E_I-E_R|=2|eta|/a.
```

Status: **PASS** across unified theory, AMNAT V4, Figure 2 specification, executable verifier, and ecological-deduction tests.

The exact spacing is claimed only for the registered affine slice with locally constant `eta`.

## Varying-feedback environmental check

For

```text
Phi(E)=a(E-E_V)
eta(E)=eta_0+b(E-E_V),
```

the registered invasion equations give

```text
E_I-E_V=eta_0/(a-b)
E_R-E_V=-eta_0/(a+b).
```

For `|b|<a`,

```text
|E_I-E_R|=2a|eta_0|/(a^2-b^2)
(E_I+E_R)/2-E_V=eta_0 b/(a^2-b^2).
```

Status: **PASS** across unified theory, AMNAT V4, executable threshold helpers, verifier, and unit tests.

## Independent witness arithmetic

All registered separations were recalculated inside the common family

```text
R(d)=d+d^2
K(d)=kd
d in [0,1]
k_local=1
k_global=2
Phi=2-k
```

with the following results:

```text
NE1: L=2, k=2.2
     R(1)=2, K(1)=2.2
     Phi=-0.2                              PASS

NE2: k=1.5
     Phi=0.5>0
     Phi'(0)=1-1.5=-0.5<0                 PASS

NE3: k=0.8, eta=1.5
     Phi=1.2
     Phi'(0)=0.2>0
     Delta(0)=Phi-eta=-0.3                PASS

NE4: k=2.2, eta=-1
     Phi=-0.2
     Delta(0)=0.8
     beta>0,N>2 -> rho_D/rho_S<1          PASS

NE5: k=2.1, eta=-0.5
     Phi=-0.1
     3Phi=-0.3 > -0.5=eta
     Phi<0 -> Pi_D<Pi_S                   PASS
```

## Manuscript-surface check

The internal audit manuscript remains the C/G/INV-labelled traceability surface. The current journal-facing surface is `manuscript/SLK_MANUSCRIPT_AMNAT_V4.md`; `docs/SECTION_CLAIM_MAP_V1.md` maps the unified theorem and prevents journal prose from exceeding the audit claim ceiling.

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
UNIFIED_CRITICAL_SURFACES       PASS
CROSS_LEVEL_PHI_COMPATIBILITY    PASS
ECOLOGICAL_THRESHOLD_DISPLACEMENT PASS
ECOLOGICAL_FEEDBACK_GRADIENT      PASS
WITNESS_ARITHMETIC              PASS
MANUSCRIPT_LEDGER_SYNC          PASS_AFTER_REPAIR
```

No remaining theorem/formula contradiction was found in the audited flagship surfaces. This audit does not establish biological G1–G9 closure and does not generalize the registered population-process results beyond their stated assumptions.
