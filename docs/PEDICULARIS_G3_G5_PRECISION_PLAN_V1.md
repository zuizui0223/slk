# Pedicularis G3-G5 precision plan v1

Status: **PROSPECTIVE / SAMPLE-SIZE PLANNING ONLY / NO G3-G5 EFFECT CLAIM**.

## 1. Purpose

The final G3-G5 effect experiment already has registered worlds, a preregistered z grid, complete-grid plant bootstrap, and final R/K/Phi estimands. This document removes the last manual design gap: how many new plants each world must recruit.

The planning chain is:

```text
independent D0 qualification final-fitness data
        -> planning-only S / D0 / D plant-level SDs
        -> frozen transport multiplier + frozen resolution targets
        -> prospective G3-G5 sample-size plan
        -> compile n into the final effect-freeze sampling block
        -> final human/commit freeze
        -> only then generate the G3-G5 field layout.
```

D0-qualification plants remain permanently ineligible for G3-G5 effect estimation.

## 2. Variance source

The planning variance comes from the already independent D0 qualification partition:

```text
S_QUAL
D0_QUAL
D_QUAL
```

on the registered fitness scale:

```text
mature viable undamaged seeds per focal flower.
```

Use:

```bash
python scripts/summarize_pedicularis_g3_g5_planning_variance.py \
  PED_D0_QUAL_CONFIRM_V1.csv \
  PEDICULARIS_D0_CONFIRMATORY_RECEIPT.json
```

The summarizer requires:

```text
D0_FULLY_QUALIFIED
all Q1-Q6 = pass
all source rows are D0-qualification eligible
all source rows are G3-G5 ineligible
matching context / fitness scale / horizon
complete mature-seed follow-up for all qualified LOW-Y and HIGH-Y plants.
```

Output:

```text
G3_G5_PLANNING_VARIANCE_READY
```

with world-specific SDs and their maximum.

## 3. Why the maximum world SD is used

The D0 qualification experiment observes only a limited structural state, whereas the final G3-G5 experiment evaluates all registered z levels.

Therefore v1 uses:

```text
SD_plan = max(SD_S, SD_D0, SD_D) x frozen safety multiplier.
```

The multiplier must be at least one and frozen before G3-G5 outcomes.

It is a transparent variance-transport safeguard, not a parameter that can be lowered after seeing the final data.

## 4. Precision targets are biological/decision targets

The precision freeze requires three targets that may not be defined from the later G3-G5 outcomes:

```text
world_cell_mean_half_width
minimum_recoverable_benefit_R
minimum_abs_architecture_value_Phi.
```

Allowed target-source classes are:

```text
DOWNSTREAM_DECISION_INVARIANCE
EXTERNAL_BIOLOGICAL_BOUND
COMBINED_PREDECLARED.
```

Rules such as

```text
target = c x observed G3-G5 SD
```

or post-hoc target relaxation are not allowed.

## 5. Simultaneous world-by-z cell precision

For the decomposition block there are:

```text
3 worlds x J registered z levels.
```

The planning approximation Bonferroni-controls the familywise alpha across all `3J` world-by-z cell means.

For target half-width `h` and planning SD `sigma`:

```text
n_cell = ceil[(z_(1-alpha_cell/2) sigma / h)^2]
alpha_cell = familywise alpha / (3J).
```

This does not assert that the final max-of-grid estimator is normally distributed. It only protects the raw cell precision needed by the later registered bootstrap re-optimization.

## 6. Minimum R and Phi resolution

The planner also computes equal-allocation two-group normal approximations for:

```text
minimum R worth resolving
minimum |Phi| worth resolving.
```

The familywise alpha assigned to this focal-effect planning is split across R and Phi.

The decomposition floor is:

```text
max(n_cell, n_R, n_Phi).
```

A prospectively frozen attrition fraction then determines recruitment n.

## 7. Independent direct-Phi block

If the final effect route is:

```text
INDEPENDENT_DIRECT_PHI_BLOCK,
```

the direct block contains only S and D.

Its prospective floor is:

```text
max(two-world simultaneous cell-precision n, n_Phi).
```

The direct block remains independent of the S/D0/D decomposition block.

## 8. Planning commands

Freeze the planning targets first using:

```text
data/PEDICULARIS_G3_G5_PRECISION_FREEZE_TEMPLATE_V1.json
```

Then run:

```bash
python scripts/plan_pedicularis_g3_g5_effect_precision.py \
  PEDICULARIS_G3_G5_PRECISION_FREEZE.json \
  PEDICULARIS_G3_G5_PLANNING_VARIANCE.json
```

The output is:

```text
SLK_PEDICULARIS_G3_G5_PRECISION_PLAN_V1
status = G3_G5_EFFECT_SAMPLE_SIZE_PROSPECTIVELY_PLANNED.
```

## 9. Automatic handoff into the final effect freeze

Do not manually copy n values.

Use:

```bash
python scripts/compile_pedicularis_g3_g5_effect_sampling.py \
  PEDICULARIS_G3_G5_EFFECT_FREEZE_CANDIDATE.json \
  PEDICULARIS_G3_G5_PRECISION_FREEZE.json \
  PEDICULARIS_G3_G5_PRECISION_PLAN.json
```

The compiler verifies:

```text
same context / population / season / scale / horizon
same number of registered z levels
same R / Phi / cell-precision targets
precision freeze occurred before G3-G5 outcomes
valid decomposition and direct-block sample sizes.
```

It fills:

```text
minimum_analyzable_plants_per_world
recruitment_plants_per_world
minimum_analyzable_plants_per_direct_world
recruitment_plants_per_direct_world
sample_size_source
sample_size_rationale.
```

## 10. Compiler output is not the final freeze

The compiler deliberately returns:

```text
SAMPLING_COMPILED_AWAITING_FINAL_EFFECT_FREEZE.
```

At that point the user must review the complete effect contract, freeze the remaining final metadata/bootstrap fields, commit it prospectively, and set the final registered effect-freeze state required by the field-layout generator.

This keeps one explicit human responsibility point while eliminating hand-transcription of n.

## 11. Final inference remains unchanged

None of the planning approximations replaces the final inference.

The G3-G5 effect adjudicator still:

```text
resamples independent plants with complete z grids
recomputes every world-by-z cell mean
reselects the best registered z cell within every bootstrap replicate
and propagates the independently qualified D0 burden correction.
```

The planning data determine only how many new plants to recruit.

## 12. Claim ceiling

This layer can only establish:

```text
G3_G5_EFFECT_SAMPLE_SIZE_PROSPECTIVELY_PLANNED.
```

It cannot establish:

```text
R > 0
K
Phi
or any G1-G5 biological closure.
```

Those claims still require the completely new final G3-G5 effect plants.
