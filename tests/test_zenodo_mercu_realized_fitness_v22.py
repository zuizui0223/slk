"""Source-schema and independent-unit guards for V22."""
import io
import sys
import unittest
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from audit_zenodo_mercu_realized_fitness_v22 import analyze_zip,number,summary

def archive():
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,"w") as z:
        z.writestr("Geito_NewPhyto_v2/3G.csv",
                   "ID,Population,Male_flower_total,Female_flower_total,Genotyped_number,Selfed_seed_number,Selfing_rate,Biomass_whole,Realized_G,Phenotypic_G\n"
                   "1,P1,10,20,3,1,0.333,4,0.4,0.3\n2,P1,15,25,3,0,0,5,0.5,0.6\n")
        z.writestr("Geito_NewPhyto_v2/3G_ID01.csv",
                   "ID,Population,Biomass_whole,Realized_G,Male_fitness,Female_fitness,Total_fitness,Inbreeding,Pop_ID\n"
                   "1,P1,4,0.4,5,10,15,0,P1-1\n2,P1,5,0.5,6,11,17,0,P1-2\n"
                   "1,P1,4,0.4,5,7,12,1,P1-1\n2,P1,5,0.5,6,9,15,1,P1-2\n")
        z.writestr("Geito_NewPhyto_v2/Genotype_3P.csv",
                   "Sample_Name,Population,Parent_Offspring\nA,P1,Parent\nB,P1,Offspring\n")
    return buf.getvalue()

class RealFitnessSourceAudit(unittest.TestCase):
    def test_missing_numeric_and_no_imputed_zero(self):
        self.assertIsNone(number("NA"))
        self.assertIsNone(number(""))
        self.assertEqual(summary([{"a":"NA"},{"a":"2"}],"a")["n_valid"],1)
    def test_scenarios_not_counted_as_independent_plants(self):
        result=analyze_zip(archive())
        self.assertEqual(result["raw_rows"]["fitness_scenarios"],4)
        self.assertEqual(result["unique_population_mother_ids"]["fitness"],2)
        self.assertEqual(result["sex_fitness_overlap_population_mother_ids"],2)
        self.assertEqual(result["verified_normalized_population_mother_overlap"],2)
        self.assertEqual(result["sex_source_key_examples"],[("P1","1"),("P1","2")])
        self.assertEqual(result["fitness_source_key_examples"],[("P1","1"),("P1","2")])
        self.assertEqual(len(result["fitness_scenarios"]),2)
        self.assertEqual(result["fitness_scenarios"]["1"]["total_fitness"]["mean"],13.5)
    def test_no_p_values_or_natural_inbreeding_depression_claim(self):
        r=analyze_zip(archive())
        self.assertNotIn("p_value",r)
        self.assertIn("not independent plants",r["limits"][0])
        self.assertIn("natural inbreeding depression",r["limits"][1])
    def test_reject_malformed_original_columns(self):
        raw=io.BytesIO()
        with zipfile.ZipFile(raw,"w") as z:
            z.writestr("3G.csv","ID,Population\n1,P1\n")
            z.writestr("3G_ID01.csv","ID,Population\n1,P1\n")
            z.writestr("Genotype_3P.csv","Sample_Name,Population,Parent_Offspring\nA,P1,Parent\n")
        with self.assertRaises(ValueError):
            analyze_zip(raw.getvalue())
if __name__=="__main__":
    unittest.main()
