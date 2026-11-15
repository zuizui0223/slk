"""Original 2021 male-free treatment source and biological inference checks."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from audit_mercurialis_2021_mate_absence_leakiness_v1 import compute

SOURCE=ROOT/"data/evidence/mercurialis_2021_mate_absence_leaky_female_source_v1.json"
FROZEN=ROOT/"results/mercurialis_2021_mate_absence_leakiness_v1.json"
NOTE=ROOT/"docs/SLK_MERCURIALIS_2021_MATE_LOSS_FUNCTIONAL_REEXPRESSION_V1_20261115.md"


class RealMateAbsenceGeneticPotential(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src=json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.r=compute(cls.src)

    def test_diploid_original_source_and_no_hexaploid_equation(self):
        self.assertEqual(self.r["source_doi"],"10.1111/jeb.13720")
        self.assertEqual(self.r["source_ploidy"],"DIPLOID_XX_FEMALES_XY_MALES")
        self.assertFalse(self.r["may_be_pooled_with_2024_hexaploid_distance_LMM"])

    def test_six_gardens_three_per_treatment_and_real_mate_counts(self):
        d=self.r
        self.assertEqual(d["treatment_population_counts"],
                         {"controls_with_males":3,"female_only":3})
        self.assertEqual(d["parental_sex_counts_per_population"]["control"],
                         {"male":90,"female":90})
        self.assertEqual(d["parental_sex_counts_per_population"]["female_only"],
                         {"male":0,"female":180})
        self.assertEqual(d["initial_control_total_plants"],540)
        self.assertEqual(d["initial_female_only_total_plants"],540)
        self.assertEqual(d["initial_total_plants"],1080)
        self.assertEqual(d["source_seed_demes"],35)

    def test_272_females_are_nested_in_223_pots_not_independent_populations(self):
        d=self.r
        self.assertEqual(d["female_phenotyped_n"],272)
        self.assertEqual(d["sampled_unique_pots_from_source_occupancy"],223)
        self.assertEqual(d["sampled_female_plants_sharing_pots_with_other_sampled_females"],80)
        self.assertAlmostEqual(d["fraction_females_from_multi_sampled_pots"],80/272,places=8)
        self.assertEqual(d["experimental_plot_replicates"],6)

    def test_actual_male_flower_allocation_response_and_original_p(self):
        x=self.r["male_relative_reproductive_allocation_no_mates_over_with_males"]
        self.assertEqual(x["published_ratio"],2.33)
        self.assertEqual(x["published_p"],.01)
        self.assertIn("dry biomass",x["metric"])
        self.assertIsNone(x["new_effect_size_or_CI"])

    def test_incidence_p058_not_significant_and_control5pct_by_definition(self):
        x=self.r["incidence_of_leaky_females"]
        self.assertEqual(x["published_group_comparison_p"],.058)
        self.assertFalse(x["significant_at_point_zero_five"])
        self.assertEqual(x["source_control_incidence_by_threshold_definition"],.05)
        self.assertTrue(x["control_incidence_is_not_independent_natural_prevalence"])

    def test_female_effort_not_detectably_changed_does_not_prove_zero_cost(self):
        x=self.r["female_reproductive_effort"]
        self.assertEqual(x["published_group_comparison_p"],.19)
        self.assertTrue(x["no_detected_mean_difference"])
        self.assertFalse(x["zero_female_cost_proven"])

    def test_neighbour_males_not_sensed_by_proven_direct_pollen_signal(self):
        x=self.r["pot_male_neighbor_count"]
        self.assertEqual(x["male_effort_original_p"],.851)
        self.assertEqual(x["female_effort_original_p"],.977)
        self.assertFalse(x["pollen_or_fruit_signal_identity_demonstrated"])

    def test_no_proof_of_adaptive_seed_fitness_or_clonal_reaction_norm(self):
        d=self.r
        self.assertFalse(d["self_paternity_or_seed_viability_measured"])
        self.assertFalse(d["same_clonal_genotype_treatment_comparison"])
        self.assertFalse(d["adaptive_reaction_norm_crossing_with_fitness_measured"])
        self.assertFalse(d["SLK_Phi_g0_Delta_R_measured"])
        self.assertFalse(d["raw_Dryad_individual_file_downloaded"])
        self.assertIsNone(d["all_new_p_values"])

    def test_island_hypothesis_not_an_island_field_experiment(self):
        self.assertTrue(self.r["published_paper_proposes_island_colonization_without_testing_islands"])
        self.assertIn("NO oceanic island",self.src["discussion"]["island_colonization"])
        self.assertIn("founder events",self.src["discussion"]["island_colonization"])

    def test_false_ploidy_or_p_or_experiment_sample_fails(self):
        d=copy.deepcopy(self.src)
        d["plant"]["ploidy"]="HEXAPLOID"
        with self.assertRaisesRegex(ValueError,"SOURCE_PLOIDY_OR_PROVENANCE_CHANGED"):
            compute(d)
        d=copy.deepcopy(self.src)
        d["published_results"]["male_effort_group_treatment_p"]=.10
        with self.assertRaisesRegex(ValueError,"REPORTED_TREATMENT_OR_RESPONSE_CHANGED"):
            compute(d)
        d=copy.deepcopy(self.src)
        d["design"]["sampled_pot_occupancy_counts"]["pots_with_three_sampled_females"]=17
        with self.assertRaisesRegex(ValueError,"NESTED_SAMPLE_COUNT_NOT_REPRODUCED"):
            compute(d)
        d=copy.deepcopy(self.src)
        d["published_results"]["actual_self_sired_seed_count_in_original_plots"]=123
        with self.assertRaisesRegex(ValueError,"FALSE_ADAPTIVE_PLASTICITY_FITNESS_PROOF"):
            compute(d)

    def test_frozen_reanalysis_and_biological_ceiling_in_note(self):
        self.assertEqual(self.r,json.loads(FROZEN.read_text(encoding="utf-8")))
        d=NOTE.read_text(encoding="utf-8")
        for term in ("2021","272","2.33","0.058","0.19","35","80/272","島","未","倍体"):
            self.assertIn(term,d)
        self.assertNotIn("本研究が雌株の雄花による自殖父性を遺伝子型検証した",d)


if __name__=="__main__":
    unittest.main()
