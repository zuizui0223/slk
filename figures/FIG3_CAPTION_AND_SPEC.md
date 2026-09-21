# Figure 3 — empirical measurement ladder

## Caption

**Figure 3. A sequential empirical programme for testing SLK.** Each gate introduces a distinct estimand required for a stronger biological claim. G1 establishes opposing functional geometry on a shared phenotypic coordinate; G2 estimates or bounds the conflict load `L`; G3 quantifies recoverable loss `s` or `R`; G4 places architecture cost `K` on the same fitness scale; and G5 evaluates the global architecture margin `Phi=R-K`. G6 then asks whether sufficiently small changes toward the globally superior architecture are selectively uphill along a declared release path. G7 estimates rare-frequency performance and population feedback needed for invasion claims. G8 specifies a finite-population fixation process, while G9 specifies mutation connectivity for weak-mutation occupancy. Failure at a later gate does not invalidate an earlier result; it simply limits the strongest claim that can be made. No single biological system is currently claimed by SLK to have passed G1–G9 end to end.

## Purpose

Figure 3 is the empirical counterpart to Figures 1 and 2.

- Figure 1: inferential logic — where criteria split and where they re-align.
- Figure 2: coordinate geometry — which criteria share a phase space and which require new coordinates.
- Figure 3: measurement logic — what an empirical study must measure to move from one claim level to the next.

## Gate table

| Gate | Primary estimand | Minimal design/data need | Strongest justified claim if passed |
|---|---|---|---|
| G1 | shared-axis causal conflict | manipulations or contrasts that isolate opposing function-specific effects on one coordinate | a real conflict exists |
| G2 | `L` | common fitness scale and valid conflict receipt | conflict magnitude is estimated/bounded |
| G3 | `s` or `R` | matched shared vs differentiated comparison | recoverable compromise loss is quantified |
| G4 | `K` | operational architecture-cost definition on same scale | architecture cost is quantified |
| G5 | `Phi=R-K` | G2–G4 on compatible scales | persistent compromise (`Phi<0`) or global differentiated advantage (`Phi>0`) |
| G6 | small-step accessibility | mutation/release neighborhood or stepwise intervention path | sufficiently small changes toward the target are selectively uphill/downhill on the declared path |
| G7 | invasion / feedback | finite rare-D/resident-D assays with endpoint certification; 2–3+ frequency treatments when feedback mechanism/shape is interpreted | invasion phase is certified or left unresolved; internal frequency-response structure is diagnosed only to the measured resolution |
| G8 | fixation | explicit stochastic finite-population process | reciprocal fixation ordering and/or absolute fixation advantage |
| G9 | occupancy | mutation graph and mutation kernel | weak-mutation monomorphic stationary occupancy |

## Anti-shortcut rule

No later gate may be inferred solely from an earlier endpoint comparison. In particular:

```text
Phi>0
!= evidence of local accessibility
!= evidence of rare invasion
!= evidence of fixation
!= evidence of stationary occupancy.
```

Likewise, passing G7 does not determine G8 without a fixation model, and G8 does not determine G9 without a mutation graph/kernel. Under the registered symmetric rare-mutation exponential-Moran model, reciprocal fixation ordering and stationary occupancy ordering coincide, but this is a process-level invariant rather than a generic shortcut.


## Prospective ecological-gradient test

UTA1.4 can be tested by repeating the architecture-value and invasion measurements across an ecological coordinate `E`.

Minimal design:

```text
estimate Phi(E) across contexts
-> locate E_V where Phi crosses 0
-> estimate eta or rare-frequency performance across the same contexts
-> locate E_I where rare-D invasion crosses 0
-> compare observed E_I-E_V with eta / (dPhi/dE).
```

Under the affine registered slice, the prediction is exact:

```text
E_I-E_V=eta/a.
```

For smooth non-affine systems, use the local slope `dPhi/dE` at the architecture-value crossing and treat the formula as a first-order prediction.


## Two-frequency identification design

Within the registered canonical pair,

```text
Delta(p)=Phi+eta(2p-1).
```

Choose symmetric frequencies `p_-=1/2-q` and `p_+=1/2+q`. Then

```text
Phi=[Delta(p_+)+Delta(p_-)]/2
eta=[Delta(p_+)-Delta(p_-)]/(4q).
```

Repeating this crossed frequency design across ecological contexts `E` provides direct estimates of `Phi(E)` and `eta(E)`, which can be used to locate `E_V`, `E_I`, and estimate the local slopes required by UTA1.4b. This identification is conditional on the registered linear-in-frequency pair. Add a balanced-frequency treatment `p=1/2` to test that assumption: with independently measured `Phi`, the three treatments identify `h0`, `eta`, and quadratic curvature `kappa`. Nonzero `h0` or `kappa` rejects the minimal canonical mapping but still yields repaired invasion surfaces under UTA1.7.


## Shape-robust endpoint invasion design

The most general G7 invasion receipt does not require a linear or quadratic frequency fit. With independently measured `Phi`, estimate the endpoint selection limits

```text
Delta_rare = lim_{p->0} Delta(p)
Delta_residentD = lim_{p->1} Delta(p).
```

Then

```text
h_R = Delta_rare-Phi
h_D = Delta_residentD-Phi
```

and invasion is determined directly by the signs of `Delta_rare` and `Delta_residentD`.

Additional interior frequency treatments have a different role: they identify or test the ecological mechanism generating those endpoint offsets. Two symmetric treatments estimate the canonical `eta`; adding `p=1/2` identifies `h0` and quadratic curvature `kappa`; further frequencies test whether the quadratic approximation is adequate.

Thus G7 separates **invasion identification** from **frequency-response mechanism identification**.


## Finite-frequency endpoint certification

Exact endpoint frequencies are not required. For rare-D invasion, first choose a feasible small frequency `epsilon`.

Under a local Lipschitz bound `M_R`,

```text
Delta_R
in
[Delta(epsilon)-M_R epsilon,
 Delta(epsilon)+M_R epsilon].
```

For a stronger second-order design, measure at `epsilon` and `2epsilon`. If local curvature satisfies `|Delta''|<=C_R`,

```text
Delta_R_hat
=
2Delta(epsilon)-Delta(2epsilon)

|Delta_R_hat-Delta_R|
<=
C_R epsilon^2.
```

When measured effects have uncertainty intervals, widen the endpoint interval by the same deterministic remainder. The analogous design applies near `p=1`.

A lower endpoint above zero certifies invasion. An upper endpoint below zero certifies non-invasion. An interval that overlaps zero is **unresolved**, not a biological negative.

This provides a prospective frequency-resolution rule for G7 rather than requiring ideal `p=0` or `p=1` treatments.
