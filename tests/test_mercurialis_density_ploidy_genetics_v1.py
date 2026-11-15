"""Source-grounded Mercurialis ecology × QTL validation, no cross-ploidy fit."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from audit_mercurialis_density_and_tradeoff_v1 import compute

SRC=ROOT/"data/evidence/mercurialis_density_ploidy_genetic_tradeoff_v1_20261115.json"
FROZEN=ROOT/"results/mercurialis_density_ploidy_tradeoff_audit_v1.json"
DOC=ROOT/"docs/SLK_MERCURIALIS_PLOIDY_GENETIC_SUPPLY_AND_RARE_ESTABLISHMENT_V1_20261115.md"


class MercurialisPublishedContrasts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src=json.loads(SRC.read_text(encoding="utf-8"))
        cls.s=cls.src["study_blocks"]

    def test_2007_study_is_diploid_male_by_hexaploid_hermaphrodite(self):
        x=self.s["mating_2007"]
        self.assertIn("Allohexaploid",x["female_function_phenotype"])
        self.assertIn("Diploid",x["male_function_phenotype"])
        self.assertIn("4x",x["offspring_male_sired_ploidy"])
        self.assertEqual((x["field2004"]["array_n"],x["field2004"]["array_size"]),(12,100))
        self.assertEqual(x["field2004"]["male_frequencies_tested"],[0,.5])
        self.assertTrue(compute(self.src)["mating_2007"]["rare_male_invasion_directly_observed"] is False)

    def test_2003_density_and_2004_two_factor_trials_are_not_same_test(self):
        d=self.s["mating_2007"]
        self.assertEqual(d["field2003"]["spacing_m"],[.11,.22,.33,.44,.66,1.5])
        self.assertEqual(d["field2004"]["spacing_m"],[.11,.33])
        self.assertEqual(d["field2003"]["outcross_by_spacing"],
                         {"0.11":.68,"0.22":.61,"0.33":.16})
        self.assertEqual(d["field2004"]["original_ANOVA"]["density"]["p"],.5901)
        self.assertEqual(d["field2004"]["original_ANOVA"]["male_presence_by_density"]["p"],.3945)

    def test_original_2004_outcross_33_8_point_difference(self):
        res=compute(self.src)["mating_2007"]
        self.assertAlmostEqual(res["outcross_mean_no_males"],.425)
        self.assertAlmostEqual(res["outcross_mean_half_males"],.763)
        self.assertAlmostEqual(res["outcross_absolute_point_difference"],.338)
        self.assertAlmostEqual(res["outcross_mean_ratio"],.763/.425,places=8)
        self.assertEqual(res["original_presence_F"],15.64)
        self.assertEqual(res["original_presence_p"],.0042)

    def test_conditional_per_pollen_alpha_not_separate_new_significance(self):
        res=compute(self.src)["mating_2007"]
        self.assertAlmostEqual(res["descriptive_per_pollen_siring_alpha"],35.2/21,places=8)
        self.assertEqual(res["lambda_imported_from_2006_other_study"],21)
        self.assertIsNone(res["new_alpha_significance_or_ci"])
        self.assertEqual(res["original_relative_siring_beta"],35.2)

    def test_density_and_male_maintenance_are_model_only(self):
        res=compute(self.src)["mating_2007"]
        self.assertEqual(res["male_invades_below_reported_spacing_approx_model_only"],[.2,.3])
        self.assertEqual(res["male_maintenance_density_approx_model_only"],[4,5])
        self.assertFalse(res["density_threshold_directly_observed"])
        self.assertFalse(res["rare_male_invasion_directly_observed"])

    def test_2026_PNAS_is_diploid_XX_evolution_not_2007_hexaploid(self):
        g=self.s["genetic_2026"]
        res=compute(self.src)["genetic_2026"]
        self.assertEqual((res["diploid_X_only_populations"],res["diploid_XY_control_populations"]),(3,3))
        self.assertEqual((res["shared_common_garden_total_N"],res["trait_model_N"]),(1116,318))
        self.assertEqual(res["evolution_generations"],8)
        self.assertEqual((res["GLMM_generation_beta"],res["GLMM_seed_mass_beta"]),(.09,-.18))
        self.assertIn("XY/Y male determination absent",g["original_sex_chromosome"])

    def test_major_QTL_not_one_gene_or_one_universal_variance_fraction(self):
        x=compute(self.src)["genetic_2026"]
        self.assertEqual([(z["cross"],z["chromosome"],z["reported_variance_percent"])
                         for z in x["published_QTL_variance_by_cross"]],
                         [(1,5,24.1),(2,7,32.0),(4,4,8.03)])
        self.assertIn("same_direction",x["sex_allocation_locus_categories"])
        self.assertIn("one_side_not_significant",x["sex_allocation_locus_categories"])
        self.assertFalse(x["single_gene_pleiotropy_proven"])
        self.assertFalse(x["rare_XY_reinvasion_directly_observed"])

    def test_wild_2026_incidence_increases_but_conditional_degree_not(self):
        g=compute(self.src)["natural_geography_2026"]
        self.assertEqual(g["sexes_with_positive_incidence_distance_gradient"],["female","male"])
        self.assertEqual(g["female_incidence_percent_points_per_km_approx"],.012)
        self.assertEqual(g["male_incidence_percent_points_per_km_approx"],.010)
        self.assertFalse(g["degree_conditional_on_leaky_trend_detected"])
        self.assertIsNone(g["new_geographic_selection_causal_effect"])

    def test_cross_ploidy_bridge_and_raw_files_not_silently_merged(self):
        d=compute(self.src)
        self.assertIsNone(d["cross_ploidy_combined_fitness_estimate"])
        self.assertIsNone(d["same_genotype_density_by_QTL_effect"])
        self.assertFalse(d["SLK_Phi_g0_Delta_R_measured"])
        self.assertFalse(d["raw_individual_reanalysis"])
        self.assertFalse(d["genetic_2026"]["raw_phenotype_and_RadSeq_downloaded"])
        self.assertFalse(d["natural_geography_2026"]["individual_data_downloaded"])
        fw=self.src["inferential_firewall"]
        self.assertTrue(fw["cross_ploidy_cohort_bridge"].startswith("BLOCKED"))
        self.assertIn("not independent",fw["nonindependent_studies"].replace("not independent","not independent"))

    def test_invalid_artificial_frequency_or_ploidy_detected(self):
        d=copy.deepcopy(self.src)
        d["study_blocks"]["mating_2007"]["field2004"]["male_frequencies_tested"]=[0,.01,.5]
        with self.assertRaisesRegex(ValueError,"ORIGINAL_MATING_ARRAY_UNITS_CHANGED"):
            compute(d)
        d=copy.deepcopy(self.src)
        d["study_blocks"]["mating_2007"]["female_function_phenotype"]="Diploid XX"
        with self.assertRaisesRegex(ValueError,"CROSS_PLOIDY_STUDY_BRIDGE"):
            compute(d)
        d=copy.deepcopy(self.src)
        d["study_blocks"]["genetic_2026"]["F2_QTL_crosses"]=5
        with self.assertRaisesRegex(ValueError,"GENETIC_2026_COHORT_CHANGED"):
            compute(d)
        d=copy.deepcopy(self.src)
        d["study_blocks"]["genetic_2026"]["archive"]["raw_files_retrieved"]=True
        with self.assertRaisesRegex(ValueError,"ORIGINAL_SOURCE_SCOPE_UNTRUSTWORTHY"):
            compute(d)

    def test_frozen_reproduction_and_biology_note(self):
        self.assertEqual(compute(self.src),json.loads(FROZEN.read_text(encoding="utf-8")))
        doc=DOC.read_text(encoding="utf-8")
        for token in ("2007","2003","2004","2026","六倍体","二倍体","QTL","33.8","未同定","雄"):
            self.assertIn(token,doc)
        self.assertNotIn("SLKが自然集団における希少変異の固定率を実証した",doc)

if __name__=="__main__":
    unittest.main()
