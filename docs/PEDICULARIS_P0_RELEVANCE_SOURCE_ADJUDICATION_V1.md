# Pedicularis P0 minimum-relevance source adjudication v1

Status: **PRIMARY-SOURCE AUDIT / NO PRODUCTION NUMERIC MINIMUM-RELEVANCE VALUES QUALIFIED YET**.

## 1. Purpose

The P0 context screen now has a prospective effort planner. The planner can convert a frozen minimum-relevance signal and a desired detection probability into field effort. That does **not** answer the biological question of what minimum signal is worth detecting.

This document adjudicates whether the existing `Pedicularis rex` literature can supply those numeric minimum-relevance inputs without a fresh natural-history calibration.

The three biological inputs are:

```text
pollinator  = minimum legitimate visit rate per flower-minute
predator    = minimum early attacked-flower / oviposition prevalence
water       = minimum water-positive flowering-plant prevalence.
```

The rule is fail-closed:

```text
published biological reality
!=
production numeric threshold.
```

An external number is usable only when endpoint, denominator/unit and context transport are explicitly qualified.

## 2. Pollinator source — method match, numeric value still open

Primary source:

```text
Sun & Huang 2015
AoB PLANTS 7: plv019
DOI 10.1093/aobpla/plv019.
```

The visitor protocol is structurally useful for P0:

```text
30-min plot censuses
20-30 h of observation in each year during peak bloom
morning / afternoon sampling alternated
visitor species and flower visits recorded
simultaneously open flowers counted after each census
visitation expressed as visits per flower per 30 min.
```

Therefore the correct P0 exposure scale is:

```text
flower-minutes
= observed minutes x simultaneously open focal flowers.
```

and the target rate is:

```text
legitimate visits / flower-minute.
```

This fixes an earlier P0 draft that used raw visits/min. Raw time alone is not transportable across populations with different numbers of open flowers.

### Numeric qualification

The paper's searchable text establishes the denominator and analytical method, but does not tabulate an exact baseline legitimate-pollinator mean suitable for copying into the P0 minimum-relevance field. The figure is graphical evidence, not a sufficiently auditable production number.

Current adjudication:

```text
endpoint match:        YES
unit/denominator match:YES after conversion to flower-minutes
external numeric value:NOT QUALIFIED
status:                OPEN_RAW_VALUE_OR_FRESH_CALIBRATION.
```

Production route:

```text
recover exact underlying/table source value and justify transport
OR
estimate the minimum-relevance anchor from a disjoint fresh natural-history calibration.
```

Do not derive the production value by reading a bar height from a figure.

## 3. Predator source — endpoint mismatch

Existing sources clearly establish biologically important and geographically variable predispersal seed predation:

```text
Xia et al. 2013
Sun & Huang 2015
Sun, Armbruster & Huang 2016.
```

The 2015 experiment reports seed predation ranging strongly among six populations, and the 2013/2016 studies show substantial density, year and population dependence.

However the P0 screen is intended to detect the **upstream antagonist signal needed for the later Qg method**:

```text
early attack / oviposition on focal flowers.
```

Published final seed-predation or fruit-predation proportions are not the same endpoint. Converting one into the other would require an additional prospectively registered bridge.

Current adjudication:

```text
biological reality:    DIRECTLY SUPPORTED
endpoint match:        NO
numeric transport:     NOT QUALIFIED
status:                FRESH_CALIBRATION_REQUIRED.
```

Production route:

```text
fresh independent natural-history sample
-> score early attack / oviposition using the exact P0 definition
-> freeze a minimum relevant attacked-flower prevalence
-> only then compute the P0 flower count.
```

A high or low historical final seed-predation percentage may guide candidate-site ranking, but may not define the production P0 early-attack threshold.

## 4. Water-state source — functional reality without prevalence denominator

Sun & Huang 2015 experimentally established that water in the cupulate bracts is biologically functional: drainage increased seed predation, while the study directly describes water-bearing cupulate bracts as a natural feature of `P. rex`.

That evidence qualifies:

```text
water-state biological relevance.
```

It does **not** identify:

```text
fraction of flowering plants water-positive at a particular screen moment.
```

The P0 prevalence depends on rainfall, time since rain, drainage/leakage and the exact observation definition. Statements that bracts are commonly or usually water-filled have no denominator suitable for a production binomial detection calculation.

Current adjudication:

```text
biological reality:    DIRECTLY SUPPORTED
prevalence denominator:NOT REPORTED
numeric transport:     NOT QUALIFIED
status:                FRESH_CALIBRATION_REQUIRED.
```

Production route:

```text
fresh independent natural-history sample
-> define the registered screen moment / weather window
-> record water-positive / total flowering plants
-> freeze a minimum relevant prevalence before P0 outcomes.
```

## 5. Decision inputs are separate from biological-rate inputs

The following are design decisions, not quantities to estimate from P0 outcomes:

```text
desired pollinator detection probability
desired predator detection probability
desired water-state detection probability
pollinator temporal-bout coverage
capacity reserve fraction above the fixed 84-plant Y-CAL + D0-CAL base.
```

They can be prospectively frozen under `DOWNSTREAM_DESIGN_REQUIREMENT` after their scientific/operational rationale is written down.

A stronger detection probability must never reduce field effort.

## 6. Source qualification statuses

The P0 effort freeze uses source-type-specific qualification labels:

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

The planner rejects a numeric external source that is merely labelled `EXTERNAL_MATCHED_PRIMARY_SOURCE` without `NUMERIC_TRANSPORT_QUALIFIED`.

## 7. Current source decision

As of this audit:

| Input | Existing literature | Numeric production readiness | Required next action |
|---|---|---|---|
| pollinator minimum rate | method/denominator directly matched after flower-minute correction | **OPEN** | recover exact underlying value + transport justification, or fresh calibration |
| predator minimum prevalence | antagonism reality strong, final predation geographically variable | **NOT QUALIFIED** | fresh early-attack/oviposition calibration |
| water-positive prevalence | functional water defence directly established | **NOT QUALIFIED** | fresh water-positive prevalence calibration |
| desired detection probabilities | design choice | **OPEN DECISION** | freeze prospectively |
| temporal coverage | historical method anchor + design choice | **OPEN DECISION** | freeze prospectively |
| capacity reserve | base 84 fixed; reserve is operational | **OPEN DECISION** | freeze prospectively |

Therefore:

```text
P0 EFFORT PLANNER:                       IMPLEMENTED
P0 POLLINATOR EXPOSURE UNIT:             FLOWER-MINUTES
EXTERNAL NUMERIC TRANSPORT GATE:         IMPLEMENTED
POLLINATOR MINIMUM RELEVANCE VALUE:      OPEN
PREDATOR MINIMUM RELEVANCE VALUE:        FRESH CALIBRATION REQUIRED
WATER MINIMUM RELEVANCE VALUE:           FRESH CALIBRATION REQUIRED
PRODUCTION P0 FREEZE:                    BLOCKED.
```

## 8. Practical implication

The cleanest field sequence is now:

```text
candidate site visit
-> small independent natural-history calibration
     pollinator flower-minute exposure
     early attack / oviposition prevalence
     water-positive prevalence
-> freeze minimum-relevance inputs + design detection probabilities
-> run P0 effort planner
-> compile and review final P0 freeze
-> generate P0 field packet
-> execute fresh context screen.
```

The independent natural-history calibration units are not P0 decision units and remain ineligible for Qz/Qp/Qg, G1-G2, Y-CAL/D0-CAL or G3-G5 effect estimation.

## 9. Claim ceiling

This source audit licenses no biological result.

```text
SOURCE_ADJUDICATION_ONLY
NO_P0_PASS
NO_G1_G2
NO_R_K_PHI.
```
