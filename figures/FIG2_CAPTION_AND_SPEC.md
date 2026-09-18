# Figure 2 — phase map and ecological threshold displacement

## Reader-facing caption

**Figure 2. Architecture value and evolutionary realization occupy different coordinates and can cross at different ecological thresholds.**
(A) The `L-Phi` plane classifies architecture value. `L>0, Phi<0` is persistent compromise, whereas `Phi>0` means the declared differentiated endpoint is globally favored. The `Phi=0` crossing is therefore an architecture-value boundary, not an evolutionary transition boundary. (B) Small-step accessibility introduces a release-path coordinate `d`; for convex recovery, `k_local<k<k_global` creates a region in which sufficiently small release steps are selectively downhill even though complete release has positive payoff. (C) Population feedback introduces `eta`, splitting the static architecture crossing into rare-invasion thresholds at `Phi=±eta`. (D) If an ecological coordinate `E` changes architecture value as `Phi(E)=a(E-E_V)`, the rare-invasion crossing is displaced to `E_I=E_V+eta/a`. Positive `eta` delays rare invasion beyond the environment where differentiation already pays; negative `eta` allows rare invasion before intrinsic endpoint value becomes positive and produces the coexistence ordering in the registered pair game. The distance `eta/a` is therefore a testable ecological separation between value and establishment.

## Scientific role

Figure 2 makes two points.

First, the full SLK hierarchy cannot be projected onto a single `L-Phi` plane. Different biological questions require different coordinates:

```text
architecture value:       L, R, K, Phi
small-step construction:  release-path geometry, k_local
population establishment: eta
ecological displacement:  environmental slope dPhi/dE
finite population:        N, beta, fixation process
long-run occupancy:       mutation graph/kernel
```

Second, those distinct coordinates generate a comparative ecological prediction rather than merely a bookkeeping distinction. Along a common environmental axis, the architecture-value transition and the invasion transition can occur at different locations.

For the registered affine environmental slice,

```text
Phi(E)=a(E-E_V),  a>0
```

one obtains

```text
E_I = E_V + eta/a
E_R = E_V - eta/a.
```

Therefore:

```text
eta>0
-> E_R < E_V < E_I
-> coordination interval
-> differentiation can pay before a rare differentiated type can establish

eta<0
-> E_I < E_V < E_R
-> coexistence interval
-> a rare differentiated type can invade while its intrinsic endpoint margin is still negative.
```

## Claim mapping

- Panel A: C1-C5.
- Panel B: C6.
- Panel C: C7.
- Panel D: ecological corollary UTA1.4.
- Fixation/occupancy remain in Figure 1 because they require explicit stochastic process assumptions.

## Anti-overclaim rule

Panel D is exact for the declared affine `Phi(E)` and locally constant `eta` slice. For smooth non-affine functions it is a local first-order prediction, not a universal constant spacing. Negative-frequency feedback allowing rare invasion with `Phi<0` does not mean the differentiated endpoint is intrinsically superior; in the registered deterministic pair game it identifies the coexistence route. Likewise, positive `eta` delaying rare invasion does not prove permanent historical absence of differentiation.
