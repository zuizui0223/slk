"""Regression and source-provenance guards for published *Mercurialis* 2024 stage audit.

No original records are rehosted. Frozen values come from publisher MD5-verified
ZIP, 71 mother-level assays, not from independent n=4826 treatment replicates.
"""
import json
import math
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"analysis"))
from analyze_mercurialis_2024_germination_binomial_v9 import fit

EVIDENCE = ROOT/"results"/"mercurialis_2024_germination_binomial_source_v9.json"
NOTE = ROOT/"docs"/"SLK_MERCURIALIS_REPRODUCTION_BEYOND_SEED_PRIORART_AND_V9_20261117.md"

class GerminationVerifiedV9(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(EVIDENCE.read_text(encoding="utf-8"))
    def test_provenance(self):
        self.assertEqual(self.d["source"],"10.6084/m9.figshare.26521189.v1")
        self.assertEqual(self.d["source_zip_md5"],"365ab41f1d6192344a3b3fec87654e49")
        self.assertTrue(self.d["audit_provenance"]["source_zip_retrieved_and_md5_verified"])
        self.assertFalse(self.d["audit_provenance"]["source_raw_redistributed"])
    def test_mother_and_seed_denominators(self):
        cells=list(self.d["sex_ring"].values())
        self.assertEqual(sum(x["n_mothers"] for x in cells),72)
        self.assertEqual(sum(x["n_assayed"] for x in cells),71)
        self.assertEqual(sum(x["sown"] for x in cells),4826)
        self.assertEqual(sum(x["germinated"] for x in cells),2856)
        self.assertAlmostEqual(self.d["main"]["pooled_germination"],2856/4826)
        self.assertEqual(self.d["main"]["n_mothers"],71)
    def test_grouped_binomial_odds(self):
        x=self.d["main"]; ci=self.d["main_bootstrap"]["distance_OR_95pct"]
        self.assertAlmostEqual(x["distance_odds_ratio_per_m"],math.exp(x["distance_log_odds_per_m"]),places=12)
        self.assertTrue(ci[0] < x["distance_odds_ratio_per_m"] < ci[1] < 1)
        self.assertGreater(x["pearson_dispersion_plant_clustered"],3)
        self.assertEqual(self.d["main_bootstrap"]["successful_mother_resamples"],1200)
    def test_plant_level_sensitivity(self):
        for result in self.d["leave_one_block_out"].values():
            self.assertLess(result["distance_log_odds_per_m"],0)
            self.assertLess(result["n_mothers"],self.d["main"]["n_mothers"])
        self.assertLess(self.d["outer_rings_only"]["distance_log_odds_per_m"],0)
        self.assertLess(self.d["exclude_flagged"]["distance_log_odds_per_m"],0)
    def test_morph_interaction_not_confirmed(self):
        ci=self.d["interaction_bootstrap"]["sex_by_distance_log_odds_95pct"]
        self.assertLess(ci[0],0)
        self.assertGreater(ci[1],0)
        self.assertGreater(self.d["sex_ring"]["F_0.5"]["pooled_germination"],self.d["sex_ring"]["F_1.5"]["pooled_germination"])
        self.assertGreater(self.d["sex_ring"]["H_0.5"]["pooled_germination"],self.d["sex_ring"]["H_1.5"]["pooled_germination"])
    def test_sampling_fraction_not_constant(self):
        a=self.d["sex_ring"]["F_0.5"]["mean_fraction_crop_assayed"]
        b=self.d["sex_ring"]["F_1.5"]["mean_fraction_crop_assayed"]
        self.assertLess(a,.80)
        self.assertGreater(b,.90)
    def test_note_preserves_prior_art_and_access_denial(self):
        s=NOTE.read_text(encoding="utf-8")
        for required in ("10.1111/1365-2745.12659","10.5061/dryad.55186",
                         "401 Unauthorized","403 Forbidden","−0.5727〜+0.0041",
                         "2017","2024","未計数","未確定"):
            self.assertIn(required,s)
    def test_synthetic_grouped_glm(self):
        rs=[]
        for b in ("1","2","3"):
            for sex in ("F","H"):
                for d in (0.,.5,1.5):
                    for i in range(10):
                        logodds=.7-.4*d+(.1 if sex=="F" else 0)+.05*(int(b)-1)+.015*(i-5)
                        n=100
                        y=round(n/(1+math.exp(-logodds)))
                        rs.append({"block":b,"Sex":sex,"dist":d,
                                   "sown":n,"germinated":y})
        output=fit(rs)
        self.assertIsNotNone(output)
        self.assertAlmostEqual(output["distance_log_odds_per_m"],-.4,delta=.05)
        self.assertEqual(output["n_mothers"],180)
        self.assertEqual(output["sown"],18000)

if __name__=="__main__":
    unittest.main()
