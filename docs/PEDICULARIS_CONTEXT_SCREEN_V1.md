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

A low-signal context may be revisited with more effort or replaced by a higher-signal population-season without creating a biological negative receipt.

## 3. Pollen limitation stays open at P0

The field-execution policy previously required pollen limitation to be “not obviously absent”. That wording is too easy to overinterpret. P0 v1 therefore freezes:

```text
pollen limitation = UNRESOLVED_UNTIL_QP_CALIBRATION
```

Natural pollen receipt can be recorded descriptively, but no P0 threshold on pollen limitation is allowed. The selective supplementation gate Qp remains the first place where pollination dependence is tested.

## 4. Immediate calibration capacity

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

This is a capacity screen, not a claim that 84 plants are sufficient for the later Qz/Qp/Qg, D0-confirmatory or G3-G5 effect partitions. Those retain their own independent sample-size contracts.

## 5. Historical source anchors

Two published Pedicularis rex studies establish that multiple field populations with the required biological ingredients have existed in the Hengduan Mountains system:

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

These papers justify **where to recover candidate historical populations and what signals to screen**. They do not make any historical site automatically qualified today. Historical sample sizes are explicitly forbidden as the sole source of a production P0 effort threshold.

Exact historical site names / coordinates belong to the supplementary Table S1 source recovery. Until fresh access, flowering phenology and signal are verified, they remain `HISTORICAL_CANDIDATE_ONLY`.

## 6. Freeze before screening

Fill and commit:

```text
data/PEDICULARIS_CONTEXT_SCREEN_FREEZE_TEMPLATE_V1.json
```

The production freeze must specify:

```text
candidate_site_id
population_id
season_id
screen_window_id
registered observation-effort floors
presence / relevance thresholds
capacity reserve fraction
source and rationale for every threshold / effort floor.
```

Allowed source classes are:

```text
DOWNSTREAM_DESIGN_REQUIREMENT
INDEPENDENT_NATURAL_HISTORY_CALIBRATION
EXTERNAL_MATCHED_PRIMARY_SOURCE
COMBINED_PREDECLARED.
```

Forbidden shortcuts include historical n alone, post-hoc screen outcomes, non-significant P values and convenience alone.

## 7. Field packet

After the freeze is valid, generate the screen packet:

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

Every row is permanently:

```text
screen_only = true
confirmatory_eligible = false.
```

## 8. Summarize and adjudicate

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

## 9. Relocation rule

For a fully observed low-signal context:

```text
retain P0 receipt
label context uninformative for the current causal programme
no biological negative claim
screen the next candidate population-season.
```

This implements the existing rule that near-zero predator pressure is not a negative Qg result.

## 10. Current state

```text
P0 DESIGN: REGISTERED
P0 BIOLOGICAL RECEIPT: NOT EXECUTED
CURRENT ACTION: recover candidate population access + freeze P0 effort/threshold sources + run fresh context screen
```

No real Pedicularis G1-G5 receipt is created by this protocol.
