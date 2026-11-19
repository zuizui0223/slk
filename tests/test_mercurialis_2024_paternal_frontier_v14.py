"""Reproducibility and inference guards for 2024 Mercurialis sire non-identification.

Both inputs are frozen from the true publisher-MD5-verified 2024 F/H
reproductive cohort; this test does not make any new genetic paternity claim.
"""
import json
import math
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from audit_mercurialis_2024_paternal_identification_frontier_v14 import compute

SOURCE12=ROOT/"results"/"mercurialis_2024_xy_morph_route_bounds_v12.json"
SOURCE13=ROOT/"results"/"mercurialis_2024_maternal_sex_distance_DID_v13.json"
FREEZE=ROOT/"results"/"mercurialis_2024_xy_paternal_identification_frontier_v14.json"
NOTE=ROOT/"docs"/"SLK_MERCURIALIS_2024_PARENTAGE_PARTIAL_IDENTIFICATION_V14_20261117.md"

class SourceVerifiedPaternityNonidentification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v12=json.loads(SOURCE12.read_text(encoding="utf8"))
        cls.v13=json.loads(SOURCE13.read_text(encoding="utf8"))
        cls.d=json.loads(FREEZE.read_text(encoding="utf8"))
        cls.r=compute(cls.v12,cls.v13)

    def test_source_integrity(self):
        self.assertEqual(self.d["publisher_source_doi"],"10.6084/m9.figshare.26521189.v1")
        self.assertEqual(self.d["publisher_MD5"],"365ab41f1d6192344a3b3fec87654e49")
        self.assertEqual(self.v12["n_F_H_with_progeny"],71)
        self.assertEqual(self.v13["main"]["group_germinated"]["H_0.0"],491)
        self.assertEqual(self.v13["main"]["group_germinated"]["H_1.5"],325)

    def test_frozen_values_recompute_from_independent_python(self):
        self.assertEqual(set(self.d),set(self.r))
        for sex in ("H_mothers","F_mothers"):
            for key in ("near_Ylike_range","far_Ylike_range","far_over_near_Ylike_range"):
                self.assertEqual(len(self.r[sex][key]),2)
                for frozen,actual in zip(self.d[sex][key],self.r[sex][key]):
                    self.assertAlmostEqual(frozen,actual,places=12)
            self.assertAlmostEqual(self.d[sex]["far_over_near_known_only"],
                                   self.r[sex]["far_over_near_known_only"],places=12)

    def test_missingness_does_not_establish_sire_paternity(self):
        h=self.d["H_mothers"]
        self.assertAlmostEqual(h["far_over_near_Ylike_range"][0],
                              (41/325)/(211/491),places=12)
        self.assertAlmostEqual(h["far_over_near_Ylike_range"][1],
                              (63/325)/(188/491),places=12)
        self.assertGreater(h["far_over_near_Ylike_range"][1],.50)
        self.assertLess(h["far_over_near_Ylike_range"][1],.51)
        self.assertGreater(self.d["nonnegative_sex_unknowns_always"]
                           ["H_minus_F_difference_in_drops_minimum"],.12)

    def test_two_opposite_mechanisms_exactly_predict_same_observations(self):
        s=self.d["hypothetical_nonidentifiability_scenarios"]
        a=s["A_constant_Y_morph_given_XY_q_half"]
        b=s["B_constant_XY_paternity_share_p_80pct"]
        near=188/491
        far=41/325
        self.assertAlmostEqual(a["assume_q_center"]*a["implied_XY_paternity_share_center"],near)
        self.assertAlmostEqual(a["assume_q_far"]*a["implied_XY_paternity_share_far"],far)
        self.assertAlmostEqual(b["assume_XY_paternity_share_center"]*b["implied_Y_morph_probability_given_XY_center"],near)
        self.assertAlmostEqual(b["assume_XY_paternity_share_far"]*b["implied_Y_morph_probability_given_XY_far"],far)
        self.assertGreater(a["implied_XY_paternity_share_center"],a["implied_XY_paternity_share_far"])
        self.assertEqual(b["assume_XY_paternity_share_center"],b["assume_XY_paternity_share_far"])

    def test_prior_source_fm_cross_shows_nonuniversal_half(self):
        x=self.d["source_controlled_cross_counterexample"]
        self.assertEqual(x["sex_phenotyped_offspring"],49)
        self.assertEqual(x["fertile_males"]+x["male_sterile_males"],5)
        self.assertAlmostEqual(x["Y_like_fraction"],5/49)
        self.assertLess(x["Y_like_fraction"],.11)

    def test_conservative_note_and_valid_source_hypotheses(self):
        t=NOTE.read_text(encoding="utf8")
        for required in ("10.1002/ajb2.16429","10.6084/m9.figshare.26521189.v1",
                         "0.2936〜0.5063","49子中","未測定","自殖","2017年","未検証"):
            self.assertIn(required,t)
        self.assertIn("父性",t)
        self.assertIn("3区画",t)
        self.assertIn("XX",t)

    def test_falsification_mechanism_outside_model(self):
        bad=dict(self.v12)
        bad["zip_md5"]="00000000000000000000000000000000"
        with self.assertRaises(ValueError):
            compute(bad,self.v13)
        bad2=dict(self.v13)
        bad2["source_doi"]="mismatched"
        with self.assertRaises(ValueError):
            compute(self.v12,bad2)

if __name__=="__main__":
    unittest.main()
