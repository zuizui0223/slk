"""Published Cyananthus causal-scope and study-dependence regression checks.

This is a provenance/claim validation suite, NOT a reanalysis of raw
Wang et al. (2021) plants or a novel fitness estimation.
"""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/evidence/cyananthus_temporal_conflict_three_study_source_v1.json"
DOC=ROOT/"docs/SLK_CYANANTHUS_SEXUAL_PHASE_CONFLICT_EMPIRICAL_V1_20261115.md"


class CyananthusRealStudies(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.s={s["year"]:s for s in cls.d["primary_studies"]}

    def test_distinct_three_primary_source_dois(self):
        self.assertEqual({y:s["doi"] for y,s in self.s.items()},
                         {2015:"10.1371/journal.pone.0117149",
                          2017:"10.1002/ece3.3391",
                          2021:"10.1111/evo.14113"})
        self.assertIn("NOT_THREE_INDEPENDENT_ORIGINS",self.d["evidence_dependence"])

    def test_2015_specific_treatment_and_qualitative_female_loss(self):
        s=self.s[2015]
        self.assertIn("Throat-hair excision",s["original_interventions"])
        self.assertIn("0%, 50%, 100% pollen removal under pollinator exclusion",s["original_interventions"])
        self.assertIn("Approximately one-third",s["observed"]["no_pollen_removal"])
        self.assertIn("female",s["observed"]["reduced_pollen_removal"].lower())

    def test_2015_full_life_did_change_2021_did_not(self):
        early=self.s[2015]
        late=self.s[2021]
        self.assertEqual(early["sampling"]["phase_experiment"]["perfect_flowers"],125)
        self.assertEqual(early["sampling"]["phase_experiment"]["maternal_plants"],20)
        self.assertEqual(early["original_tests"]["total_floral_longevity"],
                         {"F":31.02,"df1":5,"df2":118,"p":"<0.001"})
        self.assertIn("Significantly increased",early["observed"]["total_flower_life"])
        self.assertEqual(late["published_results"]["total_floral_longevity"],
                         "No detected treatment effect")
        self.assertNotEqual(
            early["original_tests"]["original_author_conclusion"],
            late["published_results"]["total_floral_longevity"]
        )

    def test_2017_original_sample_grain(self):
        d=self.s[2017]
        counts=d["sampling"]["single_visit_flower_sample_sizes"]
        self.assertEqual(sum(v for group in counts.values() for v in group.values()),147)
        self.assertTrue(d["sampling"]["tracked_same_flower_single_visit_to_seed"])
        self.assertEqual(d["sampling"]["selected_plants"],{"female":30,"hermaphrodite":30})
        self.assertEqual(d["original_table3_reported"]["residual_df"],137)

    def test_2017_pollen_deposition_not_a_fitness_effect_estimate(self):
        s=self.s[2017]
        self.assertEqual(s["original_table3_reported"]["conditional_pollen_deposition_p"],0.850)
        self.assertEqual(s["original_table3_reported"]["conditional_pollen_deposition_F"],0.036)
        self.assertEqual(s["original_table3_reported"]["pollinator_group_p"],"<0.001")
        self.assertEqual(s["original_table2_reported"]["seed_production_sex_p"],.794)
        self.assertEqual(s["original_table2_reported"]["seed_production_pollinator_group_F"],15.591)

    def test_2021_actual_maternal_fertility_and_flower_life(self):
        s=self.s[2021]
        p=s["published_results"]
        self.assertIn("similar",p["early_removal"])
        self.assertIn("female phase shortened",p["restricted_removal"])
        self.assertEqual(p["total_floral_longevity"],"No detected treatment effect")
        self.assertIn("2-fold",p["female_advantage_across_five_populations"])
        self.assertIn("paywall",s["access"].lower())

    def test_wurmbea_is_not_identical_manipulation(self):
        c=self.d["comparative_interpretation"]
        self.assertTrue(c["no_pooled_effect"])
        self.assertEqual(c["independent_organismal_origins_estimated"],0)
        self.assertEqual(c["SLK_empirical_gates_closed"],[])
        for k in ("Phi","g0","Delta_R"):
            self.assertIn(k,c["not_estimated"])
        self.assertIn("NOT equivalent",c["different_causal_treatments"])

    def test_no_undocumented_full_paper_fit_or_slk_origin(self):
        limits=" ".join(self.d["interpretation_limits"]).lower()
        self.assertIn("abstract",limits)
        self.assertIn("not the 2021",limits)
        self.assertIn("historical",limits)
        note=DOC.read_text(encoding="utf-8")
        for phrase in ("2015", "2017", "2021", "5集団", "雄相", "雌相", "未同定"):
            self.assertIn(phrase,note)
        self.assertNotIn("SLKで進化的起源を証明した",note)

if __name__=="__main__":
    unittest.main()
