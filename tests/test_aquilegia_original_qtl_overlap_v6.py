"""Source-frozen Johns 2024 real F2 QTL support-interval comparison.

This is a publication table reinterpretation: original QTL were inferred by
the AUTHORS. Overlap is NOT pleiotropy, and separation is NOT a proof of
developmentally independent genes. No processed 329×599 genotype matrix used.
"""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
from audit_aquilegia_original_qtl_overlap_v6 import (
    parse_publisher_table, pairwise_overlap, audit_original_qtl_table
)

ROOT=Path(__file__).resolve().parents[1]
TABLE=ROOT/"data/external/johns2024_aquilegia_qtl_table1_publisher_v6.md"


class OriginalQtlIntervalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=audit_original_qtl_table(TABLE,strict=True)

    def test_original_publisher_table_has_16_trait_rows_not_16_independent_genetic_loci(self):
        x=self.report["source"]
        self.assertEqual(x["original_table_rows"],16)
        self.assertEqual(x["author_reported_independent_QTL"],9)
        self.assertEqual(x["trait_row_counts"],{
            "Anther, inner":3,"Anther, outer":4,
            "Lateral expansion, inner":4,"Lateral expansion, outer":2,
            "Fusion":3
        })

    def test_inner_outer_anther_support_regions_shared(self):
        x=self.report["contrasts"]["anther_inner_vs_outer"]
        self.assertEqual(x["same_chr_comparisons"],3)
        self.assertEqual(x["overlapping_support_regions"],3)
        self.assertEqual([v["chromosome"] for v in x["pairs"]],[2,3,5])

    def test_inner_outer_filament_expansion_regions_separate(self):
        x=self.report["contrasts"]["lateral_expansion_inner_vs_outer"]
        self.assertEqual(x["same_chr_comparisons"],3)
        self.assertEqual(x["overlapping_support_regions"],0)
        self.assertEqual([(v["A"],v["B"]) for v in x["pairs"]],
                         [("LEIN-Q2.1","LEOU-Q2"),
                          ("LEIN-Q2.2","LEOU-Q2"),
                          ("LEIN-Q3","LEOU-Q3")])

    def test_outer_expansion_and_fusion_QTL_supported_overlaps(self):
        x=self.report["contrasts"]["lateral_expansion_outer_vs_fusion"]
        self.assertEqual(x["same_chr_comparisons"],2)
        self.assertEqual(x["overlapping_support_regions"],2)
        self.assertEqual([v["chromosome"] for v in x["pairs"]],[2,3])
        self.assertAlmostEqual(x["pairs"][0]["overlap_cM"],5.8)
        self.assertAlmostEqual(x["pairs"][1]["overlap_cM"],2.7)
        self.assertEqual(self.report["contrasts"]["lateral_expansion_inner_vs_fusion"]["overlapping_support_regions"],0)

    def test_major_QTL_preserved_as_original_author_not_this_reanalysis(self):
        locus=next(r for r in self.report["reported_rows"] if r["name"]=="LEOU-Q3")
        self.assertEqual((locus["chromosome"],locus["interval_cM"],locus["PVE_percent"]),
                         (3,[24.4,27.1],25.5))
        self.assertTrue(self.report["interpretive_limits"]["author_QTL_analyses_are_not_newly_refit"])
        self.assertFalse(self.report["interpretive_limits"]["QTL_interval_overlap_proves_pleiotropy"])

    def test_missing_original_groups_do_not_inherit_incorrect_trait(self):
        rows=parse_publisher_table(TABLE)
        self.assertEqual(rows[0]["trait"],"Anther, inner")
        self.assertEqual(rows[1]["trait"],"Anther, inner")
        self.assertEqual(rows[3]["trait"],"Anther, outer")
        self.assertEqual(rows[14]["trait"],"Fusion")
        self.assertEqual(rows[15]["trait"],"Fusion")

    def test_synthetic_loci_on_different_chromosomes_do_not_overlap(self):
        A=[{"trait":"x","chromosome":2,"name":"A","interval_cM":[1.,3.]}]
        B=[{"trait":"y","chromosome":3,"name":"B","interval_cM":[1.,3.]}]
        x=pairwise_overlap(A,B)
        self.assertEqual(x["same_chr_comparisons"],0)
        self.assertEqual(x["overlapping_support_regions"],0)

    def test_no_assumed_independent_genetic_modules_or_fitness(self):
        flags=self.report["interpretive_limits"]
        for key in ("QTL_interval_overlap_proves_pleiotropy",
                    "QTL_disjointness_proves_gene_modules_independent",
                    "source_marker_genotype_matrix_loaded",
                    "QTL_refit_by_this_repository",
                    "source_QTL_positions_identify_causal_genes",
                    "same_organ_effect_on_pollen_or_seed_fitness_estimated",
                    "natural_ancestral_reexpression_confirmed"):
            self.assertFalse(flags[key])


if __name__=="__main__":
    unittest.main()
