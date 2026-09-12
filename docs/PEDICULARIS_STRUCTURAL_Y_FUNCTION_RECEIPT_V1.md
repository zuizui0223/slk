# Pedicularis structural-y Y2/Y3 function receipt v1

Status: **PROSPECTIVE / CALIBRATION-ONLY / NO G3-G5 EFFECT CLAIM**.

## 1. Purpose

The Y-CAL receipt establishes that a structural water-retention phenotype `y` is repeatable, has a resolved natural range, and has an audited coupling to exsertion `z`. That is not yet enough to call `y` a functionally differentiated second coordinate.

This receipt adds two separate tests:

```text
Y2 natural preferential loading
    natural structural y predicts antagonist protection after controlling z
    while its pollination-facing loading stays inside a frozen equivalence margin

Y3 performance intervention
    an externalized retention intervention changes y on LOW-Y plants
    while preserving z inside a frozen equivalence margin.
```

The tests use the registered D0-CAL cohort only as **calibration evidence**. These plants remain permanently ineligible for D0 confirmatory G3-G5 estimation.

## 2. Freeze before D0-CAL outcomes

Before opening D0-CAL outcomes, freeze:

```text
primary y metric inherited from the Y receipt
one primary antagonist endpoint
one primary pollination endpoint
pollination beta_y equivalence margin
minimum useful intervention-induced y gain
maximum acceptable intervention-induced z shift
bootstrap seed and number of plant-level resamples.
```

The template is:

```text
data/PEDICULARIS_STRUCTURAL_Y_FUNCTION_FREEZE_TEMPLATE_V1.json
```

Endpoint choice after seeing which endpoint gives the best result is forbidden. A non-significant pollination coefficient does not define equivalence.

Under v1 the bootstrap validity rule is fixed at at least 90% valid resamples. The template exposes `minimum_valid_fraction = 0.90`; changing that value requires a new protocol version rather than silent tuning.

## 3. Y2 natural preferential loading

Use exactly one natural structural row per independent D0-CAL plant:

```text
LOW-Y plant  -> S_CAL
HIGH-Y plant -> D_CAL.
```

This yields a maximum of 48 independent natural structural observations.

Each natural row must still satisfy the frozen Y-CAL recruitment band on the primary y metric:

```text
LOW-Y S_CAL y <= frozen LOW-Y ceiling
HIGH-Y D_CAL y >= frozen HIGH-Y floor.
```

A plant that no longer satisfies its band does not become a convenient intermediate point. It fails the registered natural-state definition; with the current minimum `n=48`, one such failure blocks the v1 Y2 pass.

### 3.1 Antagonist loading

For the frozen antagonist endpoint, fit:

```text
outcome = alpha + beta_y y + beta_z z.
```

Allowed primary antagonist endpoints are:

```text
EARLY_ATTACK_PROP                  expected beta_y < 0
SEED_PREDATION_PROP                expected beta_y < 0
MATURE_VIABLE_UNDAMAGED_SEEDS      expected beta_y > 0.
```

The model is deliberately small: the purpose is not observational causal adjustment for every plant difference. It asks whether the frozen structural-y phenotype carries the expected preferential functional loading after accounting for the registered shared coordinate `z`.

A plant-level percentile bootstrap supplies the frozen confidence interval. Y2 antagonist loading passes only when the entire interval is in the prospectively expected direction.

### 3.2 Pollination-facing cross-loading

Using the same 48 natural structural rows, fit the same two-predictor model to one frozen pollination endpoint:

```text
VISIT_RATE_PER_MIN
POLLEN_RECEIPT_GRAINS
INITIAL_SEED_SET_PROP.
```

The pollination effect is not accepted merely because `P > 0.05`. Use the prospectively frozen equivalence margin on `beta_y`.

With the registered 90% equivalence CI:

```text
-margin < CI_lower(beta_y) < CI_upper(beta_y) < +margin
```

must hold.

Therefore Y2 passes only when both are true:

```text
antagonist loading has the expected directional CI
AND
pollination cross-loading is bounded by equivalence.
```

This is the operational meaning of **preferential functional loading** in the current Pedicularis structural-y lane.

## 4. Y3 performance intervention

Y3 uses a different comparison and must not be conflated with Y2.

On each LOW-Y D0-CAL plant compare:

```text
D0_CAL - SHAM_CAL.
```

The intervention is a reversible/externalized retention-performance manipulation. It does not manipulate the historical developmental origin of the cupulate bract.

Two conditions are required.

### 4.1 Primary-y gain

The plant-level paired difference in the same frozen primary y metric must exceed a prospectively frozen minimum useful gain:

```text
95% CI_lower(mean[D0-SHAM y]) > minimum_primary_y_gain.
```

### 4.2 z preservation

The intervention must preserve realized exsertion:

```text
90% CI(D0-SHAM z)
inside
[-max_abs_exsertion_shift, +max_abs_exsertion_shift].
```

Y3 therefore establishes **functional-performance manipulability while preserving z**. It does not establish heritability, developmental origin, or a historical modularization event.

## 5. Why Y2 and Y3 are both useful

The two gates close different loopholes.

```text
Y2 alone:
    natural y is preferentially function-loaded,
    but the association could still reflect correlated plant differences.

Y3 alone:
    retention performance can be manipulated without moving z,
    but that does not show natural structural y is preferentially loaded.

Y2 + Y3:
    a repeatable natural structural-y phenotype preferentially tracks defence,
    and the corresponding performance dimension can be moved exogenously while z stays fixed.
```

That combination is substantially stronger evidence for a contemporary second functional coordinate, while remaining below historical modularization.

## 6. Receipt statuses

```text
STRUCTURAL_Y_FUNCTION_NOT_PROMOTED
    neither full Y2 nor full Y3 is established.

STRUCTURAL_Y_Y2_PREFERENTIAL_LOADING_Y3_OPEN
    natural preferential loading passes; intervention gate remains open.

STRUCTURAL_Y_Y3_PERFORMANCE_INTERVENTION_Y2_OPEN
    intervention changes y while preserving z; natural preferential loading remains open.

STRUCTURAL_Y_Y2_PREFERENTIAL_LOADING_Y3_PERFORMANCE_INTERVENTION
    both contemporary structural-y gates pass.
```

The strongest status supports the contemporary structural-y / partial-functional-modularity interpretation used by the Pedicularis programme.

## 7. Claim ceiling

Even the strongest receipt does **not** identify:

```text
historical modularization
heritability of y
trait-level dimensional release across the full x-y surface
D0 confirmatory equivalence
G3 R
G4 K
G5 Phi.
```

Those are later gates.

In particular, the same D0-CAL plants used here must not be reused to estimate R, K, or Phi. Their role is to qualify the structural-y axis and plan the later independent confirmatory experiment.

## 8. Execution

```bash
python scripts/adjudicate_pedicularis_structural_y_function.py \
  PEDICULARIS_D0_CAL_FIELD_V1.csv \
  PEDICULARIS_STRUCTURAL_Y_CALIBRATION_RECEIPT_V1.json \
  PEDICULARIS_STRUCTURAL_Y_FUNCTION_FREEZE_V1.json \
  --output PEDICULARIS_STRUCTURAL_Y_FUNCTION_RECEIPT_V1.json
```

Only a Y0/Y1 receipt with status

```text
STRUCTURAL_Y_Y0_RANGE_QUALIFIED_Y1_AUDITED
```

and authorized disjoint D0-CAL recruitment can enter this adjudicator.
