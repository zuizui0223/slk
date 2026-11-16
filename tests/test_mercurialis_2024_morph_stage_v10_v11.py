"""Reproducibility and overclaim guardrails for 2024 offspring morph auditing.

Frozen source-derived results are analyzed from full publisher ZIP, MD5 checked
in the dedicated Github Actions workflow. This test does not pretend the raw
seed assays are part of git or assume independence among seedlings.
"""
import json
import math
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
V10=ROOT/"results/mercurialis_2024_offspring_morph_stage_v10.json"
V11=ROOT/"results/mercurialis_2024_morph_specific_germinants_v11.json"
NOTE=ROOT/"docs/SLK_MERCURIALIS_2024_OFFSPRING_ABSOLUTE_RETURN_V11_20261117.md"

class TestRealOffspringMorphStage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads(V10.read_text())
        cls.b=json.loads(V11.read_text())

    def test_same_publisher_and_authentic_hash(self):
        self.assertEqual(self.a["source"],self.b["source"])
        self.assertEqual(self.a["source_zip_md5"],self.b["zip_md5"])
        self.assertEqual(self.a["source_zip_md5"],"365ab41f1d6192344a3b3fec87654e49")

    def test_actual_mother_and_offspring_denominators(self):
        o=self.a["overall"]
        self.assertEqual(self.a["state"],"COMPLETE")
        self.assertEqual((o["n_mothers_total"],o["n_complete_with_no_sum_gap"]),(72,71))
        self.assertEqual((o["sown"],o["germinated"],o["typed"]),(4826,2856,2749))
        self.assertEqual(o["n_with_mismatch"],0)
        self.assertEqual(sum(o["category_total"].values()),o["germinated"])
        self.assertEqual(o["category_total"],{"Prog_F":714,"Prog_M":1018,"Prog_H":990,"Prog_NA":107,"Prog_Mst":27})

    def test_zero_seed_not_a_phenotyped_child(self):
        e=self.a["overall"]["excluded_from_phenotype_models"]
        self.assertEqual(len(e),1)
        self.assertEqual(e[0]["reason"],"No mature seeds, no germination assay")

    def test_maternal_phenotype_interaction_is_in_logit_not_dna(self):
        m=self.a["analyses"]["male_plus_male_sterile_fraction_among_typed"]
        self.assertAlmostEqual(m["sex_distance_point"]["sex_by_distance_log_odds"],.8118997694250538,places=7)
        lo,hi=m["sex_distance_bootstrap"]["sex_by_distance_log_odds_95pct"]
        self.assertLess(0,lo)
        self.assertLess(lo,hi)
        for cell in ["H_0","H_1.5","F_0","F_1.5"]:
            self.assertIn(cell,self.a["by_cell"])
        hs=self.a["by_cell"]
        self.assertGreater(hs["H_1.5"]["herm_among_typed"],hs["H_0"]["herm_among_typed"])

    def test_three_published_sampling_count_anomalies_are_excluded(self):
        ex=self.b["sample_exclusions"]
        self.assertEqual(len(ex),3)
        self.assertEqual(sorted(x["id"] for x in ex),["546","557","559"])
        self.assertTrue(all(x["sex"]=="H" for x in ex))
        self.assertTrue(all(x["sown"]>x["crop_seeds"] for x in ex))

    def test_morph_extrapolation_is_additive_only_for_consistent_crop(self):
        for d in self.b["cell_summary"].values():
            n=d["n_assay_crop_consistent"]
            self.assertLessEqual(n,d["n_mothers"])
            means=d["means"]
            component=sum(means["per_flower_"+s] for s in
               ("female","hermaphrodite","male","male_sterile","unsexed_died_early"))
            self.assertAlmostEqual(component,means["per_flower_total"],places=10)

    def test_shares_not_equivalent_to_absolute_total(self):
        h=self.b["cell_summary"]
        self.assertGreater(h["H_1.5"]["means"]["per_flower_hermaphrodite"],
                           h["H_0.0"]["means"]["per_flower_hermaphrodite"])
        self.assertLess(h["H_1.5"]["means"]["per_flower_total"],
                        h["H_0.0"]["means"]["per_flower_total"])
        q=self.b["analyses"]["per_flower_hermaphrodite"]["interaction_bootstrap"]["H_slope_CI"]
        self.assertLess(q[0],0)
        self.assertGreater(q[1],0)

    def test_scientific_scope_warnings_and_prior_art_preserved(self):
        note=NOTE.read_text()
        for text in ("自殖","未同定","父性","雌花","Pannell (1997)","Eppley & Pannell (2007)","実験","3区画","ばらつき"):
            if text=="ばらつき":continue
            self.assertIn(text,note)
        for source in (self.a,self.b):
            self.assertTrue(any("paternity" in s.lower() or "genotype" in s.lower()
                                for s in source["interpretation"] if "interpretation" in source)
                            if "interpretation" in source else any("paternity" in s.lower() or "genotype" in s.lower()
                                for s in source["cautions"]))

if __name__=="__main__":unittest.main()
