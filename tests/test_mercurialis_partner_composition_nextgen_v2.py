"""Tests for ORIGINAL 2008 paired and 2012 20-plot sex-ratio data; not a pooled fit."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from analyze_mercurialis_2008_2012_2024_nextgen_composition_v2 import analyze

SRC=ROOT/"data/evidence/mercurialis_2008_2012_2024_density_partner_composition_original_v2.json"
FROZEN=ROOT/"results/mercurialis_2008_2012_2024_nextgen_partner_composition_v2.json"
NOTE=ROOT/"docs/SLK_MERCURIALIS_DENSITY_TRIOECY_PARTNER_COMPOSITION_V2_20261115.md"


class MercurialisDensityPartnerContext(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=json.loads(SRC.read_text(encoding="utf-8"))

    def test_original_study_years_genetic_sex_context_separate(self):
        x=self.s
        self.assertEqual(x["study_2008"]["experimental_source_populations"],8)
        self.assertEqual(x["study_2012"]["original_source_populations"],10)
        self.assertEqual(x["study_2024"]["sample_size_populations"],109)
        self.assertIn("NO_FEMALES",x["study_2008"]["array_parent_sex_system"])
        self.assertIn("ALL_TREATMENTS_CONTAIN_FEMALES",x["study_2012"]["type"])

    def test_source_2008_population_level_child_male_rates(self):
        r=analyze(self.s)["androdioecy_2008"]
        self.assertEqual(r["populations"],8)
        self.assertEqual((r["low_density"],r["high_density"]),(12.25,250))
        self.assertEqual(r["progeny_male_low_unweighted_plot_fraction"],.2925)
        self.assertEqual(r["progeny_male_high_unweighted_plot_fraction"],.40375)
        self.assertEqual(r["progeny_male_high_minus_low"],.11125)

    def test_source_2008_paired_parent_adjusted_t_reproduced(self):
        r=analyze(self.s)["androdioecy_2008"]
        self.assertAlmostEqual(r["paired_t_high_minus_low_rounded_source"],4.64757163,places=7)
        self.assertAlmostEqual(r["paired_t_parent_delta_rounded_source"],2.63087907,places=7)
        self.assertAlmostEqual(r["male_frequency_change_high_minus_low_after_parent_adjustment"],.105)
        self.assertAlmostEqual(r["lambda_paired_t_rounded_source"],4.12085706,places=7)
        self.assertIsNone(r["new_p_values"])

    def test_original_published_2008_table_total_is_internally_inconsistent(self):
        r=analyze(self.s)["androdioecy_2008"]
        self.assertEqual(r["sum_of_original_row_progeny_N"],{"low":7293,"high":3371})
        self.assertEqual(r["original_published_progeny_total"],{"low":7239,"high":3371})
        self.assertEqual(r["unresolved_original_low_N_difference"],54)
        self.assertFalse(r["individual_pedigree_recovered"])

    def test_2012_20_plots_6076_offspring_not_independent_6076_experiments(self):
        r=analyze(self.s)["trioecy_2012"]
        self.assertEqual(r["plot_replicates"],20)
        self.assertEqual(r["offspring_phenotyped"],6076)
        self.assertTrue(r["female_present_in_all_20_plots"])
        self.assertTrue(r["male_treatment_is_presence_not_female_presence"])
        self.assertEqual(set(r["factorial_cells"]),{"low_absent","low_present","high_absent","high_present"})
        self.assertTrue(all(v["n_plots"]==5 for v in r["factorial_cells"].values()))
        self.assertEqual(sum(v["n_progeny_reported"] for v in r["factorial_cells"].values()),6076)

    def test_2012_male_present_density_contrast_small_and_original_null(self):
        r=analyze(self.s)["trioecy_2012"]
        cells=r["factorial_cells"]
        self.assertEqual(cells["low_present"]["male_progeny_plot_mean"],.316)
        self.assertEqual(cells["high_present"]["male_progeny_plot_mean"],.326)
        self.assertEqual(r["male_present_high_minus_low_progeny_male_plot_mean"],.01)
        self.assertEqual(r["original_male_density_test"],{"t":-.54,"p":">.50"})
        self.assertFalse(r["causal_female_buffering_effect_measured"])

    def test_2012_manipulated_male_presence_changes_female_and_cosex_effort_oppositely(self):
        r=analyze(self.s)["trioecy_2012"]["male_presence_sex_specific_seed_effort"]
        self.assertEqual((r["female_no_males"],r["female_with_males"]),(.067,.061))
        self.assertEqual((r["hermaphrodite_no_males"],r["hermaphrodite_with_males"]),(.042,.047))
        self.assertEqual(r["female_delta_with_minus_without_males"],-.006)
        self.assertEqual(r["hermaphrodite_delta_with_minus_without_males"],.005)
        self.assertEqual(r["published_interaction_F"],6.3)
        self.assertEqual(r["published_interaction_df"],[1,445])
        self.assertEqual(r["published_interaction_p"],"<.05")
        self.assertIsNone(r["new_male_paternity_effect_estimated"])

    def test_2012_male_presence_replaces_hermaphrodites_at_fixed_density(self):
        x=self.s["study_2012"]["parental_sex_counts"]
        for density in ("low","high"):
            without=x[density]["absent"]
            with_m=x[density]["present"]
            self.assertEqual(without["female"],with_m["female"])
            self.assertEqual(without["hermaphrodite"]-with_m["hermaphrodite"],
                             with_m["male"])
            self.assertEqual(sum(without.values()),sum(with_m.values()))
        self.assertEqual(x["low"]["absent"],{"male":0,"hermaphrodite":33,"female":16})
        self.assertEqual(x["low"]["present"],{"male":16,"hermaphrodite":17,"female":16})
        self.assertTrue(any("not pure addition" in limit
                            for limit in self.s["inferential_limits"]))

    def test_2012_more_female_seed_biomass_does_not_ensure_daughter_freq_gain(self):
        r=analyze(self.s)["trioecy_2012"]
        self.assertAlmostEqual(r["female_seed_allocation_fraction_relative_to_hermaphrodite"],.061/.043,places=8)
        self.assertAlmostEqual(r["male_pollen_allocation_fraction_relative_to_hermaphrodite"],.205/.035,places=8)
        self.assertEqual(r["female_next_generation_direction_certain_under_rounding"],
                         {"decrease":17,"increase":2,"ambiguous":1})
        self.assertEqual({k for k in ("decrease","increase","ambiguous")},set(r["female_next_generation_direction_certain_under_rounding"]))

    def test_2012_0_to_4pct_male_without_male_parent_pollen_contamination(self):
        r=analyze(self.s)["trioecy_2012"]
        self.assertEqual(r["male_absent_low_plot_mean_male_progeny"],.02)
        self.assertEqual(r["male_absent_high_plot_mean_male_progeny"],.002)
        self.assertTrue(r["male_progeny_without_male_parents_indicates_gene_flow"])

    def test_2024_real_trioecy_populations_and_arbitrary_cutoff(self):
        r=analyze(self.s)["natural_trioecy_2024"]
        self.assertEqual(r["studied_population_count"],109)
        self.assertEqual(r["reported_categories"],
                         {"cosex_only":36,"androdioecious":25,"gynodioecious":12,"trioecious":36})
        self.assertEqual(r["original_grouping_threshold"],.025)
        self.assertFalse(r["demonstrated_indefinite_evolutionary_equilibrium"])

    def test_2024_grouping_significant_but_full_population_density_null(self):
        r=analyze(self.s)["natural_trioecy_2024"]
        g=r["female_mean_in_male_rich_vs_poor_populations"]
        self.assertEqual((g["male_rich"],g["male_poor"]),(8.2,1.6))
        self.assertEqual(g["original_wilcoxon_p"],"<.0001")
        self.assertEqual(r["full_population_female_vs_density_p"],.620)
        self.assertEqual(r["full_population_female_vs_male_frequency_p"],.103)
        self.assertFalse(r["CMS_nuclear_restorer_linkage_confirmed_molecularly"])
        self.assertFalse(r["restorer_fitness_cost_measured"])

    def test_no_cross_study_causal_female_buffering_or_slk_claim(self):
        r=analyze(self.s)
        self.assertAlmostEqual(r["cross_study_difference_in_density_contrast_2008_vs_2012_descriptive"],.10125,places=8)
        self.assertIsNone(r["cross_study_difference_significance"])
        self.assertFalse(r["directly_randomized_female_presence_between_studies"])
        self.assertFalse(r["SLK_Phi_g0_Delta_R_measured"])
        self.assertIsNone(r["new_causal_effect_sizes"])

    def test_corrupted_2012_or_2008_original_table_rejected(self):
        d=copy.deepcopy(self.s)
        d["study_2008"]["original_table1"][0]["low"]["progeny_n"]+=54
        with self.assertRaisesRegex(ValueError,"PUBLISHED_2008_TABLE_INTERNAL_N_MISMATCH_LOST"):
            analyze(d)
        d=copy.deepcopy(self.s)
        d["study_2012"]["original_table2"][0]["n"]+=5
        with self.assertRaisesRegex(ValueError,"ORIGINAL_2012_PLOT_COUNTS_CHANGED"):
            analyze(d)
        d=copy.deepcopy(self.s)
        d["study_2012"]["original_table2"][0]["female"]=.07
        with self.assertRaisesRegex(ValueError,"ORIGINAL_2012_PROPORTION_INVALID"):
            analyze(d)
        d=copy.deepcopy(self.s)
        d["study_2024"]["source_category_counts"]["trioecious"]=37
        with self.assertRaisesRegex(ValueError,"ORIGINAL_2024_POPULATION_FRAME_CHANGED"):
            analyze(d)

    def test_frozen_source_calculations_and_note_biology(self):
        self.assertEqual(analyze(self.s),json.loads(FROZEN.read_text(encoding="utf-8")))
        note=NOTE.read_text(encoding="utf-8")
        for term in ("2008","2012","2024","7,293","7,239","17／20","109","雌型","密度","未実測"):
            self.assertIn(term,note)
        self.assertNotIn("SLKが自然の希少型侵入を確認した",note)


if __name__=="__main__":
    unittest.main()
