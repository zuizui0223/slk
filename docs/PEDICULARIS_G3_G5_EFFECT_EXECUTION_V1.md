# Pedicularis G3-G5 effect execution v1

Status: **PROSPECTIVE / FINAL EFFECT LAYER / NO BIOLOGICAL G3-G5 RESULT CLAIMED**.

## 1. Purpose

This is the final empirical layer of the registered Pedicularis same-system chain:

```text
G1 causal shared-axis conflict
-> G2 conflict load L
-> structural-y Y0-Y3
-> independent D0 qualification Q1-Q6
-> G3 recoverable benefit R
-> G4 incremental architecture cost K
-> G5 architecture value Phi.
```

The effect experiment uses new plants. No G1/G2, Y-CAL, D0-CAL, structural-y function, or D0-qualification plant is eligible for the G3-G5 effect layer.

## 2. Prerequisites

Before a layout can be generated, all of the following must be positive in the same registered context:

```text
G2 = DIRECT_PASS / G2_DIRECT_PASS_POSITIVE
structural-y Y0 range = qualified
Y1 z-y coupling = audited
Y2 preferential loading = pass
Y3 retention-performance intervention = pass
D0 = D0_FULLY_QUALIFIED
all D0 Q1-Q6 = pass.
```

The effect freeze must match:

```text
context_id
population_id
season_id
fitness_scale_id
time_horizon_id
primary_y_metric
q5_route.
```

## 3. Registered worlds

```text
S
    LOW-Y plant
    no external qualified retention

D0
    LOW-Y plant
    qualified externalized retention comparator

D
    HIGH-Y plant
    natural realized structural retention phenotype.
```

The target cost is still:

```text
K_incremental_y
```

conditional on the background cupulate-bract architecture already existing.

This experiment does not estimate the historical total cost of originating the bract.

## 4. Registered z-grid rather than post-hoc continuous optimization

Before outcomes are opened, freeze at least five ordered z targets:

```text
level_id
target_exsertion_z
tolerance.
```

Each independent plant supplies one focal flower at every registered z level.

The plant is analyzable only if its complete grid survives and every realized z remains inside the registered tolerance.

The world optimum is the accessible-grid estimand:

```text
W_j* = max over registered z levels of mean fitness in world j at z.
```

The primary fitness scale is:

```text
mature viable undamaged seeds per focal flower.
```

Continuous curves may be visualized secondarily, but they do not replace the registered grid estimand.

## 5. Bootstrap re-optimization

The bootstrap resampling unit is:

```text
independent plant with complete registered z-grid.
```

At every bootstrap replicate:

```text
1. resample complete plants within each world;
2. recompute every world x z cell mean;
3. reselect the maximum registered z cell for that world;
4. carry the resulting W_S*, W_D0*, and W_D* forward.
```

The optimizer is therefore not frozen to the observed best z level. Max-selection uncertainty remains inside the empirical interval.

## 6. D0 apparatus-burden correction

The observed D0 world includes the already-qualified external apparatus. Let

```text
B_device = W(S_qual) - W(SHAM_qual)
```

from the independent D0 qualification receipt.

The pre-cost D0 optimum is

```text
W_D0,pre* = W_D0,observed* + B_device.
```

This correction is imported only from the independent D0 qualification partition.

### Q5-E negligible-burden route

For a D0 qualified under burden equivalence, R/K robust intervals use the full frozen burden-equivalence range rather than pretending that the observed burden point is known without uncertainty.

### Q5-A measured-burden route

For a D0 qualified under measured adjustment, R/K use the independent burden point and its qualified CI.

The same burden correction enters R and K and therefore cancels from Phi exactly.

## 7. G3

```text
R = W_D0,pre* - W_S*.
```

The receipt reports:

```text
point estimate
world-bootstrap interval before burden
burden-robust interval
whether the robust lower bound exceeds zero.
```

A non-positive R remains a measured G3 result. It is not rewritten as a positive architecture benefit.

## 8. G4

```text
K = W_D0,pre* - W_D*.
```

K may be positive, zero, or negative.

No truncation at zero is allowed.

The interpretation remains comparison-specific incremental structural-y cost.

## 9. G5 internal worldline

```text
Phi_internal = W_D* - W_S*.
```

Because

```text
R - K
= (W_D0,pre* - W_S*) - (W_D0,pre* - W_D*)
= W_D* - W_S*,
```

the same-block equality is an algebraic identity.

It is reported as internal coherence only.

Sign classification is:

```text
Phi CI entirely > 0 -> DIFFERENTIATION_FAVORED
Phi CI entirely < 0 -> PERSISTENT_COMPROMISE
otherwise           -> CRITICAL_OR_UNRESOLVED.
```

## 10. Optional independent direct-Phi block

The stronger route preregisters a new independent S:D block using new plants.

It estimates

```text
Phi_direct = W_D,direct* - W_S,direct*.
```

The bridge residual is

```text
Delta_bridge = Phi_direct - Phi_internal.
```

`STRUCTURAL_G1_G5` independent concordance requires both:

```text
abs(point residual) <= frozen point tolerance
and
residual CI includes zero.
```

Only this route is called an empirical concordance test.

## 11. Diagnostic outcomes

One of the strongest outcomes is:

```text
L lower95 > 0
R robust lower > 0
Phi upper95 < 0.
```

This yields:

```text
CONFLICT_REAL_RECOVERABLE_BUT_ARCHITECTURE_NOT_WORTH_COST.
```

It directly demonstrates that a real conflict can be recoverable while differentiation remains disfavored once architecture cost is charged.

A positive Phi outcome is also informative:

```text
CONFLICT_REAL_RECOVERABLE_AND_ARCHITECTURE_VALUE_POSITIVE.
```

## 12. Field layout

Generate only after all prerequisite receipts and the final freeze exist:

```bash
python scripts/generate_pedicularis_g3_g5_layout.py \
  PEDICULARIS_G3_G5_EFFECT_FREEZE.json \
  PEDICULARIS_G2_ADJUDICATION.json \
  PEDICULARIS_STRUCTURAL_Y_RECEIPT.json \
  PEDICULARIS_STRUCTURAL_Y_FUNCTION_RECEIPT.json \
  PEDICULARIS_D0_CONFIRMATORY_RECEIPT.json \
  --randomization-seed <integer> \
  --output-dir <directory>
```

The decomposition block uses:

```text
S, D0, D
x all registered z levels.
```

LOW-Y S and D0 assignment is randomized within one candidate pool. D plants are recruited from the frozen HIGH-Y band.

For the independent route a second, disjoint S:D block is generated.

## 13. Analysis

After outcomes are complete:

```bash
python scripts/adjudicate_pedicularis_g3_g5_effect.py \
  PEDICULARIS_G3_G5_RK_CONFIRM_V1.csv \
  PEDICULARIS_G3_G5_EFFECT_FREEZE.json \
  PEDICULARIS_G2_ADJUDICATION.json \
  PEDICULARIS_STRUCTURAL_Y_RECEIPT.json \
  PEDICULARIS_STRUCTURAL_Y_FUNCTION_RECEIPT.json \
  PEDICULARIS_D0_CONFIRMATORY_RECEIPT.json \
  [--direct-phi-csv PEDICULARIS_G5_DIRECT_CONFIRM_V1.csv]
```

## 14. Final statuses

```text
PEDICULARIS_G3_G5_EFFECT_INCOMPLETE
    one or more decomposition worlds fall below the complete-grid plant floor.

PEDICULARIS_G3_G5_EFFECT_INCOMPLETE_DIRECT_BLOCK
    R/K/internal Phi are identified, but the independent direct block is incomplete.

PEDICULARIS_G3_G5_MEASURED_INTERNAL_IDENTITY
    G3 R, G4 K and internal G5 Phi are identified in one new effect block;
    direct/decomposed equality is only algebraic.

PEDICULARIS_G3_G5_MEASURED_CONCORDANT
    independent direct Phi agrees with the R/K target under the frozen bridge rule.

PEDICULARIS_G3_G5_MEASURED_BRIDGE_NOT_CONCORDANT
    both routes are measured, but the independent bridge rule fails.
```

## 15. What this closes

A successful effect receipt finally changes the Pedicularis role in SLK from:

```text
real biological examples attached to separate gates
```

to:

```text
one same-system empirical chain
G1 -> G2(L) -> G3(R) -> G4(K) -> G5(Phi).
```

The route still does not by itself establish evolutionary invasion, fixation, or occupancy. Those remain G6-G9.
