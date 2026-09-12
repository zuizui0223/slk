# SLK Pedicularis G1-G5 same-system closure protocol v1

Status: **PROSPECTIVE / FAIL-CLOSED / EXECUTION NOT STARTED**.

## 1. Purpose

This protocol extends the registered Pedicularis G2 programme into one same-system chain:

```text
G1 causal shared-axis conflict
 -> G2 conflict load L
 -> G3 recoverable architecture benefit R
 -> G4 architecture cost K
 -> G5 architecture margin Phi = R-K.
```

The target is not five positive-looking measurements assembled after the fact. The target is one prospectively frozen `Pedicularis rex` population-season in which all promoted quantities share the same biological comparison, reproductive fitness scale, and declared time horizon.

The existing `PEDICULARIS_G2_CLOSURE_PROTOCOL_V1` remains authoritative for G1-G2. This document adds the downstream architecture-value contract and the handoff constraints needed to make G1-G5 one biological chain.

## 2. Frozen identity carried across all gates

Before confirmatory outcomes are opened, freeze:

```text
context_id        = population x season x protocol version
system            = Pedicularis rex
population_id
season_id
fitness_scale_id  = UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER
time_horizon_id
z_trait_id        = realized corolla exsertion above the cupulate bract
y_trait_id        = qualified structural water-retention performance coordinate
```

No G2-G5 algebra is allowed across mismatched `context_id`, `fitness_scale_id`, or `time_horizon_id` without a separately registered bridge.

## 3. Upstream lock: G1-G2

G1-G2 inherit the non-circular V2 route:

```text
z >= 5 validated realized levels
x P0/P1 pollination intervention
x G0/G1 independently qualified predator intervention
water-y held fixed during the SCH surface
```

The water-retention axis intended for G3-G5 must not be reused as the SCH antagonist intervention.

Required upstream handoff:

```text
G1 = DIRECT_PASS
G2 = DIRECT_PASS
G2_detail = G2_DIRECT_PASS_POSITIVE
conflict_load.lower_95 > 0
THREE_WORLD_CONFLICT_HANDOFF_V1 present
```

If G2 is measured but zero-compatible, retain the G2 result but do not promote the same context into the confirmatory G3-G5 chain.

## 4. Two downstream lanes must remain distinct

Pedicularis currently supports a strong acute water-defence intervention, but acute water OFF/ON is a functional state, not by itself a structural second trait coordinate.

Therefore this protocol distinguishes:

```text
Lane A: FUNCTIONAL_STATE_RELEASE
        water OFF/ON
        -> may test state-dependent conflict release
        -> may provide a direct functional-state worldline contrast
        -> cannot by itself close structural G4 K.

Lane B: STRUCTURAL_ARCHITECTURE_VALUE
        repeatable/manipulable water-retention phenotype y
        -> preferential loading on antagonist protection
        -> bounded pollination-facing cross-effect
        -> matched S / D0 / D worlds
        -> eligible for G3 R, G4 K, and G5 Phi.
```

A positive Lane-A result is not silently relabelled as Lane-B architecture value.

## 5. Structural-y qualification before G3

The candidate second coordinate is not bract height itself because bract height contributes mechanically to the registered exsertion coordinate. The preferred `y` is a directly measured functional phenotype such as standardized water-holding capacity or retention performance.

Before G3, require:

```text
Y0 repeatable among-plant / genotype / population variation;
Y1 explicit x-y covariance and measurement independence audit;
Y2 preferential loading: y predicts antagonist protection after conditioning on x;
Y2-cross bounded pollination-facing cross-effect using an equivalence criterion;
Y3 intervention or natural-experiment support that changes y while preserving x within tolerance.
```

Failure of Y0-Y3 keeps the result at functional-state release and blocks structural G3-G5 promotion.

## 6. Three registered architecture worlds

To decompose architecture value, register three worlds prospectively.

### S — shared / one-axis world

`S` is the qualified shared-coordinate comparison inherited from G1-G2, with the second structural degree of freedom unavailable or fixed at its registered baseline while the valid `z` range remains accessible.

Estimate

```text
W_S* = max_z W_S(z).
```

### D0 — pre-cost differentiated counterfactual

`D0` is a benefit-accessible comparison in which the functional consequence of the second coordinate is supplied without requiring the focal plant to express the full realized structural architecture being costed.

A candidate implementation is a reversible externalized retention support such as a standardized sleeve/reservoir. This is only admissible if it passes the D0 qualification gates below.

Estimate

```text
W_D0* = max_(z,y_ext) W_D0(z,y_ext).
```

`D0` is not assumed costless by declaration. Any apparatus burden must be measured with a sham or bounded. If the burden cannot be isolated, `K` is only partially identified.

### D — realized differentiated architecture

`D` is the prospectively registered structural-y phenotype in the same context, optimized over the admissible joint `z,y` region:

```text
W_D* = max_(z,y) W_D(z,y).
```

The `D` state must satisfy the same functional target definition used for `D0`; otherwise the comparison confounds architecture cost with unequal recovered benefit.

## 7. D0 qualification gates

Before interpreting `D0` as the pre-cost comparator, freeze equivalence margins and require all of the following:

```text
D0-Q1  z preservation:
       externalized y does not materially change realized exsertion or its valid range.

D0-Q2  functional-benefit matching:
       D0 and D overlap within the frozen equivalence margin for the intended y-mediated
       retention/protection benefit over the comparison range.

D0-Q3  pollination-facing equivalence:
       D0 does not alter legitimate pollinator handling/pollen receipt beyond tolerance.

D0-Q4  antagonist-channel fidelity:
       D0 changes seed-predator exposure through the intended retention/protection channel,
       not through an unrelated physical barrier.

D0-Q5  apparatus-burden accounting:
       sham burden is estimated on the registered fitness scale or bounded tightly enough
       for the intended K/Phi classification.

D0-Q6  common horizon:
       S, D0, and D are evaluated over the same declared reproductive time horizon.
```

If D0-Q2 or D0-Q4 fails, the pre-cost comparator is biologically invalid and point identification of `R` and `K` stops.

## 8. G3 — recoverable architecture benefit R

For a qualified structural lane,

```text
R = W_D0* - W_S*.
```

Interpretation: improvement available when the second functional degree of freedom is supplied before charging the realized architecture debit.

Required receipt:

```text
status = RECOVERABLE_ARCHITECTURE_BENEFIT_IDENTIFIED
R.point
R.95_ci
comparison = S_TO_D0
same context / fitness scale / horizon
D0 qualification = PASS
```

Promotion rule:

```text
G3 DIRECT_PASS_POSITIVE     if R.lower_95 > 0
G3 MEASURED_ZERO_COMPATIBLE if R.lower_95 <= 0 <= R.upper_95
G3 DIRECT_NEGATIVE          if R.upper_95 < 0
```

A positive acute water-state interaction without structural-y qualification is reported as `R_state` and does not close structural G3.

## 9. G4 — architecture cost K

Define the comparison-specific net debit:

```text
K = W_D0* - W_D*.
```

This is admissible only when D0 and D deliver equivalent recovered functional benefit within the prospectively frozen matching rule.

Required receipt:

```text
status = ARCHITECTURE_COST_IDENTIFIED
K.point
K.95_ci or identified bounds
comparison = D0_TO_D
included cost channels
excluded cost channels
apparatus/sham burden treatment
benefit-equivalence result
double-counting audit
same context / fitness scale / horizon
```

Do not call the residual `K` if D0 and D differ materially in retained-water performance, antagonist protection, or pollination cross-effects. In that case report `K = NOT_IDENTIFIED` or bounded partial identification.

The protocol allows `K < 0`: the realized architecture may carry a net advantage beyond the matched benefit channel. Do not truncate K at zero.

## 10. G5 — architecture value Phi

Two routes are retained.

### Decomposed route

```text
Phi_decomp = R - K.
```

### Direct matched-worldline route

```text
Phi_direct = W_D* - W_S*.
```

These are the same target estimand. If `R`, `K`, and `Phi_direct` are all calculated from the same fitted `W_S*`, `W_D0*`, and `W_D*`, then

```text
Phi_direct = Phi_decomp
```

is an algebraic identity. That same-block equality is an **internal coherence check**, not independent empirical validation.

A nontrivial empirical concordance test is permitted only when the direct route and the R/K decomposition are estimated from prospectively declared independent or partially independent experimental/fitted blocks that target the same context, fitness scale, horizon, and comparison states. In that case record

```text
bridge_residual = Phi_direct - Phi_decomp
```

with joint uncertainty and a frozen concordance tolerance.

G5 structural direct pass requires:

```text
G1 DIRECT_PASS
G2 DIRECT_PASS positive
structural-y qualification PASS
S and D prospectively registered
Phi_direct identified on the common scale/horizon.
```

G5 decomposition pass additionally requires qualified D0 plus identified R and K.

Classify the architecture-value sign using the interval:

```text
Phi lower_95 > 0  -> DIFFERENTIATION_FAVORED
Phi upper_95 < 0  -> PERSISTENT_COMPROMISE
otherwise         -> CRITICAL_OR_UNRESOLVED
```

## 11. Strongest empirical SLK result

A complete same-system G1-G5 receipt contains:

```text
L > 0 on the registered reproductive fitness scale;
R identified from S -> D0;
K identified from D0 -> D;
Phi_decomp = R-K identified;
Phi_direct = W_D* - W_S* identified;
all uncertainty propagated on the common scale/horizon.
```

There are then two evidence grades.

```text
INTERNAL_COHERENCE
    direct and decomposed quantities come from the same world estimates;
    equality checks algebra and bookkeeping only.

INDEPENDENT_CONCORDANCE
    direct and decomposed routes come from prospectively declared independent or
    partially independent blocks targeting the same estimand;
    the frozen bridge-residual rule is satisfied.
```

The second grade is stronger, but it is not required to say that G1-G5 were measured in the same biological system. It is required before claiming that the decomposition received an independent empirical cross-check.

A particularly informative biological outcome is not necessarily `Phi > 0`. The theoretically diagnostic result may be

```text
L > 0
R > 0
Phi < 0,
```

showing directly that conflict is real and recoverable, yet the realized architecture still does not pay after its cost is charged.

## 12. Environmental crossing extension

Only after one context closes G1-G5 should a prospectively ordered environmental axis `e` be used to ask whether architecture value crosses zero:

```text
Phi(e) = R(e) - K(e)
e_c: Phi(e_c) = 0.
```

This is an extension, not a rescue for a failed focal context. Environment levels and the crossing rule must be frozen before outcome inspection.

## 13. Stop rules

Fail closed for structural G3-G5 if any of the following occurs:

```text
G2 is not positive in the same context;
water retained/drained was reused as SCH antagonist G;
structural y is not qualified independently of x;
S, D0, or D was chosen after inspecting fitness outcomes;
D0 changes pollination geometry or predator access through an unintended channel;
D0 and D do not satisfy the frozen benefit-equivalence rule;
D0 apparatus burden is neither measured nor bounded;
fitness scale or time horizon changes across worlds;
R/K double-count the same channel;
context/population/season identity changes without a registered bridge.
```

A failed decomposition does not erase a valid direct `Phi` worldline comparison. Report the lower claim ceiling explicitly.

## 14. Receipt hierarchy

The machine-adjudicated statuses distinguish:

```text
G1_G2_READY_ONLY
FUNCTIONAL_STATE_RELEASE_ONLY
STRUCTURAL_DIRECT_PHI_IDENTIFIED
STRUCTURAL_G1_G5_CLOSED_INTERNAL_IDENTITY
STRUCTURAL_G1_G5_DECOMPOSED
STRUCTURAL_G1_G5_CLOSED_CONCORDANT
```

`STRUCTURAL_G1_G5_CLOSED_INTERNAL_IDENTITY` means the same-system chain is closed, but direct/decomposed equality is only algebraic because the same fitted world estimates were reused.

`STRUCTURAL_G1_G5_CLOSED_CONCORDANT` is reserved for prospectively declared independent/partially independent estimation blocks whose bridge residual satisfies the frozen concordance rule.

## 15. Current status

```text
G1 observational / design support:                    RECOVERED / REGISTERED
G1 confirmatory same-context receipt:                 NOT YET EXECUTED
G2 biological L receipt:                              NOT YET EXECUTED
functional water-defence state:                       BIOLOGICALLY SUPPORTED
functional-state dimensional-release experiment:     REGISTERED / NOT YET EXECUTED
structural y repeatability/preferential loading:      NOT YET IDENTIFIED
D0 pre-cost counterfactual:                           CONCEPT REGISTERED / NOT YET QUALIFIED
G3 structural R:                                      NOT IDENTIFIED
G4 K:                                                 NOT IDENTIFIED
G5 direct structural Phi:                             NOT IDENTIFIED
G5 decomposed Phi:                                    NOT IDENTIFIED
same-system G1-G5 closure:                            OPEN
```

## 16. Immediate next executable work

Do not add another theorem. Execute in this order:

```text
1. finish the already registered Qz/Qp/Qg threshold freeze and field qualification;
2. obtain the non-circular Pedicularis G1-G2 receipt;
3. in parallel, qualify structural y (Y0-Y3);
4. pilot D0 with sham burden + benefit-equivalence measurements, without opening confirmatory Phi;
5. freeze S/D0/D comparison states and G3-G5 thresholds;
6. execute the matched architecture-value experiment;
7. adjudicate direct Phi and decomposed R-K jointly;
8. only call the bridge an empirical concordance test if separate preregistered estimation blocks exist.
```
