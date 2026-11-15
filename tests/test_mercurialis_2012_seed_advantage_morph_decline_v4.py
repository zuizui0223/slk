"""Source reanalysis of seed-output ratio and daughter morph turnover.

Tests are over ORIGINAL 2012 plot summaries and the 2025 published CMS
model's prior-art boundary; NOT reconstructed parental haplotypes.
"""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from analyze_mercurialis_2012_seed_advantage_morph_decline_v4 import (
    compute, classify
)

SOURCE=ROOT/"data/evidence/mercurialis_2008_2012_2024_density_partner_composition_original_v2.json"
PRIOR=ROOT/"data/evidence/mercurialis_2012_seed_advantage_and_CMS_prior_art_v4.json"
FROZEN=ROOT/"results/mercurialis_2012_seed_advantage_morph_decline_v4.json"
NOTE=ROOT/"docs/SLK_MERCURIALIS_SEED_ADVANTAGE_VERSUS_GENETIC_TRANSMISSION_V4_20261115.md"


class MercurialisSeedBenefitNotGeneticIncrease(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.prior=json.loads(PRIOR.read_text(encoding="utf-8"))
        cls.result=compute(cls.source,cls.prior)

    def test_original_20_plots_are_independent_experimental_units(self):
        p=self.result
        self.assertEqual(p["count_independent_experimental_plots"],20)
        self.assertEqual(sum(r["progeny_sample_n"] for r in p["plot_level_records"]),6076)
        self.assertEqual(p["primary_source_doi"],"10.1371/journal.pone.0035597")
        self.assertTrue(p["male_presence_is_male_for_hermaphrodite_substitution"])

    def test_original_oh_seed_ratio_direction_19_of_20(self):
        out=self.result
        self.assertEqual(out["female_seed_biomass_allocation_higher_plots"],19)
        self.assertEqual(sum(r["relative_seed_allocation_advantage_under_rounding"]=="female_seed_allocation_higher"
                             for r in out["plot_level_records"]),19)
        self.assertEqual(out["source_ratio_definition"],
                         "o_h = (seed dry biomass / aboveground biomass)_hermaphrodite divided by (seed dry biomass / aboveground biomass)_female")

    def test_joint_advantage_does_not_imply_frequency_increase(self):
        d=self.result["joint_outcomes_counted_from_original_plot_summary"]
        self.assertEqual(d,{
            "female_seed_allocation_higher_and_female_morph_decrease":17,
            "female_seed_allocation_higher_and_female_morph_increase":1,
            "female_seed_allocation_higher_and_morph_ambiguous":1,
            "hermaphrodite_seed_allocation_higher_and_female_morph_decrease":0,
            "hermaphrodite_seed_allocation_higher_and_female_morph_increase":1,
            "hermaphrodite_seed_allocation_higher_and_morph_ambiguous":0,
            "seed_allocation_ambiguous":0
        })
        self.assertFalse(self.result["evidence_morph_increase_when_seed_higher_must_occur"])

    def test_actual_original_seed_ratio_bins_1_15_4(self):
        d=self.result
        x=d["descriptive_female_to_hermaphrodite_seed_allocation_share_ratio_bins_from_oh"]
        self.assertEqual(x,{
            "female_allocation_not_higher":1,
            "female_allocation_ratio_strictly_between_1_and_2":15,
            "female_allocation_ratio_strictly_above_2":4,
            "uncertainty_from_oh_rounding_crossing_bin_boundary":0
        })
        self.assertEqual(sum(x.values()),20)
        self.assertEqual(sum(
            r["relative_allocation_bin_not_model_viable_seed_g"]==
            "female_allocation_ratio_strictly_above_2"
            for r in d["plot_level_records"]),4)

    def test_nuclear_vs_maternal_thresholds_are_only_old_theory(self):
        prior=self.prior["model_2025_prior_art"]["idealized_original_intro_thresholds"]
        self.assertEqual(prior["nuclear_male_sterility_female_seed_ratio_required"],"g>2")
        self.assertEqual(prior["maternal_CMS_female_seed_ratio_required"],"g>1")
        self.assertFalse(self.result["theoretical_prior_nuclear_and_CMS_thresholds_apply_to_real_2012_plots"])
        self.assertFalse(self.result["o_h_allocation_ratio_can_equal_Heredity_viable_seed_g"])
        self.assertEqual(self.result["idealized_ancestral_thresholds_from_original_Heredity"],
                         {"nuclear_male_sterility":"g>2","maternally_inherited_CMS":"g>1"})
        self.assertEqual(prior["actual_2012_plot_invasion_inference"],
            "BLOCKED_BY_ALLOCATION_FRACTION_NOT_VIABLE_SEED_NUMBER_SELFING_EXISTING_MALES_AND_CMS_UNTYPED")

    def test_source_exceptions_and_rounding_unresolved(self):
        rows={r["original_plot"]:r for r in self.result["plot_level_records"]}
        self.assertEqual(rows[6]["relative_seed_allocation_advantage_under_rounding"],"female_seed_allocation_higher")
        self.assertEqual(rows[6]["female_morph_change_under_rounding"],"female_morph_increase")
        self.assertEqual(rows[12]["relative_seed_allocation_advantage_under_rounding"],"hermaphrodite_seed_allocation_higher")
        self.assertEqual(rows[12]["female_morph_change_under_rounding"],"female_morph_increase")
        self.assertEqual(rows[20]["female_morph_change_under_rounding"],"undetermined_under_source_rounding")
        self.assertAlmostEqual(rows[12]["female_over_hermaphrodite_seed_allocation_share_ratio_from_printed_oh"],
                               1/1.03,places=8)

    def test_strict_rounding_guards_at_boundaries(self):
        self.assertEqual(classify(.9,.25,.3333),
                         ("female_seed_allocation_higher","female_morph_decrease"))
        self.assertEqual(classify(1.00,.33,1/3),
                         ("undetermined_under_source_rounding",
                          "undetermined_under_source_rounding"))
        self.assertEqual(classify(1.03,.40,.33),
                         ("hermaphrodite_seed_allocation_higher","female_morph_increase"))
        with self.assertRaisesRegex(ValueError,"BAD_SOURCE_NUMBER"):
            classify(float("nan"),.3,.3)
        with self.assertRaisesRegex(ValueError,"SOURCE_FREQUENCIES_OUT_OF_RANGE"):
            classify(0,.3,.3)

    def test_model_2025_invasion_versus_stability_is_prior_art(self):
        p=self.prior["model_2025_prior_art"]
        self.assertEqual(p["doi"],"10.1038/s41437-024-00729-7")
        self.assertEqual(p["publication_online"],"2024-10-14")
        self.assertEqual(p["simulated_initial_rare_CMS_frequency"],1e-6)
        self.assertTrue(p["author_simulation_not_natural_invasion"])
        self.assertTrue(self.result["Heredity_2025_is_existing_theory_not_new_SLK_causal_model"])
        self.assertTrue(any("males in a population" in s.lower() or "males can hinder" in s.lower()
                            for s in p["source_results"]))
        self.assertIn("e_m",p["model_parameter_definitions"])

    def test_2025_snail_direct_selection_is_independent_taxon(self):
        p=self.prior["cross_taxon_direct_selection_prior_art"]
        self.assertEqual(p["taxon"],"Physa acuta")
        self.assertEqual(p["doi"],"10.1086/735820")
        self.assertIn("11-generation",p["study_type"])
        self.assertTrue(self.result["experimental_2025_P_phys_acuta_cross_taxon_not_plant"])
        self.assertTrue(p["prior_direct_empirical_example"])

    def test_2012_original_seed_ratio_is_biomass_fraction_not_fecundity(self):
        m=self.prior["method_correction_2026_11_15"]
        self.assertEqual(m["severity"],"MATERIAL_SOURCE_MEASUREMENT_CORRECTION")
        self.assertEqual(m["corrected_endpoint"],
            "SEED_BIOMASS_PER_ABOVEGROUND_BIOMASS_ALLOCATION_FRACTION")
        self.assertIn("aboveground biomass",self.result["source_ratio_definition"])
        self.assertFalse(self.result["o_h_allocation_ratio_can_equal_Heredity_viable_seed_g"])

    def test_plots_do_not_supply_genetic_CMS_or_paternity(self):
        d=self.result
        self.assertFalse(d["same_genotype_genetic_fitness_recovered"])
        self.assertFalse(d["CMS_cytotype_frequency_or_fatherhood_recovered"])
        self.assertTrue(d["no_novel_p_values"])
        self.assertFalse(d["SLK_Phi_g0_Delta_R_identified"])
        self.assertTrue(all(not r["inheritance_cytotype_or_parentage_observed"]
                            for r in d["plot_level_records"]))

    def test_corrupted_source_fails_closed(self):
        src=copy.deepcopy(self.source)
        for z in src["study_2012"]["original_table2"]:
            if z["id"]==1:
                z["oh"]=1.8
                break
        with self.assertRaisesRegex(ValueError,"SOURCE_CROSS_TAB_PLOT_BIOLOGY_CHANGED"):
            compute(src,self.prior)
        prior=copy.deepcopy(self.prior)
        prior["model_2025_prior_art"]["author_simulation_not_natural_invasion"]=False
        with self.assertRaisesRegex(ValueError,"UNSUPPORTED_NOVEL_INVASION_CLAIM"):
            compute(self.source,prior)
        prior=copy.deepcopy(self.prior)
        prior["cross_taxon_direct_selection_prior_art"]["doi"]="unknown"
        with self.assertRaisesRegex(ValueError,"INCORRECT_CROSS_TAXON_CMS_SOURCE"):
            compute(self.source,prior)

    def test_saved_output_and_biology_note_match(self):
        self.assertEqual(self.result,json.loads(FROZEN.read_text(encoding="utf-8")))
        note=NOTE.read_text(encoding="utf-8")
        for term in ("19","17","20","2012","2025","CMS","種子","次世代","先行研究","未"):
            self.assertIn(term,note)
        self.assertNotIn("SLKが実測で希少CMSの固定を証明した",note)

if __name__=="__main__":
    unittest.main()
