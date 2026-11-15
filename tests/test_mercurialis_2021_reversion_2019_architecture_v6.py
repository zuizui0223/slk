"""Real 2019 architectural paternal costs vs true 2021 experimental reversal.

No new experimental life histories. Original 2021 common-garden historical
cohorts, RMES SSR Table 1 selfing, G5 offspring-sex fatherhood inference and
2019 natural-source 2-group plant inflorescence competition.
"""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from audit_mercurialis_2021_reversion_siring_2019_legacy_v6 import compute

SRC=ROOT/"data/evidence/mercurialis_2019_2021_restored_function_siring_source_v6.json"
FROZEN=ROOT/"results/mercurialis_2021_reversion_2019_siring_architecture_v6.json"
DOC=ROOT/"docs/SLK_MERCURIALIS_REAL_EXPERIMENTAL_REVERSAL_AND_ARCHITECTURAL_LEGACY_V6_20261115.md"


class TrueExperimentalReversionAndMaleArchitectureLegacy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src=json.loads(SRC.read_text(encoding="utf-8"))
        cls.r=compute(cls.src)

    def test_2021_g0_to_g4_actual_control_comparison_not_23fold_relative_base(self):
        r=self.r
        self.assertEqual(r["source_dois"]["experiment_2021"],"10.1016/j.cub.2020.12.028")
        self.assertEqual(r["true_population_evolutionary_replicates"],3)
        self.assertEqual(r["G0_acute_plastic_ratio_vs_same_generation_controls"],2.33)
        self.assertEqual(r["G1_evolved_line_male_flower_ratio_vs_current_controls"],8.77)
        self.assertEqual(r["G4_evolved_line_male_flower_ratio_vs_current_controls"],23.3)
        self.assertAlmostEqual(r["base_to_G4_incidence_difference_percentage_points"],63.82)
        self.assertEqual(self.src["experimental_2021"]["plant_n_per_population"],
                         {"G0":180,"G1_G4":210})

    def test_actual_2021_G1_G4_three_populations_and_six_rmES_controls(self):
        r=self.r["selfing_8_SSR_markers_author_RMES"]
        self.assertEqual(r["G1"]["female_only_population_n"],3)
        self.assertEqual(r["G4"]["female_only_population_n"],3)
        self.assertEqual(r["G1"]["control_population_n"],3)
        self.assertEqual(r["G4"]["control_population_n"],3)
        self.assertEqual([z["author_RMES_selfing_s"] for z in r["G1"]["female_only_population_estimates"]],[.124,.225,.225])
        self.assertEqual([z["author_RMES_selfing_s"] for z in r["G4"]["female_only_population_estimates"]],[.172,.074,.121])
        self.assertEqual(r["G1"]["female_only_reported_n_genotyped"],351)
        self.assertEqual(r["G4"]["female_only_reported_n_genotyped"],355)

    def test_increasing_male_flower_number_does_not_prove_selfing_rate_increased(self):
        x=self.r["selfing_8_SSR_markers_author_RMES"]
        self.assertAlmostEqual(x["G1"]["female_only_unweighted_mean_s"],.191333333,places=8)
        self.assertAlmostEqual(x["G4"]["female_only_unweighted_mean_s"],.122333333,places=8)
        self.assertAlmostEqual(x["G4_minus_G1_female_only_unweighted_mean_s"],-.069)
        self.assertEqual(x["author_test_between_G1_and_G4_p"],.10)
        self.assertFalse(x["increasing_selfing_proven"])
        self.assertIsNone(x["new_selfing_model_fit"])
        self.assertEqual(x["G1"]["female_only_significantly_nonzero_populations"],3)
        self.assertEqual(x["G4"]["female_only_significantly_nonzero_populations"],2)

    def test_real_2021_G0_male_immigrants_not_spontaneous_reappearance(self):
        x=self.r["G0_immigrant_male_progeny"]
        self.assertEqual((x["original_male_n"],x["original_offspring_n"]),(9,812))
        self.assertAlmostEqual(x["male_fraction"],9/812,places=9)
        self.assertTrue(x["confirms_mating_system_not_perfectly_hermetically_sealed"])

    def test_real_2021_G5_male_reintroduction_female_father_fraction(self):
        p=self.r["G5_XY_males_reintroduced_sex_ratio_fatherhood"]
        self.assertEqual(p["reintroduction_mating_arrays"],6)
        self.assertEqual((p["female_plants_per_array"],p["XY_males_per_array"]),(50,50))
        self.assertEqual((p["control_male_progeny_fraction"],p["evolved_XX_mother_male_progeny_fraction"]),(.503,.436))
        self.assertEqual(p["son_deficit_vs_XY_half_sex_ratio"],.064)
        self.assertEqual(p["source_author_inferred_XX_female_sired_fraction"],.128)
        self.assertTrue(p["not_direct_father_genotypes"])
        self.assertTrue(p["selfing_fraction_cannot_be_separated_from_XX_cross"])
        self.assertTrue(p["one_generation_not_male_reinvasion_fixed"])
        self.assertNotEqual(.128,round(2*(.503-.436),3))

    def test_architecture_2019_30_and_12_arrays_independent(self):
        p=self.r["2019_independent_source_architecture_paternal_penalty"]
        self.assertEqual(self.r["source_dois"]["morphology_2019"],"10.1111/ele.13207")
        self.assertEqual((p["exp1_arrays"],p["exp2_arrays"]),(30,12))
        self.assertEqual((p["exp1_original_progeny_sexed"],
                          p["exp2_5_SSR_offspring_genotyped"]),(6000,720))
        self.assertEqual(p["exp1_F_like_paternal_reduction_vs_M_like_with_males"],.25)
        self.assertEqual(p["exp2_F_like_paternal_reduction_vs_M_like"],.31)
        self.assertTrue(p["exp2_equal_selfing_assumption_required"])
        self.assertTrue(p["exp2_M_like_selfing_unidentified"])

    def test_not_same_genetic_architecture_or_cohort_causal_counterfactual(self):
        x=self.r["2019_independent_source_architecture_paternal_penalty"]
        self.assertTrue(x["not_same_cohort_as_2021_selected_XX"])
        self.assertTrue(x["not_isogenic_inflorescence_swap"])
        self.assertIsNone(self.r["rare_genotype_or_historical_origin_SLK_Phi_g0_Delta_R"])
        self.assertFalse(self.r["2021_data_S1_Excel_raw_downloaded"])
        self.assertTrue(self.r["source_2021_initial_seed_origin_20_vs_35_discrepancy_unresolved"])

    def test_wrong_published_2021_paternity_assumption_or_male_sample_fails(self):
        s=copy.deepcopy(self.src)
        s["experimental_2021"]["G5_reintroduced_males"]["author_inferred_fraction_XX_female_sired"]=.134
        with self.assertRaisesRegex(ValueError,"G5_REINTRODUCTION_SOURCE_CHANGED"):
            compute(s)
        s=copy.deepcopy(self.src)
        s["experimental_2021"]["selfing_genotypes"]["G4"]["S2"]["s"]=.900
        with self.assertRaisesRegex(ValueError,"PRINTED_SELFING_AUTHOR_AVERAGES_CHANGED"):
            compute(s)

    def test_false_morphology_reference_or_equal_selfing_assumption_fails(self):
        s=copy.deepcopy(self.src)
        s["architecture_2019"]["exp2"]["assumption"]="M-like selfing directly typed and controlled"
        with self.assertRaisesRegex(ValueError,"2019_ARCHITECTURE_SIRING_EXPERIMENT_CHANGED"):
            compute(s)
        s=copy.deepcopy(self.src)
        s["architecture_2019"]["not_the_2021_evolved_lineages"]=False
        with self.assertRaisesRegex(ValueError,"SOURCE_MORPHOLOGY_INFERENCE_CHANGED"):
            compute(s)

    def test_regenerate_exact_frozen_original_receipt_and_biology_note(self):
        self.assertEqual(self.r,json.loads(FROZEN.read_text(encoding="utf-8")))
        note=DOC.read_text(encoding="utf-8")
        for phrase in ("23.3","69.3%","0.1913","0.1223","12.8%","2019","2021",
                       "25%","31%","G5","自殖","父性","未"):
            self.assertIn(phrase,note)
        self.assertNotIn("SLKが初めて雌雄異株の逆進化を実験で示した",note)


if __name__=="__main__":
    unittest.main()
