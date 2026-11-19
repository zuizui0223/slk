# Wurmbea reproductive return implementation plan

> **For agentic workers:** Use superpowers:executing-plans for this small continuation; inspect the original study before interpreting derived values.

**Goal:** Carry the existing biological continuation from re-expression to realized reproductive return using Ramsey, Vaughton & Peakall (2006), Table 2.

**Architecture:** Preserve five published treatment groups and four life-stage means. Compute ratios of successive products of treatment means, as a descriptive aggregate reanalysis. Keep source-reported quantities, recomputed indices, and unresolved discrepancies separate.

**Tech Stack:** Python standard library; unittest; matplotlib for an optional static research figure.

**Spec:** The existing `docs/SLK_ANTO_WURMBEA_REAL_GENDER_REEXPRESSION_V1_20261114.md` asks to connect female re-expression to reproductive success. This continuation executes the available published-aggregate comparison; it cannot create the missing same-individual genotype-to-lifetime-fitness experiment.

## Global constraints

- Continue draft PR #121; no main-manuscript change, merge, or submission.
- Published means are not raw family records; no new bootstrap, P value or confidence interval.
- Seed germination and second-growing-season survival are conditional stages. Corm mass is a growth proxy, not reproduction at maturity.
- Multiplication of marginal means does not recover the mean of family-specific products.
- The 1999, 2006 and 2012 cohorts are separate. The 1999 table has two observed flowering censuses, not a demonstrated individual M→FM→M round trip.
- Correct 1999 author attribution to Barrett, Case & Peters; retain the observed counts.

## Review focus

- Percentages must be converted once; survival must not be counted twice.
- Match female/male comparisons within pollination treatment.
- Do not substitute the published seed-only 1.4 ratio for the four-component ratio.
- Do not treat rounding bounds as uncertainty intervals.
- Do not treat seedling outcrossing rates as zygotic rates or infer net male-plus-female lifetime fitness.

## Task 1: Source, calculation and biological interpretation

- [x] Store transcribed Table 2 means, SE, stage definitions, family-sampling notes and source URLs in `data/evidence/wurmbea_2006_reproductive_return_source_v2.json`.
- [x] Write and run failing tests for stage ordering, percentage conversion, the independently computed Fo/Mo and Fc/Mc ratios, self/cross cumulative depression, rounding limits, and invalid input units.
- [x] Implement `analysis/analyze_wurmbea_reproductive_return_v2.py` with `stage_indices`, `compare_groups`, and `analyze` functions, plus a reproducible CLI.
- [x] Generate `results/wurmbea_reproductive_return_v2.json` and the static stage comparison figure.
- [x] Correct author/census wording in the existing v1 source note and receipt; add a concise v2 biological interpretation and README pointer.
- [x] Run both Wurmbea test modules, reproduce outputs, inspect figure and diff; obtain independent scientific/code review before committing.

## Execution notes

- Isolated fresh clone; branch based on PR #121 head `40027932b93cfc594534fe4f737c2c2042fa92d8`.
- Baseline: existing 7 Wurmbea unittest checks pass. The default runtime lacks pytest, so use repository's dependency-free unittest workflow for this scoped change.
- Independent arithmetic was calculated by two read-only agents before implementation.

- Completion: 14/14 Wurmbea tests pass; deterministic result equality, figure inspection, scope check and manuscript-limit check pass. Independent review found no critical or important defect.
- Optional additional source-linked corm-discrepancy assertions were suggested for future regression hardening; current source values were independently verified and no numerical defect was found.
