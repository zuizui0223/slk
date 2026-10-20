# SLK x ANTO v5: when environmental timing changes the persistence of recoverability

2026-10-20. Theory-only companion to [ANTO 011eedb](https://github.com/zuizui0223/anto/commit/011eedbaa3c465beedb12a77ac4611bcbb32f86b).
The numerical implementation remains exclusively in ANTO. This note does not
change SLK main or the submission manuscript.

## Biological question

The v4 example maintained a functional toolkit through a nonexpressing,
reproductively active state C that always outperformed the expressing D.
The new question is whether a recoverable genealogy can persist when the
advantage reverses between environments, neither phenotype is always favored,
and the total amount of each environment is unchanged.

The prediction is **not simply that environmental history matters**. The
specific result is that the long-run boundary between retention and loss of
functional capacity can move when only the consecutive duration of ecological
conditions changes, and the direction depends on expression-state inheritance.

## Conditional comparison

D expresses the focal candidate; C reproduces without expressing it while
retaining the necessary toolkit. Each child can switch state or irreversibly
lose the toolkit. Loss exits the competent genealogy but does not imply death
of the organism. This is exactly the v4 offspring kernel, now under a prescribed
periodic environment shared by all descendants.

In environment A, reproductive-slot success is q_D=.90 and q_C=.40. In B,
these are reversed. Both environments occupy half of all generations.
Toolkit retention is .80 per child in every state and environment. All values
are illustrative, not calibrated plant rates, selection gradients or SLK Phi.

Compare the indefinitely repeated sequences ABABABAB and AAAABBBB, both
containing four A and four B generations. Start with the same single silent
competent C immediately before an A generation.

| Conditional offspring switching a=s | Environmental schedule | Long-run normalized growth of competent descendants | Indefinite competent-genealogy survival from C |
|---|---|---:|---:|
| .10 | ABABABAB | .968925 | 0% |
| .10 | AAAABBBB | 1.016400 | 2.08593% |
| .90 | ABABABAB | 1.308580 | 10.35677% |
| .90 | AAAABBBB | .977826 | 0% |

Within each pair, initial competence, first environment, average environmental
conditions, offspring parameters and first-generation visible expression
probability are identical. At switching .10, both first-expression probabilities
are 6.2976%. The different long-run outcomes therefore cannot be attributed to
unequal initial capacity or unequal immediate re-expression.

The low-switching example retains recoverability only when environments remain
in consecutive blocks. The high-switching example reverses that comparison.
There is NO universal rule that slower environmental change is beneficial,
and high-switching responses can show nonmonotonic periodic resonances.

## What actually sets the boundary

The long-run mean operator is the chronological product of the phase-specific
offspring matrices, not their arithmetic average. The average is identical for
both schedules and predicts growth 1.04 here, but the actual periodic growth
can be below one. A permanently expressing lineage and a permanently silent
lineage, each with switching disabled, both have geometric competent-descendant
growth .96 in this construction. Switching between the two states can maintain
a genealogy that neither permanent state can sustain alone.

For period length L and a common per-child loss d, let P_0 be the chronological
product at zero loss. Then

```
P(d)=(1-d)^L P_0,
d_critical=1-rho(P_0)^(-1/L).
```

At switching .10 the threshold is .174343 for ABABABAB and .212908 for
AAAABBBB. The entire open interval between these thresholds produces opposite
retention classifications; this is not a single numerical-seed anomaly.
The illustrative loss .20 lies inside that interval.

Cycle rotations are a necessary negative control. AB and BA are the same
periodic regime with different starting phases; they cannot have different
long-run growth boundaries. Single-founder survival may depend on the phase,
and that dependence is computed separately. When offspring expression no
longer depends on the parent (a=s=.50 in this symmetric example), changing
environmental block length has no effect on growth.

## What this adds to the SLK connection

SLK asks which viable structural resolution of functional conflict is favored
under a particular ecological partner context. ANTO asks whether the resources
to express that same functional structure persist through nonexpression and
subsequent reproduction. Here D and C really exchange their reproductive
ranking between contexts: beating an original S reference does not establish
that D always outperforms C. No positive-Phi eligibility mask is used as an
unjustified demographic calibration.

The resulting hypothesis is that **the temporal arrangement of selective
contexts can filter future functional possibilities even when average ecology
and present visible traits agree**. It remains conditional, not a demonstrated
plant mechanism. A proper organismal application must connect the retained
resource to the same multifunctional structure that SLK compares; white/coloured
flowers alone do not identify division of labour.

## Prior art, validation and scope

Acar, Mettetal & van Oudenaarden (2008, DOI 10.1038/ng.110) already demonstrated
environment-frequency-dependent advantages of phenotypic switching in engineered
yeast. Hufton, Lin & Galla (2018, DOI 10.1088/1742-5468/aaa78e) distinguish
periodic and stochastic regimes. Neither switching-assisted survival nor the
matrix-product criterion is claimed as new mathematics. The present contribution
is the explicitly tested functional-capacity loss boundary and the matched
history/first-expression comparison in the existing ANTO process.

ANTO contains 15 new focused tests, exact forward offspring-count checks,
364 independent matrix/eigenvalue comparisons, and a full-repository CI workflow.
The model, summary and interpretation are in
`src/anto_slk_periodic_capacity_v5.py`,
`results/slk_anto_periodic_capacity_v5_summary.json`, and
`docs/SLK_ANTO_PERIODIC_CAPACITY_V5.md`.
Numerical survival brackets are 70-digit Decimal approximations, not
outward-rounded interval certificates. No natural regain, genetic fixation,
evolved optimal strategy or organismal extinction is inferred. Density
regulation, gene flow and feedback on ecological partners are absent.
Cirsium empirical ownership remains in aza3; both PRs remain draft and unmerged.
