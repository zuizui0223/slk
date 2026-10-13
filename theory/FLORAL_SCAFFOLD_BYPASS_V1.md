# SLK supplementary biological deduction — a retained scaffold need not retain anther dimorphism

## Ecological question

**If a flower's pollen-feeding versus pollen-export division loses its advantage after a pollinator shift, can mechanical support preserve the differentiated stamens?**

A positive mechanical contribution to buzzing does not by itself answer this. One must compare a *third*, biologically coherent option: **reduce anther dimorphism while retaining the filament scaffold**. This bypass candidate is missing from a simple contrast between an intact heterantherous flower and an unsupported, completely simplified flower.

The question concerns a particular plant–pollinator interaction and its accessible alternative floral forms. It is not a new general theory of modularity, epistasis, evolutionary constraint, or exaptation.

## What the natural intervention establishes — and does not

Fukano & Denda (2026, *Plant Species Biology* 41:e70070, DOI 10.1111/1442-1984.70070) compared *Bredia hirsuta* flower treatments retaining or removing anther and filament components:

- **B, short stamens only:** long anthers and long filaments removed; 12 slipping events in 39 visits and 13 events of ventral stigma contact in 39 visits.
- **D, short stamens + long filaments:** long anthers removed, but long filaments retained; **zero** slipping and **zero** ventral stigma-contact events in 31 visits.
- **C, long stamens only:** short stamens removed, complete long stamens retained; **zero** slips in 26 visits.
- **A, intact:** zero slips in 33 visits.

These selected manipulations show that mechanically useful floral geometry can persist after experimentally removing the **long anther**. The B–D contrast particularly implicates retained long-stamen filaments in stable bee posture. It does not establish that the pollen-bearing long anther is needed for mechanical support, and C rules out a claim that **both stamen classes are indispensable**. Counts are visit-level descriptions from repeatedly visited flowers, not independent whole-plant lifetime-fitness replicates. Stigma-contact patterns are not direct anther-specific siring assays.

**Crucially, treatment D is not an evolved uniform-anther flower**. It is an experimentally altered flower without the long anthers, and its ability to retain stable buzzing does not prove that a heritable, lower-cost scaffold-preserving reduced-dimorphism architecture can arise or reproduce successfully. Conversely, the treatment makes it scientifically unsafe to *assume* that all support function disappears whenever long anthers or anther dimorphism are reduced.

## Four counterfactual architectures, only three needed to expose the problem

Let `a in {0,1}` indicate anatomical differentiation of **pollen-bearing anthers**, not whether pollen or stamens exist. Let `h in {0,1}` denote a mechanically useful filament/grip scaffold. Both axes describe **viable, pollen-bearing hypothetical flowers**, not an emasculated plant. Specifically:

| Architecture | a: dimorphic anthers | h: scaffold | Ecological interpretation |
|---|---:|---:|---|
| G (generalized) | 0 | 0 | Simplified pollen-bearing anthers without specialized support |
| F (filament-preserving bypass) | 0 | 1 | Reduced anther dimorphism with a retained or reconstructed support scaffold |
| H (heterantherous intact) | 1 | 1 | Differentiated pollen-bearing anthers and specialized support |
| U (unsupported heterantherous) | 1 | 0 | Differentiated pollen-bearing anthers with support disrupted |

F is a **hypothetical evolved candidate**, not equivalent to Bredia treatment D. Whether F can develop as a heritable architecture, how many generations it takes to arise, and its complete reproductive fitness are unmeasured. U may also be developmentally hard to construct. The set of **accessible** architectures must therefore be declared in any evolutionary inference.

For a fixed pollinator ecology `z`, define the *illustrative* common-scale, **absolute fitness** contribution relative to generalized G as

```text
W_z(a,h) = pi_z*a + mu_z*h + gamma_z*a*h - c_a*a - c_h*h.
```

- `pi_z`: incremental reproductive return of anther dimorphism when the scaffold is absent, including any residual pollen-class differentiation benefit under pollinator `z`;
- `mu_z`: gain from mechanical/grip support in the generalized-anther background (not a stigma-contact frequency);
- `gamma_z`: additional *interaction* in reproductive return when differentiation and support are combined. This may be positive, zero, or negative; the Bredia behavioral interventions do **not** estimate it;
- `c_a>0`: the **incremental** cost of maintaining dimorphic pollen-bearing anthers versus reduced anthers at fixed scaffold condition;
- `c_h>=0`: cost of a specialized support scaffold.

These terms are on one declared complete-fitness scale; visitation, pollen deposition, fruit set and siring are not individually interchangeable for them. Ecological replacement of pollinators can change `pi_z, mu_z,` and `gamma_z`. Holding costs fixed is an assumption, not a biological necessity.

Then

```text
W(G)=0,
W(F)=mu_z-c_h,
W(H)=pi_z+mu_z+gamma_z-c_a-c_h,
W(U)=pi_z-c_a.
```

## Biological result 1: mechanical support alone does not establish dimorphism maintenance

The difference between an intact differentiated flower and a *scaffold-preserving simplified* candidate is

```text
W(H)-W(F)=pi_z+gamma_z-c_a.
```

**The stand-alone mechanical gain `mu_z` cancels.** Therefore, under an ecology where pollen-class differentiation has no remaining advantage (`pi_z=0`), if an accessible F costs less (`c_a>0`) and there is no positive interaction (`gamma_z=0`), H is selected against relative to F **however strongly the scaffold contributes to floral performance**. The mechanical benefit can select to preserve the filament scaffold **without selecting to preserve dimorphic anthers**.

A concrete model witness sets `pi=0, mu=1.2, gamma=0, c_a=0.3, c_h=0.1`. It yields:

```text
W(G)=0,
W(F)=1.1,
W(H)=0.8,
W(U)=-0.3.
```

A naive *H versus G* comparison (`0.8>0`) would misleadingly imply differentiated anatomy is favored by its secondary mechanical function. Yet the bypass architecture F (`1.1`) performs better than both. This is **not** an estimate for Bredia or Senna; it is the candidate-set logic of the biological question.

## Biological result 2: what would allow differentiation to remain favored?

When F is viable and evolutionarily accessible, a sufficient payoff criterion **within this four-option witness** for H to outperform F is

```text
pi_z+gamma_z>c_a.
```

After the original reward-versus-export division weakens (`pi_z~0`), positive integration between differentiated anthers and support (`gamma_z>c_a`) could keep H favored. For example `gamma=0.5` with the same other numbers gives `W(H)=1.3>W(F)=1.1`. The mere independent benefit `mu_z` **cannot** do this; a genuine *extra benefit of differentiation given the scaffold* is required on this stated fitness model.

The observable signature is the four-architecture interaction contrast

```text
C_z = [W_z(1,1)-W_z(0,1)]
    - [W_z(1,0)-W_z(0,0)]
    = gamma_z.
```

If `C_z>0`, support and anther differentiation are synergistic on the declared fitness scale; `C_z=0` implies additivity. **A change in slip rate for B versus D estimates neither `gamma_z` nor `pi_z`**; it concerns behavior in a narrower manipulation. Furthermore `C_z>0` alone is insufficient for H to win if its incremental cost `c_a` is larger, or if a fifth accessible architecture performs better.

Anatomical differentiation can also persist for a different reason: if F is unavailable because of developmental linkage, ecological constraints, or mutational supply, only a smaller accessible candidate set may matter. However, observed persistence due to absence of F is then **historical/developmental or accessibility dependent**, not proof that mechanical function adaptively favors differentiated anthers.

## A pollinator switch gives opposing, falsifiable predictions

Consider a selective pollen-collecting visitor versus a visitor that indiscriminately exploits both anther classes. The 2024 *Senna arnottiana* study reports the latter behavior for introduced *Bombus terrestris*; it does not quantify these terms.

Three biological possibilities predict different results **after** a shift that lowers `pi_z`:

1. **Scaffold-only maintenance:** bees still need the long-filament support (`mu_z>c_h`), but no genuine support-by-dimorphism interaction remains (`gamma_z~0`). F should outperform H if available and cheaper; long filaments may persist while pollen-bearing anther dimorphism erodes.
2. **Mechanically integrated anther differentiation:** the spatial differences between anther classes contribute an extra complete-cycle fitness benefit to the supported buzzing system (`gamma_z>c_a-pi_z`). H should outperform F under that visitor environment. This interaction has **not** been measured in the cited studies.
3. **Evolutionary legacy:** even if F would now outperform H experimentally, ancestral dimorphism may persist if F is not developmentally accessible or appears too rarely. Its retention would then be a lag/constraint outcome, not the selective advantage of H over all viable alternatives.

The **discriminating experiment** must orthogonally vary functional anther-class differentiation and mechanically useful filaments (or credible inert support replacements) in an otherwise comparable viable pollen-bearing flower. Compare four cell types and visitor ecologies at matched pollen supply and flower age. Measure attractiveness, buzz grip, slip, dorsal/ventral stigma contact, anther-class pollen export, successful transfer to other flowers and *complete-cycle reproductive performance*; do not treat stigma-contact powder as a genetic paternity marker. Replicate over flowers and plants, accounting for repeated visits and nonrandom bee identity. The key endpoint is `W(H)-W(F)` and the interaction `C_z`, not only whether support improves posture when a long anther is absent.

## Prior-art and submission ceiling

Existing multifunctionality, developmental linkage, modular architecture, role reassignment, and exaptation theory anticipate such distinctions (e.g. Farina, Kane & Hernandez 2019; Rueffler, Hermisson & Wagner 2012). The claim here is an **explicit biological counterfactual audit for this floral system**: does supporting *a function* maintain the differentiated *morphological feature*, or can an accessible alternative retain the support without that feature?

The 2026 Bredia paper supports mechanical scaffold behavior but not the `W(H)-W(F)` fitness difference; the 2024 Senna paper supports visitor-dependent anther handling but not subsequent architectural evolution; Merianieae (Dellinger et al. 2021) mainly supports repeated **de novo** heteranthery under changed rewards, not persistence of a differentiated ancestor. No published case cited here identifies the model's `gamma_z` or full candidate-set payoff comparisons. This note is supplemental and should not replace the biology-first manuscript's central comparison; it strengthens the boundary on what the floral empirical bridge currently proves.

References: Fukano & Denda 2026, DOI 10.1111/1442-1984.70070; Rego et al. 2024, DOI 10.1111/plb.13673; Dellinger et al. 2021, DOI 10.1111/evo.14260; Wilkins et al. 2022, DOI 10.1007/s00442-022-05246-0.
