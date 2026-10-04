# Figure 3 — empirical diagnosis of persistent multifunctionality

## Caption

**Figure 3. How to distinguish the biological causes of persistent multifunctionality.** The empirical sequence begins by establishing a genuine functional conflict and placing its magnitude on a common fitness scale. It then asks three progressively different questions: does division of labor pay (`Phi=R-K`), is a fitter differentiated state reachable from the integrated architecture, and can that state establish when rare? Negative answers at these stages diagnose the three explanations in Figure 1. If all three early tests are positive, they exclude those explanations but do not prove historical realization or long-run persistence. Fixation and stationary occupancy therefore appear only as optional downstream extensions requiring additional demographic and mutation-process assumptions.

## Purpose

The figure makes the experimental logic match the biological question.

~~~text
documented conflict
      |
      v
measure L
      |
      v
measure R and K
      |
      +-- Phi < 0 -> differentiation does not pay
      |
      v
measure local release gradient g0
      |
      +-- g0 < 0 -> fitter endpoint is locally inaccessible
      |
      v
measure rare-frequency selection Delta_R
      |
      +-- Delta_R < 0 -> differentiated type cannot establish when rare
      |
      v
early explanations excluded
~~~

The empirical programme can stop when the biological question has been answered. Fixation and long-run occupancy are not mandatory endpoints for a study of why multifunctionality persists.

## Core measurements

| Step | Quantity | Minimal biological design | Interpretation |
|---|---|---|---|
| conflict | opposing functional effects and `L` | manipulations or contrasts that identify different functional optima on the same structure and put their consequences on a common fitness scale | establishes that persistence occurs despite real conflict |
| value | `R`, `K`, `Phi=R-K` | matched integrated and experimentally or naturally differentiated comparisons | `Phi<0` supports the "does not pay" explanation |
| reachability | local gradient `g0` | small developmental, mutational, or experimental release steps away from integration | `g0<0` supports a local accessibility barrier |
| establishment | `Delta_R` and frequency response | rare-frequency differentiated types in the relevant ecological background | `Delta_R<0` supports rare-establishment failure |

## Environmental test

Repeat the value and rare-frequency measurements across an ecological coordinate `E`.

If

~~~text
Phi(E)=a(E-E_V)
~~~

and frequency feedback is locally summarized by `eta`, then the rare-establishment boundary is displaced from the profitability boundary by

~~~text
E_I-E_V=eta/a.
~~~

This predicts a measurable ecological interval in which division of labor is already profitable but cannot establish when rare, or the reverse when frequency dependence favors rarity.

## Frequency-response design

For the canonical local model

~~~text
Delta(p)=Phi+eta(2p-1),
~~~

two symmetric frequency treatments estimate `Phi` and `eta`:

~~~text
Phi=[Delta(p_+)+Delta(p_-)]/2
eta=[Delta(p_+)-Delta(p_-)]/(4q).
~~~

A balanced treatment at `p=1/2` can test curvature. More generally, invasion itself depends on the endpoint selection limits rather than on a particular interior curve:

~~~text
Delta_R = lim_{p->0} Delta(p)
Delta_D = lim_{p->1} Delta(p).
~~~

Interior frequencies are then used to identify the ecological mechanism generating those endpoint effects.

## Finite-frequency endpoint certification

Exact `p=0` or `p=1` treatments are not necessary. If the local response is Lipschitz bounded, a measurement at small `epsilon` gives an explicit interval for the endpoint. With measurements at `epsilon` and `2epsilon` and a valid curvature bound,

~~~text
Delta_R_hat = 2Delta(epsilon)-Delta(2epsilon)

|Delta_R_hat-Delta_R| <= C_R epsilon^2.
~~~

A certified interval entirely above zero supports rare establishment; one entirely below zero supports failure; overlap with zero remains unresolved.

## Optional downstream extensions

A fixation claim additionally requires a finite-population stochastic model. A long-run occupancy claim additionally requires a mutation graph and mutation kernel. Under the specific symmetric rare-mutation exponential-Moran model used in the mathematical extension, reciprocal fixation ordering and stationary occupancy ordering happen to share the same `Phi=0` boundary. That process result is useful but is not part of the core empirical diagnosis of persistent multifunctionality.
