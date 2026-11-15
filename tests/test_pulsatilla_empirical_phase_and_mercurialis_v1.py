"""Primary-source unit audit: Pulsatilla phases vs Mercurialis conditional fitness."""
import json
import sys
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from recompute_pulsatilla_2025_phase_turnover_v1 import compute, count_from_p

P=ROOT/"data/evidence/pulsatilla_sexual_conflict_multi_paper_primary_v1.json"
M=ROOT/"data/evidence/mercurialis_inbreeding_disruption_2025_primary_v1.json"
R=ROOT/"results/pulsatilla_2025_published_phase_turnover_v1.json"
NOTE=ROOT/"docs/SLK_NATURAL_CONFLICT_ROUTES_AND_PRIOR_ART_V1_20261115.md"


class FloralSexConflictOriginalEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=json.loads(P.read_text(encoding="utf-8"))
        cls.m=json.loads(M.read_text(encoding="utf-8"))

    def test_same_pulsatilla_site_and_date_not_four_replicates(self):
        d=self.p
        self.assertEqual(d["primary_2023"]["dual_fitness_flower_n"],57)
        for key in ("primary_2024","primary_2025_current_biology","primary_2025_amnat"):
            self.assertTrue(d[key]["same_solalex_2022_population"])
        self.assertIn("NOT independent", " ".join(d["inference_limits"]).replace("not independent","NOT independent"))

    def test_opposite_pistil_selection_measured_by_two_sex_functions(self):
        d=self.p["primary_2023"]["selection_pistil"]
        self.assertEqual((d["female_beta"],d["male_beta"]),(0.72,-0.51))
        self.assertEqual(d["reported_SAS"],1.22)
        self.assertEqual(d["reported_SA_index"],-.58)
        self.assertEqual(d["original_interaction_p"],"<0.001")
        self.assertTrue(self.p["primary_2023"]["delayed_male_days_per_100_pistils"]>0)

    def test_stamen_source_not_two_significant_opposite_gradients(self):
        d=self.p["primary_2023"]["selection_stamen"]
        self.assertEqual(d["female_beta"],-.08)
        self.assertEqual(d["male_beta"],.42)
        self.assertTrue(d["not_supported_as_two_significant_opposite_gradients"])

    def test_original_tagged_2025_phase_counts_match_article(self):
        a=compute(self.p)
        a1=a["transitions"]["2020-2021"]
        a2=a["transitions"]["2021-2022"]
        self.assertEqual(a["original_tagged_plants"],70)
        self.assertEqual(a1["rounded_table_reconstructed_counts"],{"M_to_H":5,"H_to_M":2})
        self.assertEqual(a2["rounded_table_reconstructed_counts"],{"M_to_H":2,"H_to_M":1})
        self.assertEqual(a1["original_author_denom"],{"M":7,"H":26})
        self.assertEqual(a2["original_author_denom"],{"M":6,"H":41})
        self.assertAlmostEqual(a1["fraction_by_original_year_source_phase"]["M_to_H"],5/7)
        self.assertAlmostEqual(a2["fraction_by_original_year_source_phase"]["H_to_M"],1/41)

    def test_pulsatilla_no_new_p_value_or_same_person_round_trip(self):
        a=compute(self.p)
        for k in ("unique_individuals_with_round_trip","flower_by_flower_raw_records",
                  "new_p_values","genetic_loss_and_reacquisition","slk_Phi_g0_Delta_R"):
            self.assertIsNone(a[k])
        self.assertFalse(a["published_gain_curve"]["male_significantly_saturating"])
        self.assertEqual(a["published_gain_curve"]["male_p_value_reported"],.051)
        self.assertGreater(a["published_gain_curve"]["female_CI"][0],1)

    def test_pulsatilla_prior_art_current_biology_fitness_peaks(self):
        d=self.p["primary_2025_current_biology"]
        self.assertEqual(d["doi"],"10.1016/j.cub.2025.04.022")
        self.assertEqual(d["fitness_landscape_male_bisexual_peaks"],
                         "ALREADY_PUBLISHED_BY_ORIGINAL_AUTHORS")
        self.assertEqual(d["analysed_single_flower_n"],87)

    def test_mercurialis_experiment_and_actual_vs_assumed_delta(self):
        m=self.m
        self.assertEqual(m["source"]["doi"],"10.1111/nph.70356")
        self.assertEqual(m["experiment"]["common_garden_replicates"],3)
        self.assertEqual(m["experiment"]["individuals_per_replicate"],61)
        self.assertEqual(m["experiment"]["mean_selfing_rate"],.296)
        self.assertEqual(m["experiment"]["assigned_paternity_seeds"],915)
        self.assertEqual(m["fitness_estimands"]["inbreeding_scenarios"],[0,1])
        self.assertEqual(m["fitness_estimands"]["diploid_actual_delta"],
                         "NOT_MEASURED_IN_THIS_STUDY")

    def test_mercurialis_large_disruptive_only_significant_under_assumed_delta_one(self):
        z=self.m["primary_table1_total_fitness_quadratic"]
        self.assertEqual((z["large"]["delta0"],z["large"]["delta1"]),(2.07,4.86))
        self.assertFalse(z["large"]["delta0_significant"])
        self.assertTrue(z["large"]["delta1_significant"])
        self.assertFalse(z["small"]["delta1_significant"])
        self.assertTrue(z["medium"]["delta1_significant"])
        self.assertIn("CONDITIONAL",self.m["biological_limit"])

    def test_published_transition_recalculation_exact_source_frozen(self):
        self.assertEqual(compute(self.p),json.loads(R.read_text(encoding="utf-8")))
        self.assertEqual(count_from_p(15,.07),1)
        with self.assertRaisesRegex(ValueError,"AMBIGUOUS_PUBLISHED_ROW"):
            count_from_p(15,.5)

    def test_biology_synthesis_fitness_limits_and_distinct_systems(self):
        txt=NOTE.read_text(encoding="utf-8")
        for term in ("Cyananthus","Pulsatilla","Mercurialis","近交弱勢","2025","未同定","先行研究"):
            self.assertIn(term,txt)
        self.assertNotIn("SLKが分業の進化起源を実証した",txt)


if __name__=="__main__":
    unittest.main()
