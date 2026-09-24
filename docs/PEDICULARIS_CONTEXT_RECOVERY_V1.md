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
