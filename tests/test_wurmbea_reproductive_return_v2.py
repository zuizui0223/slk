"""Life-stage meaning and independently calculated published-table ratios."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
SPEC = importlib.util.find_spec("analyze_wurmbea_reproductive_return_v2")
if SPEC is not None:
    from analyze_wurmbea_reproductive_return_v2 import (
        analyze, compare_groups, stage_indices,
    )


def row(seeds, germination, survival, corm):
    return dict(seeds_mean=seeds, germination_pct_mean=germination,
                survival_pct_mean=survival, corm_mass_mg_mean=corm)


class ReproductiveReturnTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(SPEC, "Stage-matched Wurmbea calculation is missing")

    def test_percent_conversion_and_conditional_survival_once(self):
        # A synthetic cohort with constant within-family values has known totals.
        self.assertEqual(stage_indices(row(100, 50, 20, 3)),
                         [100.0, 50.0, 10.0, 30.0])

    def test_published_open_female_to_fruiting_male_stage_ratios(self):
        result = compare_groups(row(55.3, 96.4, 82.3, 19.0),
                                row(27.2, 80.9, 72.5, 14.2))
        expected = [2.0330882352941178, 2.422616883589035,
                    2.750087855439691, 3.6796950178418397]
        for actual, target in zip(result["stage_ratios"], expected):
            self.assertAlmostEqual(actual, target, places=12)

    def test_crossed_seed_advantage_is_not_the_corm_weighted_advantage(self):
        result = compare_groups(row(60.1, 94.7, 83.3, 20.1),
                                row(42.6, 94.8, 88.5, 21.4))
        self.assertAlmostEqual(result["stage_ratios"][0], 1.4107981220657277)
        self.assertAlmostEqual(result["stage_ratios"][2], 1.3265030267582913)
        self.assertAlmostEqual(result["stage_ratios"][3], 1.2459210671888628)

    def test_self_cross_depression_uses_each_stage_exactly_once(self):
        result = compare_groups(row(20.9, 74.7, 55.7, 13.1),
                                row(42.6, 94.8, 88.5, 21.4))
        self.assertAlmostEqual(1 - result["stage_ratios"][-1],
                               0.8510575826288472, places=12)

    def test_printed_mean_rounding_cannot_explain_reported_point_discrepancy(self):
        result = compare_groups(row(27.2, 80.9, 72.5, 14.2),
                                row(42.6, 94.8, 88.5, 21.4))
        low, high = result["rounding_only_bounds"][-1]
        self.assertLess(low, 0.29618891178421747)
        self.assertGreater(high, 0.29618891178421747)
        self.assertGreater(low, 0.29)
        self.assertLess(high, 0.30)
        self.assertGreater(low, 0.23)

    def test_invalid_probabilities_nonfinite_and_zero_denominator_rejected(self):
        for bad in [row(10, 101, 50, 2), row(10, -1, 50, 2),
                    row(float("nan"), 90, 50, 2), row(True, 90, 50, 2)]:
            with self.assertRaises(ValueError):
                stage_indices(bad)
        with self.assertRaises(ValueError):
            compare_groups(row(10, 90, 50, 2), row(0, 90, 50, 2))

    def test_source_preserves_groups_stages_and_unavailable_uncertainty(self):
        data = json.loads((ROOT / "data/evidence/wurmbea_2006_reproductive_return_source_v2.json").read_text())
        result = analyze(data)
        self.assertEqual(set(result["group_indices"]), {"Ms", "Mo", "Mc", "Fo", "Fc"})
        self.assertIsNone(result["new_confidence_intervals"])
        self.assertIsNone(result["new_p_values"])
        self.assertAlmostEqual(result["comparisons"]["Fo_over_Mo"]["stage_ratios"][2],
                               2.750087855439691, places=12)
        self.assertAlmostEqual(result["comparisons"]["Fc_over_Mc"]["stage_ratios"][2],
                               1.3265030267582913, places=12)
        self.assertEqual(result["source_sampling"]["seedling_families"],
                         {"Ms": 11, "Mo": 10, "Mc": 12, "Fo": 12, "Fc": 12})
        bad = copy.deepcopy(data)
        bad["measurement_semantics"]["germination_and_survival_unit"] = "proportion"
        with self.assertRaises(ValueError):
            analyze(bad)


if __name__ == "__main__":
    unittest.main()
