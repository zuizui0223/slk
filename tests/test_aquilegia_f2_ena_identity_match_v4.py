"""Aquilegia PRJNA1089234 published metadata versus original F2 phenotype IDs.

No genotype reconstruction or downloading sequence reads in these tests.
Source 2024 F2 phenotype CSV (DOI 10.1186/s13227-024-00225-3).
"""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
from audit_aquilegia_f2_partial_reassembly_v1 import load_rows
from audit_aquilegia_f2_ena_identity_match_v4 import (
    parse_f2_id, load_manifest, link_pheno_to_run_metadata,
)

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/external/johns2024_aquilegia_f2_phenotypes_source.csv"
MANIFEST=ROOT/"data/external/aquilegia_f2_PRJNA1089234_ena_run_metadata_v4.json"


class AquilegiaSraJoinMetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=link_pheno_to_run_metadata(load_rows(SOURCE),load_manifest(MANIFEST),strict=True)

    def test_published_F2_sample_aliases_match_original_same_individual_ids(self):
        r=self.result
        self.assertEqual(r["phenotypes"]["unique_F2_plant_ids"],231)
        self.assertEqual(r["ENA_run_metadata"]["total_run_rows"],341)
        self.assertEqual(r["ENA_run_metadata"]["F2_run_rows"],340)
        self.assertEqual(r["ENA_run_metadata"]["canonical_F2_id_count"],336)
        self.assertEqual(r["linked_plant_count"],231)
        self.assertEqual(r["unlinked_phenotype_plant_ids"],[])
        self.assertEqual(r["ENA_run_metadata"]["unphenotyped_SRA_F2_id_count"],105)
        self.assertEqual(len(r["linked_phenotype_plants"]),231)

    def test_F2_alias_parser_requires_exact_accession_name(self):
        self.assertEqual(parse_f2_id("F2.16"),"16")
        self.assertEqual(parse_f2_id("F2.16_1"),"16")
        self.assertEqual(parse_f2_id("F2.036_2"),"36")
        for name in ("Aj2_parent_HMR","F2.A","F2.16_r","F2.16_",
                     "F3.16","F2.16_2_more","F2.16;F2.17","F2.0"):
            self.assertIsNone(parse_f2_id(name))

    def test_duplicate_F2_ids_are_distinct_source_BioSamples(self):
        v=self.result["ENA_run_metadata"]
        self.assertEqual(v["canonical_ids_with_more_than_one_run"],4)
        self.assertEqual(v["ambiguous_F2_id_list"],["16","19","36","50"])
        for id in v["ambiguous_F2_id_list"]:
            x=next(y for y in v["all_F2_duplicate_records"] if y["plant"]==id)
            self.assertEqual(len(x["run_accessions"]),2)
            self.assertEqual(len(x["biosample_accessions"]),2)
        self.assertEqual(v["duplicated_alias_ids_present_in_phenotypes"],3)
        self.assertTrue(self.result["scientific_limits"]["duplicates_cannot_be_assumed_technical_replicates"])

    def test_sequence_download_size_requires_staging_not_blind_processing(self):
        m=self.result["ENA_run_metadata"]
        self.assertEqual(m["fastq_file_count"],681)
        self.assertEqual(m["all_source_FASTQ_bytes"],78243926288)
        self.assertEqual(m["phenotyped_plant_alias_matched_FASTQ_bytes"],49374744454)
        self.assertGreater(m["phenotyped_plant_alias_matched_FASTQ_bytes"],40_000_000_000)
        self.assertEqual(m["zero_bytes_run_count"],0)
        self.assertTrue(self.result["scientific_limits"]["source_FASTQ_files_have_not_been_downloaded"])

    def test_sample_alias_repeats_are_not_independent_genetic_replicates(self):
        r=self.result
        self.assertFalse(r["scientific_limits"]["marker_genotypes_computed_or_validated"])
        self.assertFalse(r["scientific_limits"]["all_source_samples_successfully_passed_author_QTL_QC"])
        self.assertFalse(r["scientific_limits"]["structural_trait_associated_with_genomic_allele_identified"])
        self.assertFalse(r["scientific_limits"]["functional_reexpression_genes_confirmed"])
        self.assertFalse(r["scientific_limits"]["direct_Slk_ANTO_fitness_test_complete"])

    def test_source_collisions_are_not_arbitrarily_matched(self):
        raw=load_manifest(MANIFEST)
        x=[dict(t) for t in raw["run_metadata_rows"]]
        x[0]["run_accession"]=x[1]["run_accession"]
        raw["run_metadata_rows"]=x
        with self.assertRaisesRegex(ValueError,"DUPLICATE_RUN"):
            link_pheno_to_run_metadata(load_rows(SOURCE),raw,strict=False)

    def test_missing_validated_phenotype_plant_fails_closed(self):
        raw=load_manifest(MANIFEST)
        raw["run_metadata_rows"]=[r for r in raw["run_metadata_rows"]
          if not (r["sample_alias"]=="F2.2")]
        with self.assertRaisesRegex(ValueError,"ORIGINAL_PHENOTYPE_SAMPLE_HAS_NO_ENA_RUN"):
            link_pheno_to_run_metadata(load_rows(SOURCE),raw,strict=False)


if __name__=="__main__":
    unittest.main()
