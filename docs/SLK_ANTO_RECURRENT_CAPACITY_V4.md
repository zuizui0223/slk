# SLK × ANTO v4 — persistence of a capacity is not fixation of its expression

2026-10-20. Conditional theory, not a new plant result. Companion to
[ANTO commit 0d57f46](https://github.com/zuizui0223/anto/commit/0d57f461c3e2e00181251c412f32d2a4df9c898e).

## The biological advance over the finite-census example

The v3 connection asked whether a hypothetically heritable recovered phenotype
could leave four descendants by generation 14. The v4 model removes that
arbitrary census and permits expression to disappear again in descendants.
Some nonexpressing descendants retain the complete toolkit and reproduce;
others lose the toolkit irreversibly. The target is indefinite persistence of
the competent genealogy, not uninterrupted expression or fixation.

**Central conditional prediction:** a nonexpressing but reproducing state can
maintain the route back to expression. Sending more offspring into the
expressing state can increase immediate visible recovery while reducing the
long-run chance that any competent descendants remain. This requires a
relative demographic advantage of the silent state; it is not a universal
claim that suppressing floral traits is adaptive.

C is a reproducing, nonexpressing state, not a dormant seed. Loss of capacity
in this model is NOT extinction of the plant lineage: descendants that lost
the toolkit may still be viable organisms outside the modeled process.

## Exact comparison and common starting unit

The constant-environment model has D expressing and C silently competent.
Each has two independent reproductive slots, with birth probabilities q_D
and q_C; each child retains the necessary toolkit with probability 1-d.
A retained D child silences with probability s; a retained C child expresses
with probability a. Assigned rates are not estimates from SLK's Phi or from
photographs. Holding q_D=0.65, q_C=0.90, d=0.30, s=0.25 fixed gives:

| Conditional activation a | At least one D child next generation from one C | Indefinite competent-lineage survival from that same C |
|---:|---:|---:|
| 0.30 | 34.2279% | 35.6158% |
| 0.50 | 53.0775% | 16.2928% |
| 0.90 | 81.2511% | 0% |

The exact activation boundary is a*=1651/2268=0.7279541446... in this
illustrative parameter slice. It is not a plant-world percentage. A classical
multitype branching criterion determines survival: the largest eigenvalue of

```
M=(1-d)*[[2*q_D*(1-s),2*q_D*s],
         [2*q_C*a,    2*q_C*(1-a)]]
```

must exceed one. At a=0.30, both same-state diagonal means are below one
(0.6825 and 0.882), yet the full eigenvalue is 1.092. Cross-state transmission
matters: considering only uninterrupted same-state descendants misses the
reproducing competent genealogy. Under the irreducible model, survival of that
genealogy permits expression at arbitrarily late generations, not fixation of
expression throughout the genealogy.

## A correction to how the two repositories should be connected

Do not attach SLK's positive D-versus-S selection signs to this offspring model
as if they proved D superior to C. In the displayed example, C reproduces
better than D. It is an additional viable alternative, analogous in candidate-
set logic to the scaffold-preserving reduced-dimorphism alternative already
examined in `theory/FLORAL_SCAFFOLD_BYPASS_V1.md`. Beating one original reference
is not equivalent to beating every available state.

Accordingly, v4 does not import a positive-Phi eligibility mask or claim a
calibrated SLK payoff-to-demography map. SLK contributes the explicit alternative-
architecture comparison; ANTO contributes retention, loss and re-expression of
the same functional capacity. A joint organismal test must independently show
that the retained capacity belongs to the same multifunctional structure whose
specialization is being compared. Pigment return alone does not establish this.

Initial competent frequency theta multiplies one-founder survival probability
but, for theta>0, does not change the constant-environment spectral boundary.
Thus initial evolutionary resources and the ecological ability to propagate
them remain different questions. No finite initial supply cures a genuinely
subcritical closed branching process; gene flow and density feedback would be
separate mechanisms.

## Scope and ownership

Carja & Plotkin (2019, DOI 10.1534/genetics.118.301758) and Blath, Hermann &
Slowik (2021, DOI 10.1007/s00285-021-01639-6) already establish relevant
phenotypic-switching and two-type persistence theory. Neither the eigenvalue
criterion nor switching-assisted persistence is claimed as new mathematics.
The contribution here is a parameter-explicit, reproducible biological
hypothesis separating visible restoration from persistence of recoverability.
No field parameters, plant fitness, true trait reversal or evolutionary optimum
were estimated. All Cirsium empirical work remains in aza3.

Model, 14 focused tests, 324-case independent eigensolver check, and selected
results are recorded in ANTO's `docs/SLK_ANTO_RECURRENT_CAPACITY_V4.md` and
`results/slk_anto_recurrent_capacity_v4_summary.json`. Numerical code is not
copied into SLK. Existing v1–v3 remain preserved; this note does not change the
main Am Nat manuscript or merge either draft PR.
