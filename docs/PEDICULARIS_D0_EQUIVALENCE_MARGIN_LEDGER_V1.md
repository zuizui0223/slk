# Pedicularis D0 equivalence-margin ledger v1

Status: **PROSPECTIVE / MARGIN-SOURCE CONTRACT / NO NUMERIC BIOLOGICAL MARGINS FROZEN YET**.

## 1. Purpose

The structural-y / D0 programme now has a registered pilot and a prospective precision planner. The remaining bottleneck is not variance estimation. It is deciding what biological difference is small enough to count as equivalent at each D0 gate.

This document separates two objects that must never be conflated:

```text
BIOLOGICAL / DECISION MARGIN
    how large a difference can be while preserving the intended biological interpretation

CALIBRATION VARIANCE
    how noisy the endpoint is, used to determine the confirmatory sample size
```

The margin determines the scientific claim. The pilot SD/ICC determines how many independent plants are needed to test that claim.

Therefore the programme forbids rules of the form

```text
margin = c x pilot SD
margin = c x observed confirmatory SD
```

unless `c x SD` is independently justified as a biological or decision-invariance bound. A noisier endpoint must not automatically receive a looser definition of equivalence.

## 2. General freeze rule

Every production margin or minimum-effect threshold must be frozen before confirmatory D0 outcomes are opened and must include:

```text
endpoint_id
gate
comparison
units
criterion_type
numeric_value
margin_basis
biological_rationale
source_type
source_reference
calibration_dataset_id, if used
confirmatory_outcomes_opened = false
variance_only_basis = false
frozen_before_confirmatory_outcomes = true
```

The corresponding pilot SD, paired-difference SD, or ICC is recorded separately and may enter only the precision planner.

## 3. Allowed margin-source classes

### A. DESIGN_INVARIANCE

The endpoint has a registered geometry or state-classification boundary that must not be crossed.

Examples:

```text
D0-induced z shift must not move a flower across the registered exsertion-level assignment;
S, D0 and D must use the same declared reproductive time horizon.
```

### B. FUNCTIONAL_INVARIANCE

Independent calibration maps a physical perturbation onto a biological function. The margin is the largest perturbation that keeps that function inside a predeclared negligible-effect region.

Examples:

```text
opening-width shift -> pollinator entry/contact probability;
retention-duration mismatch -> predicted antagonist protection;
stigma-position shift -> pollen receipt.
```

### C. DOWNSTREAM_DECISION_INVARIANCE

The margin is the largest nuisance effect that cannot change a registered downstream classification or minimum effect of interest under a prospectively declared sensitivity analysis.

Examples:

```text
apparatus burden bound small enough that the planned K/Phi classification cannot be reversed;
pollination cross-effect small enough that it cannot explain the registered D0-D benefit match.
```

### D. EXTERNAL_BIOLOGICAL_BOUND

A directly relevant published experiment or independent external dataset supplies a biological bound under a sufficiently matched endpoint and context.

Historical sample sizes and non-significant P-values are not bounds. The current `P. rex` literature is primarily a scale and feasibility anchor rather than a ready-made D0 equivalence source.

### E. COMBINED_PREDECLARED

The final margin is the most restrictive of multiple independently justified bounds, for example:

```text
margin_z = min(design-preservation ceiling, pollinator-function ceiling).
```

Every component must be documented separately.

## 4. Forbidden margin sources

The validator rejects or blocks promotion when the margin is based only on:

```text
PILOT_SD_MULTIPLE_ONLY
CONFIRMATORY_SD_MULTIPLE
NONSIGNIFICANT_P_VALUE
HISTORICAL_SAMPLE_SIZE
OBSERVED_CONFIRMATORY_EFFECT
POSTHOC_SIGN_PRESERVATION
CONVENIENCE_OR_FIELD_CAPACITY_ONLY
```

Pilot variability can reveal that an endpoint is too noisy to test a biologically meaningful margin. The response is a larger confirmatory sample, a better measurement, or a failed route -- not widening the margin until the endpoint passes.

## 5. D0-Q1 geometry / coordinate preservation

### Q1a. Realized exsertion z

Comparison:

```text
D0_CAL - SHAM_CAL
```

Primary margin source:

```text
DESIGN_INVARIANCE + FUNCTIONAL_INVARIANCE
```

The frozen z margin must satisfy both:

1. it is smaller than the registered coordinate-preservation ceiling implied by the frozen adjacent-z spacing / treatment assignment;
2. independent pollinator-handling calibration does not predict a biologically meaningful change within that shift.

The pilot paired-difference SD(z) determines n only.

Current readiness:

```text
NUMERIC_MARGIN = BLOCKED
requires Qz spacing freeze + focal manipulation/pollinator calibration.
```

### Q1b. Corolla opening width

Margin source:

```text
FUNCTIONAL_INVARIANCE
```

Use independent sham/manipulation calibration to map opening-width changes onto pollinator entry, handling, stigma contact, or pollen receipt. Freeze the largest change still inside the pollination-neutral region.

Measurement repeatability defines whether that margin is resolvable, not the margin itself.

### Q1c. Stigma position

Margin source:

```text
FUNCTIONAL_INVARIANCE
```

Freeze from the relationship between stigma displacement and legitimate contact / pollen receipt. If no focal sensitivity calibration can be recovered, the endpoint remains `REQUIRED_BEFORE_USE`.

### Q1d. Flower orientation

Margin source:

```text
FUNCTIONAL_INVARIANCE
```

Freeze from a focal handling/contact sensitivity calibration or an external biological bound that is demonstrably transportable to the focal floral geometry.

### Q1e. Mechanical damage

Criterion is an off-target contamination ceiling rather than a zero-effect test.

Preferred source:

```text
DOWNSTREAM_DECISION_INVARIANCE
```

The allowed damage difference must be small enough that plausible damage-associated reproductive loss cannot account for the D0 benefit or burden contrast.

## 6. D0-Q2 functional-benefit matching

D0 and natural D do not need identical physical morphology. They must deliver the same registered y-mediated functional benefit closely enough that `D0 -> D` isolates architecture debit rather than unequal recovered benefit.

### Q2a. Retained-water magnitude

Endpoints may include:

```text
maximum retained volume
standardized water depth
```

Primary source:

```text
FUNCTIONAL_INVARIANCE
```

The preferred derivation is:

```text
physical y mismatch
-> independently calibrated change in protection
-> largest mismatch whose protection effect stays within the frozen protection-equivalence budget.
```

A fixed fraction of the natural HIGH-Y minus LOW-Y contrast may be used only if that fraction itself has a predeclared biological justification.

### Q2b. Retention duration / half-life

Primary source:

```text
FUNCTIONAL_INVARIANCE
```

The margin must reflect overlap with the antagonist attack window. Equal mean water volume with a materially shorter protection duration is not equivalent.

### Q2c. Protected vulnerable-region fraction

Primary source:

```text
FUNCTIONAL_INVARIANCE
```

Freeze using the relationship between protected ovary/corolla-base coverage and early attack / oviposition / viable-seed loss.

### Q2d. Protection outcome

Where direct early-attack or predation outcomes are sufficiently selective, a biological equivalence margin may also be frozen directly on the protection scale.

This is often the most interpretable Q2 criterion because it compares D0 and D at the function that y is intended to recover.

Current literature note:

The registered 2015 `P. rex` water-defence experiment establishes that drainage altered seed predation and final seed set while showing no detected pollinator/initial-seed-set treatment effect. Those coefficients establish biological relevance of the y axis, but the non-significant effects are not production equivalence margins.

## 7. D0-Q3 pollination-facing neutrality

The D0 apparatus must not create an attraction or handling benefit/cost that natural structural y does not have.

Priority endpoints:

```text
legitimate visit rate/probability
handling time
stigma contact
pollen receipt
initial seed set
```

Preferred margin source:

```text
FUNCTIONAL_INVARIANCE or DOWNSTREAM_DECISION_INVARIANCE
```

Two admissible derivations are:

### Route Q3-F

Map the endpoint onto pollination function and freeze the largest D0-SHAM difference that leaves predicted pollination function inside a negligible-effect region.

### Route Q3-D

Freeze a maximum pollination contamination effect whose worst-case contribution cannot explain the registered D0-D protection/fitness benefit or alter the intended R/K interpretation.

The historical near-zero pollinator-visit and initial-seed-set coefficients are background evidence only. `P > 0.05` is not neutrality.

## 8. D0-Q4 antagonist-channel fidelity

D0 must protect through water retention rather than by physically blocking the seed predator.

This gate has two complementary thresholds.

### Q4a. Wet-channel efficacy

Criterion type:

```text
MINIMUM_USEFUL_EFFECT
```

Source:

```text
BIOLOGICAL_RELEVANCE + INDEPENDENT_CALIBRATION
```

Freeze the smallest retention-mediated reduction in early attack/predation that is large enough to qualify the D0 benefit channel.

### Q4b. Dry-device physical-exclusion residual

Criterion type:

```text
EQUIVALENCE / CONTAMINATION BOUND
```

Source:

```text
FUNCTIONAL_INVARIANCE or DOWNSTREAM_DECISION_INVARIANCE
```

Under a dry/non-retaining device state, the physical structure must not reduce antagonist access beyond the frozen contamination margin. A large dry-device effect means D0 is a barrier treatment, not an externalized water-retention comparator.

## 9. D0-Q5 apparatus burden

Q5 has two admissible lanes and should not be forced into a single zero-burden equivalence test.

### Lane Q5-E: negligible burden

Use a prospective equivalence margin on

```text
B_device = W(S) - W(SHAM)
```

where the margin comes from downstream decision invariance: a burden smaller than this value cannot materially alter the intended K/Phi resolution.

### Lane Q5-A: measured adjustment

A non-negligible burden is allowed if it is independently estimated and explicitly corrected/bounded. In this lane the key freeze is a **precision target**, not a zero-burden margin:

```text
maximum CI half-width for B_device
```

The half-width must be small enough that burden uncertainty cannot dominate the minimum K/Phi effect the experiment is intended to resolve.

The production receipt must declare which lane was selected before confirmatory outcomes are opened.

## 10. D0-Q6 common horizon

This is an identity requirement, not an equivalence test.

```text
S horizon == D0 horizon == D horizon
```

Preferred registered horizon:

```text
focal flower at treatment assignment -> mature viable undamaged seeds.
```

No numerical tolerance is permitted unless a separate time-horizon bridge is prospectively registered.

## 11. Margin ledger

| ID | Gate | Endpoint | Criterion | Preferred source | Current readiness |
|---|---|---|---|---|---|
| `D0_Q1_Z` | Q1 | realized exsertion | equivalence | DESIGN + FUNCTIONAL invariance | blocked: Qz spacing + sensitivity |
| `D0_Q1_OPENING` | Q1 | corolla opening | equivalence | FUNCTIONAL invariance | calibration required |
| `D0_Q1_STIGMA` | Q1 | stigma position | equivalence | FUNCTIONAL invariance | calibration required |
| `D0_Q1_ORIENTATION` | Q1 | flower orientation | equivalence | FUNCTIONAL invariance | calibration required |
| `D0_Q1_DAMAGE` | Q1 | damage rate | contamination bound | DECISION invariance | calibration + consequence bound |
| `D0_Q2_VOLUME` | Q2 | retained volume/depth | equivalence | FUNCTIONAL invariance | y/protection calibration required |
| `D0_Q2_DURATION` | Q2 | retention duration | equivalence | FUNCTIONAL invariance | attack-window calibration required |
| `D0_Q2_COVERAGE` | Q2 | protected fraction | equivalence | FUNCTIONAL invariance | protection calibration required |
| `D0_Q2_PROTECTION` | Q2 | early attack/predation | equivalence | FUNCTIONAL invariance | biological margin required |
| `D0_Q3_VISIT` | Q3 | visitation | equivalence | FUNCTIONAL / DECISION invariance | calibration required |
| `D0_Q3_POLLEN` | Q3 | pollen receipt | equivalence | FUNCTIONAL / DECISION invariance | calibration required |
| `D0_Q3_INITIAL_SEED` | Q3 | initial seed set | equivalence | DECISION invariance | calibration required |
| `D0_Q4_WET_EFFECT` | Q4 | retention-mediated protection | minimum effect | BIOLOGICAL relevance + calibration | unresolved |
| `D0_Q4_DRY_RESIDUAL` | Q4 | dry-device attack effect | contamination equivalence | FUNCTIONAL / DECISION invariance | unresolved |
| `D0_Q5_BURDEN_EQ` | Q5 | sham burden | equivalence, lane E | DECISION invariance | unresolved |
| `D0_Q5_BURDEN_PRECISION` | Q5 | sham burden CI half-width | precision, lane A | DECISION resolution | unresolved |
| `D0_Q6_HORIZON` | Q6 | time horizon | exact identity | DESIGN invariance | definition ready |

## 12. Interaction with the precision planner

The workflow is deliberately one-way:

```text
independent biology / decision logic
        -> freeze margin or minimum useful effect

independent Y-CAL / D0-CAL
        -> estimate SD / paired-difference SD / ICC

margin + SD
        -> plan_pedicularis_y_d0_precision.py
        -> confirmatory independent-plant n
```

The planner may never write or revise the margin.

## 13. Freeze-readiness status

As of this version:

```text
numeric biological equivalence margins directly recoverable from literature: 0
exact identity requirements ready now:                                      1 (Q6)
margin derivations structurally specified:                                  Q1-Q5
pilot variance design registered:                                           YES
confirmatory outcome peeking permitted:                                     NO
```

This is progress rather than a failure: the programme now knows exactly which information the pilot may estimate and which scientific judgments must come from biology/decision logic instead of variance.

## 14. Promotion rule

A D0 margin manifest can become `FROZEN_FOR_CONFIRMATORY_USE` only when:

```text
all required numeric margins/effects are non-null;
all have allowed source types;
no margin uses variance-only justification;
all calibration sources are independent of confirmatory units;
Q5 lane is prospectively declared;
Q6 horizon identity is frozen;
confirmatory outcomes remain unopened;
manifest is committed and validated before confirmatory analysis.
```

Until then, `D0` remains a qualification programme and cannot point-identify structural G4 `K`.
