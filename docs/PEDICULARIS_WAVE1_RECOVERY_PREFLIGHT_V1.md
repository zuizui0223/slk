# Pedicularis WAVE1 recovery preflight v1

Status: **CURRENT OPERATIONAL ACCESS PREFLIGHT / SAMPLING PERMISSION UNRESOLVED / NO FRESH BIOLOGICAL RESULT**.

## Purpose

The three WAVE1 recovery candidates are geographically compact around Shangri-La and now have source-backed scouting locators. Before a field recovery attempt, this preflight separates two questions that must not be collapsed:

```text
Is the place/institution currently active or publicly reachable?
!=
Is scientific observation / plant sampling / collecting authorized?
```

Current operation can reduce the risk of travelling to a defunct or inaccessible destination. It cannot substitute for explicit permission.

## WAVE1 current-operation anchors

### SONGZANLIN_EIA_2025

Current-operation evidence:

```text
XGLL_GOV_2026_SONGZANLIN_TOURISM
```

The official 2026 Spring Festival tourism report records active visitation to Songzanlin Scenic Area.

Interpretation:

```text
current public operation supported
sampling permission unresolved
exact current P. rex population still requires fresh recovery.
```

### SHANGRILA_WUFENG

Current-operation evidence:

```text
XGLL_GOV_2026_WUFENG_HORSERACE
```

The 2026 Diqing-Shangri-La horse-racing programme was held at Wufeng Mountain Stadium.

Interpretation:

```text
current venue activity supported
access to the historical 2005 study micro-site unresolved
sampling permission unresolved
fresh P. rex recovery still required.
```

### SHANGRILA_ALPINE_BOT_GARDEN

Current-operation evidence:

```text
BOTANY_CN_2026_ALPINE_GARDEN_MEETING
```

Shangri-La Alpine Botanical Garden hosted the 2026 national fern symposium.

Interpretation:

```text
current research-institution operation supported
institutional contact route exists
sampling / collecting permission unresolved
fresh P. rex recovery still required.
```

## Executable contract

Canonical files:

```text
data/PEDICULARIS_WAVE1_RECOVERY_ACCESS_ANCHORS_V1.csv
scripts/validate_pedicularis_wave1_access_anchors.py
tests/test_pedicularis_wave1_access_anchors.py
```

The validator requires exactly the current WAVE1 inventory and requires every access anchor to retain:

```text
sampling_permission_status = UNRESOLVED
permitted_use = RECOVERY_PREFLIGHT_ONLY.
```

A later explicit permission receipt may resolve the permission field in the fresh recovery observation. The preflight table itself cannot do so.

## Field sequencing

The three WAVE1 candidates may be contacted and checked in parallel because recovery does not inspect P0 ecological signal. A positive recovery at any candidate authorizes only the next P0 natural-history calibration gate for that population-season.

Do not use tourist opening, public events, conference hosting or project activity as evidence for:

```text
P. rex flowering presence
pollinator activity
predator activity
water-state functionality
P0 capacity
sampling permission
G1-G5 biology.
```

## Claim ceiling

```text
CURRENT_OPERATIONAL_ACCESS_PREFLIGHT_ONLY
SAMPLING_PERMISSION_UNRESOLVED
NO_FRESH_CONTEXT_PASS
NO_P0_SIGNAL
NO_G1_G5_RESULT
```
