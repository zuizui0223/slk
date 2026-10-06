# Figure 3 — loss of evolutionary resistance before morphological change

## Reader-facing caption

**Figure 3. Multifunctionality can lose evolutionary resistance before morphology changes.** (A) The `L-Phi` plane separates persistent compromise from positive net architecture value. (B) Convex recovery can create a range in which the differentiated endpoint is fitter but sufficiently small release steps are still downhill. (C) Frequency-dependent ecology changes not only the establishment threshold but the population outcome: positive feedback can produce history-dependent alternative stable architectures and, if interactions are local, cluster-assisted establishment, whereas negative feedback can produce stable coexistence through rare-form advantage. (D) When an environmental gradient lowers marginal architecture cost, profitability precedes local reachability. If positive feedback is strong enough, establishment occurs later still, producing `E_V<E_A<E_I` and a distinct ecological-stabilization phase.

## Scientific role

Figure 3 makes four biological points. First, profitability, evolutionary accessibility, and establishment are different evolutionary transitions and need not occur at the same environmental condition. Second, strict convex recovery can create architecture-path hysteresis, so forward and reverse environmental change can retain different architectures even without frequency dependence. Third, persistence can lose robustness before morphology changes: the minimum favorable one-step structural release `d_J` shrinks toward zero at the accessibility boundary, and under positive frequency dependence the critical initial frequency `p_C=(eta-Phi)/(2eta)` shrinks toward zero at rare establishment. Fourth, ecology determines whether the population outcome is priority-dependent alternative states (`eta>0`) or stable coexistence through rare-form advantage (`eta<0`).

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
- Panel C: C7.
- Panel D: ecological barrier-turnover corollary UTA1.4c.
- Fixation/occupancy are downstream extensions and are not part of the three core explanations in Figure 1.

## Anti-overclaim rule

Panel D is exact for the declared affine `Phi(E)` and locally constant `eta` slice. For smooth non-affine functions it is a local first-order prediction, not a universal constant spacing. Negative-frequency feedback allowing rare invasion with `Phi<0` does not mean the differentiated endpoint is intrinsically superior; in the registered deterministic pair game it identifies the coexistence route. Likewise, positive `eta` delaying rare invasion does not prove permanent historical absence of differentiation.


## Spatial-scope note

The canonical frequency model is not explicitly spatial. Statements about clustered establishment are therefore conditional: if the relevant frequency-dependent interaction is local, the critical frequency `p_C` becomes a local concentration threshold. No claim is made here for a derived spatial wave speed, nucleation radius, or universal spatial critical cluster size.
