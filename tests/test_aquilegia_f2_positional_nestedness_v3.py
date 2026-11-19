"""Original-source biological positional nestedness is not free organ Lego.

Copyright Johns et al 2024; source CC BY 4.0 and DOI 10.1186/s13227-024-00225-3.
Tests require same-flower paired whorls and one retained flower per unique F2 plant.
Anther-presence is not measured pollen fertility; expansion score is morphological.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
from audit_aquilegia_f2_partial_reassembly_v1 import load_rows
from audit_aquilegia_f2_positional_nestedness_v3 import summarize_ordered_identity

SOURCE=Path(__file__).resolve().parents[1]/"data/external/johns2024_aquilegia_f2_phenotypes_source.csv"


class AquilegiaNestedMorphologyV3Tests(unittest.TestCase):
    def setUp(self):
        self.r=summarize_ordered_identity(load_rows(SOURCE),strict=True)

    def test_genotype_flower_whorl_grain_is_source_actual(self):
        self.assertEqual(self.r["sample"]["plants"],231)
        self.assertEqual(self.r["sample"]["flowers"],400)
        self.assertEqual(self.r["sample"]["inner_outer_whorl_score_rows"],800)
        self.assertEqual(self.r["sample"]["one_flower_per_plant_sensitivity_n"],231)
        self.assertEqual(self.r["sample"]["double_scored_plants"],169)

    def test_anther_is_directionally_nested_not_arbitrary_exchange(self):
        a=self.r["positionally_nested_anther"]
        self.assertEqual(a["all_flowers"]["inner_anther_present"],184)
        self.assertEqual(a["all_flowers"]["outer_anther_present"],283)
        self.assertEqual(a["all_flowers"]["inner_yes_outer_no_violation"],0)
        self.assertEqual(a["all_flowers"]["outer_yes_inner_no"],99)
        self.assertEqual(a["first_flower_per_plant"]["inner_anther_present"],115)
        self.assertEqual(a["first_flower_per_plant"]["outer_anther_present"],165)
        self.assertEqual(a["first_flower_per_plant"]["inner_yes_outer_no_violation"],0)
        self.assertEqual(a["first_flower_per_plant"]["outer_yes_inner_no"],50)

    def test_lateral_expansion_order_robust_to_threshold(self):
        t=self.r["lateral_expansion_threshold_sensitivity"]
        self.assertEqual({z["threshold"]:z["all_flowers"]["outer_high_inner_low_violation"]
                          for z in t},{1:1,2:1,3:0})
        self.assertEqual({z["threshold"]:z["first_flower_per_plant"]["outer_high_inner_low_violation"]
                          for z in t},{1:1,2:1,3:0})
        self.assertEqual(t[1]["all_flowers"]["inner_high"],323)
        self.assertEqual(t[1]["all_flowers"]["outer_high"],243)
        self.assertEqual(t[1]["first_flower_per_plant"]["inner_high"],186)
        self.assertEqual(t[1]["first_flower_per_plant"]["outer_high"],141)
        self.assertEqual(t[1]["all_flowers"]["violation_plant_flower_keys"],["132|a"])
        self.assertEqual(t[0]["all_flowers"]["violation_plant_flower_keys"],["39|a"])
        self.assertEqual(t[2]["all_flowers"]["violation_plant_flower_keys"],[])

    def test_conjunction_of_opposed_order_rules_nearly_unbroken(self):
        s=self.r["conjunctive_nesting_at_LE2"]
        self.assertEqual(s["all_flowers"]["both_rules_hold"],399)
        self.assertEqual(s["all_flowers"]["either_rule_fails"],1)
        self.assertEqual(s["first_flower_per_plant"]["both_rules_hold"],230)
        self.assertEqual(s["first_flower_per_plant"]["either_rule_fails"],1)
        self.assertEqual(s["double_scored_flower_a"]["both_rules_hold"],168)
        self.assertEqual(s["double_scored_flower_b"]["both_rules_hold"],169)
        self.assertEqual(s["observed_exception_keys"],["132|a"])

    def test_marginal_preserving_random_whorl_pairing_is_negative_control(self):
        s=self.r["marginal_independence_counterfactual"]
        self.assertAlmostEqual(s["one_flower_per_plant"]["anther_expected_violations_if_unpaired"],115*66/231)
        self.assertAlmostEqual(s["one_flower_per_plant"]["LE2_expected_violations_if_unpaired"],141*45/231)
        self.assertGreater(s["one_flower_per_plant"]["anther_expected_violations_if_unpaired"],30)
        self.assertGreater(s["one_flower_per_plant"]["LE2_expected_violations_if_unpaired"],25)
        self.assertFalse(s["independent_pairing_is_biologically_realistic_null"])
        self.assertFalse(s["marginal_null_means_genetically_independent_modules"])

    def test_induced_directional_exceptions_are_preserved(self):
        rows=load_rows(SOURCE)
        # Change just one inner anther from 0 to 1 where the outer whorl
        # lacks anthers: don't silently enforce the observed rule by code.
        sample=[dict(x) for x in rows]
        target=next(x for x in sample if x["whorl"]=="inner"
                    and x["anther"]=="0"
                    and any(y["plant"]==x["plant"] and y["flower"]==x["flower"]
                            and y["whorl"]=="outer" and y["anther"]=="0"
                            for y in sample))
        target["anther"]="1"
        q=summarize_ordered_identity(sample,strict=False)
        self.assertGreater(q["positionally_nested_anther"]["all_flowers"]["inner_yes_outer_no_violation"],0)

    def test_no_phenotypic_orientation_is_equivalent_to_evolutionary_transition(self):
        g=self.r["evidence_ceiling"]
        self.assertFalse(g["observed_gene_modules_independent"])
        self.assertFalse(g["pollen_viability_of_anther_positive_organs_known"])
        self.assertFalse(g["whorl_order_equates_developmental_or_evolutionary_time"])
        self.assertFalse(g["field_pollinator_fitness_of_mosaics_measured"])
        self.assertFalse(g["natural_ancestral_trait_regain_rate_estimated"])
        self.assertFalse(g["direct_same_lineage_SLK_ANTO_causal_test_complete"])

    def test_duplicate_whorl_and_improper_scope_rejected(self):
        rows=load_rows(SOURCE)
        with self.assertRaisesRegex(ValueError,"DUPLICATE_FLOWER_WHORL"):
            summarize_ordered_identity(rows+[dict(rows[0])],strict=False)
        with self.assertRaisesRegex(ValueError,"MISSING_INNER_OR_OUTER"):
            summarize_ordered_identity(rows[1:],strict=False)


if __name__=="__main__":
    unittest.main()
