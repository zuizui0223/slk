# Pedicularis fresh context recovery gate v1

Status: **PROSPECTIVE / EXECUTABLE ENTRY GATE / NO BIOLOGICAL SIGNAL CLAIM**.

## Purpose

The candidate ledger identifies places where `Pedicularis rex` has previously been collected, studied, or recently recorded in an official environmental assessment. These prior anchors are useful for prioritization, but none can establish that a usable population exists in the current field season.

This gate sits before P0 natural-history calibration.

```text
prior candidate anchor
-> fresh context recovery
-> P0 natural-history calibration
-> P0 context screen
-> Qz/Qp/Qg and downstream SLK chain
```

## What recovery asks

A candidate becomes usable only when the current season supplies fresh evidence that:

```text
P. rex identity is confirmed
AND a flowering population is currently present
AND at least one independent flowering plant is seen
AND the site is currently accessible
AND sampling permission is resolved
AND a same-season revisit for P0 work is feasible.
```

The flowering-plant count here is an existence check only. It is **not** the P0 capacity census and cannot establish the 84-plant calibration requirement.


Every resolved recovery decision must be auditable. A complete observation therefore carries:

```text
taxon_verification_method
taxon_evidence_reference
flowering_population_evidence_reference
access_evidence_reference
sampling_permission_reference
revisit_plan_reference.
```

Registered taxon-verification routes are:

```text
FIELD_MORPHOLOGY_PHOTO
VOUCHER_OR_SPECIMEN
EXPERT_CONFIRMATION
COMBINED.
```


For `FIELD_MORPHOLOGY_PHOTO` and `COMBINED`, the positive field-identification checklist is defined in:

```text
docs/PEDICULARIS_REX_RECOVERY_TAXON_CHECKLIST_V1.md
```

and requires photo documentation of the registered Flora of China key characters. Flower color is not a required diagnostic because it varies among `P. rex` infraspecific taxa.


The taxon route cannot silently enlarge the permission scope. A pre-existing authorized specimen may support `VOUCHER_OR_SPECIMEN` only when its lawful provenance **and same candidate-site / population / season context** are receipted. An older specimen from another season cannot substitute for fresh recovery. Collecting a new voucher during recovery requires activity-D authorization from both regulatory and site sides, valid on the recovery date, and its collection date must equal the recovery verification date. `COMBINED` must state whether its secondary route is expert confirmation or voucher/specimen.

A boolean `taxon_identity_confirmed=true` without its evidence reference is incomplete, not a pass. The same rule applies to flowering presence, access, permission and revisit feasibility.


Permission is additionally scope-bound. A positive recovery observation must carry:

```text
sampling_permission_status = CONFIRMED
sampling_permission_scope  = RECOVERY_PLUS_P0A_PLUS_P0B_NONDESTRUCTIVE
permission_scope_receipt    = confirmed WAVE1 permission-scope receipt.
```

The receipt must show A-C (observation, morphology photography and non-destructive measurement) passing on both regulatory and site sides. D-F destructive activities are not inferred from this receipt.


The embedded receipt is the **full adjudicated permission receipt**, not a matrix/date-only summary. It retains adjudication metadata, audited incoming-response events and content hashes, activity-decision evidence extraction, condition reviews, and all activity validity intervals.

Recovery revalidates that receipt with:

```text
scripts/pedicularis_permission_scope.py
```

before treating permission as confirmed. Removing source-response provenance, decision evidence, condition-review metadata, or interval/source cross-links makes the recovery packet invalid.

## What recovery does not ask

Recovery must not score or infer:

```text
pollinator activity
predator attack/exposure
water-state functionality
pollen limitation
P0 capacity pass
G1/G2 or any downstream effect.
```

Those belong to later prospectively frozen gates.

A failed recovery means only that the current candidate/context is not ready for this execution chain. It is not evidence that the species is absent from the wider region or that an ecological interaction is absent.

## Canonical files

```text
data/PEDICULARIS_CONTEXT_CANDIDATE_LEDGER_V1.csv
data/PEDICULARIS_CONTEXT_RECOVERY_FREEZE_TEMPLATE_V1.json
data/PEDICULARIS_CONTEXT_RECOVERY_OBSERVATION_TEMPLATE_V1.json
scripts/generate_pedicularis_context_recovery_packet.py
scripts/adjudicate_pedicularis_context_recovery.py
scripts/compile_pedicularis_context_recovery_to_p0_calibration.py
tests/test_pedicularis_context_recovery.py
tests/test_pedicularis_context_recovery_packet.py
```

## Recovery queue

Candidate choice is organized prospectively as waves rather than a false-precision scalar ranking:

```text
data/PEDICULARIS_CONTEXT_RECOVERY_QUEUE_V1.csv
scripts/validate_pedicularis_context_recovery_queue.py
```

`WAVE1` contains three complementary high-information anchors:

```text
SONGZANLIN_EIA_2025
    freshest locality-specific record (2025 official environmental assessment)

SHANGRILA_WUFENG
    strongest direct historical interaction-site evidence

SHANGRILA_ALPINE_BOT_GARDEN
    second direct historical interaction-site anchor.
```

A wave is a recovery order, not a biological ranking. No prior anchor becomes a fresh pass without the recovery gate.

## Scouting locators

Where published or official sources provide spatial information, recovery uses a separate scouting-locator layer:

```text
data/PEDICULARIS_CONTEXT_RECOVERY_SCOUTING_LOCATORS_V1.csv
scripts/validate_pedicularis_context_recovery_scouting.py
```

The locator layer currently covers all three WAVE1 candidates plus Hutiaoxia:

```text
SHANGRILA_WUFENG
    27°47′46″N, 99°42′35″E
    historical 2005 study population point

SHANGRILA_ALPINE_BOT_GARDEN
    27°54′9–30″N, 99°38′8–20″E
    historical 2011 study-population envelope

SONGZANLIN_EIA_2025
    official 2025 project/evaluation-area coordinate envelope
    not an exact plant coordinate

HUTIAOXIA_SHANGRILA
    27°21′00″N, 99°54′36″E
    voucher HW10086 collection point.
```

These are **scouting locators only**. They do not prove that a current flowering population is present. In particular, the Songzanlin envelope represents the official project/evaluation area, not the position of an individual `P. rex` plant.

## Permission routing

For WAVE1, official contact routes are registered separately from permission outcomes:

```text
docs/PEDICULARIS_WAVE1_PERMISSION_ROUTING_V1.md
data/PEDICULARIS_WAVE1_PERMISSION_CONTACT_ROUTES_V1.csv
scripts/validate_pedicularis_wave1_permission_contacts.py
```

A contact route may identify whom to ask, but it cannot populate `sampling_permission_status=CONFIRMED`. Only an auditable permission/reference covering the needed activity can do that.

## Draft packet generation

Use the canonical ledger-backed generator so source type, source reference and prior candidate status are copied rather than retyped:

```bash
python scripts/generate_pedicularis_context_recovery_packet.py \
  --candidate-id SHANGRILA_WUFENG \
  --candidate-site-id <fresh-site-id> \
  --population-id <fresh-population-id> \
  --season-id <season> \
  --recovery-window-id <recovery-window> \
  --p0-calibration-window-id <planned-calibration-window> \
  --p0-screen-window-id <planned-screen-window> \
  --packet-output PEDICULARIS_CONTEXT_RECOVERY_PACKET_DRAFT.json \
  --freeze-output PEDICULARIS_CONTEXT_RECOVERY_FREEZE_DRAFT.json \
  --observation-output PEDICULARIS_CONTEXT_RECOVERY_OBSERVATION_V1.json
```

The generated packet also embeds the candidate's recovery-wave snapshot and, when registered, its scouting point/envelope. Candidates without a source-backed locator retain `scouting_locator_snapshot = null`; the generator never invents coordinates.

The generated freeze is deliberately **not frozen**. It cannot be adjudicated until freeze metadata are filled, the object is committed, `status` is changed to `FROZEN_CANDIDATE`, and `frozen_before_recovery_observations=true`.

## Execution

1. Choose a historical candidate from the candidate ledger or generate its draft packet with the ledger-backed generator.
2. Freeze candidate/site/population/season identifiers, recovery window, and the future P0 calibration/screen windows before fresh recovery observations.
3. Fill the fresh observation payload.
4. Run the adjudicator.
5. Only `CONTEXT_RECOVERY_READY_FOR_P0_RELEVANCE_CALIBRATION` authorizes compiling the context into the P0 natural-history calibration template.

The compiler copies only context identifiers and future windows. Sampling floors, bootstrap settings, source qualifications and freeze metadata remain unresolved and must still be prospectively frozen before P0 calibration outcomes are opened.

## Operational statuses

```text
CONTEXT_RECOVERY_READY_FOR_P0_RELEVANCE_CALIBRATION
CONTEXT_RECOVERY_INCOMPLETE
CONTEXT_RECOVERY_TAXON_UNCONFIRMED
CONTEXT_RECOVERY_NO_FLOWERING_POPULATION
CONTEXT_RECOVERY_ACCESS_BLOCKED
CONTEXT_RECOVERY_CURRENT_SEASON_NOT_FEASIBLE
```

## Claim ceiling

```text
FRESH_CONTEXT_EXISTENCE_AND_LOGISTICAL_FEASIBILITY_ONLY
NO_P0_SIGNAL
NO_CAPACITY_PASS
NO_G1_G5_RESULT
```
