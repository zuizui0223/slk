"""Source-grounded noncausal Wurmbea 2004 visit/seed contrast tests."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

from analyze_wurmbea_2004_visit_seed_decoupling_v3 import analyze


class PublishedWurmbeaVisitSeedContrastV3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads(
            (ROOT / "data/evidence/wurmbea_2004_visit_to_seed_stage_source_v3.json")
            .read_text(encoding="utf-8")
        )

    def test_source_is_original_publication_and_study_design(self):
        data = self.source
        self.assertEqual(data["source"]["doi"], "10.1086/382796")
        self.assertEqual(
            data["observation_design"]["15_min_periods_by_morph"],
            {"female": 65, "male": 65, "cosexual": 45}
        )
        self.assertTrue(data["observation_design"]["flowering_periods_nonoverlapping"])
        self.assertTrue(data["observation_design"]["sex_system_populations_distinct"])

    def test_opposite_observed_group_ordering(self):
        result = analyze(self.source)
        self.assertTrue(result["same_paper_opposite_ordering"])
        self.assertAlmostEqual(
            result["fly_visits_cosexual_over_female_from_rounded_means"],
            5.1 / 0.7
        )
        lo, hi = result["seed_to_ovule_female_over_cosexual_reported_range_ratio"]
        self.assertAlmostEqual(lo, .24 / .07)
        self.assertAlmostEqual(hi, .25 / .05)
        self.assertLess(lo, hi)

    def test_non_significant_pollen_receipt_not_equivalence(self):
        result = analyze(self.source)
        self.assertEqual(
            result["pollen_deposition_female_vs_cosexual"],
            "NO_SIGNIFICANT_DIFFERENCE_DETECTED"
        )
        self.assertEqual(
            result["hand_cross_supplementation"],
            "NO_SIGNIFICANT_EFFECT_DETECTED"
        )
        self.assertNotIn("POLLEN_EQUIVALENT", json.dumps(result))

    def test_no_per_visit_fitness_or_causal_inference(self):
        result = analyze(self.source)
        for field in ("per_visit_seed_fitness_ratio", "new_p_values",
                      "new_confidence_intervals", "slk_gate_fit",
                      "causal_origin_of_gender_dimorphism"):
            self.assertIsNone(result[field], field)
        self.assertFalse(result["same_season_or_same_individual_comparison"])
        self.assertFalse(result["published_ranges_are_sampling_intervals"])

    def test_unsafe_same_cohort_relabeling_rejected(self):
        for field, value in (
            ("flowering_periods_nonoverlapping", False),
            ("sex_system_populations_distinct", False),
            ("paired_individual_visit_and_seed_records_available", True)
        ):
            altered = copy.deepcopy(self.source)
            altered["observation_design"][field] = value
            with self.assertRaisesRegex(ValueError, "UNSUPPORTED_MATCHED"):
                analyze(altered)

    def test_invalid_rate_or_seed_range_rejected(self):
        altered = copy.deepcopy(self.source)
        altered["fly_visits_per_flower_15min"]["female"]["mean"] = 0
        with self.assertRaisesRegex(ValueError, "ZERO_FLY"):
            analyze(altered)
        altered = copy.deepcopy(self.source)
        altered["female_seed_to_ovule_reported_ranges"]["female"]["min"] = .8
        with self.assertRaisesRegex(ValueError, "INVALID_SEED"):
            analyze(altered)
        altered = copy.deepcopy(self.source)
        altered["fly_visits_per_flower_15min"]["female"]["se"] = -2
        with self.assertRaisesRegex(ValueError, "INVALID_FLY"):
            analyze(altered)

    def test_committed_result_exact_reproduction(self):
        actual = analyze(self.source)
        committed = json.loads(
            (ROOT / "results/wurmbea_2004_visit_seed_decoupling_v3.json")
            .read_text(encoding="utf-8")
        )
        self.assertEqual(actual, committed)

if __name__ == "__main__":
    unittest.main()
