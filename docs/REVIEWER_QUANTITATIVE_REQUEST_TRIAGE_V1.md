# SLK reviewer quantitative request triage V1

## Purpose

This document classifies likely reviewer requests by whether the requested analysis increases the identification or theorem content of the active SLK paper. `DO_NOW` means the request is low-risk and directly strengthens or audits an existing claim; `DO_IF_REQUESTED` means it is defensible only if a reviewer explicitly challenges the registered scope; `DECLINE` means it adds parameter volume, new biological data requirements, or a new model class without strengthening the present claim.

| Reviewer request | Decision | Quantitative value gained | Trigger / boundary |
|---|---|---|---|
| Re-run the registered INV1 fixation/occupancy numerical verification across the existing finite-population test grid. | `DO_NOW` | Confirms implementation of the process-conditional invariant and catches coding drift. | This is an audit of the theorem implementation, not new evidence for nature; the analytic INV1 result remains primary. |
| Provide an additional compact table linking each non-implication to its registered numerical witness. | `DO_NOW` | Makes the estimand separations inspectable without changing any witness value or theorem. | Use only frozen witnesses already in the manuscript; do not infer frequency or effect size from them. |
| Extend INV1 to asymmetric mutation or a different mutation kernel. | `DO_IF_REQUESTED` | Tests which part of the fixation-to-occupancy realignment depends on symmetric rare mutation. | This is a new process class. Keep it out of the core paper unless a reviewer specifically challenges the symmetry boundary; an asymmetric mutation extension must be labelled as an extension, not as the registered theorem. |
| Add another local-accessibility construction if a reviewer argues the present witness is pathological. | `DO_IF_REQUESTED` | Can demonstrate that the separation is structural rather than tied to a single algebraic parameterization. | Add only if the reviewer identifies a concrete degeneracy; otherwise one valid counterexample is logically sufficient. |
| Add a dense parameter sweep around every witness value. | `DECLINE` | Little or no inferential gain: a non-implication requires one valid witness, not a frequency map over an arbitrary parameter box. | Do not turn parameter-grid area into a prevalence statement or pseudo-probability. |
| Perform empirical calibration of L/R/K/Phi from the current paper. | `DECLINE` | None without new matched biological measurements on a common fitness scale. | **No single biological system** in the paper completes the end-to-end ladder. `FIELD_DISTRIBUTION_OF_PHI = NOT_ESTIMATED`; witness values are **not an empirical estimate**. |
| Estimate how often accessibility, invasion, fixation, or occupancy disagree in nature from the cited literature. | `DECLINE` | The compact prior-art set was not sampled to estimate natural frequencies. | This would violate the registered claim ceiling and requires a new systematic empirical programme. |

## Revision rule

Prefer analyses that test a declared implication, implementation invariant, or process boundary. Reject analyses whose only output is more points in parameter space. In particular, numerical robustness does not promote theoretical witnesses to empirical calibration, and a reviewer request for broader process classes should be answered by the narrowest explicit extension that addresses the stated concern.

```text
FIELD_DISTRIBUTION_OF_PHI = NOT_ESTIMATED
```

The active SLK paper remains a theory-and-measurement-framework paper. The witness values are **not an empirical estimate** of natural effect magnitudes, and **No single biological system** is claimed to supply the entire conflict-to-occupancy calibration.
