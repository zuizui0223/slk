# Pedicularis WAVE1 permission-routing protocol v1

Status: **OFFICIAL CONTACT ROUTES IDENTIFIED / SAMPLING PERMISSION UNRESOLVED / NO FRESH BIOLOGICAL RESULT**.

## Purpose

The WAVE1 candidates now have current-operation preflight evidence. That does not establish scientific access or permission to observe, voucher, sample, or collect plants.

This protocol records where to ask without pretending that a contact route is itself an authorization.

## Common regulatory routing

For all three WAVE1 candidates, the first regulatory routing contact is:

```text
Shangri-La Municipal Forestry and Grassland Bureau
public office contact: 0887-8222611
```

The bureau publicly identifies itself as the municipal forestry/grassland authority and maintains the official wild-plant / forest-grassland regulatory contact route.

This is a routing contact. The protocol does not assume that this office alone can authorize every proposed activity.

## Candidate-specific routing

### SONGZANLIN_EIA_2025

```text
regulatory routing:
    Shangri-La Municipal Forestry and Grassland Bureau

site-management routing:
    Shangri-La Songzanlin Monastery Management Bureau
    public office contact: 0887-8223882
```

Questions to resolve:

```text
who manages the exact recovery ground?
is scientific access permitted?
what site-level approval is required?
what separate forestry/wild-plant permission is required?
```

### SHANGRILA_WUFENG

```text
regulatory routing:
    Shangri-La Municipal Forestry and Grassland Bureau

site-management routing:
    Shangri-La State-owned Forest Farm, Jiantang Branch
    contact routed through the municipal forestry/grassland bureau

local territorial routing:
    Jiantang Town People's Government
    public office contact: 0887-8222229
```

A 2026 municipal report states that Jiantang Branch staff and rangers patrol Wufeng Mountain, and recent municipal forestry approvals identify Jiantang Branch as an on-ground forest/grassland management and supervision unit within Jiantang Town. The branch therefore supplies the registered site-management route for Wufeng recovery. The town-government route remains routing-only and cannot satisfy the site authorization side.

### SHANGRILA_ALPINE_BOT_GARDEN

```text
regulatory routing:
    Shangri-La Municipal Forestry and Grassland Bureau

institutional site routing:
    Shangri-La Alpine Botanical Garden
    public professional contact published in the 2026 Chinese Botanical Society meeting notice
```

The current route in the contact ledger uses the publicly published garden meeting contact. It is a way to reach the institution, not a pre-existing approval to conduct the recovery work.

## Outreach tracking

After generating inquiry drafts, actual sends and replies are tracked separately:

```text
docs/PEDICULARIS_WAVE1_PERMISSION_OUTREACH_V1.md
data/PEDICULARIS_WAVE1_PERMISSION_OUTREACH_LEDGER_TEMPLATE_V1.csv
scripts/manage_pedicularis_wave1_permission_outreach.py
```

A candidate becomes ready to build a permission-response draft only after a substantive reply has been received from both a regulatory route and a site-authorizing route. Routing-only replies cannot satisfy the site side.

The response-draft compiler starts every A-F activity at `UNRESOLVED` and exposes activity-specific `valid_from`, `valid_through`, and `conditions` fields. It never interprets a returned message as permission.

## Inquiry packet generation

Generate an unsent candidate-specific packet with:

```bash
python scripts/generate_pedicularis_wave1_permission_inquiry.py \
  --candidate-id <WAVE1_CANDIDATE_ID> \
  --output PEDICULARIS_WAVE1_PERMISSION_INQUIRY_DRAFT.json
```

The draft automatically embeds the candidate, recovery wave, scouting locator when available, and all registered official contact routes. It begins at:

```text
status = DRAFT_NOT_SENT
permission_status = UNKNOWN / UNRESOLVED.
```

Generating the packet does not contact anyone and does not alter the recovery gate.

## Questions that must be resolved before P-1 can pass

The inquiry must distinguish activity classes:

```text
A. visual observation only
B. photography / morphology documentation
C. non-destructive measurements
D. voucher specimen collection
E. leaf/tissue sampling
F. seed/fruit collection
```

A response authorizing one class must not be generalized to another. The validity window and conditions must also be recorded **per activity class**; a response-level date range cannot be copied onto activities whose authorization period differs.


For every positive activity response, the project must also review whether the stated conditions are compatible with the exact registered procedure. Record the compatibility judgment and its review reference. If no additional conditions are stated, record `NO_ADDITIONAL_CONDITIONS`; a blank conditions field is not a positive permission record. A raw `ALLOWED` or `NO_PERMISSION_REQUIRED` response with incompatible conditions cannot count as a usable PASS.

The recovery observation may set:

```text
sampling_permission_status = CONFIRMED
```

only when the project has an auditable permission/reference that covers the activity needed for the prospective recovery/P0 path.

Otherwise the status remains:

```text
UNRESOLVED
```

and the context cannot pass the recovery gate.

## Canonical files

```text
data/PEDICULARIS_WAVE1_PERMISSION_CONTACT_ROUTES_V1.csv
scripts/validate_pedicularis_wave1_permission_contacts.py
scripts/generate_pedicularis_wave1_permission_inquiry.py
tests/test_pedicularis_wave1_permission_contacts.py
tests/test_pedicularis_wave1_permission_inquiry.py
```

## Response adjudication

Returned authority/site responses are not interpreted manually. Record them in:

```text
data/PEDICULARIS_WAVE1_PERMISSION_RESPONSE_TEMPLATE_V1.json
```

and adjudicate with:

```text
scripts/adjudicate_pedicularis_wave1_permission_responses.py
```

The minimum P-1/P0a scope is defined in:

```text
docs/PEDICULARIS_WAVE1_PERMISSION_RESPONSE_V1.md
```

Only its confirmed receipt can be compiled into the fresh recovery observation.

## Claim ceiling

```text
OFFICIAL_CONTACT_ROUTING_ONLY
NO_PERMISSION_GRANTED
NO_FRESH_CONTEXT_PASS
NO_P0_SIGNAL
NO_G1_G5_RESULT
```
