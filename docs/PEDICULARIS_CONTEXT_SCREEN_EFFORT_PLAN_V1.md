# Pedicularis P0 signal-detection effort plan v1

Status: **PROSPECTIVE / EFFORT PLANNING ONLY / MINIMUM-RELEVANCE INPUTS STILL REQUIRE BIOLOGICAL JUSTIFICATION**.

## 1. Problem

A P0 screen needs enough effort that a low but biologically relevant signal is unlikely to be missed. Choosing `60 min`, `30 flowers`, or `20 plants` because they look convenient is not a defensible rule.

The registered alternative is:

```text
biology / decision logic
-> freeze a minimum signal worth detecting
-> freeze the desired probability of at least one detection
-> calculate observation effort
-> commit final P0 freeze
-> collect fresh screen data.
```

The planner determines **effort**, not the biological relevance threshold.

## 2. Pollinator detection

Let

```text
lambda_min = frozen minimum legitimate-visit rate per minute
q         = desired probability of at least one detection.
```

Under the registered scouting approximation of a homogeneous Poisson arrival process:

```text
P(no visit in T min) = exp(-lambda_min * T)
```

so the minimum total observation time is:

```text
T = ceil[-log(1-q) / lambda_min].
```

Temporal coverage is a separate design constraint. Freeze:

```text
minimum_temporal_bouts
minimum_minutes_per_bout.
```

The final pollinator effort is:

```text
max(Poisson detection minutes,
    temporal bouts x minimum minutes per bout).
```

This avoids satisfying a large total-minute target in one narrow observation window.

The Poisson model is a planning approximation only. It is not a claim that real bumblebee visitation is homogeneous in time.

## 3. Predator and water-state detection

For a binary signal with frozen minimum relevant prevalence `p_min`:

```text
P(no positive among n independent screen units) = (1-p_min)^n.
```

Thus:

```text
n = ceil[ log(1-q) / log(1-p_min) ].
```

This rule is used separately for:

```text
predator-attacked flowers
water-positive plants.
```

The production P0 pass threshold remains one detected event because P0 is a presence/detectability screen. The frozen `p_min` controls how much effort is required before a zero is considered an **uninformative context at the declared detection resolution**.

It still does not convert a zero into evidence of true absence.

## 4. Capacity census

The calibration base requires disjoint:

```text
Y-CAL  = 36 plants
D0-CAL = 48 plants
base   = 84 plants.
```

With a frozen reserve fraction `r`:

```text
required capacity = ceil[84(1+r)].
```

The P0 census obeys:

```text
STOP_AT_REQUIRED_CAPACITY_OR_EXHAUST_FOCAL_POPULATION.
```

Therefore:

```text
count >= required capacity
    -> capacity resolved PASS; exhaustive census unnecessary

count < required capacity AND population_census_exhausted = true
    -> capacity resolved FAIL / CONTEXT_SIGNAL_PRESENT_CAPACITY_LIMITED

count < required capacity AND census not exhausted
    -> CONTEXT_SCREEN_INCOMPLETE; continue census.
```

A partial census may never justify a capacity-limited declaration.

## 5. Source requirements

The outstanding biological/decision inputs are tracked in:

```text
data/PEDICULARIS_CONTEXT_SCREEN_EFFORT_SOURCE_LEDGER_V1.csv
```

The main open items are:

```text
minimum relevant legitimate visit rate
minimum relevant predator-attack prevalence
minimum relevant water-positive prevalence
three desired detection probabilities / temporal coverage rule
capacity reserve fraction.
```

Historical Pedicularis work is useful for source recovery but is not automatically transportable.

### Pollinator

Published P. rex studies establish bumblebee dependence and directly observed visitation, but the searchable literature currently does not provide a production-ready, transport-qualified `visits/min` threshold for a fresh P0 context.

A historical pollination percentage is not interchangeable with a legitimate visit rate.

### Predator

Historical studies show substantial predispersal predation but also strong year, patch-density, site and population variation. Therefore a historical predation percentage may anchor biological relevance but may not be copied blindly as the fresh-screen `p_min`.

### Water state

Water-filled cupulate bracts are biologically real, but the fraction of plants with a functional measurable water state in a fresh screen window is rainfall-dependent. Fresh natural-history calibration is preferred if a transportable external prevalence is unavailable.

## 6. Files

Freeze the relevance assumptions in:

```text
data/PEDICULARIS_CONTEXT_SCREEN_EFFORT_FREEZE_TEMPLATE_V1.json
```

Then run:

```bash
python scripts/plan_pedicularis_context_screen_effort.py \
  PEDICULARIS_CONTEXT_SCREEN_EFFORT_FREEZE_V1.json \
  --output PEDICULARIS_CONTEXT_SCREEN_EFFORT_PLAN_V1.json
```

Compile the result into the ordinary P0 screen template:

```bash
python scripts/compile_pedicularis_context_screen_effort.py \
  PEDICULARIS_CONTEXT_SCREEN_FREEZE_TEMPLATE_V1.json \
  PEDICULARIS_CONTEXT_SCREEN_EFFORT_PLAN_V1.json \
  --output PEDICULARIS_CONTEXT_SCREEN_FREEZE_COMPILED_V1.json
```

The compiler output is intentionally:

```text
EFFORT_COMPILED_AWAITING_FINAL_P0_FREEZE.
```

It cannot generate a field packet until a human review has:

```text
filled final freeze metadata
committed the contract
set status = FROZEN_CANDIDATE
set frozen_before_screen_outcomes = true.
```

## 7. Interpretation firewall

The planner must never be used backwards:

```text
observed screen rate
-> choose a convenient p_min/lambda_min
-> recompute effort
-> reinterpret the same screen.
```

That is forbidden.

If the completed effort detects zero signal, the result is still:

```text
CONTEXT_UNINFORMATIVE_...
```

at the frozen detection resolution, not biological absence.

## 8. Current state

```text
P0 field packet / adjudicator:          REGISTERED
capacity-census stopping rule:          REGISTERED
signal-detection effort equations:      REGISTERED
minimum-relevance source ledger:        REGISTERED
production lambda_min / p_min values:   OPEN
real P0 screen:                         NOT EXECUTED.
```

The immediate scientific task is therefore source adjudication or a small independent natural-history calibration for those minimum-relevance inputs, not further expansion of the G1-G5 theory.
