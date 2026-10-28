"""F2 allometry versus constrained organ reassembly, author-source data tests.

Original Johns et al. (2024) Aquilegia Supplementary Material 3,
DOI 10.1186/s13227-024-00225-3. No QTL genotype or pollen fitness.
"""
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"analysis"))
from audit_aquilegia_f2_partial_reassembly_v1 import load_rows
from audit_aquilegia_f2_allometry_v5 import (
    analyse_mosaic_allometry, fit_binomial_logit, prepare_original_flowers
)

SOURCE=Path(__file__).resolve().parents[1]/"data/external/johns2024_aquilegia_f2_phenotypes_source.csv"


class AquilegiaOrganSizeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=load_rows(SOURCE)
        cls.r=analyse_mosaic_allometry(cls.rows,strict=True)

    def test_original_plant_and_flower_denominators(self):
        s=self.r["source"]
        self.assertEqual((s["F2_plants"],s["flowers"],s["whorl_score_rows"]),(231,400,800))
        self.assertEqual((s["flowers_with_stamen_count"],s["flowers_missing_stamen_count"]),(367,33))
        self.assertEqual((s["one_per_plant_with_stamen_count"],s["one_per_plant_missing_stamen_count"]),(211,20))
        self.assertEqual(s["size_tertile_cutoffs_calculated_on_all_available_flowers"],[37,43])
        self.assertTrue(s["missing_stamen_count_not_assigned_zero"])

    def test_three_actual_size_classes_have_mixed_organ_configuration(self):
        x=self.r["first_flower_per_genotype"]
        self.assertEqual({k:(v["n"],v["mosaic_count"])
                          for k,v in x["allometry_classes"].items()},
                         {"low":(67,17),"middle":(72,26),"high":(72,28)})
        self.assertEqual(x["sample_n"],211)
        self.assertEqual(x["mosaic_phenotypes"],71)
        self.assertEqual(x["full_nesting_exception_count"],1)
        self.assertEqual([x["allometry_classes"][k]["full_nesting_exceptions"]
                          for k in ("low","middle","high")],[1,0,0])
        self.assertEqual([x["allometry_classes"][k]["anther_inner_only_violations"]
                          for k in ("low","middle","high")],[0,0,0])

    def test_logit_mosaic_vs_stamen_count_is_uncertain_not_an_effect(self):
        x=self.r["first_flower_per_genotype"]["unadjusted_logit"]
        self.assertAlmostEqual(x["OR_per_10_stamens"],1.204217770027566,places=10)
        self.assertAlmostEqual(x["lower_95_percent_Wald_CI"],0.8358264422388334,places=10)
        self.assertAlmostEqual(x["upper_95_percent_Wald_CI"],1.7349779384411883,places=10)
        self.assertLess(x["lower_95_percent_Wald_CI"],1)
        self.assertGreater(x["upper_95_percent_Wald_CI"],1)
        self.assertFalse(x["independent_genetic_effect_inferred"])

    def test_flower_count_and_morphology_are_not_independent_genotypes(self):
        x=self.r["all_scored_flowers"]["allometry_classes"]
        self.assertEqual([x[k]["n"] for k in ("low","middle","high")],[126,127,114])
        self.assertEqual([x[k]["full_nesting_exceptions"]
                          for k in ("low","middle","high")],[1,0,0])
        self.assertEqual([x[k]["mosaic_count"]
                          for k in ("low","middle","high")],[32,45,42])
        self.assertFalse(self.r["biological_ceiling"]["400_flowers_equal_400_independent_genotypes"])

    def test_synthetic_null_logistic_has_zero_size_coefficient(self):
        y=[0,1]*5
        x=[-2,-2,-1,-1,0,0,1,1,2,2]
        fit=fit_binomial_logit(x,y)
        self.assertAlmostEqual(fit["slope"],0,places=9)
        self.assertAlmostEqual(fit["OR"],1,places=9)

    def test_zero_or_missing_flower_size_is_not_valid_observation(self):
        data=[dict(r) for r in self.rows]
        data[0]["stamens"]="NA"
        data[1]["stamens"]="NA"
        x=analyse_mosaic_allometry(data,strict=False)
        self.assertEqual(x["source"]["flowers_missing_stamen_count"],34)
        data2=[dict(r) for r in self.rows]
        data2[0]["stamens"]="-2"
        data2[1]["stamens"]="-2"
        with self.assertRaisesRegex(ValueError,"INVALID_STAMEN_COUNT"):
            analyse_mosaic_allometry(data2,strict=False)

    def test_no_source_data_means_no_conclusions_about_slk_anto_joint_selection(self):
        b=self.r["biological_ceiling"]
        for key,value in b.items():
            self.assertFalse(value, key)


if __name__=="__main__":
    unittest.main()
