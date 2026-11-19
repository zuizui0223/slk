"""Published aggregate G0-G8 ecological contrast; no invented genotype fitness."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from audit_mercurialis_g0_g8_return_pressure_v7 import compute

GATE = ROOT / "data/evidence/mercurialis_g0_g8_return_pressure_source_v7.json"
X2021 = ROOT / "data/evidence/mercurialis_2019_2021_restored_function_siring_source_v6.json"
Y2025 = ROOT / "data/evidence/mercurialis_inbreeding_disruption_2025_primary_v1.json"
FROZEN = ROOT / "results/mercurialis_g0_g8_return_pressure_v7.json"
NOTE = ROOT / "docs/SLK_MERCURIALIS_FUNCTION_RETURN_AND_RENEWED_CONFLICT_V7_20261115.md"


class ActualG0G8SexFunctionReturn(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gate, cls.x, cls.y = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in (GATE, X2021, Y2025)
        ]
        cls.result = compute(cls.gate, cls.x, cls.y)

    def test_real_experimental_series_not_three_independent_returns(self):
        r = self.result
        self.assertTrue(r["linked_evolution_program_not_independent_origins"])
        self.assertFalse(r["G4_to_G8_same_individual_longitudinal_data"])
        self.assertEqual(r["G4_male_flower_ratio_vs_contemporaneous_controls"], 23.3)
        self.assertEqual(set(r["original_dois"].values()), {
            "10.1016/j.cub.2020.12.028", "10.1111/nph.70356",
            "10.1111/ele.13207"})

    def test_G5_fatherhood_from_sex_ratio_not_DNA(self):
        r = self.result
        self.assertEqual(r["G5_XX_paternal_fraction_from_offspring_sex_ratio"], .128)
        self.assertFalse(r["G5_measured_individual_XX_fathers_by_SSR"])
        self.assertFalse(r["observed_G8_reversion_to_XX_XY_dioecy"])

    def test_G8_parentage_denominators_not_whole_population_coverage(self):
        r = self.result["G8_paternity"]
        self.assertEqual((r["parents_DNA_extracted"], r["seed_DNA_extracted"]), (181, 958))
        self.assertEqual((r["successfully_genotyped"], r["paternity_assigned"]), (948, 915))
        self.assertEqual((r["not_successfully_genotyped_of_extracted"],
                          r["genotyped_without_father_assignment"]), (10, 33))
        self.assertAlmostEqual(r["assignment_fraction_of_genotyped_not_population_coverage"],
                               915 / 948, places=8)
        self.assertAlmostEqual(r["sampled_paternity_fraction_of_approx_total_seed_population"],
                               915 / 13800, places=8)
        self.assertFalse(r["original_raw_Zenodo_reanalysis"])

    def test_G1_G4_population_RMES_not_comparable_to_G8_individual_selfing(self):
        r = self.result["selfing_estimates_not_longitudinally_comparable"]
        self.assertAlmostEqual(r["G1_2021_mean_of_three_population_RMES"], .191333333, places=8)
        self.assertAlmostEqual(r["G4_2021_mean_of_three_population_RMES"], .122333333, places=8)
        self.assertEqual(r["G4_minus_G1_descriptive_not_significant"], -.069)
        self.assertEqual(r["G1_G4_author_difference_p"], .1)
        self.assertEqual(r["G8_2025_mean_of_172_individual_selfing_fractions"], .296)
        self.assertTrue(r["SSR_methods_differ_8_vs_9_loci"])
        self.assertFalse(r["G4_to_G8_selfing_change_estimable"])

    def test_G8_scenario_curvature_not_new_fitness_or_diploid_delta(self):
        r = self.result
        q = r["G8_relative_total_fitness_quadratic_from_original_table1"]
        self.assertEqual([q[k]["arithmetic_delta1_minus_delta0_no_new_inference"]
                          for k in ("small", "medium", "large")], [.47, 1.62, 2.79])
        self.assertEqual([q[k]["published_delta1_quadratic_significant"]
                          for k in ("small", "medium", "large")], [False, True, True])
        self.assertTrue(all(not q[k]["published_delta0_quadratic_significant"]
                            for k in q))
        self.assertFalse(r["G8_actual_diploid_inbreeding_depression_measured"])
        self.assertFalse(r["rare_mutant_invasion_or_SLK_Phi_g0_Delta_R_estimated"])

    def test_bad_DOI_or_false_matched_cohort_is_rejected(self):
        g = copy.deepcopy(self.gate)
        g["study_relationships"]["longitudinal_individual_matched_G4_G8"] = True
        with self.assertRaisesRegex(ValueError, "FALSE_INDEPENDENCE"):
            compute(g, self.x, self.y)
        g = copy.deepcopy(self.gate)
        g["study_relationships"]["published_g8_fitness_2025_doi"] = "10.1111/incorrect"
        with self.assertRaisesRegex(ValueError, "ORIGINAL_STUDY"):
            compute(g, self.x, self.y)

    def test_false_delta_measurement_or_paternity_counts_rejected(self):
        y = copy.deepcopy(self.y)
        y["fitness_estimands"]["diploid_actual_delta"] = .5
        with self.assertRaisesRegex(ValueError, "G8_DELTA_OBSERVED"):
            compute(self.gate, self.x, y)
        y = copy.deepcopy(self.y)
        y["experiment"]["assigned_paternity_seeds"] = 948
        with self.assertRaisesRegex(ValueError, "G8_DIRECT_PATERNITY"):
            compute(self.gate, self.x, y)

    def test_frozen_result_reproduces_and_Japanese_note_retains_scope(self):
        self.assertEqual(self.result, json.loads(FROZEN.read_text(encoding="utf-8")))
        note = NOTE.read_text(encoding="utf-8")
        for s in ("G0", "G4", "G5", "G8", "12.8%", "915", "948", "13,800",
                  "29.6%", "δ=1", "0.1223", "未測定", "未確認", "未観測"):
            # The final note may use equivalent explicit "not observed" wording.
            if s == "未観測":
                self.assertIn("観測されていない", note)
            else:
                self.assertIn(s, note)
        self.assertNotIn("G8で雌雄異株への再進化を直接実証した", note)


if __name__ == "__main__":
    unittest.main()
