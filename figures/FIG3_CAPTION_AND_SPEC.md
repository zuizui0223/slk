# Figure 3 — empirical measurement ladder

## Caption

**Figure 3. A sequential empirical programme for testing SLK.** Each gate introduces a distinct estimand required for a stronger biological claim. G1 establishes opposing functional geometry on a shared phenotypic coordinate; G2 estimates or bounds the conflict load `L`; G3 quantifies recoverable loss `s` or `R`; G4 places architecture cost `K` on the same fitness scale; and G5 evaluates the global architecture margin `Phi=R-K`. G6 then asks whether the globally superior architecture is locally reachable from the current state. G7 estimates rare-frequency performance and population feedback needed for invasion claims. G8 specifies a finite-population fixation process, while G9 specifies mutation connectivity for weak-mutation occupancy. Failure at a later gate does not invalidate an earlier result; it simply limits the strongest claim that can be made. No single biological system is currently claimed by SLK to have passed G1–G9 end to end.

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
| G6 | local accessibility | mutation/release neighborhood or stepwise intervention path | current state is locally reachable/trapped relative to target architecture |
| G7 | invasion / feedback | rare-frequency assays or frequency-dependent performance | invasion phase is identified under declared population mapping |
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
