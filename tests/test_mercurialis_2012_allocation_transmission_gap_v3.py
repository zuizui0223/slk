"""Original published 10-plot source and exploratory permutation checks."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from reanalyze_mercurialis_2012_pollen_allocation_transmission_gap_v3 import (
    analyze,permutation_split,
)

SOURCE=ROOT/"data/evidence/mercurialis_2008_2012_2024_density_partner_composition_original_v2.json"
OUTPUT=ROOT/"results/mercurialis_2012_pollen_effort_transmission_gap_v3.json"
NOTE=ROOT/"docs/SLK_MERCURIALIS_2012_ACTUAL_PLOT_POLLEN_EFFORT_VS_OFFSPRING_V3_20261115.md"


class RealSourcePlotReanalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.a=analyze(cls.s)

    def test_2012_source_and_10_actual_manipulated_plots(self):
        self.assertEqual(self.a["source_doi"],"10.1371/journal.pone.0035597")
        self.assertEqual(self.a["plot_ids_ordered"],[1,3,8,17,19,4,12,13,15,18])
        self.assertEqual(self.a["low_and_high_plot_counts"],{"low":5,"high":5})
        self.assertEqual(self.s["study_2012"]["plot_count"],20)
        self.assertEqual(self.s["study_2012"]["original_table2"][0]["males"],"absent")

    def test_pollen_allocation_ratio_is_relative_biomass_not_siring(self):
        d=self.a["published_metric_analyses"]["ph"]
        self.assertEqual(d["low_density_five_plot_unweighted_mean"],.188)
        self.assertEqual(d["high_density_five_plot_unweighted_mean"],.106)
        self.assertEqual(d["high_minus_low_from_published_plot_means"],-.082)
        self.assertIn("biomass_to_pollen",d["measurement_semantics"])
        self.assertFalse(self.a["biomass_pollen_allocation_equivalent_to_actual_siring"])

    def test_male_offspring_frequency_diff_small_and_parent_fractions_differ(self):
        d=self.a["published_metric_analyses"]["male"]
        self.assertEqual((d["low_density_five_plot_unweighted_mean"],
                          d["high_density_five_plot_unweighted_mean"]),(.316,.326))
        self.assertEqual(d["high_minus_low_from_published_plot_means"],.01)
        self.assertEqual(self.a["sex_composition_parental_male_share"],
                         {"low":.32653061,"high":.33333333})

    def test_exact_all_252_high_label_combinations_and_new_test_marked(self):
        x=self.a["published_metric_analyses"]
        self.assertEqual({k:v["possible_labelings"] for k,v in x.items()},
                         {"ph":252,"male":252,"female":252})
        self.assertEqual([x[k]["two_sided_extreme_labelings"]
                          for k in ("ph","male","female")],[2,210,222])
        self.assertAlmostEqual(x["ph"]["exploratory_two_sided_permutation_p"],2/252,places=9)
        self.assertAlmostEqual(x["male"]["exploratory_two_sided_permutation_p"],210/252,places=9)
        self.assertAlmostEqual(x["female"]["exploratory_two_sided_permutation_p"],222/252,places=9)
        self.assertTrue(all(z["is_a_new_test_not_original_published_GLMM"] for z in x.values()))

    def test_rounding_bounds_keep_pollen_gap_negative_not_male_response(self):
        x=self.a["published_metric_analyses"]
        self.assertEqual(x["ph"]["printed_2_decimal_group_gap_rounding_bounds"],[-.092,-.072])
        self.assertEqual(x["male"]["printed_2_decimal_group_gap_rounding_bounds"],[0,.02])
        self.assertEqual(x["female"]["printed_2_decimal_group_gap_rounding_bounds"],[-.004,.016])

    def test_explicit_published_male_density_glm_is_not_exploratory_permutation(self):
        self.assertEqual(self.a["2012_published_male_progeny_density_GLM"],
                         {"t":-.54,"p":">.50"})
        self.assertEqual(self.a["published_metric_analyses"]["male"]
                         ["exploratory_two_sided_permutation_p"],.8333333333)
        self.assertFalse(self.a["evidence_no_effect_on_male_offspring_frequency_proven"])

    def test_permutation_relabeling_symmetry_and_small_sample_guard(self):
        x=permutation_split([1,2,3,4,5,6,7,8,9,10],
                            [False]*5+[True]*5)
        self.assertEqual(x["possible_labelings"],252)
        self.assertEqual(x["two_sided_extreme_labelings"],2)
        with self.assertRaisesRegex(ValueError,"EXPECTED_FIVE_VS_FIVE_PLOTS"):
            permutation_split([1]*10,[True]*4+[False]*6)

    def test_corrupt_plot_value_or_row_id_rejected(self):
        b=copy.deepcopy(self.s)
        row=next(r for r in b["study_2012"]["original_table2"] if r["id"]==1)
        row["ph"]=.04
        with self.assertRaisesRegex(ValueError,"PUBLISHED_POLLEN_EFFORT_SEPARATION_CHANGED"):
            analyze(b)
        b=copy.deepcopy(self.s)
        row=next(r for r in b["study_2012"]["original_table2"] if r["id"]==1)
        row["id"]=999
        with self.assertRaisesRegex(ValueError,"PUBLISHED_PLOT_IDS_NOT_MATCHED"):
            analyze(b)

    def test_not_claiming_new_rare_invasion_or_raw_paternity(self):
        self.assertFalse(self.a["offspring_sex_frequency_is_actual_fitness_of_rare_genotype"])
        self.assertIsNone(self.a["SLK_rare_invasion_estimate"])
        self.assertIsNone(self.a["multiple_exploratory_tests_family_wise_adjustment"])
        self.assertIsNone(self.a["novel_individual_observation_data"])
        self.assertEqual(self.a["plot_pollen_alloc_change_and_progeny_change_decouple_in_observed_means"],True)

    def test_tracked_result_matches_recalculation_and_note(self):
        self.assertEqual(self.a,json.loads(OUTPUT.read_text(encoding="utf-8")))
        d=NOTE.read_text(encoding="utf-8")
        for token in ("2012","0.188","0.106","0.316","0.326","252","0.00794",
                      "0.83333","未同定","父性","雌型"):
            self.assertIn(token,d)
        self.assertNotIn("SLKが希少変異の侵入率を直接測定した",d)

if __name__=="__main__":
    unittest.main()
