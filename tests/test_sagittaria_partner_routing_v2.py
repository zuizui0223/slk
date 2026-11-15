"""Primary-source reproduction and inference firewall for Sagittaria mating routes.

This validates reported study units, relationships and arithmetic; it is NOT
a genotype-level, meta-analytic, or rare-frequency fitness reanalysis.
"""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from audit_sagittaria_partner_routing_v2 import analyze

SRC=ROOT/"data/evidence/sagittaria_partner_routing_mating_filter_primary_v2_20261115.json"
RESULT=ROOT/"results/sagittaria_partner_routing_realized_paternity_v2.json"
NOTE=ROOT/"docs/SLK_SAGITTARIA_PARTNER_ROUTING_VS_RARE_ESTABLISHMENT_V2_20261115.md"


class SagittariaRouteToRealPaternity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(SRC.read_text(encoding="utf-8"))
        cls.s=cls.d["primary_sources"]

    def test_2006_array_not_independent_dioecy_invasion(self):
        x=self.s["mating_display_2006"]
        self.assertEqual(x["doi"],"10.1098/rspb.2006.3599")
        self.assertEqual((x["array_trials"],x["plants_per_array"],
                          x["total_plant_appearances"]),(20,4,80))
        self.assertEqual((x["flower_visits"],x["foraging_trips"]),(3143,872))
        self.assertAlmostEqual(analyze(self.d)["experimental_transfer_2006"]
                               ["mean_flower_visits_per_trip_computed"],3143/872,places=8)
        self.assertIn("not actual deposited pollen",x["measurement_level"])

    def test_2006_sex_system_by_display_rank_reversal_only_in_proxy(self):
        x=self.s["mating_display_2006"]
        tests=x["published_tests"]
        self.assertEqual(tests["display_times_sex_system_for_interplant_pollen_delivery_proxy"],
                         {"F":4.91,"df1":1,"df2":16,"p":.041})
        self.assertEqual(tests["display_association_monoecious"]["p"],.032)
        self.assertEqual(tests["display_association_dioecious"]["p"],.56)
        out=analyze(self.d)["experimental_transfer_2006"]
        self.assertEqual(out["original_low_display_winner"],"dioecious")
        self.assertEqual(out["original_high_display_winner"],"monoecious")
        self.assertEqual(out["outcome"],"BETWEEN_PLANT_TRANSFER_SEQUENCE_PROXY_NOT_PATERNITY")
        self.assertIsNone(out["relative_lifetime_fitness_ratio"])

    def test_2022_clone_size_adjusted_Bateman_and_samples(self):
        x=analyze(self.d)["bateman_natural_2022"]["sex_function_gradients"]
        self.assertEqual(x["monoecious"]["genet_samples_for_sex_functions"],
                         {"female":25,"male":18})
        self.assertEqual(x["dioecious"]["genet_samples_for_sex_functions"],
                         {"female":16,"male":9})
        self.assertEqual((x["monoecious"]["male_size_adjusted_beta"],
                          x["dioecious"]["male_size_adjusted_beta"]),(1.02,.95))
        self.assertEqual((x["monoecious"]["female_size_adjusted_beta"],
                          x["dioecious"]["female_size_adjusted_beta"]),(.42,.20))

    def test_2022_size_adjustment_changes_sign_not_biological_environment(self):
        out=analyze(self.d)["bateman_natural_2022"]
        x=out["sex_function_gradients"]
        self.assertEqual([x[k]["published_male_minus_female_unadjusted"]
                          for k in ("monoecious","dioecious")],[-.03,-1.28])
        self.assertEqual([x[k]["published_male_minus_female_size_adjusted"]
                          for k in ("monoecious","dioecious")],[.60,.76])
        self.assertTrue(all(x[k]["sign_reversal_after_size_adjustment"]
                            for k in x))
        self.assertEqual(out["male_beta_monoecious_minus_dioecious_descriptive"],.07)
        self.assertIsNone(out["new_equivalence_test_or_p"])
        self.assertFalse(out["cross_sex_effect_measured"])

    def test_2023_modelled_opportunity_does_not_detect_real_siring(self):
        x=analyze(self.d)["temporal_paternity_2023"]
        self.assertEqual((x["genotyped_seeds"],x["paternity_assigned_seeds"]),(358,312))
        self.assertEqual((x["reported_sires_mll"],x["regression_genets"]),(52,39))
        self.assertEqual((x["date_original_p"],x["opportunity_original_p"]),(.92,.24))
        self.assertEqual(x["evidence_for_positive_temporal_proxy_to_realized_siring"],
                         "NOT_DETECTED")
        self.assertFalse(x["temporal_proxy_hypothesis_proven_false"])
        self.assertIsNone(x["spatial_causal_effect_estimated"])

    def test_2002_population_marker_selfing_not_same_cycle_fitness(self):
        d=analyze(self.d)["marker_mating_2002"]
        self.assertEqual(d["population_count_by_system"],
                         {"monoecious":6,"dioecious":6})
        self.assertEqual(d["population_mean_selfing"],
                         {"monoecious":.41,"dioecious":.11})
        self.assertEqual(d["population_mean_marker_inbreeding_depression"],
                         {"monoecious":.83,"dioecious":.84})
        self.assertEqual(d["monoecious_minus_dioecious_selfing_point_difference"],.30)
        self.assertIsNone(d["joint_delta_times_selfing_lifetime_fitness_loss"])

    def test_monociecy_is_not_one_bisexual_flower_and_dioecy_not_one_mutant(self):
        d=self.d["inference_contract"]
        self.assertIn("not a bisexual flower",d["no_morph_equation"])
        self.assertIn("NOT the same single mutant genotype",d["candidate_relative_pairing"])
        self.assertFalse(analyze(self.d)["rare_complete_dioecy_is_one_single_mutant"])

    def test_no_SLK_real_invasion_or_new_significance_or_pooled_effect(self):
        d=analyze(self.d)
        self.assertFalse(d["SLK_Phi_g0_Delta_R_identified"])
        self.assertEqual(d["genet_mutant_frequency_evidence"],"ABSENT")
        self.assertIsNone(d["new_p_values"])
        self.assertFalse(d["individual_original_data_downloaded"])
        self.assertTrue(d["inference_contract"]["pooling_not_permitted"])
        self.assertFalse(d["inference_contract"]["raw_data_reanalysis_performed"])

    def test_wrong_source_direction_or_units_do_not_silently_pass(self):
        bad=copy.deepcopy(self.d)
        bad["primary_sources"]["mating_display_2006"]["flower_visits"]=3144
        with self.assertRaisesRegex(ValueError,"ORIGINAL_VISIT_DENOMINATORS_CHANGED"):
            analyze(bad)
        bad=copy.deepcopy(self.d)
        bad["primary_sources"]["mating_display_2006"]["observed_direction"]["low_display"]="monoecious"
        with self.assertRaisesRegex(ValueError,"VISITOR_ROUTE_DIRECTION_CHANGED"):
            analyze(bad)
        bad=copy.deepcopy(self.d)
        bad["primary_sources"]["natural_bateman_2022"]["original_table1_size_adjusted"]["monoecious"]["male"]["significant"]=False
        with self.assertRaisesRegex(ValueError,"BATEMAN_ADJUSTED_PUBLISHED_SIGNS_CHANGED"):
            analyze(bad)
        bad=copy.deepcopy(self.d)
        bad["inference_contract"]["raw_data_reanalysis_performed"]=True
        with self.assertRaisesRegex(ValueError,"SOURCE_CEILING_VIOLATED"):
            analyze(bad)

    def test_frozen_receipt_and_biological_claim_ceiling(self):
        self.assertEqual(analyze(self.d),json.loads(RESULT.read_text(encoding="utf-8")))
        note=NOTE.read_text(encoding="utf-8")
        for phrase in ("2006","2022","2023","2002","F[1,16]=4.91",
                       "父性","近交弱勢","空間","希少","未"):
            self.assertIn(phrase,note)
        self.assertNotIn("SLKが実測で希少型の侵入率を確定した",note)

if __name__=="__main__":
    unittest.main()
