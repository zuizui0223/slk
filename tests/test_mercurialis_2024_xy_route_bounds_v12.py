"""Source-receipt regression tests: offspring Y-phenotype is NOT DNA paternity.

Fixtures are frozen, independently reverified outputs from the publisher's
MD5-matched Figshare source archive; original raw data are not rehosted here.
"""
import json
import math
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from audit_mercurialis_2024_xy_pollen_route_bounds_v12 import aggregate,compare

SOURCE = ROOT/"results"/"mercurialis_2024_xy_morph_route_bounds_v12.json"
V10 = ROOT/"results"/"mercurialis_2024_offspring_morph_stage_v10.json"
NOTE = ROOT/"docs"/"SLK_MERCURIALIS_2024_OFFSPRING_XY_ROUTE_SPATIAL_BOUNDS_V12_20261117.md"

class XYMorphBoundsV12(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(SOURCE.read_text(encoding="utf8"))
        cls.v10=json.loads(V10.read_text(encoding="utf8"))

    def test_publisher_archive_and_provenance(self):
        self.assertEqual(self.d["source"],"10.6084/m9.figshare.26521189.v1")
        self.assertEqual(self.d["zip_md5"],"365ab41f1d6192344a3b3fec87654e49")
        self.assertTrue(self.d["provenance"]["source_archive_md5_verified"])
        self.assertTrue(self.d["provenance"]["source_raw_not_redistributed"])
        self.assertEqual(self.d["provenance"]["status"],"completed_success")
        self.assertEqual(self.d["provenance"]["run_id"],43901716042)

    def test_original_71_assays_and_all_107_unknowns(self):
        self.assertEqual(self.d["n_published_field_plants"],84)
        self.assertEqual(self.d["n_F_H_with_progeny"],71)
        self.assertEqual(len(self.d["excluded_zero_seed_mother"]),1)
        cells=self.d["cell_counts_and_worst_case_early_death_bounds"]
        self.assertEqual(sum(z["mothers"] for z in cells.values()),71)
        self.assertEqual(sum(z["germinated"] for z in cells.values()),2856)
        self.assertEqual(sum(z["unsexed_died_early"] for z in cells.values()),107)
        self.assertEqual(sum(z["known_Y_morph"] for z in cells.values()),1045)

    def test_exact_v10_count_agreement_and_bounded_fractions(self):
        cells=self.d["cell_counts_and_worst_case_early_death_bounds"]
        for sex in ("H","F"):
            for dist in ("0","0.5","1.5"):
                a=cells[sex+"_"+dist]
                b=self.v10["by_cell"][sex+"_"+dist]
                self.assertEqual(a["germinated"],b["germinated"])
                self.assertEqual(a["known_Y_morph"],b["category_total"]["Prog_M"]+b["category_total"]["Prog_Mst"])
                self.assertEqual(a["unsexed_died_early"],b["category_total"]["Prog_NA"])
                self.assertAlmostEqual(a["Y_fraction_lower"],a["known_Y_morph"]/a["germinated"],places=12)
                self.assertAlmostEqual(a["Y_fraction_upper"],
                                       (a["known_Y_morph"]+a["unsexed_died_early"])/a["germinated"],places=12)

    def test_strict_worst_case_gap(self):
        d=self.d["H_center_vs_far"]
        self.assertEqual(d["center"]["known_Y_morph"],188)
        self.assertEqual(d["far"]["known_Y_morph"],41)
        self.assertEqual(d["center"]["germinated"],491)
        self.assertEqual(d["far"]["germinated"],325)
        self.assertAlmostEqual(d["strict_minimum_center_minus_far_Y_fraction"],188/491-63/325)
        self.assertGreater(d["strict_minimum_center_minus_far_Y_fraction"],.18)

    def test_three_blocks_and_single_mother_influence(self):
        self.assertEqual(len(self.d["H_center_vs_far_by_block"]),3)
        for v in self.d["H_center_vs_far_by_block"].values():
            self.assertGreater(v["strict_minimum_center_minus_far_Y_fraction"],0)
        for v in self.d["H_center_vs_far_leave_one_block_out"].values():
            self.assertGreater(v["strict_minimum_center_minus_far_Y_fraction"],0)
        j=self.d["H_center_vs_far_leave_one_mother_out_influence"]
        self.assertEqual(j["count"],21)
        self.assertTrue(j["all_leave_one_mother_out_strict_margins_positive"])
        self.assertGreater(j["min_strict_margin"],.15)

    def test_crop_source_discrepancies_explicit(self):
        x=self.d["sown_greater_than_reported_crop_rows"]
        self.assertEqual({z["id"] for z in x},{"546","557","559"})
        self.assertTrue(all(z["mother_sex"]=="H" for z in x))
        self.assertGreater(self.d["H_center_vs_far_excluding_seed_crop_mismatch"]
                           ["strict_minimum_center_minus_far_Y_fraction"],.15)

    def test_v10_mother_sex_interaction_still_only_exploratory(self):
        p=self.v10["analyses"]["male_plus_male_sterile_fraction_among_typed"]
        a=p["sex_distance_point"]["sex_by_distance_log_odds"]
        ci=p["sex_distance_bootstrap"]["sex_by_distance_log_odds_95pct"]
        self.assertGreater(a,0)
        self.assertGreater(ci[0],0)
        self.assertLess(ci[0],a)
        self.assertGreater(ci[1],a)

    def test_mendelian_proxy_is_conditional_and_not_direct_paternity(self):
        note=NOTE.read_text(encoding="utf8")
        for word in ("実測父性","条件付き","DNA","CMS","1母株","自殖"):
            self.assertIn(word,note)
        self.assertIn("10.1002/ajb2.16429",note)
        self.assertIn("10.1111/1365-2745.12659",note)
        self.assertIn("3区画",note)

    def test_synthetic_worst_case_bound_math(self):
        rows_center=[{"germinated":100,"Prog_M":35,"Prog_Mst":5,
                     "Prog_NA":5,"Prog_F":20,"Prog_H":35}]
        rows_far=[{"germinated":100,"Prog_M":10,"Prog_Mst":0,
                  "Prog_NA":20,"Prog_F":30,"Prog_H":40}]
        a=aggregate(rows_center);b=aggregate(rows_far)
        self.assertAlmostEqual(a["Y_fraction_lower"],.40)
        self.assertAlmostEqual(b["Y_fraction_upper"],.30)
        self.assertAlmostEqual(compare(rows_center,rows_far)
                               ["strict_minimum_center_minus_far_Y_fraction"],.10)

if __name__=="__main__":
    unittest.main()
