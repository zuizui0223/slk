# SLK prior-art boundary V2 — biology-first framing

## Biological question

The manuscript asks:

> **When functional conflict is real, why does division of labor sometimes evolve and sometimes fail to appear?**

The novelty claim is not that conflict can favor specialization, nor that specialization can fail. The contribution is to treat **persistent multifunctionality under documented conflict** as an inverse diagnostic problem and to separate three experimentally distinguishable explanations:

1. differentiation does not pay;
2. a fitter differentiated state is locally difficult to reach;
3. a favorable and reachable differentiated type cannot establish when rare.

## What is already established

### General theory of division of labor

Rueffler, Hermisson & Wagner (2012) provide direct general theory for when functional specialization and division of labor are favored. They identify positional effects, accelerating performance functions, and synergistic interactions as factors promoting division of labor, and explicitly note that developmental constraints and costs of maintaining differentiated developmental pathways can limit its evolution.

Therefore SLK must **not** claim:
- a first theory that trade-offs can produce specialization;
- a first benefit-versus-cost condition for division of labor;
- a first recognition that developmental constraints or maintenance costs can block specialization.

### Pleiotropy versus specialization

Guillaume & Otto (2012) show that whether genes evolve multifunctionality or specialization depends on functional trade-offs and on how component function maps to fitness. Perfect subfunctionalization after gene duplication requires restrictive conditions, and multifunctional redundancy can persist.

Therefore SLK must **not** claim:
- that strong trade-offs automatically imply specialization;
- that persistent multifunctionality under trade-offs is itself surprising or previously unexplained in every model class.

### Empirical conflict resolution after gene duplication

Des Marais & Rausher (2008) provide an empirical case of escape from adaptive conflict after gene duplication: duplication releases a multifunctional ancestral gene from detrimental pleiotropic effects and permits descendant copies to improve different functions.

This is prior art for division of labor as one route out of adaptive conflict.

### Sexual dimorphism and sex-specific regulation

Work on intralocus sexual conflict shows that sex-biased or sex-specific expression can decouple phenotypes constrained by a shared genome. Ingleby, Flis & Morrow (2015) review sex-biased expression as a mechanism that can help resolve differing male and female optima.

This is prior art for regulatory differentiation as a route out of a shared-function conflict.

### Floral division of labor

Vallejo-Marín et al. (2009) experimentally support a division-of-labor interpretation of heteranthery in *Solanum rostratum*, where different anthers contribute differently to pollen feeding and pollen export.

Kay et al. (2020) are an equally important caution: in *Clarkia*, heteranthery was better supported as staggered pollen presentation than as division of labor. Morphological differentiation therefore does not by itself demonstrate that conflicting functions have been partitioned.

### Trade-off geometry and invasion

Bowers et al. (2005) already combine trade-off geometry with resident-mutant invasion boundaries. Adaptive-dynamics theory more broadly treats establishment through invasion fitness rather than endpoint performance alone.

SLK must therefore **not** claim a first connection between trade-offs and invasion.

### Finite populations and weak mutation

Taylor et al. (2004) distinguish invasion and fixation in finite populations. Fudenberg et al. (2006) analyze long-run evolutionary-game dynamics under strong selection and weak mutation.

Fixation and occupancy are retained only as downstream process extensions.

### Numerical extrapolation

The two-frequency endpoint certificate uses Richardson-type cancellation. Richardson & Gaunt (1927) are prior art for the extrapolation device.

## Empirical anchor: Pedicularis rex

Two existing studies provide a strong biological starting point without supplying a new SLK empirical result.

Sun & Huang (2015) experimentally drained the rainwater held by the cupulate bracts of *Pedicularis rex*. Seed predation increased after drainage, supporting a defensive function of the water-filled bracts.

Sun, Armbruster & Huang (2016) studied floral traits across 14 populations. Greater corolla exsertion was associated with greater stigmatic pollen receipt and also greater seed predation, demonstrating opposing pollinator- and seed-predator-mediated selection.

These studies establish a real conflict around floral presentation and protection. They do **not** establish why that conflict remains integrated. In SLK terms, they motivate the entry problem but do not yet estimate `R`, `K`, local reachability, or rare establishment.

## Defensible residual contribution

The manuscript's contribution is best stated as:

> Existing theories mostly ask which parameters favor specialization. We ask the inverse question posed by an observed multifunctional phenotype: once conflict is documented, which biological stage prevents division of labor?

The answer is organized around three measurements.

~~~text
value:
    Phi = R-K
    Phi < 0 -> differentiation does not pay

reachability:
    g0 = R'(0)-k
    Phi > 0 but g0 < 0 -> fitter endpoint is locally difficult to reach

establishment:
    Delta_R = lim_{p->0} Delta(p)
    Phi > 0, g0 > 0, Delta_R < 0 -> favorable/reachable type fails when rare
~~~

This yields two further predictions:

- conflict magnitude alone cannot rank systems by their tendency toward division of labor when recoverability or architecture cost differs;
- the environmental condition at which division of labor becomes profitable can differ from the condition at which a rare differentiated type can establish.

The formal threshold atlas, witness family, fixation invariant, and uncertainty machinery support these claims but should not be presented as the biological subject of the manuscript.

## Required manuscript language

A defensible positioning paragraph is:

> Theory already explains many conditions that favor division of labor, including performance curvature, positional effects, synergy, pleiotropic trade-offs, developmental constraints, and the costs of differentiated pathways. Empirical studies also document several routes by which shared functions become decoupled, from gene duplication to sexual dimorphism and heteranthery. We address a partly inverse problem. Given a multifunctional structure that remains integrated despite documented opposing selection, what can that persistence mean? We distinguish failure of net value, failure of local reachability, and failure of rare establishment, and show which measurements separate these explanations.

## Citation targets

- Bowers RG, Hoyle A, White A, Boots M. 2005. The geometric theory of adaptive evolution: trade-off and invasion plots. *Journal of Theoretical Biology* 233:363–377.
- Des Marais DL, Rausher MD. 2008. Escape from adaptive conflict after duplication in an anthocyanin pathway gene. *Nature* 454:762–765.
- Fudenberg D, Nowak MA, Taylor C, Imhof LA. 2006. Evolutionary game dynamics in finite populations with strong selection and weak mutation. *Theoretical Population Biology* 70:352–363.
- Guillaume F, Otto SP. 2012. Gene functional trade-offs and the evolution of pleiotropy. *Genetics* 192:1389–1409.
- Ingleby FC, Flis I, Morrow EH. 2015. Sex-biased gene expression and sexual conflict throughout development. *Cold Spring Harbor Perspectives in Biology* 7:a017632.
- Kay KM, Jogesh T, Tataru D, Akiba S. 2020. Darwin's vexing contrivance: a new hypothesis for why some flowers have two kinds of anther. *Proceedings of the Royal Society B* 287:20202593.
- Richardson LF, Gaunt JA. 1927. The deferred approach to the limit. *Philosophical Transactions of the Royal Society of London, Series A* 226:299–361.
- Rueffler C, Hermisson J, Wagner GP. 2012. Evolution of functional specialization and division of labor. *Proceedings of the National Academy of Sciences USA* 109:E326–E335.
- Sun S-G, Huang S-Q. 2015. Rainwater in cupulate bracts repels seed herbivores in a bumblebee-pollinated subalpine flower. *AoB PLANTS* 7:plv019.
- Sun S-G, Armbruster WS, Huang S-Q. 2016. Geographic consistency and variation in conflicting selection generated by pollinators and seed predators. *Annals of Botany* 118:227–237.
- Taylor C, Fudenberg D, Sasaki A, Nowak MA. 2004. Evolutionary game dynamics in finite populations. *Bulletin of Mathematical Biology* 66:1621–1644.
- Vallejo-Marín M, Manson JS, Thomson JD, Barrett SCH. 2009. Division of labour within flowers: heteranthery, a floral strategy to reconcile contrasting pollen fates. *Journal of Evolutionary Biology* 22:828–839.

## Boundary status

The literature boundary is intentionally conservative. Any claim that resembles a general theory of specialization, trade-offs, invasion, fixation, or weak-mutation dynamics should be treated as prior art unless the manuscript is making the narrower diagnostic claim above.
