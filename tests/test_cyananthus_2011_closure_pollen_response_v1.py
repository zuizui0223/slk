"""Public original 2011 Cyananthus Table 1 and inference-ceiling tests."""
import copy
import json
import math
import sys
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from analyze_cyananthus_2011_closure_pollen_response_v1 import compute
SRC=ROOT/"data/evidence/cyananthus_2011_closure_pollen_response_primary_source_v1.json"
RES=ROOT/"results/cyananthus_2011_closure_pollen_response_v1.json"
NOTE=ROOT/"docs/SLK_CYANANTHUS_TWO_TEMPORAL_BOTTLENECKS_ECOLOGY_V2_20261115.md"


class Cyananthus2011RealOriginalSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(SRC.read_text(encoding="utf-8"))

    def test_verified_original_study_and_flower_nested_design(self):
        d=self.data
        self.assertEqual(d["citation"]["doi"],"10.1093/aob/mcr224")
        self.assertEqual(d["female_experiment"]["female_source_plants"],24)
        self.assertEqual(d["female_experiment"]["initiated_flowers_per_pollen_dose"],72)
        self.assertEqual(d["perfect_experiment"]["initiated_plants"],15)

    def test_2011_female_original_closed_open_rows(self):
        d=self.data["female_experiment"]
        self.assertEqual(d["source_table1_usable"],
            {"10":{"closed":20,"open":32},"20":{"closed":40,"open":23},
             "30":{"closed":41,"open":7}})
        self.assertEqual(sum(v["closed"]+v["open"] for v in d["source_table1_usable"].values()),163)
        self.assertEqual(d["initiated_total"],216)
        self.assertEqual(compute(self.data)["female_source_unusable_n"],53)

    def test_exact_published_chisq_reproduced_without_new_model(self):
        r=compute(self.data)
        self.assertAlmostEqual(r["pearson_chisq_on_published_usable_counts"],23.45108558,places=7)
        self.assertEqual(r["pearson_df"],2)
        self.assertAlmostEqual(r["pearson_p_for_df2"],8.084655e-6,places=10)
        self.assertEqual(r["published_original_chisq"],23.451)

    def test_three_female_doses_and_usable_denominators(self):
        r=compute(self.data)["female_usable_table_rows"]
        self.assertEqual({k:v["usable_n"] for k,v in r.items()},
                         {"10":52,"20":63,"30":48})
        self.assertAlmostEqual(r["10"]["closure_fraction"],20/52,places=8)
        self.assertAlmostEqual(r["20"]["closure_fraction"],40/63,places=8)
        self.assertAlmostEqual(r["30"]["closure_fraction"],41/48,places=8)
        self.assertTrue(r["10"]["closure_fraction"]<r["20"]["closure_fraction"]<r["30"]["closure_fraction"])

    def test_missingness_extremes_preserve_30_vs_10_direction(self):
        result=compute(self.data)
        bounds=result["female_all_initially_treated_closure_fraction_bounds"]
        self.assertEqual(
            {k:v["unknown_outcome_n"] for k,v in bounds.items()},
            {"10":20,"20":9,"30":24}
        )
        self.assertAlmostEqual(bounds["10"]["worst_case_closure_lower"],20/72,places=8)
        self.assertAlmostEqual(bounds["10"]["worst_case_closure_upper"],40/72,places=8)
        self.assertAlmostEqual(bounds["30"]["worst_case_closure_lower"],41/72,places=8)
        self.assertAlmostEqual(bounds["30"]["worst_case_closure_upper"],65/72,places=8)
        self.assertTrue(result["female_30_vs_10_direction_robust_to_any_missing_outcomes"])
        self.assertTrue(result["female_20_vs_10_nonstrict_direction_robust_to_any_missing_outcomes"])
        self.assertFalse(result["female_30_vs_20_direction_robust_to_any_missing_outcomes"])
        # Even if every missing 10-grain flower closed and every missing
        # 30-grain flower stayed open, the 30-grain total exceeds the 10-grain total.
        self.assertGreater(41,40)

    def test_20_grain_female_vs_perfect_cross_morph_response(self):
        comp=compute(self.data)["morph_response_at_20_cross_pollen"]
        self.assertEqual((comp["female_usable_closed"],comp["female_usable_open"]),(40,23))
        self.assertEqual((comp["perfect_usable_closed"],comp["perfect_usable_open"]),(7,19))
        self.assertAlmostEqual(comp["reproduced_pearson_chisq"],9.87603467,places=7)
        self.assertEqual(comp["original_p"],.002)
        self.assertAlmostEqual(comp["female_minimum_closure_fraction_all_72"],40/72,places=8)
        self.assertAlmostEqual(comp["perfect_maximum_closure_fraction_all_30"],11/30,places=8)
        self.assertTrue(comp["female_higher_than_perfect_with_any_missing_outcomes"])
        self.assertFalse(comp["sex_morph_randomized_treatment"])
        self.assertFalse(comp["same_maternal_plant_or_genotype"])

    def test_perfect_ten_grain_fruit_missing_not_zero_seeds(self):
        p=self.data["perfect_experiment"]
        r=compute(self.data)
        self.assertEqual(r["perfect_source_treated_n"],180)
        self.assertEqual(r["perfect_source_usable_n"],98)
        self.assertEqual(r["perfect_source_unusable_n"],82)
        self.assertIn("fruits were lost",p["ten_grain_condition"])
        self.assertEqual(r["perfect_usable_closure_table"]["cross"]["20"]["closure_fraction"],round(7/26,8))
        self.assertEqual(r["perfect_usable_closure_table"]["self"]["30"]["closure_fraction"],.5)

    def test_paired_ring_ample_pollen_is_null_statistical_difference(self):
        r=compute(self.data)["paired_ring_ample_pollen"]
        self.assertEqual(r["perfect"]["pairs"],22)
        self.assertEqual(r["female"]["pairs"],30)
        self.assertAlmostEqual(r["perfect"]["seed_mean_ring_minus_control"],1.86)
        self.assertAlmostEqual(r["female"]["seed_mean_ring_minus_control"],-1.4)
        self.assertEqual((r["perfect"]["original_p"],r["female"]["original_p"]),(.391,.531))

    def test_latency_and_2011_donor_manipulation_claim_limits(self):
        r=compute(self.data)
        self.assertEqual(r["closure_latency_hours"]["female"]["mean"],5.38)
        self.assertEqual(r["closure_latency_hours"]["perfect_cross"]["mean"],6.2)
        self.assertFalse(r["pollen_donor_manipulation_established"])
        self.assertIsNone(r["early_closure_caused_seed_loss_under_low_pollen"])
        self.assertIsNone(r["slk_historical_origin_or_fitness_gate"])
        self.assertIsNone(r["new_plant_cluster_adjusted_p"])
        self.assertIsNone(r["new_confidence_intervals"])
        self.assertTrue(r["different_flower_cohorts_not_one_path"])

    def test_bad_dataset_or_missing_counts_fails(self):
        broken=copy.deepcopy(self.data)
        broken["female_experiment"]["source_table1_usable"]["20"]["closed"]=30
        with self.assertRaisesRegex(ValueError,"ORIGINAL_USABLE_SAMPLE_CHANGED"):
            compute(broken)
        broken=copy.deepcopy(self.data)
        broken["female_experiment"]["source_table1_usable"]["10"]["closed"]=-2
        with self.assertRaisesRegex(ValueError,"INVALID_TABLE_COUNT"):
            compute(broken)
        broken=copy.deepcopy(self.data)
        broken["citation"]["doi"]="unknown"
        with self.assertRaisesRegex(ValueError,"UNEXPECTED_PRIMARY_SOURCE"):
            compute(broken)

    def test_frozen_output_is_exact_recalculation(self):
        self.assertEqual(compute(self.data),json.loads(RES.read_text(encoding="utf-8")))

    def test_biology_note_maintains_stage_and_life_cycle_boundaries(self):
        d=NOTE.read_text(encoding="utf-8")
        for phrase in ("2011","2015","2021","23.451","163","216","花粉","父性","未同定"):
            self.assertIn(phrase,d)
        self.assertNotIn("2011年に花粉提供者の操作を証明した",d)

if __name__=="__main__":
    unittest.main()
