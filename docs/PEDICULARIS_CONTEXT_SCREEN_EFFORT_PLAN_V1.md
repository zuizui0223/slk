# Pedicularis P0 signal-detection effort plan v1

Status: **PROSPECTIVE / FLOWER-MINUTE CORRECTED / MINIMUM-RELEVANCE NUMERIC SOURCES STILL OPEN**.

## 1. Purpose

P0 must use enough effort that a biologically relevant but uncommon signal is unlikely to be missed. The planner does not decide what is biologically relevant. It converts **prospectively qualified** minimum-relevance inputs into observation effort.

The workflow is:

```text
source qualification
-> freeze biological minimum-relevance values
-> freeze detection probability / temporal coverage / capacity reserve
-> calculate P0 effort
-> compile final P0 freeze
-> execute fresh context screen.
```

A production value cannot enter the planner merely because it appeared in a paper. External numeric values require `NUMERIC_TRANSPORT_QUALIFIED`; fresh calibration values require `FRESH_CALIBRATION_QUALIFIED`.

## 2. Pollinator exposure is flower-minutes

The 2015 `P. rex` visitor study did not express visitation as raw visits per clock minute. It conducted 30-min plot censuses, counted simultaneously open flowers and expressed visitation as visits per flower per 30 min.

Therefore P0 v1 uses:

```text
flower-minutes
= observation minutes x simultaneously open focal P. rex flowers
```

and the minimum-relevance rate is:

```text
lambda_min = legitimate visits / flower-minute.
```

This matters because 30 minutes observing one open flower is not the same exposure as 30 minutes observing 20 open flowers.

### Poisson detection planning

For a frozen minimum relevant rate `lambda_min` and desired probability `q` of at least one legitimate visit:

```text
P(no visit after E flower-minutes)
= exp(-lambda_min x E)
```

so:

```text
E_required
= ceil[-log(1-q) / lambda_min].
```

This is an exposure requirement, not automatically a clock-time requirement.

## 3. Temporal coverage is a separate constraint

P0 also freezes:

```text
minimum_temporal_bouts
minimum_minutes_per_bout.
```

Thus pollinator collection must satisfy **both**:

```text
cumulative observation minutes >= temporal coverage minimum
AND
cumulative flower-minutes      >= Poisson exposure minimum.
```

If few flowers are open, more clock time is needed to reach the flower-minute requirement. If many are open, the flower-minute requirement may be reached early, but the registered bout/time coverage must still be completed.

The Poisson model is a planning approximation only; it is not a claim of homogeneous bumblebee arrival through time.

## 4. Predator and water-state detection

For a binary signal with frozen minimum relevant prevalence `p_min`:

```text
P(no positive among n screen units)
= (1-p_min)^n.
```

Thus:

```text
n = ceil[log(1-q) / log(1-p_min)].
```

The two target endpoints are deliberately specific:

```text
predator
    early attacked-flower / oviposition-positive prevalence

water state
    water-positive flowering-plant prevalence at the registered screen moment.
```

Final seed predation is not a substitute for early attack. A statement that bracts are commonly water-filled is not a prevalence denominator.

## 5. Numeric source qualification

The source-type-specific gates are:

```text
DOWNSTREAM_DESIGN_REQUIREMENT
    -> DESIGN_REQUIREMENT_QUALIFIED

INDEPENDENT_NATURAL_HISTORY_CALIBRATION
    -> FRESH_CALIBRATION_QUALIFIED

EXTERNAL_MATCHED_PRIMARY_SOURCE
    -> NUMERIC_TRANSPORT_QUALIFIED

COMBINED_PREDECLARED
    -> COMBINED_PREDECLARED_QUALIFIED.
```

The planner rejects a source whose type and qualification status do not match.

Canonical source audit:

```text
docs/PEDICULARIS_P0_RELEVANCE_SOURCE_ADJUDICATION_V1.md
data/PEDICULARIS_P0_RELEVANCE_SOURCE_ADJUDICATION_V1.csv
```

As currently adjudicated:

```text
pollinator external method/denominator: matched after flower-minute correction
pollinator external numeric value:      NOT QUALIFIED
predator external numeric prevalence:   NOT QUALIFIED / endpoint mismatch
water external numeric prevalence:      NOT QUALIFIED / denominator absent.
```

## 6. Source-qualification receipt

A numeric value may be promoted only through:

```text
data/PEDICULARIS_P0_RELEVANCE_QUALIFICATION_TEMPLATE_V1.json
scripts/validate_pedicularis_p0_relevance_qualification.py
```

Allowed routes are:

```text
EXTERNAL_NUMERIC_TRANSPORT
FRESH_INDEPENDENT_CALIBRATION.
```

External route requires:

```text
endpoint match
unit / denominator match
explicit focal-context transport justification
exact auditable numeric value
freeze before P0 outcomes.
```

Fresh route requires:

```text
exact target endpoint
independent calibration units
no reuse as P0 decision units
no reuse as downstream confirmatory units
freeze before P0 outcomes.
```

Reading an approximate bar height from a figure cannot earn `NUMERIC_TRANSPORT_QUALIFIED`.

## 7. Compile qualified biology into the effort freeze

After all three biological inputs qualify:

```bash
python scripts/compile_pedicularis_p0_relevance_into_effort_freeze.py \
  data/PEDICULARIS_CONTEXT_SCREEN_EFFORT_FREEZE_TEMPLATE_V1.json \
  PEDICULARIS_P0_RELEVANCE_QUALIFICATION_FILLED.json \
  --output PEDICULARIS_CONTEXT_SCREEN_EFFORT_RELEVANCE_COMPILED.json
```

The result remains incomplete. It still needs prospectively chosen:

```text
desired detection probabilities
pollinator temporal coverage
capacity reserve
final metadata.
```

Only after those design inputs are frozen may the effort planner run.

## 8. Capacity census

The fixed calibration base is:

```text
Y-CAL  = 36 independent plants
D0-CAL = 48 independent plants
base   = 84 plants.
```

With frozen reserve fraction `r`:

```text
required capacity = ceil[84(1+r)].
```

Census rule:

```text
STOP_AT_REQUIRED_CAPACITY_OR_EXHAUST_FOCAL_POPULATION.
```

Therefore a site below required capacity is called `CONTEXT_SIGNAL_PRESENT_CAPACITY_LIMITED` only after the focal population has been exhaustively censused. A partial low count is `CONTEXT_SCREEN_INCOMPLETE`.

## 9. Compile the effort plan into P0

After the relevance values and design decisions are frozen:

```bash
python scripts/plan_pedicularis_context_screen_effort.py \
  PEDICULARIS_CONTEXT_SCREEN_EFFORT_FREEZE_FINAL.json \
  --output PEDICULARIS_CONTEXT_SCREEN_EFFORT_PLAN_V1.json

python scripts/compile_pedicularis_context_screen_effort.py \
  data/PEDICULARIS_CONTEXT_SCREEN_FREEZE_TEMPLATE_V1.json \
  PEDICULARIS_CONTEXT_SCREEN_EFFORT_PLAN_V1.json \
  --output PEDICULARIS_CONTEXT_SCREEN_FREEZE_COMPILED_V1.json
```

The compiler output remains:

```text
EFFORT_COMPILED_AWAITING_FINAL_P0_FREEZE.
```

A final prospective review/commit is still required before field-packet generation.

## 10. Current source status

```text
P0 effort equations:                     REGISTERED
pollinator flower-minute correction:     REGISTERED
external numeric transport gate:         REGISTERED
source-qualification validator:          REGISTERED
pollinator minimum relevant rate:        OPEN
predator minimum relevant prevalence:    FRESH CALIBRATION REQUIRED
water-positive minimum prevalence:       FRESH CALIBRATION REQUIRED
production P0 freeze:                    BLOCKED
real P0 screen:                          NOT EXECUTED.
```

The scientifically clean next action is a small, disjoint natural-history calibration at the candidate site unless an exact external pollinator rate can be recovered and independently transport-qualified.

## 11. Claim ceiling

```text
P0_EFFORT_AND_SOURCE_QUALIFICATION_ONLY
NO_CONTEXT_PASS
NO_G1_G2
NO_R_K_PHI.
```
