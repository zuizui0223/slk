"""Real published Wurmbea 1999/2012 aggregate source reproduction.

These tests check only original-author published counts and arithmetic.
1999 tagged individuals != 2012 greenhouse population samples; anthers,
female expression and functional fruit/seed outcome are separate endpoints.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from audit_wurmbea_published_state_plasticity_v1 import (
    audit_wurmbea_published_aggregates,fisher_two_sided,
)

PATH=ROOT/"data/evidence/WURMBEA_1999_2012_REAL_SEX_REEXPRESSION_SOURCE_RECEIPT_V1.json"


class PublishedWurmbeaSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=json.loads(PATH.read_text(encoding="utf-8"))
        cls.r=audit_wurmbea_published_aggregates(cls.source)

    def test_original_tagged_1999_90_plants_and_1983_nonflowering(self):
        self.assertEqual(self.r["1999_tagged"],90)
        self.assertEqual(self.r["1999_1983_reflowered"],68)
        self.assertEqual(self.r["1999_1983_nonflowering"],22)
        self.assertTrue(self.source["original_1999"]["drought_no_aboveground_flowering_1982"])

    def test_within_individual_male_to_bisexual_return_not_new_allele(self):
        self.assertEqual(self.r["1999_male_to_fruiting_male"],14)
        self.assertEqual(self.r["1999_male_reflowered"],28)
        self.assertEqual(self.r["1999_male_to_fruiting_male_fraction"],.5)
        self.assertEqual(self.r["1999_fruiting_male_to_male"],7)
        self.assertEqual(self.r["1999_fruiting_male_reflowered"],23)
        self.assertAlmostEqual(self.r["1999_fruiting_male_to_male_fraction"],7/23)
        self.assertEqual(self.r["1999_females_remaining_female_if_reflowered"],17)

    def test_resource_high_low_are_distinct_phenotypic_male_plants(self):
        g=self.source["original_2012"]["population_groups"]
        self.assertEqual(len(g),4)
        self.assertEqual([x["n"] for x in g],[66,100,50,50])
        self.assertEqual(self.r["2012_subdioecious_high_positive"],33)
        self.assertEqual(self.r["2012_subdioecious_low_positive"],21)
        self.assertEqual(self.r["2012_dioecious_perfect_flower_positive"],0)
        self.assertTrue(self.r["2012_biglandulosa_all_positive"])
        self.assertTrue(self.source["claim_limits"]["different_1999_2012_cohorts_not_same_tagged_individuals"])

    def test_two_sided_exact_aggregate_not_the_authors_one_sided_chi_squared(self):
        r=self.r
        self.assertAlmostEqual(r["2012_resource_absolute_difference"],.24,places=14)
        self.assertAlmostEqual(r["2012_resource_exact_fisher_two_sided"],
                               0.026802559248039502,places=12)
        self.assertAlmostEqual(fisher_two_sided(33,17,21,29),
                               0.026802559248039502,places=12)
        self.assertEqual(self.source["original_2012"]["Wallan_resource_contrast"]
                         ["authors_chisquare_one_tailed_p"],.014)

    def test_original_source_row_sum_drift_fails_closed(self):
        d=json.loads(json.dumps(self.source))
        d["original_1999"]["followup_1983"][1]["count_FM_1983"]+=1
        with self.assertRaisesRegex(ValueError,"PUBLISHED_1999_ROW_SUM_CHANGED"):
            audit_wurmbea_published_aggregates(d,strict=False)

    def test_original_2012_high_resource_effect_not_fabricated_if_mutated(self):
        d=json.loads(json.dumps(self.source))
        d["original_2012"]["population_groups"][1]["high"]["positive"]=32
        with self.assertRaisesRegex(ValueError,"ORIGINAL_2012_WALLAN_COUNTS_CHANGED"):
            audit_wurmbea_published_aggregates(d,strict=True)

    def test_scientific_claim_ceiling(self):
        r=self.source["claim_limits"]
        self.assertTrue(r["published_aggregate_not_original_plant_level_dataset"])
        self.assertTrue(r["different_1999_2012_cohorts_not_same_tagged_individuals"])
        self.assertTrue(r["gender_plasticity_means_expression_not_ancestral_genetic_reacquisition"])
        self.assertTrue(r["no_same_organ_SLK_payoff_or_historic_genetic_ancestral_return"])
        self.assertTrue(self.r["observed_within_lifetime_sex_change_not_native_genetic_regain"])


if __name__=="__main__":
    unittest.main()
