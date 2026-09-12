# Pedicularis P0 context-screen protocol v1

Status: **PROSPECTIVE / LOGISTICAL QUALIFICATION ONLY / NO G1-G5 CLAIM**.

## 1. Purpose

The same-system Pedicularis programme now has an end-to-end prospective path from Qz/Qp/Qg through G5. The first real-data decision is not a treatment effect. It is whether a focal population-season contains enough observable biological signal and enough flowering material to justify spending the independent calibration and qualification partitions.

P0 therefore asks only:

```text
is legitimate pollinator activity detectable?
is seed-predator attack/oviposition detectable?
is the cupulate-bract water state functional and measurable?
is there enough flowering-plant capacity to begin the disjoint calibration programme?
```

P0 does **not** ask whether conflict exists, whether pollen limitation is significant, or whether water defence has a causal effect.

## 2. Why zero detection is not a biological negative

The screen is a context-selection device. If a registered observation effort yields no legitimate pollinator visit or no predator attack, the result is:

```text
CONTEXT_UNINFORMATIVE_...
```

not:

```text
pollinators absent
predators absent
no conflict
Qg negative.
```

A low-signal context may be revisited under a newly frozen effort contract or replaced by a higher-signal population-season without creating a biological negative receipt.

## 3. Pollen limitation stays open at P0

The field-execution policy previously required pollen limitation to be “not obviously absent”. That wording is too easy to overinterpret. P0 v1 therefore freezes:

```text
pollen limitation = UNRESOLVED_UNTIL_QP_CALIBRATION
```

Natural pollen receipt can be recorded descriptively, but no P0 threshold on pollen limitation is allowed. The selective supplementation gate Qp remains the first place where pollination dependence is tested.

## 4. Detection effort is calculated, not guessed

The production P0 effort is derived prospectively under:

```text
docs/PEDICULARIS_CONTEXT_SCREEN_EFFORT_PLAN_V1.md
data/PEDICULARIS_CONTEXT_SCREEN_EFFORT_FREEZE_TEMPLATE_V1.json
data/PEDICULARIS_CONTEXT_SCREEN_EFFORT_SOURCE_LEDGER_V1.csv
scripts/plan_pedicularis_context_screen_effort.py
scripts/compile_pedicularis_context_screen_effort.py
```

The planner requires biologically / decision-justified minimum signals:

```text
minimum legitimate visit rate per minute
minimum predator-attack prevalence
minimum water-positive prevalence
```

plus desired detection probabilities and temporal-coverage rules.

It then converts those frozen inputs into:

```text
pollinator observation minutes and bouts
predator-screen flower count
water-state plant count.
```

The planner never chooses the minimum-relevance rates from P0 outcomes.

For pollinators the registered planning approximation is:

```text
P(no detection in T min) = exp(-lambda_min T).
```

For predator / water-state presence:

```text
P(no positive among n units) = (1-p_min)^n.
```

A completed zero remains context-uninformative at the declared detection resolution, not evidence of true absence.

## 5. Immediate calibration capacity and census stopping

Two already registered calibration cohorts are disjoint:

```text
Y-CAL   36 independent plants
D0-CAL  48 independent plants
```

Therefore the non-negotiable base capacity for completing both calibration cohorts in one population-season is:

```text
84 independent flowering plants.
```

P0 may freeze an additional prospective reserve fraction for losses / unavailable phenotype strata:

```text
required flowering capacity
= ceil(84 x [1 + reserve_fraction]).
```

The reserve may not be chosen after observing the site census.

The capacity census obeys the frozen stopping rule:

```text
STOP_AT_REQUIRED_CAPACITY_OR_EXHAUST_FOCAL_POPULATION.
```

Therefore:

```text
observed count >= required capacity
-> capacity resolved PASS; exhaustive census not required

observed count < required capacity
AND population_census_exhausted = true
-> CONTEXT_SIGNAL_PRESENT_CAPACITY_LIMITED, if signal gates pass

observed count < required capacity
AND census not exhausted
-> CONTEXT_SCREEN_INCOMPLETE; continue census.
```

A partial census may never be used to declare a capacity-limited context.

This is a capacity screen, not a claim that the P0 plant count is sufficient for later Qz/Qp/Qg, D0-confirmatory or G3-G5 effect partitions. Those retain their own independent sample-size contracts.

## 6. Historical source anchors

Published Pedicularis rex studies establish that field populations with the required biological ingredients have existed in the Hengduan Mountains system.

### Sun & Huang 2015, AoB PLANTS, doi:10.1093/aobpla/plv019

```text
six field populations sampled in the Hengduan Mountains
40-60 individuals tagged per population in the water-drainage experiment
bumblebee visitation observed
seed predation measured
water-filled cupulate bracts experimentally established as biologically relevant.
```

### Sun, Armbruster & Huang 2016, Annals of Botany, doi:10.1093/aob/mcw097

```text
14 populations surveyed
pollination-related traits measured across the geographic sample
seed predation/final seed production measured in 12 populations
seed-predator pressure varied geographically.
```

### Xia, Sun & Liu 2013, Biology Letters, doi:10.1098/rsbl.2013.0387

```text
Mt. Wufeng and Shangri-La Alpine Botanical Garden used as direct interaction field systems
pollination and predispersal seed predation measured
historical patch size ranged from 1 to 500 flowering plants in the 2011 system.
```

These papers justify **where to recover candidate populations and what signals to screen**. They do not make any historical site automatically qualified today. Historical sample sizes are explicitly forbidden as the sole source of a production P0 effort threshold.

Candidate contexts are tracked in:

```text
data/PEDICULARIS_CONTEXT_CANDIDATE_LEDGER_V1.csv
```

and remain historical candidates until fresh P0 admission.

## 7. Freeze sequence before screening

The execution order is:

```text
1. recover candidate population-season
2. qualify / freeze minimum-relevance signal inputs
3. run P0 effort planner
4. compile planned effort into the ordinary P0 screen template
5. review final P0 contract
6. fill final freeze metadata and commit it
7. set status = FROZEN_CANDIDATE
8. set frozen_before_screen_outcomes = true
9. only then generate the field packet.
```

The ordinary production freeze is:

```text
data/PEDICULARIS_CONTEXT_SCREEN_FREEZE_TEMPLATE_V1.json
```

Allowed source classes are:

```text
DOWNSTREAM_DESIGN_REQUIREMENT
INDEPENDENT_NATURAL_HISTORY_CALIBRATION
EXTERNAL_MATCHED_PRIMARY_SOURCE
COMBINED_PREDECLARED.
```

Forbidden shortcuts include historical n alone, post-hoc screen outcomes, non-significant P values and convenience alone.

## 8. Field packet

After the final freeze validates, generate:

```bash
python scripts/generate_pedicularis_context_screen_packet.py \
  PEDICULARIS_CONTEXT_SCREEN_FREEZE_V1.json \
  --output PEDICULARIS_CONTEXT_SCREEN_FIELD_V1.csv
```

It contains:

```text
1 census row
registered pollinator-observation bout rows
registered predator-screen flower rows
registered water-state plant rows.
```

The census row records whether the focal population has been exhausted when required capacity has not been reached.

Every row is permanently:

```text
screen_only = true
confirmatory_eligible = false.
```

## 9. Summarize and adjudicate

After collection:

```bash
python scripts/summarize_pedicularis_context_screen_packet.py \
  PEDICULARIS_CONTEXT_SCREEN_FIELD_V1.csv \
  --output PEDICULARIS_CONTEXT_SCREEN_RECEIPT_V1.json

python scripts/adjudicate_pedicularis_context_screen.py \
  PEDICULARIS_CONTEXT_SCREEN_RECEIPT_V1.json \
  PEDICULARIS_CONTEXT_SCREEN_FREEZE_V1.json
```

The possible operational outputs are:

```text
CONTEXT_SCREEN_PASS_CALIBRATION_READY
CONTEXT_SIGNAL_PRESENT_CAPACITY_LIMITED
CONTEXT_UNINFORMATIVE_POLLINATOR_LOW
CONTEXT_UNINFORMATIVE_PREDATOR_LOW
CONTEXT_UNINFORMATIVE_WATER_STATE
CONTEXT_UNINFORMATIVE_MULTIPLE_SIGNALS
CONTEXT_SCREEN_INCOMPLETE.
```

Only the first status unlocks the default Y-CAL/D0-CAL programme in that population-season.

Signal-effort completion and capacity-census resolution are reported separately. Thus a site can retain completed signal information while requiring further census effort.

## 10. Relocation rule

For a fully observed low-signal context:

```text
retain P0 receipt
label context uninformative for the current causal programme
no biological negative claim
screen the next candidate population-season.
```

This implements the existing rule that near-zero predator pressure is not a negative Qg result.

## 11. Current state

```text
P0 field packet / adjudicator:          REGISTERED
P0 detection-effort planner:            REGISTERED
P0 capacity-census stopping rule:       REGISTERED
historical candidate-source ledgers:    REGISTERED
production minimum-relevance rates:     OPEN
final production P0 freeze:             NOT YET FROZEN
P0 biological receipt:                  NOT EXECUTED
```

The immediate task is no longer to invent a screen sample size. It is to qualify the minimum-relevance inputs in `PEDICULARIS_CONTEXT_SCREEN_EFFORT_SOURCE_LEDGER_V1.csv`, freeze them prospectively, and then let the planner determine the effort.

No real Pedicularis G1-G5 receipt is created by this protocol.
