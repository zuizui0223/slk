"""V15 biological guard: apparent buffer vs measured evolutionary fitness."""
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from audit_mercurialis_2024_maternal_buffer_v15 import compute
SOURCE=ROOT/"results"/"mercurialis_2024_morph_specific_germinants_v11.json"
FROZEN=ROOT/"results"/"mercurialis_2024_maternal_buffer_v15.json"
NOTE=ROOT/"docs"/"SLK_MERCURIALIS_MATERNAL_BUFFER_V15_20261117.md"

class MaternalBufferOnly(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=json.loads(SOURCE.read_text(encoding="utf8"))
        cls.out=json.loads(FROZEN.read_text(encoding="utf8"))

    def test_canonical_input_and_exact_frozen_recompute(self):
        self.assertEqual(compute(self.source),self.out)
        self.assertEqual(self.out["n_original_F_H_mothers"],72)
        self.assertEqual(self.out["n_model_mothers"],69)
        self.assertEqual(self.out["n_independent_field_blocks"],3)

    def test_mean_center_near_equal_far_descriptive(self):
        d=self.out["descriptive_contrasts"]
        self.assertAlmostEqual(d["H_minus_F_center"],-0.000519793,places=8)
        self.assertAlmostEqual(d["H_minus_F_far"],0.159435525,places=8)
        self.assertGreater(d["H_far_over_F_far"],1.25)
        self.assertLess(d["H_far_over_F_far"],1.26)
        self.assertLess(d["H_center_to_far_percent_change"],0)
        self.assertLess(d["F_center_to_far_percent_change"],d["H_center_to_far_percent_change"])

    def test_not_a_confirmed_adaptive_fitness_crossing(self):
        a=self.out["source_existing_total_interaction"]
        self.assertTrue(a["interval_crosses_zero"])
        self.assertLess(a["conditional_bootstrap_95pct_interval"][0],0)
        self.assertGreater(a["conditional_bootstrap_95pct_interval"][1],0)
        self.assertEqual(self.out["cells"]["H_center"]["n_crop_consistent_mothers"],10)
        self.assertEqual(self.out["cells"]["H_far"]["n_crop_consistent_mothers"],8)
        self.assertGreaterEqual(len(self.out["biological_claim_boundary"]),5)
        text=NOTE.read_text(encoding="utf8")
        for key in ["因果","父性","95%","3区画","2025","2026","全体の適応度"]:
            self.assertIn(key,text)

    def test_altered_sources_cannot_masquerade(self):
        bad=dict(self.source,zip_md5="not publisher verified")
        with self.assertRaises(ValueError):
            compute(bad)

if __name__=="__main__":
    unittest.main()
