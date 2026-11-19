"""Original Johns et al. (2024) staminode F2 phenotype cross-checks.

Data used under CC BY 4.0: doi:10.1186/s13227-024-00225-3,
Supplementary Material 3. Morphological scores are NOT viable pollen
assays, field fitness, latent genetic toolkits, or independent evolution.
"""
import csv
import io
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
from audit_aquilegia_f2_partial_reassembly_v1 import load_rows, summarize_rows


ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/external/johns2024_aquilegia_f2_phenotypes_source.csv"


class RealAquilegiaPhenotypes(unittest.TestCase):
    def test_source_scored_grain_and_sample(self):
        result=summarize_rows(load_rows(SOURCE),strict=True)
        self.assertEqual(result["source"]["scored_whorl_rows"],800)
        self.assertEqual(result["source"]["scored_flowers"],400)
        self.assertEqual(result["source"]["unique_f2_plants"],231)
        self.assertEqual(result["source"]["plants_scored_one_flower"],62)
        self.assertEqual(result["source"]["plants_scored_two_flowers"],169)
        self.assertEqual(result["source"]["repeated_fusion_measurement_is_not_independent"],True)

    def test_original_floral_mosaic_counts(self):
        r=summarize_rows(load_rows(SOURCE),strict=True)
        v=r["morphology"]
        self.assertEqual(v["anther_present_whorl_rows"],467)
        self.assertEqual(v["anther_absent_whorl_rows"],333)
        self.assertEqual(v["pure_staminode_endpoint_whorl_rows"],240)
        self.assertEqual(v["pure_stamen_endpoint_whorl_rows"],119)
        self.assertEqual(v["non_endpoint_whorl_rows"],441)
        self.assertEqual(v["observed_distinct_anther_LE_fusion_combinations"],15)
        self.assertEqual(v["anther_present_LEge2_fused_whorl_rows"],187)
        self.assertEqual(v["flowers_with_any_anther_present_LEge2_fused_whorl"],129)
        self.assertEqual(v["plants_with_any_anther_present_LEge2_fused_whorl"],91)
        self.assertFalse(r["biological_claim_limits"]["pollen_fertility_confirmed"])

    def test_same_flower_whorl_order_not_arbitrary_two_sample_contrast(self):
        p=summarize_rows(load_rows(SOURCE),strict=True)["paired_whorls"]
        self.assertEqual(p["flower_pairs"],400)
        self.assertEqual(p["outer_anther_yes_inner_no"],99)
        self.assertEqual(p["inner_anther_yes_outer_no"],0)
        self.assertEqual(p["anther_same"],301)
        self.assertEqual(p["LE_inner_greater"],181)
        self.assertEqual(p["LE_outer_greater"],2)
        self.assertEqual(p["LE_equal"],217)
        self.assertEqual(p["fusion_identical_by_scoring"],400)
        self.assertEqual(p["fused_flowers"],234)
        self.assertEqual(p["fusion_independent_whorl_measurements"],0)

    def test_rare_lateral_expansion_reverse_cases_are_not_a_new_evolutionary_path(self):
        p=summarize_rows(load_rows(SOURCE),strict=True)["paired_whorls"]
        self.assertEqual(p["LE_outer_greater_flower_keys"],["132|a","39|a"])
        self.assertFalse(p["every_f2_flower_obeys_strict_LE_gradient"])
        self.assertTrue(p["one_per_plant_author_analysis_not_our_all_flower_analyses"])

    def test_synthetic_partial_switch_and_true_flower_level_fusion(self):
        heads=("plant","flower","stamens","whorl","anther",
               "lateral_expansion","fusion","std_whorl_organs",
               "total_organs","notes")
        data=[
          ("7","a","40","inner","0","3","1","10","50","NA"),
          ("7","a","40","outer","1","2","1","10","50","NA"),
          ("8","b","41","inner","1","2","0","10","51","NA"),
          ("8","b","41","outer","1","0","0","10","51","NA"),
        ]
        src=io.StringIO();w=csv.writer(src);w.writerow(heads);w.writerows(data)
        r=summarize_rows(list(csv.DictReader(io.StringIO(src.getvalue()))),strict=False)
        self.assertEqual(r["source"]["scored_flowers"],2)
        self.assertEqual(r["paired_whorls"]["fused_flowers"],1)
        self.assertEqual(r["morphology"]["anther_present_LEge2_fused_whorl_rows"],1)
        self.assertEqual(r["paired_whorls"]["outer_anther_yes_inner_no"],1)

    def test_duplicate_or_unpaired_rejected(self):
        rows=load_rows(SOURCE)
        with self.assertRaisesRegex(ValueError,"DUPLICATE_FLOWER_WHORL"):
            summarize_rows(rows+[dict(rows[0])],strict=False)
        with self.assertRaisesRegex(ValueError,"MISSING_INNER_OR_OUTER"):
            summarize_rows(rows[1:],strict=False)
        with self.assertRaisesRegex(ValueError,"INVALID_TRAIT_SCORE"):
            t=[dict(r) for r in rows]
            t[0]["anther"]="2"
            summarize_rows(t,strict=False)

    def test_same_genetic_and_function_claims_unobserved(self):
        r=summarize_rows(load_rows(SOURCE),strict=True)
        limits=r["biological_claim_limits"]
        for name in ("pollen_fertility_confirmed",
                     "individual_locus_genotype_linked_in_this_CSV",
                     "biochemical_developmental_toolkit_retention_measured",
                     "ecological_fitness_or_pollinator_payoff_estimated",
                     "recurrent_natural_re_expression_confirmed",
                     "SLK_candidate_structural_payoff_calibrated"):
            self.assertFalse(limits[name])


if __name__=="__main__":
    unittest.main()
