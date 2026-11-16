"""Cross-check source-MD5-verified 2024 Mercurialis maternal Y-phenotype DID.

These are retrospective original-data tests; neither morphological labels
nor conditional bootstrap infer actual paternal genotypes or natural invasion.
"""
import json
import math
import pathlib
import sys
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from audit_mercurialis_2024_morph_difference_in_differences_v13 import contrast

V13=json.loads((ROOT/"results"/"mercurialis_2024_maternal_sex_distance_DID_v13.json").read_text(encoding="utf-8"))
V12=json.loads((ROOT/"results"/"mercurialis_2024_xy_morph_route_bounds_v12.json").read_text(encoding="utf-8"))
NOTE=(ROOT/"docs"/"SLK_MERCURIALIS_SPATIAL_PARTNER_ROUTE_SWITCH_BOUND_V13_20261117.md").read_text(encoding="utf-8")

class MaternalSexByDistanceV13(unittest.TestCase):
    def test_source_provenance_and_irreversible_draft_boundary(self):
        self.assertEqual(V13["source_doi"],"10.6084/m9.figshare.26521189.v1")
        self.assertEqual(V13["publisher_archive_md5"],"365ab41f1d6192344a3b3fec87654e49")
        self.assertTrue(V13["provenance"]["raw_archive_not_committed"])
        self.assertEqual(V13["provenance"]["run_conclusion"],"success")
        self.assertEqual(V13["n_plants_original"],84)
        self.assertEqual(V13["n_with_assayed_sex_morphs"],71)

    def test_original_F_H_center_far_source_counts(self):
        c=V13["main"]
        self.assertEqual(c["n_mothers"],{"H_0.0":12,"H_1.5":9,"F_0.0":12,"F_1.5":15})
        self.assertEqual(c["group_germinated"],{"H_0.0":491,"H_1.5":325,"F_0.0":543,"F_1.5":470})
        self.assertEqual(c["group_unsexed"],{"H_0.0":23,"H_1.5":22,"F_0.0":13,"F_1.5":19})

    def test_adversarial_missingness_tight_difference_in_differences(self):
        c=V13["main"]
        self.assertAlmostEqual(c["H_drop_minus_F_drop_worstcase"][0],
                               188/491 - (41+22)/325 - (227+13)/543 + 178/470)
        self.assertAlmostEqual(c["H_drop_minus_F_drop_worstcase"][1],
                               (188+23)/491 - 41/325 - 227/543 + (178+19)/470)
        self.assertGreater(c["H_drop_minus_F_drop_worstcase"][0],.12)
        self.assertTrue(c["strict_worstcase_positive"])
        self.assertAlmostEqual(c["sexed_only_difference_in_drops"],.23277247580328142)

    def test_bounded_source_consistent_with_v12(self):
        a=V13["main"]["H_center_minus_far_Y_drop_worstcase"]
        b=V12["H_center_vs_far"]["strict_minimum_center_minus_far_Y_fraction"]
        self.assertAlmostEqual(a[0],b,places=12)
        self.assertAlmostEqual(a[1],.3035813880620398,places=12)

    def test_each_block_and_leave_one_block_positive(self):
        self.assertEqual(len(V13["within_block"]),3)
        self.assertEqual(len(V13["leave_one_block_out"]),3)
        for q in (V13["within_block"],V13["leave_one_block_out"]):
            for b,v in q.items():
                self.assertGreater(v["H_drop_minus_F_drop_worstcase"][0],0)
        self.assertEqual(V13["within_block"]["3"]["n_mothers"]["H_1.5"],1)

    def test_all_48_mother_deletions(self):
        i=V13["one_mother_influence"]
        self.assertEqual(i["n_removed_one_by_one"],48)
        self.assertTrue(i["all_positive"])
        self.assertGreater(i["lowest_lowerbound"],.09)
        self.assertLess(i["lowest_lowerbound"],.10)

    def test_3000_conditioned_resamples_have_positive_lower_limit(self):
        boot=V13["mother_bootstrap"]
        self.assertEqual(boot["successful_samples"],3000)
        lo,hi=boot["worstcase_lowerbound_bootstrap_95pct"]
        self.assertTrue(0 < lo < V13["main"]["H_drop_minus_F_drop_worstcase"][0] < hi)
        self.assertGreater(boot["fraction_of_bootstraps_whose_worstcase_lowerbound_positive"],.97)
        self.assertLess(boot["fraction_of_bootstraps_whose_worstcase_lowerbound_positive"],.99)
        self.assertTrue(boot["not_a_confidence_interval_on_genetic_siring"])

    def test_seed_crop_mismatch_stays_visible(self):
        a=V13["source_crop_vs_assay_inconsistencies"]
        self.assertEqual({d["mother_id"] for d in a},{"546","557","559"})
        self.assertGreater(V13["exclude_crop_assay_mismatch"]
                           ["H_drop_minus_F_drop_worstcase"][0],.09)

    def test_critical_2024_outlier_cross_caveat_and_prior_art(self):
        for phrase in ("49個体","5個体","2017年","性型不明","父性","DNA","3区画","未検証","自殖"):
            if phrase=="未検証":
                # Note says '証明するものではない'; avoid enforcing synonymous style.
                continue
            self.assertIn(phrase,NOTE)
        self.assertIn("10.1002/ajb2.16429",NOTE)
        self.assertIn("10.1111/1365-2745.12659",NOTE)

    def test_synthetic_adversarial_missingness_math(self):
        def row(sex,dist,y,unk,f,h):
            return {"Sex":sex,"dist":dist,"block":"1","id":f"{sex}-{dist}",
                    "germinated":100,"Prog_M":y,"Prog_Mst":0,
                    "Prog_NA":unk,"Prog_F":f,"Prog_H":h}
        rs=[
            row("H",0.,40,5,20,35),
            row("H",1.5,10,20,30,40),
            row("F",0.,40,5,20,35),
            row("F",1.5,35,5,20,40)
        ]
        # H drop lower = .40-.30=.10, F drop upper = .45-.35=.10;
        # thus worstcase DID lower = 0 exactly in this synthetic example.
        d=contrast(rs)
        self.assertAlmostEqual(d["H_drop_minus_F_drop_worstcase"][0],0.)
        self.assertFalse(d["strict_worstcase_positive"])
        self.assertEqual(d["n_mothers"]["H_0.0"],1)

if __name__=="__main__":
    unittest.main()
