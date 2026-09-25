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
scripts/compile_pedicularis_outreach_to_permission_response_draft.py
scripts/render_pedicularis_wave1_permission_messages.py
tests/test_pedicularis_wave1_permission_outreach.py
tests/test_pedicularis_wave1_permission_messages.py
tests/test_pedicularis_outreach_to_permission_response_draft.py
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

## Unsent message rendering

Candidate- and route-specific Chinese/English inquiry drafts can be rendered with:

```bash
python scripts/render_pedicularis_wave1_permission_messages.py \
  --candidate-id <WAVE1_CANDIDATE_ID> \
  --output PEDICULARIS_WAVE1_PERMISSION_MESSAGE_DRAFTS.json
```

The renderer uses the canonical candidate, scouting locator and contact-route records. Every message remains:

```text
status = DRAFT_NOT_SENT
automatic_send_allowed = false
human_review_required = true.
```

Requester identity, institution and reply address remain `REQUIRED_BEFORE_SEND`. The message asks for A-F decisions separately and asks for activity-specific validity dates and conditions. Scouting coordinates are explicitly described as historical/project locators rather than current plant positions.

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

## Response-bundle draft handoff

Once a candidate has substantive regulatory and site-authorizing replies, compile an unresolved response-bundle starter with:

```bash
python scripts/compile_pedicularis_outreach_to_permission_response_draft.py \
  PEDICULARIS_WAVE1_PERMISSION_OUTREACH_LEDGER.csv \
  --candidate-id <WAVE1_CANDIDATE_ID> \
  --output PEDICULARIS_WAVE1_PERMISSION_RESPONSE_DRAFT.json
```

The draft pre-fills only the returned organizations, route ids, response dates/references and A-F activity inventory. Every A-F decision begins as:

```text
UNRESOLVED
```

and the bundle status remains:

```text
DRAFT_AWAITING_ACTIVITY_DECISIONS.
```

The compiler deliberately excludes routing-only contacts from the authorizing response list and cannot create an `ALLOWED` decision.

## Relationship to the permission gate

```text
outreach ledger
-> substantive response material
-> unresolved response bundle draft
-> human extraction of A-F decisions / validity / conditions
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
