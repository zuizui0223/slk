"""Guard published 2024 ring-distance ecology, proxied pollen failure and cost claims.

Not refitting 2024 original LMM. Uses source coefficient checks,
model-prediction arithmetic and inferences that stop at each stage.
"""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from reconstruct_mercurialis_2024_pollination_distance_v5 import compute

SOURCE=ROOT/"data/evidence/mercurialis_2024_pollen_distance_unfruiting_vs_seed_v5.json"
FROZEN=ROOT/"results/mercurialis_2024_pollen_distance_stage_v5.json"
NOTE=ROOT/"docs/SLK_MERCURIALIS_2024_SPATIAL_POLLINATION_STAGE_FILTER_V5_20261115.md"


class Original2024MercurialisPollenDistances(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.a=compute(cls.d)

    def test_2024_original_doi_ploidy_separate_from_diploid_studies(self):
        self.assertEqual(self.a["source_doi"],"10.1002/ajb2.16429")
        self.assertEqual(self.d["taxon"]["cytotype"],"HEXAPLOID_IBERIAN")
        self.assertIn("unisexual flowers",self.d["taxon"]["sexual_structures"])
        self.assertIsNone(self.a["actual_male_or_female_genotype_frequency_invasion"])

    def test_original_pollen_assay_is_3_times_28_and_only_71_analyzed(self):
        d=self.d["distance_experiment"]
        self.assertEqual(self.a["original_distance_experimental_plants_planted"],84)
        self.assertEqual(self.a["original_analyzed_distance_plants"],71)
        self.assertEqual(d["experimental_replicate_assemblies"],3)
        self.assertEqual(d["ring_each_of_two_distances_each_assembly"],{"female":4,"hermaphrodite":4,"number":8})
        self.assertEqual(d["central_group_each_assembly"],{"male":4,"female":4,"hermaphrodite":4,"number":12})

    def test_direct_stigma_pollen_count_not_performed(self):
        d=self.d["distance_experiment"]
        self.assertTrue(self.a["source_unfruiting_proxy_not_direct_pollen_receipt"])
        self.assertIn("DID NOT develop fruits",d["response_definition"])
        self.assertIn("resource-related fruit failure",d["proxy_observation_warning"])
        self.assertFalse(d["actual_plant_panel_data_available"])

    def test_0_5_and_1_5_meter_original_model_fitted_values(self):
        z=self.a["model_fitted_unfruiting_fraction_by_original_ring"]
        self.assertEqual(z["0.5m"]["published_model_conditional_hermaphrodite"],.194)
        self.assertEqual(z["0.5m"]["published_model_conditional_female"],.247)
        self.assertEqual(z["1.5m"]["published_model_conditional_hermaphrodite"],.278)
        self.assertEqual(z["1.5m"]["published_model_conditional_female"],.331)
        for row in z.values():
            self.assertEqual(row["female_minus_hermaphrodite"],.053)
            self.assertIsNone(row["model_CI_with_covariances"])
            self.assertIn("NOT measured",row["source_level"])

    def test_distance_and_morph_effect_original_CIs_not_independent_combined_CIs(self):
        a=self.a
        self.assertEqual(a["one_meter_difference_both_morphs"],.084)
        self.assertEqual(a["one_meter_slope_95CI_from_original_model"],[.047,.121])
        self.assertEqual(a["female_minus_hermaphrodite_offset"],.053)
        self.assertEqual(a["original_female_offset_95CI"],[.006,.1])
        self.assertEqual((a["original_female_offset_p"],a["original_slope_p"]),(.029,"<0.001"))
        self.assertIsNone(a["full_model_prediction_CIs_without_covariance"])

    def test_interaction_not_detected_does_not_mean_identical_true_slopes(self):
        self.assertEqual(self.a["source_no_detected_morph_distance_interaction_p"],.80)
        self.assertIsNone(self.a["source_morph_by_distance_interaction_effect_estimated"])

    def test_2024_downstream_seed_biomass_effects_non_detected(self):
        self.assertEqual(self.a["source_relative_seed_biomass_morph_test_p"],.58)
        self.assertEqual(self.a["source_relative_seed_biomass_distance_test_p"],.17)
        z=self.d["distance_experiment"]["seed_biomass_followup"]
        self.assertEqual(z["reported_model_observations"],71)
        self.assertIsNone(self.a["full_model_prediction_CIs_without_covariance"])

    def test_2024_independent_common_garden_male_effort_not_paternity(self):
        m=self.a["common_garden_separate_male_effort_ratio"]
        self.assertEqual((m["estimate"],m["CI95"]),(11.7,[11.2,12.9]))
        self.assertIn("NOT actual paternal",m["source_report"])
        self.assertEqual(self.d["separate_morph_common_garden"]["reported_table1_analyzed_by_endpoint"],
                         {"male_flower_biomass":201,
                          "seed_biomass_per_aboveground_biomass":383,
                          "seed_count_per_biomass":383})

    def test_published_narrative_t_vs_p_vs_CI_inconsistency_is_guarded(self):
        x=self.a["source_common_garden_seed_count_model_internal_conflict"]
        self.assertEqual((x["reported_t"],x["reported_df"],x["reported_p"]),
                         (2.91,213,.097))
        self.assertEqual(x["reported_CI"],[-.76,9.46])
        self.assertTrue(x["CI_includes_zero"])
        self.assertTrue(x["t_and_p_cannot_both_be_correct"])
        self.assertIsNone(x["independent_corrected_t"])
        self.assertIsNone(x["new_p_values"])

    def test_restorer_cost_is_simulated_not_source_measured(self):
        a=self.a
        self.assertEqual(a["original_model_required_restorer_cost_rho_simulated_range"],[.15,.4])
        self.assertFalse(a["original_restorer_fitness_cost_measured"])
        self.assertFalse(a["SLK_Phi_g0_Delta_R_measured"])
        self.assertFalse(a["original_2024_raw_109pop_and_71plant_records_downloaded"])
        self.assertEqual(self.d["independent_original_population_survey_and_model"]
                         ["documented_trioecious_populations"],36)

    def test_false_direct_pollen_or_unmeasured_sex_effect_fails(self):
        d=copy.deepcopy(self.d)
        d["distance_experiment"]["response_definition"]="STIGMA POLLEN COUNTS FROM VIDEO"
        with self.assertRaisesRegex(ValueError,"FALSE_DIRECT_STIGMA_POLLEN_ESTIMATE"):
            compute(d)
        d=copy.deepcopy(self.d)
        d["distance_experiment"]["reported_linear_mixed_model"]["female_vs_hermaphrodite_offset"]["estimate"]=-.053
        with self.assertRaisesRegex(ValueError,"INVALID_PUBLISHED_LMM_COEFFICIENT"):
            compute(d)
        d=copy.deepcopy(self.d)
        d["separate_morph_common_garden"]["female_vs_hermaphrodite_seed_count_per_biomass"]["text_reported_p"]=.003
        with self.assertRaisesRegex(ValueError,"ORIGINAL_TEXT_T_P_CI_INCONSISTENCY_NOT_PRESERVED"):
            compute(d)

    def test_frozen_results_and_biology_source_ceiling(self):
        self.assertEqual(self.a,json.loads(FROZEN.read_text(encoding="utf-8")))
        s=NOTE.read_text(encoding="utf-8")
        for word in ("0.5m","1.5m","84","71","11.7","8.4","5.3",
                     "0.0040","CMS","原著","非結実","未"):
            self.assertIn(word,s)
        self.assertNotIn("SLKが野外で稀少変異の侵入率を実測した",s)


if __name__=="__main__":
    unittest.main()
