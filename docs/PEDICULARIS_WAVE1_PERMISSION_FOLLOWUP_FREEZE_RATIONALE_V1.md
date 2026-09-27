# Pedicularis WAVE1 permission follow-up freeze rationale v1

Status: **PROSPECTIVE ADMINISTRATIVE TIMING RATIONALE / FROZEN BEFORE FIRST REAL SEND**.

## Frozen cadence

The production WAVE1 permission follow-up policy uses calendar days from the initial manual send:

```text
day 7   first follow-up
day 14  second follow-up
day 21  manual escalation review
```

No route is automatically closed after silence.

## Rationale

The goal is administrative consistency rather than inference about authority behavior.

A one-week first interval gives an office or site manager a normal working window to receive and route the inquiry while still leaving enough time to resolve access before a field season is lost.

The second follow-up is fixed one additional week later rather than being chosen after seeing which candidate is slow to answer.

After two prospectively scheduled attempts, the workflow stops adding reminders automatically. Day 21 triggers a human escalation review, which may decide to wait longer, register a newly routed authority, change contact channel, or close an administrative attempt. Silence is never interpreted as refusal or permission.

The same cadence applies to all WAVE1 routes. Candidate identity, biological attractiveness, and response speed cannot change the frozen offsets.

## Firewalls

```text
automatic_close_allowed = false
response_receipt_preempts_followup = true
routing_response_preempts_same_route_followup = true
frozen_before_first_send = true
```

A response received before a scheduled follow-up cancels that same-route follow-up. A routing response redirects the workflow instead of triggering repeated contact to the old route.

## Claim ceiling

```text
ADMINISTRATIVE_FOLLOWUP_TIMING_ONLY
NO_AUTOMATIC_CONTACT
NO_PERMISSION
NO_BIOLOGICAL_RESULT
```
