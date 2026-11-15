#!/usr/bin/env python3
"""Reconstruct ORIGINAL authors' sex-phase switches from rounded Table 1.

Pulsatilla alpina 2025 Am Nat Table 1, published row proportions and n.
No access to tagged-plant raw records, no independent p values, and no
ancestral trait reacquisition or SLK evolutionary gate inference.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/evidence/pulsatilla_sexual_conflict_multi_paper_primary_v1.json"


def count_from_p(n, p):
    if type(n) is not int or n < 0 or isinstance(p, bool) or not isinstance(p, (int,float)) or not math.isfinite(p) or p < 0 or p > 1:
        raise ValueError("INVALID_PUBLISHED_ROW")
    v=n*p
    k=round(v)
    if abs(v-k) > .105:
        raise ValueError("AMBIGUOUS_PUBLISHED_ROW")
    return k


def reconstruct(pub):
    if pub["doi"] != "10.1086/737646":
        raise ValueError("WRONG_PRIMARY_SOURCE")
    transitions={}
    for years, rows in pub["cross_year_table_rows"].items():
        if years not in ("2020-2021","2021-2022"):
            raise ValueError("UNKNOWN_SEASON")
        denominators={"M":0,"H":0}
        switches={"M_to_H":0,"H_to_M":0}
        for row in rows:
            sex=row["from"][0]
            if sex not in denominators:
                raise ValueError("UNEXPECTED_SOURCE_SEX")
            n=row["n"]
            denominators[sex]+=n
            if sex=="M":
                switches["M_to_H"]+=count_from_p(n,row.get("p_to_H1",0))
                switches["M_to_H"]+=count_from_p(n,row.get("p_to_H2",0))
            else:
                switches["H_to_M"]+=count_from_p(n,row.get("p_to_M1",0))
        expected={"2020-2021":{"M":7,"H":26},"2021-2022":{"M":6,"H":41}}[years]
        if denominators!=expected:
            raise ValueError("ORIGINAL_SOURCE_STATE_TOTALS_CHANGED")
        rates={"M_to_H":switches["M_to_H"]/denominators["M"],
               "H_to_M":switches["H_to_M"]/denominators["H"]}
        reported=pub["author_reported_transition_rates"][years]
        if any(abs(rates[k]-reported[k]) > .006 for k in rates):
            raise ValueError("ORIGINAL_PRINTED_RATES_NOT_REPRODUCED")
        if sum(switches.values())!=pub["authors_reported_sex_changes"][years]:
            raise ValueError("ORIGINAL_AUTHOR_SWITCH_COUNT_NOT_REPRODUCED")
        transitions[years]={
            "original_author_denom":denominators,
            "rounded_table_reconstructed_counts":switches,
            "fraction_by_original_year_source_phase":rates,
            "repeated_year_sample_not_independent":True
        }
    return {
        "schema":"SLK_PULSATILLA_PUBLISHED_2025_TABLE1_RECONSTRUCTION_V1",
        "source_doi":pub["doi"],
        "same_tagged_population_across_years":True,
        "original_tagged_plants":pub["tagged_n"],
        "transitions":transitions,
        "unique_individuals_with_round_trip":None,
        "flower_by_flower_raw_records":None,
        "new_p_values":None,
        "genetic_loss_and_reacquisition":None,
        "slk_Phi_g0_Delta_R":None,
        "note":"Published rounded transitions, not new individual-level evidence or historical origin rates."
    }


def compute(data):
    pp=data["primary_2025_amnat"]
    out=reconstruct(pp)
    prior=data["primary_2023"]["selection_pistil"]
    if not (prior["female_beta"]>0 and prior["male_beta"]<0):
        raise ValueError("OPPOSING_PISTIL_SELECTION_NOT_PRESENT")
    out["published_opposite_pistil_gradient"]={
       "female_beta":prior["female_beta"],"male_beta":prior["male_beta"],
       "difference_of_printed_rounded_betas":round(prior["female_beta"]-prior["male_beta"],3),
       "author_reported_SAS":prior["reported_SAS"],
       "author_reported_SA_index":prior["reported_SA_index"],
       "source_2023_doi":data["primary_2023"]["doi"],
       "new_selection_model_fit":None
    }
    # 1.23 from printed two-decimal coefficients vs paper's SAS=1.22.
    if abs(out["published_opposite_pistil_gradient"]["difference_of_printed_rounded_betas"]-
           prior["reported_SAS"]) > .02:
        raise ValueError("ORIGINAL_TABLE1_GRADIENT_DISCREPANCY")
    gain=pp["gain_curve_exponent"]
    out["published_gain_curve"]={
       "female_b":gain["female"],"female_CI":gain["female_CI"],
       "male_b":gain["male"],"male_CI":gain["male_CI"],
       "male_significantly_saturating":False,
       "male_p_value_reported":0.051
    }
    if not (gain["female_CI"][0]>1 and gain["male_CI"][0]<=1<=gain["male_CI"][1]):
        raise ValueError("GAIN_CURVE_CEILING_CHANGED")
    return out


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,default=SOURCE)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    result=compute(json.loads(args.source.read_text(encoding="utf-8")))
    blob=json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(blob,encoding="utf-8")
    else:
        print(blob,end="")


if __name__=="__main__":
    main()
