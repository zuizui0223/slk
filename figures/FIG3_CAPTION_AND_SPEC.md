# Figure 3 — loss of evolutionary resistance before morphological change

## Reader-facing caption

**Figure 3. Multifunctionality can lose evolutionary resistance before morphology changes.** (A) The `L-Phi` plane separates persistent compromise from positive net architecture value. (B) Convex recovery can create a range in which the differentiated endpoint is fitter but sufficiently small release steps are still downhill. (C) Under positive frequency feedback, structural release and initial abundance lie on one escape frontier, `p_escape(d)=1/2-[dmax/(2eta)][R(d)/d-k]`: `d_J` is its `p=1/2` slice and `p_C` its `d=dmax` slice. Larger favorable structural changes therefore require less demographic support. Negative feedback instead favors rare forms and coexistence. (D) When an environmental gradient lowers marginal architecture cost, profitability precedes local reachability and the escape frontier shifts toward easier reorganization; if positive feedback is strong enough, establishment occurs later still, producing `E_V<E_A<E_I`.

## Scientific role

Figure 3 makes six biological points. First, profitability, evolutionary accessibility, and establishment are different evolutionary transitions and need not occur at the same environmental condition. Second, strict convex recovery can create architecture-path hysteresis, so forward and reverse environmental change can retain different architectures even without frequency dependence. Third, structural novelty and demographic support are coupled: `d_J` and `p_C` are orthogonal slices through one architecture-frequency escape frontier for any positive identity-preserving feedback scaling. Fourth, lowering architecture cost shifts that frontier toward easier escape across this class, while the canonical proportional scaling additionally guarantees that larger favorable structural release monotonically lowers the required initial frequency. Fifth, the limiting process changes along the gradient: the historical-trapping interval is path limited, whereas the ecology-only interval is establishment limited. Sixth, ecology determines whether the population outcome is priority-dependent alternative states (`eta>0`) or stable coexistence through rare-form advantage (`eta<0`).

For the barrier-turnover slice,

```text
k(E)=k0-c(E-E0),  c>0
```

with fixed convex recovery and fixed `eta`,

```text
E_A-E_V=(k_global-k_local)/c
E_I-E_V=eta/(c dmax).
```

If

```text
eta > dmax(k_global-k_local),
```

then

```text
E_V < E_A < E_I,
```

which yields the ordered sequence adaptive integration -> historical trapping -> ecological stabilization. More generally, ecological stabilization is a distinct final early barrier exactly when `Delta_R(E_A)<0`; if `Delta_R(E_A)>0`, rare establishment is already possible when local accessibility is gained, while equality makes the two boundaries coincide. Later re-entry under non-monotonic feedback is outside the displayed monotone slice.

## Claim mapping

- Panel A: C1-C5.
- Panel B: C6.
- Panel C: C7 + UTA1.4f.
- Panel D: ecological barrier-turnover corollary UTA1.4c.
- Fixation/occupancy are downstream extensions and are not part of the three core explanations in Figure 1.

## Anti-overclaim rule

Panel C's escape frontier is exact only for the declared one-dimensional release path with feedback amplitude `eta(d/dmax)`, which vanishes at `d=0` and equals `eta` at `d=dmax`. Panel D is exact for the declared affine `Phi(E)` and locally constant `eta` slice. For smooth non-affine functions it is a local first-order prediction, not a universal constant spacing. Negative-frequency feedback allowing rare invasion with `Phi<0` does not mean the differentiated endpoint is intrinsically superior; in the registered deterministic pair game it identifies the coexistence route. Likewise, positive `eta` delaying rare invasion does not prove permanent historical absence of differentiation.


## Spatial-scope note

The canonical frequency model is not explicitly spatial. Statements about clustered establishment are therefore conditional: if the relevant frequency-dependent interaction is local, the critical frequency `p_C` becomes a local concentration threshold. No claim is made here for a derived spatial wave speed, nucleation radius, or universal spatial critical cluster size.
