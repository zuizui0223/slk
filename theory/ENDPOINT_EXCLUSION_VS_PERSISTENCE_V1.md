# SLK supplementary audit — endpoint exclusion does not certify persistence of integration

## Biological problem

The original three-gate SLK atlas compares a visibly integrated architecture `S` with a **specified completed** division-of-labour alternative `D`. Its rare-invasion gate `Delta_R<0` certifies that *D cannot increase when introduced at rarity against S*, not that **every possible partly divided architecture** is excluded. This matters for the headline claim that an unchanged multifunctional phenotype can persist for changing reasons along an environmental gradient.

The model already includes a continuum of partial release `d in (0,dmax]`. One must therefore distinguish:

- **Candidate-relative ecological exclusion**: `Delta_w(dmax,0)<0`, concerning a specified endpoint;
- **Resident integration uninvadable under a declared mutation set A**: `Delta_w(d,0)<=0` for **every accessible** `d in A subset (0,dmax]`;
- **Observed morphological persistence**: a historical/demographic statement requiring mutational supply, stochastic persistence, and sufficient time; non-invadability helps but does not prove this observed history.

This is a **logical scope correction** and explicit conditional counterexample, not a new discovery of adaptive dynamics or evolutionary stability.

## The frequency-dependent extension already registered in SLK

For recovery `R(0)=0`, release cost `k(E)d`, ecological feedback `eta>0` and an identity-preserving shape `w(0)=0, w(dmax)=1`, the selection difference of a partial variant against resident integration at frequency `p` is

```text
Delta_w(d,p;E)=R(d)-k(E)d+eta w(d)(2p-1).

At rarity p=0:
H_E(d)=Delta_w(d,0;E)=R(d)-k(E)d-eta w(d).
```

For an architecture continuum available in infinitesimal increments, integration is **not** first-order resistant if there exists a sufficiently small `d>0` with `H_E(d)>0`. In general, `Delta_R(E)=H_E(dmax)` alone cannot determine this.

### Case A — proportional feedback: endpoint exclusion certifies all positive degrees

If `w(d)=d/dmax` and `R` is convex with `R(0)=0`, the secant slope `q(d)=R(d)/d` is nondecreasing. Therefore for every `d in (0,dmax]`,

```text
H_E(d)/d = q(d)-k(E)-eta/dmax
         <= q(dmax)-k(E)-eta/dmax
         = H_E(dmax)/dmax.
```

Hence **if complete division is selected against at rarity, every partial degree is also selected against at rarity** in this proportional-feedback, convex-recovery family. This conclusion is stronger than the original endpoint gate, but still conditional on the stated scalar pathway and feedback. In the original illustrative gradient `R(d)=d+d^2`, `dmax=1`, `k(E)=3-E`, `eta=1.5`:

```text
E_V=1, E_A=2, E_I=2.5.

At E=2.25: H_E(d)=-1.25d+d^2 <0 for every 0<d<=1.
```

Thus the integrated resident can remain resistant to **all** rare partial mutants up to `E_I`. But its putatively favorable `g0>0` only describes the intrinsic (frequency-free) release gradient; **no small rare partial mutant is actually favored** in the purported ecology-only interval. It would be misleading to call this a sequence of realized path-accessibility followed by a wholly separate ecological block.

### Case B — superlinear feedback: positive local release contradicts strict resident stasis

Suppose `R` is differentiable from the right at zero and `w'_+(0)=0`. For every environment with `g0(E)=R'(0)-k(E)>0`,

```text
lim_{d->0+} H_E(d)/d = g0(E)>0.
```

By the definition of this positive limit, there is an `epsilon>0` such that **every sufficiently small positive d is favored when rare**. Even if `H_E(dmax)<0`, the integrated resident is then invasible by partial variants on a continuous accessible release path.

In the *same* numerical witness at `E=2.25`, setting `w(d)=d^2` gives

```text
H_E(d)=0.25d-0.5d^2.

0<d<0.5: H_E(d)>0.
d=1:      H_E(1)=-0.25<0.
```

This is a valid **partial-only invasion** region, not a region in which a monomorphic integrated resident is locally protected against all accessible partial variants. It could still remain *observationally* integrated if such variants do not arise, fail for independent absolute-demographic reasons, or are eliminated later by additional interactions not included in the pairwise model. But their absence is an additional explanation, not a consequence of `Delta_R<0`.

### General escape criterion and interpretation

For any declared accessible set `A`, the relevant necessary and sufficient *one-step relative-invasion resistance* condition is

```text
H_E(d)<=0 for all d in A.
```

The endpoint-only result `H_E(dmax)<0` implies this only under special inequalities, as in Case A. When `A` contains an interval immediately to the right of zero and `H'_+(0)>0`, resident integration necessarily fails local one-step invasion resistance. This says nothing by itself about absolute population rescue, finite-time observation, mutational appearance, fixation, or stability against polymorphic coalitions.

In short, the familiar three labels `Phi<0`, `Phi>0/g0<0`, and `Phi>0/g0>0/Delta_R<0` **are conditional diagnoses about a completed candidate**. They are not automatically three *dynamically realized persistence mechanisms* for an unchanged resident architecture. The distinction remains even when all three threshold crossings satisfy `E_V<E_A<E_I`.

## What the manuscript may legitimately claim

- Functional conflict does not uniquely select structural division over temporal dosing, partial separation, plasticity, or retained integration.
- Relative to a **specified completed divided alternative**, architecture value, intrinsic pathway slope and rare endpoint invasion can cross at different environmental conditions.
- Along a declared cost-lowering convex slice, `E_V<E_A`; under sufficiently strong positive frequency feedback `E_A<E_I` as an ordering of **reference decision surfaces**, not a guarantee of a succession of resident population states.
- A visibly integrated form can persist by different mechanisms in principle, **but an observed three-regime turnover in a single natural system remains to be demonstrated**. When partial variants are available, genuine persistence requires that none has a positive effective rare-invasion advantage, or else additional constraints must be declared and evaluated.

The strongest biological prediction surviving this audit is not that all three hidden causes *must* occur while the phenotype remains identical. It is that **ecological feedback can change which architectural degrees first become invasible**, so completed specialization and early partial differentiation can be temporally decoupled — and the direction of that decoupling depends on partner dependence at the start of specialization.

## Prior art and claim ceiling

Taborsky (2025, *Philosophical Transactions of the Royal Society B* 380:20230262, DOI 10.1098/rstb.2023.0262) reviews preconditions, interdependence, partner coordination, feedback and likely irreversible specialization; the general idea that ecological feedback may constrain division of labour is established. Wahl (2002, *Journal of Theoretical Biology* 219:371–388, DOI 10.1006/jtbi.2002.3133) already develops stable generalist-specialist organization. Futuyma (2010, *Evolution* 64:1865–1884, DOI 10.1111/j.1558-5646.2010.00960.x) discusses evolutionary stasis and constraints. None of these broad premises is a SLK first-discovery claim.

This audit does **not** establish a new universal impossibility theorem: it shows exactly how two permitted feedback families produce opposite answers about integrated resident invasion in the same already registered architecture witness, then corrects the scope of biological interpretation.
