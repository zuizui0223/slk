# Pedicularis WAVE1 permission outreach ledger v1

Status: **OUTREACH TRACKING / NO PERMISSION GRANTED / NO BIOLOGICAL RESULT**.

## Purpose

The permission-routing layer identifies the official contacts to approach. This ledger records what has actually been sent and what kind of answer has actually been received.

The distinction is operationally important:

```text
contact route identified
!= inquiry sent

inquiry sent
!= substantive response received

one substantive response
!= complete permission response bundle

complete response bundle
!= permission scope confirmed.
```

Only the dedicated permission-response adjudicator can convert substantive responses into a confirmed scope receipt.

## Canonical files

```text
data/PEDICULARIS_WAVE1_PERMISSION_OUTREACH_LEDGER_TEMPLATE_V1.csv
scripts/manage_pedicularis_wave1_permission_outreach.py
tests/test_pedicularis_wave1_permission_outreach.py
```

Generate a fresh tracker from the current canonical contact routes with:

```bash
python scripts/manage_pedicularis_wave1_permission_outreach.py \
  --generate PEDICULARIS_WAVE1_PERMISSION_OUTREACH_LEDGER.csv \
  --receipt-output PEDICULARIS_WAVE1_PERMISSION_OUTREACH_STATUS.json
```

Validate an edited tracker with:

```bash
python scripts/manage_pedicularis_wave1_permission_outreach.py \
  --validate PEDICULARIS_WAVE1_PERMISSION_OUTREACH_LEDGER.csv \
  --receipt-output PEDICULARIS_WAVE1_PERMISSION_OUTREACH_STATUS.json
```

## Outreach states

```text
NOT_SENT
SENT_AWAITING_RESPONSE
ROUTED_TO_ANOTHER_AUTHORITY
RESPONSE_RECEIVED
CLOSED_NO_ACTION
```

A sent route requires both:

```text
outreach_date
outreach_reference.
```

A `NOT_SENT` row is forbidden from carrying response evidence.

## Response states

```text
NO_RESPONSE
ROUTING_RESPONSE_ONLY
SUBSTANTIVE_RESPONSE_RECEIVED
CLOSED_NO_RESPONSE_EXPECTED
```

Any non-empty response state requires:

```text
response_date
response_reference.
```

A routing-only response also requires the destination organization/contact. It does not count as a substantive regulatory or site authorization response.

## Candidate-level readiness

For a candidate to become:

```text
ready_to_build_permission_response_bundle = true
```

the ledger must contain at least:

```text
one SUBSTANTIVE_RESPONSE_RECEIVED
    from a REGULATORY_ROUTING route

AND

one SUBSTANTIVE_RESPONSE_RECEIVED
    from a SITE_MANAGEMENT_ROUTING
    or INSTITUTIONAL_SITE_ROUTING route.
```

A `LOCAL_TERRITORIAL_ROUTING` response can redirect the inquiry but cannot satisfy the site-authorizing side.

This readiness status means only that there is enough returned material to build the structured response bundle. It does **not** mean the activity decisions are positive.

## Relationship to the permission gate

```text
outreach ledger
-> substantive response material
-> permission response bundle
-> scripts/adjudicate_pedicularis_wave1_permission_responses.py
-> permission scope receipt
-> fresh context recovery.
```

The outreach ledger never assigns `ALLOWED`, `PROHIBITED`, or `NO_PERMISSION_REQUIRED` to activities A-F. Those decisions belong only in the returned authority/site response bundle.

## Claim ceiling

```text
OUTREACH_TRACKING_ONLY
NO_PERMISSION_GRANTED
NO_FRESH_CONTEXT_PASS
NO_P0_SIGNAL
NO_G1_G5_RESULT
```
