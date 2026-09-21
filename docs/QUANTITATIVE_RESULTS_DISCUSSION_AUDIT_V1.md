# SLK quantitative Results/Discussion audit V1

## Purpose

This audit translates the frozen quantitative claim ledger into Results/Discussion language. It does not add a theorem, empirical estimate, or biological calibration. Every row states what the paper may say quantitatively and what it must not promote beyond the registered evidence class.

| Qualitative claim | Quantitative claim licensed | Ceiling / not licensed |
|---|---|---|
| The same architecture comparison encounters different critical surfaces as new mechanisms enter. | In the registered composite model: small-step release switches at `k=k_local`; endpoint value, reciprocal fixation and symmetric rare-mutation occupancy at `Phi=0`; rare invasion at `Phi=eta`; reverse invasion at `Phi=-eta`; absolute fixation advantage at `3Phi=eta` under weak selection. | These are model-conditional surfaces, not universal boundaries for arbitrary mutational, game, demographic, or mutation processes. |
| Functional conflict does not by itself make differentiation profitable. | In the common family `R(d)=d+d^2`, `K(d)=kd`, choose `L=2, k=2.2`; then `R(1)=2`, `K(1)=2.2`, and `Phi=-0.2`. | This is a theoretical separation proving `L>0 !=> Phi>0`; it is **not an empirical estimate** of conflict or architecture value in nature. |
| Positive endpoint architecture value need not imply sufficiently small selectively uphill release. | `k=1.5` gives `Phi=0.5>0` but `Phi'(0)=-0.5<0`, with `k_local=1<1.5<2=k_global`. | The paper may diagnose a small-step selective barrier on the declared path; it may not infer absolute historical unreachability or how often natural populations cross it. |
| Small-step accessible positive architecture value need not imply rare invasion. | `k=0.8, eta=1.5` gives `Phi=1.2`, `Phi'(0)=0.2`, but `Delta(0)=-0.3<0`. | The numerical values are constructive witnesses, not measured ecological effect sizes. |
| Rare invasion need not imply reciprocal fixation superiority. | `k=2.2, eta=-1` gives `Phi=-0.2`, `Delta(0)=0.8>0`, while `rho_D/rho_S<1`. | The paper may separate invasion from fixation logically; it does not estimate natural fixation probabilities across systems. |
| Absolute fixation advantage can disagree with symmetric rare-mutation occupancy. | `k=2.1, eta=-0.5` gives `Phi=-0.1`, `3Phi=-0.3>eta`, while `Pi_D<Pi_S`. | The `3Phi=eta` boundary is a weak-selection result and must not be presented as process-universal. |
| Ecological context can displace the value and invasion thresholds. | With constant feedback, `E_I=E_V+eta/a`; with `eta(E)=eta_0+b(E-E_V)`, `E_I-E_V=eta_0/(a-b)` and `E_R-E_V=-eta_0/(a+b)`. | Exact only for the registered affine slices; smooth systems use local slope approximations. |
| Architecture value and frequency feedback are experimentally separable in the registered pair. | Symmetric frequency treatments identify `Phi=[Delta_++Delta_-]/2` and `eta=[Delta_+-Delta_-]/(4q)`. | Requires a linear-in-frequency fit; curvature or asymmetry rejects the minimal canonical mapping. |
| A third frequency treatment tests the canonical mapping. | With independently measured `Phi`, centered frequency treatments identify `h0`, `eta`, and curvature `kappa`; nonzero `h0` or `kappa` shifts generalized invasion surfaces away from `Phi=±eta`. | Quadratic local diagnostic only; does not license canonical Moran/occupancy results after model rejection. |
| Deterministic invasion is robust to arbitrary interior frequency shape. | Writing `Delta=Phi+H(p)`, the exact invasion surfaces are `Phi=-h_R` and `Phi=-h_D`, where the endpoint offsets are the rare-D and resident-D limits of `H`. | Endpoint invasion only; the richer frequency response does not automatically inherit fixation or occupancy formulas. |
| Endpoint invasion can be certified from finite frequencies. | A one-point Lipschitz bound yields `O(epsilon)` endpoint uncertainty; two-point extrapolation at `epsilon,2epsilon` yields `O(epsilon^2)` error under bounded curvature, with sampling intervals widened accordingly. | Requires valid local smoothness bounds; a zero-overlapping endpoint interval is unresolved, not non-invasion. |
| Stronger conflict need not imply more differentiation. | Under the quadratic bridge, `Phi=sL-K`; therefore rankings by `L` can reverse when `s` or `K` differs across systems. | Comparative statement requires valid and comparable conflict, recoverability, and cost definitions; `L` alone is not a natural effect-size proxy for differentiation. |
| Under the registered rare-mutation process, reciprocal fixation ordering and stationary occupancy ordering coincide. | Under connected symmetric rare mutation and the registered exponential Moran process, `rho(j|i)>rho(i|j)` iff `Pi_j>Pi_i`. | This is a process-conditional model prediction, not a universal law for arbitrary mutation kernels, demography, or asymmetric mutation. |
| The paper supplies an empirical measurement programme rather than an end-to-end empirical calibration. | **No single biological system** is claimed to complete the full ladder from conflict through payoff, accessibility, invasion, fixation, and occupancy. | Cross-system distributions of the theoretical quantities remain unestimated. |

## Discussion ceiling

```text
FIELD_DISTRIBUTION_OF_PHI = NOT_ESTIMATED
FIELD_DISTRIBUTION_OF_L = NOT_ESTIMATED
FIELD_DISTRIBUTION_OF_R = NOT_ESTIMATED
FIELD_DISTRIBUTION_OF_K = NOT_ESTIMATED
FIELD_ACCESSIBILITY_FREQUENCY = NOT_ESTIMATED
FIELD_INVASION_FREQUENCY = NOT_ESTIMATED
FIELD_FIXATION_FREQUENCY = NOT_ESTIMATED
FIELD_OCCUPANCY_FREQUENCY = NOT_ESTIMATED
```

Accordingly, Results may report exact non-implications, critical surfaces, and process-conditional invariants. Discussion may use them to identify which additional ecological/evolutionary measurements are required, but must not describe witness values as natural effect sizes, natural prevalences, or calibrated cross-system distributions.
