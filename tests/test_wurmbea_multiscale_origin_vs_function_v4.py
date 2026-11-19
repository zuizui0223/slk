"""Published-study unit, lineage and inference-boundary regression audit.

Does not create new phylogenetic reconstructions or fit lifetime fitness.
"""
from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/evidence/wurmbea_multiscale_origin_vs_function_source_v4.json"
WEST=ROOT/"data/evidence/wurmbea_2004_visit_to_seed_stage_source_v3.json"
NOTES=ROOT/"docs/SLK_WURMBEA_FLORAL_CONFLICT_EVOLUTION_DIRECTION_V4_20261115.md"


class WurmbeaMultiscaleSourceIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.west=json.loads(WEST.read_text(encoding="utf-8"))
        cls.sources=cls.data["findings"]

    def test_two_flower_vs_plant_comparisons_differ(self):
        j=self.sources["jones_burd_2001"]
        self.assertEqual(j["doi"],"10.1071/BT01008")
        self.assertEqual(j["whole_plant_pollen_investment_male_vs_hermaphrodite"],
                         "NO_DIFFERENCE_DETECTED")
        self.assertEqual(j["whole_plant_fruit_mass_female_vs_hermaphrodite"],
                         "NO_DIFFERENCE_DETECTED")
        self.assertEqual(j["after_controlling_flower_size"],
                         "HERMAPHRODITE_FLOWERS_HAVE_LOWER_POLLEN_AND_FRUIT_INVESTMENT_THAN_RESPECTIVE_UNISEXUAL_FLOWERS")

    def test_fitness_reversal_evidence_not_same_families(self):
        r=self.sources["ramsey_vaughton_2001"]
        self.assertEqual(r["doi"],"10.1086/320142")
        self.assertEqual(r["female_over_hermaphrodite_seed_per_plant_approx_ratio"],3)
        self.assertEqual(r["aborted_seed_pct"],{"female":21,"hermaphrodite":51})
        self.assertEqual(r["male_over_hermaphrodite_pollen_per_flower_approx_ratio"],1.3)
        self.assertFalse(r["same_individual_for_fitness_and_expression_cohorts"] is True)
        self.assertEqual(r["male_became_hermaphrodite_under_favorable_glasshouse_pct"],71)
        self.assertEqual(self.west["source"]["doi"],"10.1086/382796")

    def test_parsimony_minimum_not_independent_origin_count(self):
        p=self.sources["case_et_al_2008"]
        self.assertEqual(p["doi"],"10.1086/523368")
        self.assertEqual(p["randomly_resolved_phylogenies"],10000)
        self.assertEqual(p["minimum_parsimony_changes_across_resolutions"],
                         {"min":5,"max":8})
        self.assertEqual(p["resolved_best_tree_significantly_reconstructed_internal_nodes"],0)
        self.assertEqual(p["gains_or_losses_direction"],
                         "UNRESOLVED_ZERO_TO_EIGHT_EACH_NOT_SIMULTANEOUSLY_ZERO")
        self.assertFalse(p["phylogenetic_transition_estimate_is_natural_same_species_replicate_count"])

    def test_taxon_pruning_artificial_confidence_not_transition_rate(self):
        p=self.sources["case_et_al_2008"]
        n=p["pruned_taxon_example_significant_nodes"]
        self.assertAlmostEqual(n["numerator"]/n["denominator"],0.85,places=12)
        self.assertIn("Wurmbea dioica",p["claimed_taxonomic_nonmonophyly"])
        self.assertIn("plastid_capture",p["possible_confounds"])

    def test_macro_40_genera_not_universal_40_origin_events(self):
        g=self.sources["goldberg_et_al_2017"]
        self.assertEqual(g["doi"],"10.1111/evo.13181")
        self.assertEqual((g["species"],g["genera"]),(2145,40))
        self.assertEqual(g["reported_transition_rate_asymmetry"],
                         "LITTLE_EVIDENCE_FOR_UNIVERSAL_DIRECTION")
        self.assertTrue(g["no_wurmbea_specific_transition_reanalysis"])
        self.assertIn("not representative",g["inclusion_frame"])

    def test_current_name_vs_unresolved_taxonomic_complex(self):
        t=self.sources["western_taxonomy_status_2026"]
        self.assertTrue(t["currently_accepts_subsp_alba_under_W_dioica"])
        self.assertFalse(t["current_classification_is_formally_split"])
        self.assertEqual(t["comparison_status"],
                         "SEPARATE_STUDY_TAXON_BLOCKS_REQUIRED_NOT_SAME_SPECIES_LONGITUDINAL")
        self.assertIn("multiple",t["potential_issue"])

    def test_no_cross_source_one_lineage_or_real_fitness_gate(self):
        d=self.data
        self.assertEqual(d["status"],"SOURCE_GROUNDED_PUBLISHED_RESULTS_NOT_NEW_EMPIRICAL_FIT")
        combined=" ".join(d["interpretation_limits"]).lower()
        self.assertIn("not",combined)
        self.assertIn("phi",combined)
        doc=NOTES.read_text(encoding="utf-8")
        self.assertIn("5–8",doc)
        self.assertIn("17/20",doc)
        self.assertIn("2,145",doc)
        self.assertIn("分類",doc)
        self.assertNotIn("Wurmbeaで三ゲートを実証した",doc)

if __name__=="__main__":
    unittest.main()
