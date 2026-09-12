# SLK Pedicularis field-qualification execution policy v1

Status: **PROSPECTIVE / EXECUTION ORDER FROZEN**.

This document operationalizes the first biological SLK bottleneck identified by the G1-G9 ledger: obtaining a valid `Pedicularis rex` G2 conflict-budget receipt without circularly reusing the Chapter-2 water-defence axis.

It does not replace the SCH evaluators. SCH remains the source of truth for the three qualification receipts and the full causal surface. SLK only freezes the execution logic, promotion order, and stop rules needed for the flagship.

## 0. Fresh P0 context screen before expensive calibration

Before threshold calibration or Qz/Qp/Qg method qualification, the focal population-season must pass the registered P0 context screen:

```text
docs/PEDICULARIS_CONTEXT_SCREEN_V1.md
data/PEDICULARIS_CONTEXT_SCREEN_FREEZE_TEMPLATE_V1.json
scripts/generate_pedicularis_context_screen_packet.py
scripts/summarize_pedicularis_context_screen_packet.py
scripts/adjudicate_pedicularis_context_screen.py
```

The required operational status for the default route is:

```text
CONTEXT_SCREEN_PASS_CALIBRATION_READY.
```

P0 checks only fresh legitimate-pollinator activity, measurable predator exposure/early attack, functional cupulate-bract water state and enough flowering-plant capacity for the disjoint calibration programme.

Pollen limitation is **not** a P0 pass criterion. It remains:

```text
UNRESOLVED_UNTIL_QP_CALIBRATION.
```

A completed low-signal P0 screen is an uninformative context for the current causal programme, not a biological negative.

## 1. Mandatory threshold freeze before qualification

The Qz/Qp/Qg source evaluators are implemented, but their production config templates still contain `REQUIRED_BEFORE_USE` placeholders.

Therefore no qualification analysis may begin until the prospective threshold manifest passes:

```text
scripts/validate_pedicularis_threshold_freeze.py
```

using:

```text
data/PEDICULARIS_THRESHOLD_FREEZE_TEMPLATE_V1.json
```

under `docs/PEDICULARIS_THRESHOLD_FREEZE_PROTOCOL_V1.md`.

Calibration units used to set tolerances, timing windows, variance assumptions, or sample floors must be disjoint from the confirmatory qualification units used to decide Qz/Qp/Qg.

## 2. Required qualification receipts

The corrected Pedicularis V2 path requires three independent source receipts from the same population and season:

```text
Qz  SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1
    status = PEDICULARIS_Z_MANIPULATION_VALIDATED

Qp  SCH_PEDICULARIS_POLLINATION_WEIGHT_V1
    status = PEDICULARIS_POLLINATION_WEIGHT_VALIDATED

Qg  SCH_PEDICULARIS_PREDATOR_METHOD_V3
    status = PEDICULARIS_PREDATOR_METHOD_VALIDATED
```

Only after all three pass may SCH assemble:

```text
SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3
```

and run the V2 `z x P x G` causal surface.

## 3. Biological meanings of the three gates

### Qz — manipulate the shared coordinate without changing another coordinate

Target:

```text
z = realized corolla exsertion above the cupulate bract.
```

The manipulation must create at least the prospectively frozen number of ordered, separated realized-z levels while keeping off-target floral geometry, water depth, and handling damage within bounds.

Passing Qz means only that exsertion is experimentally manipulable. It does not establish conflict.

### Qp — manipulate pollination dependence while flowers remain open

Registered contrast:

```text
P1 = NATURAL
P0 = SUPPLEMENTED with standardized donor-mixed cross-pollen.
```

The intervention must increase pollen receipt and the preregistered pollen-limitation endpoint while leaving early predator attack, exsertion, bract geometry, water state, and handling damage within tolerance.

Passing Qp means only that pollination weight can be manipulated selectively.

### Qg — independently manipulate seed-predator pressure

Registered target:

```text
G0 = PREDATOR_EXCLUDED
G1 = PREDATOR_EXPOSED
```

with water defence held fixed.

The preferred first method-development route is a timed post-pollination lower-flower / fruit sleeve. The method must reduce early attack and later predation, improve final intact seed set, and preserve initial seed set, pollen receipt, pollinator visitation, realized z, water state, and handling integrity.

The exclusion device must be applied only in the registered post-pollination / pre-ovary-swelling timing window and must not cover the pollinator-entry zone.

Passing Qg establishes a method-qualified independent antagonist intervention, not conflict.

## 4. Logical execution order

For inference, the gates are conjunctive:

```text
P0_CONTEXT_SCREEN_PASS
AND THRESHOLDS_FROZEN
AND Qz
AND Qp
AND Qg
-> FULL_SURFACE_READY.
```

No biological Q gate is logically upstream of another.

For field-resource allocation, however, SLK freezes the following priority:

```text
0. fresh P0 context screen
1. independent calibration + threshold freeze
2. Qg predator-method qualification
3. Qz multi-level exsertion manipulation
4. Qp pollination-weight supplementation
5. assemble readiness
6. run the full V2 surface
```

Reason: P0 prevents spending calibration effort in a context with no detectable interaction signal or insufficient plant supply. Qg remains the least established causal method and the most likely to kill the same-species SCH -> BITA route once a context is admitted.

## 5. Operational field rule: parallel pilots are allowed

The logical priority above does **not** require waiting for laboratory analysis between every pilot during a short flowering season.

If flower supply permits, Qg, Qz and Qp may be run in parallel on disjoint flowers / plants within the same population and season, provided that:

```text
- P0 has already admitted the context;
- assignments are independent;
- no flower contributes to more than one pilot;
- calibration units do not enter qualification tests;
- each pilot retains its own raw-data contract;
- all thresholds/configs are frozen before opening qualification outcomes;
- the full V2 surface is not started until all three receipts pass.
```

This preserves inference while reducing the risk of losing an entire flowering season to sequential waiting.

## 6. Context-screen stop and reroute rules

### P0 effort incomplete

```text
CONTEXT_SCREEN_INCOMPLETE
-> complete the registered effort
-> no low-signal interpretation yet.
```

### P0 pollinator / predator / water signal below threshold after full effort

```text
CONTEXT_UNINFORMATIVE_*
-> no biological negative claim
-> increase future prospecting effort under a new freeze, or
-> move to another candidate population-season.
```

A near-zero predator-pressure context must never be used to declare Qg negative.

### P0 signal present but flowering capacity limited

```text
CONTEXT_SIGNAL_PRESENT_CAPACITY_LIMITED
-> retain as a possible low-capacity replication / observational context
-> do not start the default disjoint Y-CAL + D0-CAL programme there unless a new capacity plan is prospectively registered.
```

## 7. Q-gate stop and reroute rules

### Threshold manifest cannot be defensibly frozen

```text
no confirmatory Qz/Qp/Qg analysis
-> collect additional independent calibration information
-> or change method/context before qualification.
```

Do not fill production configs with convenient values borrowed from unit tests.

### Qg fails because the barrier changes pollination or water state

```text
reject that exclusion method
-> test the prospectively ranked alternative method if available
-> if no independent method passes, demote Pedicularis as the first causal SLK system.
```

Do **not** rescue Pedicularis by returning to water retained/drained as SCH `G`.

### Qg is uninformative because predator pressure is too low despite P0

Interaction intensity may still drift within a season.

```text
no biological negative claim
-> move to a higher-predation Pedicularis context
-> retain the current context as an informative low-antagonist replication candidate.
```

### Qz fails

If graded bending/tape cannot move exsertion without shifting water defence, corolla opening, orientation, or damage beyond tolerance:

```text
Pedicularis cannot close the causal shared-coordinate surface with the registered method.
-> demote to observational / functional-y anchor
-> move primary G1-G2 execution to Dalechampia or the next qualified system.
```

### Qp fails because supplementation has no effect

Natural pollination may already be saturating in the focal context.

```text
P manipulation ineffective in that context
-> do not reinterpret a null as absence of pollination function
-> move to a pollen-limited context or redesign the P intervention before the full surface.
```

### Qp fails because supplementation changes antagonist exposure

```text
P manipulation not selective
-> redesign donor/handling protocol
-> no statistical adjustment may substitute for the selectivity gate.
```

## 8. Full-surface unlock

The main experiment is unlocked only when one population/season supplies:

```text
P0 = CONTEXT_SCREEN_PASS_CALIBRATION_READY
Qz = positive qualification receipt
Qp = positive qualification receipt
Qg = positive qualification receipt
```

with matching identifiers:

```text
population_id
season_id
```

SCH then runs the registered corrected surface:

```text
>=5 realized z levels
x NATURAL / SUPPLEMENTED pollination dependence
x PREDATOR_EXPOSED / PREDATOR_EXCLUDED

water-y held fixed across all cells.
```

Primary common scale:

```text
undamaged mature viable seeds per focal flower / capsule.
```

The full-surface receipt remains a G1-stage causal-compromise result until the component-optimum and conflict-budget gates are subsequently passed.

## 9. Route from full surface to SLK G2

```text
V2 causal surface positive
-> SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1
-> context-stable component-optimum upgrade
-> SCH_COMPONENT_CONFLICT_BUDGET_V1
-> THREE_WORLD_CONFLICT_HANDOFF_V1
-> SLK_PEDICULARIS_G2_RECEIPT_V1 adjudication.
```

For a bounded positive G2 handoff, SLK requires:

```text
L.lower_95 > 0.
```

A measured `L` interval that includes zero is retained as a valid measurement attempt but does not unlock BALANCE classification.

## 10. Downstream preservation rule

The field pilots must be designed from the start to preserve the later BITA comparison.

Therefore:

```text
SCH antagonist G = independent predator exposure
BITA y            = water-defence state
```

must remain distinct.

This is not cosmetic bookkeeping. It is what makes later dimensional release non-circular.

## 11. Current execution state

```text
P0 freeze / field packet / adjudicator  IMPLEMENTED, NOT YET EXECUTED BIOLOGICALLY
Qz evaluator / template                 IMPLEMENTED, NOT YET EXECUTED BIOLOGICALLY
Qp evaluator / template                 IMPLEMENTED, NOT YET EXECUTED BIOLOGICALLY
Qg V3 evaluator / template              IMPLEMENTED, NOT YET EXECUTED BIOLOGICALLY
threshold values                        NOT YET PROSPECTIVELY FROZEN
readiness assembler                     IMPLEMENTED
V2 full-surface wrapper                 IMPLEMENTED
G2 SLK adjudicator                      IMPLEMENTED
```

Thus the remaining bottleneck is no longer software or theory. It is fresh candidate-context recovery, P0 screening, then empirical calibration / threshold freeze and field qualification.

## 12. Decision summary

```text
first executable task:          recover candidate population-season + freeze/run P0 context screen
next unlocked task:             independent calibration + threshold freeze
highest-risk biological gate:   Qg independent predator method
highest-value execution tactic: parallel Qg/Qz/Qp qualification on disjoint units after P0
hard stop:                       no full surface until P0 and all three Q gates pass
fallback if Pedicularis fails:   Dalechampia / next qualified SCH system
forbidden rescue:                water retained/drained reused as SCH antagonist G
```
