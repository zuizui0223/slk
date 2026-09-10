# Figure 1 — logic of the SLK hierarchy

## Caption

**Figure 1. From functional conflict to evolutionary outcome.** SLK separates six inferential levels that are often collapsed. A shared-coordinate conflict is summarized by the compromise load `L`. A differentiated architecture that recovers fraction `s` of that load at cost `K` has global architecture margin `Phi=sL-K`. Positive `Phi` is not an evolutionary verdict: local mutational accessibility can fail even when complete differentiation has positive payoff; frequency-dependent feedback can then shift rare-invasion boundaries away from the intrinsic architecture crossing; and finite-population fixation is governed by a process-specific rule. Under the registered reversible weak-mutation exponential-Moran model, reciprocal fixation ordering and long-run monomorphic occupancy ordering re-align because both depend on the same self-play score difference. Dashed side boxes provide explicit witness conditions for each genuine non-implication. The figure therefore emphasizes both **splits** between successive estimands and the **fixation–occupancy invariant** that appears under the declared stochastic process.

## Reader-facing message

```text
conflict
  ↓
global architecture value
  ↓
local reachability
  ↓
rare invasion
  ↓
finite-population fixation
  ↓
weak-mutation occupancy
```

The downward arrows are handoffs, not logical implications.

## Genuine split witnesses

1. `L>0` but `K>sL` -> real conflict with `Phi<0`.
2. `Phi>0` but `k_local<k<k_global` -> globally favorable but locally inaccessible differentiation.
3. `Phi>0` but `Phi-eta<0` in the declared orientation -> globally favorable architecture that cannot invade when rare.
4. Rare-invasion sign can disagree with reciprocal fixation ordering because invasion depends on `Phi ± eta`, whereas reciprocal fixation ordering in the registered Moran mapping depends on `Phi`.

## Invariant highlighted on the right

For a symmetric pair with self-play scores `u_i,u_j`, the registered exponential-Moran / symmetric rare-mutation model gives

```text
rho(j|i)/rho(i|j) = exp[beta(N-2)(u_j-u_i)]
Pi_j/Pi_i          = exp[beta(N-2)(u_j-u_i)]
```

and therefore

```text
rho(j|i)>rho(i|j)  iff  Pi_j>Pi_i.
```

This is deliberately shown as a convergence rather than another split.

## Scope

The figure does not depict continuous architecture, branching, edgewise topology, spatial migration, or temporal Floquet dynamics. Those remain PAYOFF extensions outside the SLK flagship.