"""Empirical, not simulated: paired-flower F2 organ appearance and detectability.

Source Johns et al. 2024 Supplement 3; nested two flowers in 169 F2 plants.
A chimeric organ in one flower does not establish ancestral functional regain.
"""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
from audit_aquilegia_f2_partial_reassembly_v1 import load_rows
from audit_aquilegia_f2_within_plant_variability_v2 import summarize_repeated_plants

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/external/johns2024_aquilegia_f2_phenotypes_source.csv"


class TestWithinPlantF2(unittest.TestCase):
    def setUp(self):
        self.rows=load_rows(SOURCE)
        self.result=summarize_repeated_plants(self.rows,strict=True)

    def test_original_plant_grain_and_repeated_flower_counts(self):
        s=self.result["sample"]
        self.assertEqual((s["plants"],s["flowers"],s["whorl_rows"]),(231,400,800))
        self.assertEqual((s["one_flower_plants"],s["two_flower_plants"]),(62,169))
        self.assertTrue(s["F2_cross_not_natural_regain"])

    def test_anther_whorl_cross_flower_replication(self):
        r=self.result["paired_flower_concordance"]
        self.assertEqual(r["AN_inner_same"],139)
        self.assertEqual(r["AN_outer_same"],139)
        self.assertEqual(r["AN_both_whorls_same"],119)
        self.assertEqual(r["AN_inner_different_only"],20)
        self.assertEqual(r["AN_outer_different_only"],20)
        self.assertEqual(r["AN_both_whorls_different"],10)

    def test_expansion_and_fusion_use_correct_biological_level(self):
        r=self.result["paired_flower_concordance"]
        self.assertEqual(r["LE_inner_same"],138)
        self.assertEqual(r["LE_outer_same"],123)
        self.assertEqual(r["FU_flower_level_same"],154)
        self.assertEqual(r["FU_flower_level_different"],15)
        self.assertEqual(r["LE_inner_different"],31)
        self.assertEqual(r["LE_outer_different"],46)
        self.assertTrue(self.result["source_scope"]["fusion_is_one_flower_trait"])

    def test_same_f2_plant_expresses_mosaic_in_only_one_flower(self):
        r=self.result["mosaic_anther_and_staminode_filament"]
        self.assertEqual(r["both_flower_mosaic"],38)
        self.assertEqual(r["only_flower_a_mosaic"],23)
        self.assertEqual(r["only_flower_b_mosaic"],16)
        self.assertEqual(r["neither_flower_mosaic"],92)
        self.assertEqual(r["double_plants_any_flower_mosaic"],77)
        self.assertEqual(r["double_plants_a_flower_mosaic"],61)
        self.assertEqual(r["double_plants_b_flower_mosaic"],54)
        self.assertEqual(r["single_plants_any_flower_mosaic"],14)
        self.assertEqual(r["all_F2_plants_any_mosaic"],91)
        self.assertEqual(r["double_plants_discordant_mosaic"],39)

    def test_detection_increases_when_second_flower_is_scored(self):
        r=self.result["mosaic_anther_and_staminode_filament"]
        self.assertAlmostEqual(r["double_plants_first_flower_detection_rate"],61/169)
        self.assertAlmostEqual(r["double_plants_two_flower_detection_rate"],77/169)
        self.assertAlmostEqual(r["among_first_flower_negative_second_positive"],16/108)
        self.assertLess(r["double_plants_first_flower_detection_rate"],
                        r["double_plants_two_flower_detection_rate"])
        self.assertFalse(self.result["inference_limits"]["failure_to_see_mosaic_means_no_competence"])

    def test_repeated_flower_same_rate_exceeds_unpaired_marginal_agreement(self):
        r=self.result["replication_vs_marginal_null"]
        for trait in ("AN_inner","AN_outer","LE_inner","LE_outer","FU"):
            x=r[trait]
            self.assertGreater(x["same_plant_agreement_fraction"],
                               x["independently_paired_expected_agreement_fraction"])
            self.assertGreater(x["agreement_excess_over_marginal_independence"],0)
        self.assertFalse(self.result["inference_limits"]["shared_plant_genotype_implies_genetic_locus_identified"])

    def test_biological_limits_not_synthetic_revolution(self):
        limits=self.result["inference_limits"]
        self.assertFalse(limits["field_trait_regain_documented"])
        self.assertFalse(limits["fertile_pollen_or_ovary_protection_assayed"])
        self.assertFalse(limits["natural_heritable_capacity_transition_rate_estimated"])
        self.assertFalse(limits["SLK_floral_architecture_payoff_identified"])
        self.assertFalse(limits["same_genotype_functional_gene_toolkit_measured"])
        self.assertFalse(limits["one_flower_is_independent_new_genetic_replicate"])

    def test_identical_duplicate_anther_record_not_second_whorl(self):
        with self.assertRaisesRegex(ValueError,"DUPLICATE_FLOWER_WHORL"):
            summarize_repeated_plants(self.rows+[dict(self.rows[0])],strict=False)
        with self.assertRaisesRegex(ValueError,"MISSING_INNER_OR_OUTER"):
            summarize_repeated_plants(self.rows[1:],strict=False)


if __name__=="__main__":
    unittest.main()
