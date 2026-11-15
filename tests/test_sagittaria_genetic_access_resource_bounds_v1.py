"""Original-source test of Sagittaria genotype generation and resource plasticity.

Published 2004 rounded sex-ratio table, same-genotype fertilizer contrast,
and independent 2003/2011/2012 ecological endpoints. No new G tests.
"""
import copy
import json
import sys
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from analyze_sagittaria_genetic_access_resource_bounds_v1 import compute, compatible_count_interval

SOURCE=ROOT/"data/evidence/sagittaria_genetic_access_and_ecological_filter_primary_v1.json"
RESULT=ROOT/"results/sagittaria_genetic_access_resource_bounds_v1.json"
NOTE=ROOT/"docs/SLK_SAGITTARIA_GENETIC_ACCESS_ECOLOGICAL_STABILITY_V1_20261115.md"


class SagittariaAccessEcologicalPersistence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.g=cls.d["studies"]["genetic_access_2004"]

    def test_real_cross_families_not_independent_origin_count(self):
        self.assertEqual(self.g["crossing_design"]["F1_seed_families"],18)
        self.assertEqual(self.g["crossing_design"]["F2_and_backcross_families"],23)
        self.assertIn("NOT one linked fitness dataset",self.d["system"]["unit_warning"])
        self.assertEqual(self.g["doi"],"10.1098/rspb.2003.2580")

    def test_original_F2_three_sex_classes_and_model_exception(self):
        d=self.g["f2_and_backcross_original_table2"]["class_a"]
        self.assertEqual((d["n"],d["families"]),(676,8))
        self.assertEqual([d["male_fraction"],d["hermaphrodite_fraction"],d["female_fraction"]],
                         [.48,.26,.26])
        self.assertEqual(d["expected_ratio"],[.5,.25,.25])
        self.assertEqual((d["original_pooled_G"],d["original_p"]),(1.37,.63))
        self.assertEqual(self.g["f1_original_table1"]["dioecious_male_x_monoecious_hermaphrodite"]["original_p"],.01)

    def test_source_rounding_does_not_create_exact_F2_integer_counts(self):
        r=compute(self.d)
        self.assertEqual(r["f2_feasible_integer_ranges"],
                         {"male":[322,327],"hermaphrodite":[173,179],"female":[173,179]})
        self.assertEqual(r["f2_feasible_joint_integer_triples"],33)
        self.assertEqual((r["f2_hermaphroditic_offspring_minimum"],
                          r["f2_hermaphroditic_offspring_maximum"]),(173,179))
        self.assertIsNone(r["new_genotype_access_p_values"])
        self.assertEqual(r["f1_male_x_monoecious_hermaphrodite"]["male_integer_interval"],[101,102])
        self.assertTrue(r["f1_male_x_monoecious_hermaphrodite"]["F1_skew_must_not_be_hidden"])

    def test_females_no_males_but_fertilized_males_can_reexpress_female(self):
        d=self.d["studies"]["sex_expression_resource_2004"]
        self.assertEqual((d["male_clone_genotypes"],d["female_clone_genotypes"]),(23,27))
        self.assertEqual((d["per_genotype_ramets_high"],d["per_genotype_ramets_low"]),(2,2))
        self.assertEqual(d["male_genotypes_with_male_and_female_flowers_high"],10)
        self.assertEqual(d["male_genotypes_reported_male_only_low"],21)
        self.assertEqual(d["female_genotypes_with_male_flowers_either_condition"],0)

    def test_minimum_eight_paired_genotype_reexpression_requires_no_pair_ids(self):
        result=compute(self.d)["resource_same_genotype"]
        self.assertEqual(result["male_genotypes_forced_high_mixed_and_low_male_only_minimum"],8)
        self.assertAlmostEqual(result["minimum_fraction_forced_high_mixed_low_male_only"],8/23,places=8)
        self.assertEqual(result["low_fertilizer_other_genotypes_upper_bound"],2)
        self.assertIsNone(result["low_treatment_mixed_count_exact"])
        self.assertIsNone(result["paired_male_genotype_records_recovered"])
        self.assertIsNone(result["male_genotype_independence_test"])

    def test_family_skew_and_inconstant_male_selfed_deviation_preserved(self):
        d=self.g["noted_departures"]
        self.assertEqual(d["selfed_inconstant_male"]["offspring"],58)
        self.assertEqual(d["selfed_inconstant_male"]["phenotype"],"ALL_HERMAPHRODITE")
        self.assertIn("p=.01",d["excess_f1_hermaphrodites"])

    def test_habitat_sorting_not_same_family_genetic_fitness_comparison(self):
        d=self.d["studies"]["habitat_sorting_2003"]
        self.assertEqual(d["doi"],"10.1111/j.0014-3820.2003.tb00378.x")
        self.assertIn("shaded versus unshaded",d["design"][-1])
        self.assertIn("F1",d["f1_life_history_traits"])
        self.assertIn("not rare-mutant",d["inference"])

    def test_paternity_scheduling_and_female_nutrient_costs_distinct(self):
        a=self.d["studies"]["male_reproductive_performance_2011"]
        b=self.d["studies"]["clonal_tradeoff_2012"]
        self.assertEqual(a["doi"],"10.1111/j.1558-5646.2011.01344.x")
        self.assertIn("approximately linearly",a["reported_outcome"])
        self.assertIn("lifetime male",a["authors_caveat"])
        self.assertEqual(b["n_plants"],412)
        self.assertIn("nitrogen",b["observed_male_investment"])

    def test_no_mutation_rate_or_verified_invasion(self):
        out=compute(self.d)
        for key in ("actual_rare_invasion_rate","historical_gynodioecy_path_fixed",
                    "cross_study_joint_fitness_model"):
            self.assertIsNone(out[key])
        self.assertTrue(out["recombination_or_existing_genotype_segregation_not_new_mutations"])
        self.assertTrue(any("cross-study" in c.lower() or "independent experimental" in c.lower()
                            for c in out["claim_limits"]))

    def test_corrupt_published_fractions_and_counts_rejected(self):
        corrupted=copy.deepcopy(self.d)
        corrupted["studies"]["genetic_access_2004"]["f2_and_backcross_original_table2"]["class_a"]["n"]=500
        with self.assertRaisesRegex(ValueError,"ORIGINAL_F2_STUDY_UNITS_CHANGED"):
            compute(corrupted)
        corrupted=copy.deepcopy(self.d)
        corrupted["studies"]["sex_expression_resource_2004"]["male_genotypes_reported_male_only_low"]=22
        with self.assertRaisesRegex(ValueError,"SOURCE_RESOURCE_PIGEONHOLE_CHANGED"):
            compute(corrupted)
        with self.assertRaisesRegex(ValueError,"INVALID_ORIGINAL_ROUNDED_FRACTION"):
            compatible_count_interval(100,1.5)

    def test_frozen_output_and_biology_note(self):
        self.assertEqual(compute(self.d),json.loads(RESULT.read_text(encoding="utf-8")))
        txt=NOTE.read_text(encoding="utf-8")
        for token in ("Sagittaria","676","173","8/23","施肥","生息地","父性","未取得"):
            self.assertIn(token,txt)
        self.assertNotIn("SLKが野外侵入確率を実測した",txt)

if __name__=="__main__":
    unittest.main()
