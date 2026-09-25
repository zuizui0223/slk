# Pedicularis P0 context-screen protocol v1

Status: **PROSPECTIVE / SOURCE-GATED / LOGISTICAL QUALIFICATION ONLY / NO G1-G5 CLAIM**.

## 1. Purpose

The first real-data decision in the same-system `Pedicularis rex` programme is whether one focal population-season contains enough observable interaction signal and enough flowering material to justify spending the independent calibration and qualification partitions.

P0 asks only:

```text
is legitimate pollinator activity detectable at registered exposure?
is early seed-predator attack / oviposition detectable?
is a functional cupulate-bract water state detectable?
is there enough flowering-plant capacity to begin the disjoint calibration programme?
```

P0 does **not** ask whether conflict exists, whether pollen limitation is significant, or whether water defence has a causal effect.

## 2. Zero detection is not a biological negative

P0 is a context-selection device. A completed low-signal screen yields:

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

A low-signal context may be retained as a low-interaction context and the causal programme relocated without creating a negative G1/G2 receipt.

## 3. Pollen limitation remains open

P0 freezes:

```text
pollen limitation = UNRESOLVED_UNTIL_QP_CALIBRATION.
```

Natural pollen receipt may be recorded descriptively, but selective supplementation Qp remains the first gate that can establish manipulable pollination dependence.

## 4. Biological minimum-relevance values require qualification

The P0 effort planner needs three biological numeric inputs:

```text
pollinator
    minimum legitimate visit rate per flower-minute

predator
    minimum early attacked-flower / oviposition-positive prevalence

water state
    minimum water-positive flowering-plant prevalence.
```

They cannot be inferred from convenience, historical sample size, a non-significant P value, or the P0 outcomes themselves.

Canonical audit:

```text
docs/PEDICULARIS_P0_RELEVANCE_SOURCE_ADJUDICATION_V1.md
data/PEDICULARIS_P0_RELEVANCE_SOURCE_ADJUDICATION_V1.csv
```

Current audit result:

```text
pollinator method / denominator: matched after flower-minute correction
pollinator external exact numeric minimum: OPEN
predator external numeric prevalence: NOT QUALIFIED; endpoint mismatch
water external numeric prevalence: NOT QUALIFIED; prevalence denominator absent.
```

A production numeric value must pass:

```text
data/PEDICULARIS_P0_RELEVANCE_QUALIFICATION_TEMPLATE_V1.json
scripts/validate_pedicularis_p0_relevance_qualification.py
```

Allowed qualification routes are:

```text
EXTERNAL_NUMERIC_TRANSPORT
FRESH_INDEPENDENT_CALIBRATION.
```

External values require endpoint, unit/denominator and focal-context transport to be explicitly qualified. Fresh calibration units must be disjoint from P0 decision units and downstream confirmatory units.


For plant/flower-based predator and water units this disjointness is executable: fresh calibration emits a permanent-tag firewall, the final P0 freeze hash-locks it, and the screen adjudicator rejects any reused `physical_plant_tag`. Pollinator disjointness is temporal at the registered bout level.

## 4a. Permission scope and field dates

The WAVE1 non-destructive permission contract covers:

```text
RECOVERY_PLUS_P0A_PLUS_P0B_NONDESTRUCTIVE
```

with required activities:

```text
A visual observation
B photography / morphology documentation
C non-destructive measurement.
```

The confirmed permission-scope receipt is carried automatically from recovery through P0a source qualification and effort planning into the final P0b freeze. The final freeze must declare:

```text
candidate_id
planned_screen_start_date
planned_screen_end_date
permission_scope_receipt.
```

The entire planned screen interval must lie inside at least one positive regulatory and site validity interval for every A-C activity.

Every completed P0b field row, including the capacity census, records `observation_date`. The packet receipt records the completed-date range, and final adjudication requires that range to lie inside the prospectively frozen screen interval.

Thus neither a valid P0a permission nor a once-valid P0b permission can be reused after expiry.

## 5. Pollinator exposure uses flower-minutes

Sun & Huang (2015) estimated `P. rex` visitation using 30-min plot censuses and normalized flower visits by the number of simultaneously open flowers. Therefore the P0 exposure unit is:

```text
flower-minutes
= observed minutes x simultaneously open focal P. rex flowers.
```

The field packet records, for every pollinator bout:

```text
planned_observation_minutes
observed_observation_minutes
simultaneously_open_focal_flowers
legitimate_pollinator_visits.
```

Temporal coverage is not satisfied by total clock time alone. The final freeze carries the prospectively planned `minimum_pollinator_minutes_per_bout`; at least the frozen number of bouts must each meet that duration. One long bout cannot compensate for several near-zero bouts.

The summary calculates:

```text
cumulative flower-minutes
legitimate visits / flower-minute.
```

Raw visits per minute are not the registered P0 rate.

## 6. Detection effort is calculated, not guessed

After the biological minimum-relevance inputs qualify, freeze the remaining design decisions:

```text
desired detection probabilities
pollinator temporal-bout coverage
capacity reserve fraction.
```

Then use:

```text
docs/PEDICULARIS_CONTEXT_SCREEN_EFFORT_PLAN_V1.md
data/PEDICULARIS_CONTEXT_SCREEN_EFFORT_FREEZE_TEMPLATE_V1.json
scripts/plan_pedicularis_context_screen_effort.py
scripts/compile_pedicularis_context_screen_effort.py
```

### Pollinator

For minimum rate `lambda_min` per flower-minute and required detection probability `q`:

```text
P(no visit after E flower-minutes) = exp(-lambda_min E)
E_required = ceil[-log(1-q) / lambda_min].
```

P0 must satisfy all of:

```text
minimum total clock time
minimum number of temporal bouts
minimum duration for each qualifying bout
minimum cumulative flower-minute exposure.
```

### Predator / water

For minimum prevalence `p_min`:

```text
P(no positive among n units) = (1-p_min)^n
n = ceil[log(1-q) / log(1-p_min)].
```

The planner chooses effort, not biological relevance thresholds.

## 7. Immediate calibration capacity and census stopping

The disjoint base calibration cohorts require:

```text
Y-CAL   36 independent plants
D0-CAL  48 independent plants
base    84 independent flowering plants.
```

With prospectively frozen reserve fraction `r`:

```text
required capacity = ceil[84(1+r)].
```

Census rule:

```text
STOP_AT_REQUIRED_CAPACITY_OR_EXHAUST_FOCAL_POPULATION.
```

Thus:

```text
count >= required capacity
-> capacity PASS; exhaustive census unnecessary

count < required capacity AND focal population exhausted
-> capacity-limited context

count < required capacity AND census not exhausted
-> P0 incomplete; continue census.
```

A partial low count may never be promoted to `CONTEXT_SIGNAL_PRESENT_CAPACITY_LIMITED`.

## 8. Historical anchors are candidate sources, not current passes

Published `P. rex` work provides useful scouting anchors:

```text
Sun & Huang 2015
    direct bumblebee visitation method
    experimental water-defence reality
    geographically variable seed predation

Sun, Armbruster & Huang 2016
    14 populations
    geographic mosaic in seed-predator pressure

Xia et al. 2013
    direct Shangri-La interaction systems
    density / patch-size dependence of predation.
```

These sources guide candidate recovery and source adjudication. They do not automatically qualify a current population-season or provide a production P0 number.

Candidate contexts are tracked in:

```text
data/PEDICULARIS_CONTEXT_CANDIDATE_LEDGER_V1.csv
```

## 9. Prospective freeze sequence

The correct order is:

```text
1. recover candidate population-season
2. qualify the three biological minimum-relevance inputs
3. compile qualified values into the P0 effort-freeze template
4. freeze detection probabilities / temporal coverage / capacity reserve
5. run P0 effort planner
6. compile effort into ordinary P0 screen freeze
7. review, commit and mark final P0 freeze prospective
8. only then generate the field packet.
```

Qualified biology can be compiled with:

```bash
python scripts/compile_pedicularis_p0_relevance_into_effort_freeze.py \
  data/PEDICULARIS_CONTEXT_SCREEN_EFFORT_FREEZE_TEMPLATE_V1.json \
  PEDICULARIS_P0_RELEVANCE_QUALIFICATION_FILLED.json \
  --output PEDICULARIS_CONTEXT_SCREEN_EFFORT_RELEVANCE_COMPILED.json
```

No P0 observations may be opened before the final contracts are frozen.

## 10. Field packet

After the final P0 freeze validates:

```bash
python scripts/generate_pedicularis_context_screen_packet.py \
  PEDICULARIS_CONTEXT_SCREEN_FREEZE_V1.json \
  --output PEDICULARIS_CONTEXT_SCREEN_FIELD_V1.csv
```

It contains:

```text
1 capacity-census row
registered pollinator-observation bout rows
registered predator-screen flower rows
registered water-state plant rows.
```

Completed predator observations must refer to unique `plant_id + flower_id` units. Completed water-state observations must refer to unique plant IDs. Repeating the same biological unit under several record IDs does not increase registered detection effort.

Every row is permanently:

```text
screen_only = true
confirmatory_eligible = false.
```

## 11. Summarize and adjudicate

After field collection:

```bash
python scripts/summarize_pedicularis_context_screen_packet.py \
  PEDICULARIS_CONTEXT_SCREEN_FIELD_V1.csv \
  --output PEDICULARIS_CONTEXT_SCREEN_RECEIPT_V1.json

python scripts/adjudicate_pedicularis_context_screen.py \
  PEDICULARIS_CONTEXT_SCREEN_RECEIPT_V1.json \
  PEDICULARIS_CONTEXT_SCREEN_FREEZE_V1.json
```

Possible operational outcomes:

```text
CONTEXT_SCREEN_PASS_CALIBRATION_READY
CONTEXT_SIGNAL_PRESENT_CAPACITY_LIMITED
CONTEXT_UNINFORMATIVE_POLLINATOR_LOW
CONTEXT_UNINFORMATIVE_PREDATOR_LOW
CONTEXT_UNINFORMATIVE_WATER_STATE
CONTEXT_UNINFORMATIVE_MULTIPLE_SIGNALS
CONTEXT_SCREEN_INCOMPLETE.
```

Only the first unlocks the default calibration programme in that population-season.

## 12. Current state

```text
P0 field packet / adjudicator:             REGISTERED
pollinator flower-minute exposure:         REGISTERED
P0 detection-effort planner:               REGISTERED
P0 source qualification validator:         REGISTERED
external numeric transport gate:           REGISTERED
pollinator production minimum rate:        OPEN
predator production minimum prevalence:    FRESH CALIBRATION REQUIRED
water production minimum prevalence:       FRESH CALIBRATION REQUIRED
final production P0 freeze:                BLOCKED
P0 biological receipt:                     NOT EXECUTED.
```

The cleanest next empirical action is a **small disjoint natural-history calibration at the candidate population** unless an exact pollinator source value can be recovered and transport-qualified.

## 13. Claim ceiling

```text
P0_CONTEXT_AND_SOURCE_QUALIFICATION_ONLY
NO_G1_G2
NO_R_K_PHI.
```


## 14. Incomplete-row audit

The context-screen packet summary never silently drops an unfinished registered row.

For pollinator, predator, water-state and capacity-census records, the packet receipt reports:

```text
registered rows
completed rows
incomplete rows
incomplete reason counts
record-level incomplete details.
```

The distinction from fresh calibration is deliberate.

For P0 context screening, biological signal is judged only after the **completed** units satisfy the prospectively frozen minimum effort. Therefore an extra unfinished row does not automatically invalidate a screen that still meets every registered effort floor.

However the final adjudication carries

```text
missingness_sensitivity_required = true
```

whenever incomplete registered records exist. Missingness therefore remains visible and auditable.

If missingness causes any pollinator, predator, water-state or capacity effort floor to remain unmet, the only permitted status is `CONTEXT_SCREEN_INCOMPLETE`. It may not be reinterpreted as low biological signal.


## 15. Packet-integrity rules

Before signal classification, the packet summary and adjudicator verify:

```text
registered record types only
integer biological count variables
pollinator bout details reconcile with aggregate minutes, flower-minutes and visits
the frozen minimum number of bouts each meet the frozen minimum duration
predator flower units are unique
water-state plant units are unique
registered/completed packet counts agree with the effort receipt.
```

A packet that violates these bookkeeping or biological-unit rules fails closed. These checks protect the prospective detection guarantees; they do not create new biological thresholds.
