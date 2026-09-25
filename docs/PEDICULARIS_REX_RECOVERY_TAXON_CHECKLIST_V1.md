# Pedicularis rex fresh-recovery taxon checklist v1

Status: **FIELD IDENTIFICATION SUPPORT / RECOVERY-GATE INPUT / NOT A TAXONOMIC REVISION**.

## Purpose

When the recovery route uses:

```text
FIELD_MORPHOLOGY_PHOTO
or
COMBINED
```

a positive `taxon_identity_confirmed` cannot rely on a generic photo-set reference alone. The field record must document the two characters used by the Flora of China key to distinguish `Pedicularis rex` from the closely related `P. thamnophila` within series Reges.

## Registered positive features

The recovery checklist requires both:

```text
1. leaves mostly in whorls of 4
   (3 may occur, but 4 is the predominant registered state)

2. most petiole bases and bract bases enlarged and connate,
   forming the characteristic cupular structure.
```

The contrast in the Flora of China key is important: `P. thamnophila` has leaves mostly in whorls of 3 and its petiole bases are usually not enlarged and connate.

## Required field images

A field-morphology confirmation records:

```text
whole_plant_photo_reference
leaf_whorl_photo_reference
cupular_base_photo_reference.
```

The whole-plant image documents habit and flowering state; the leaf-whorl image supports the whorl character; the close image of the petiole/bract bases supports the cupular character.

## What is not a required diagnostic

Flower color is explicitly excluded as a required positive diagnostic. Across `P. rex` infraspecific taxa, the corolla may be yellow, purple-red or white.

Therefore:

```text
flower_color_used_as_required_diagnostic = false
```

is required for a positive field-morphology recovery decision.

## Alternative taxon routes

```text
VOUCHER_OR_SPECIMEN
EXPERT_CONFIRMATION
```

do not require the field-photo diagnostic checklist, but they still require an auditable `taxon_evidence_reference`.

A voucher/specimen route must additionally declare the evidence origin:

```text
PREEXISTING_AUTHORIZED_SPECIMEN
or
NEW_FIELD_VOUCHER.
```

For `PREEXISTING_AUTHORIZED_SPECIMEN`, the recovery record must cite the accession / authorization / provenance reference showing that the material already exists lawfully.

For `NEW_FIELD_VOUCHER`, the ordinary A-C non-destructive permission scope is not enough. Activity D (voucher specimen collection) must be PASS on both regulatory and site sides and valid on the actual recovery date.

`COMBINED` must explicitly name its second route:

```text
EXPERT_CONFIRMATION
or
VOUCHER_OR_SPECIMEN.
```

If the second route is voucher/specimen, the same origin and activity-D rules apply.

## Source

Registered source reference:

```text
FLORA_OF_CHINA_PEDICULARIS_SERIES_REGES_KEY
```

Source content: Flora of China treatment of `Pedicularis`, series Reges and species 88, `P. rex`.

## Claim ceiling

A passed checklist supports only the fresh-recovery taxon-identification gate. It does not establish population abundance, P0 ecological signal, capacity, or any G1-G5 result.
