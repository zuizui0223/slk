"""Synthetic regression tests for GloPL × autofertility macro analysis.

Tests do not require network and never treat a statistical association
as evidence of SLK division-of-labour selection.
"""

import csv
import io
import sys
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))

import analyze_glopl_autofertility as macro
from analyze_glopl_context_variation import REQUIRED_COLUMNS,_git_blob_sha


def fake_breeding_workbook() -> bytes:
    columns=[
        "Data_source","Species","Family",
        "Self-compatibility_index_FS",
        "Self-compatibility_index_SFL",
        "Autofertility_index_FS",
        "Autofertility_index_SFL",
        "Annual_Biennial",
    ]
    data=[
        columns,
        ["A_2000","Example_alba","Asteraceae","0.3","NA","0.1","NA","0"],
        ["B_2000","Example_beta","Asteraceae","0.5","NA","0.5","NA","1"],
        ["C_2000","Example_ceras","Asteraceae","0.9","NA","0.9","NA","0"],
        ["D_2000","Unmatched_species","Fabaceae","0.8","NA","0.7","NA","0"],
    ]
    def colname(i):
        return chr(65+i)
    chunks=[]
    for i,values in enumerate(data,1):
        cells="".join(
            f'<c r="{colname(j)}{i}" t="inlineStr"><is><t>{cell}</t></is></c>'
            for j,cell in enumerate(values)
        )
        chunks.append(f'<row r="{i}">{cells}</row>')
    sheet='<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'+''.join(chunks)+'</sheetData></worksheet>'
    out=io.BytesIO()
    with zipfile.ZipFile(out,"w",compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("xl/workbook.xml","<workbook/>")
        z.writestr("xl/worksheets/sheet2.xml",sheet)
    return out.getvalue()


def fake_glopl_bytes():
    matrix=[]
    for sp,effect,year in (
        ("Example_alba",0.9,"2000"),
        ("Example_alba",1.1,"2001"),  # median per context -> study aggregate
        ("Example_beta",0.5,"2000"),
        ("Example_ceras",0.1,"2000"),
    ):
        r={name:"NA" for name in REQUIRED_COLUMNS}
        r.update({
            "Species_accepted_names":sp,
            "Family":"Asteraceae",
            "PL_Effect_Size":str(effect),
            "PL_Effect_Size_Type1":"FS",
            "PL_Effect_Size_Type2":"Sup",
            "Level_of_Supplementation":"flower",
            "Included_Bennett_et_al_meta_analysis":"yes",
            "Author":"Synthetic",
            "Year":"2020",
            "DOI":"10.0/example",
            "Latitude":"40",
            "Longitude":"-72",
            "population":"1",
            "year_of_study":year,
            "Constant_added":"FALSE",
        })
        matrix.append(r)
    out=io.StringIO()
    w=csv.DictWriter(out,fieldnames=list(REQUIRED_COLUMNS))
    w.writeheader()
    w.writerows(matrix)
    return out.getvalue().encode()


def test_rank_correlation_handles_ties_and_reversed_order():
    assert macro._rank([2.,3.,2.,8.]) == [1.5,3.,1.5,4.]
    assert macro._spearman([1,2,3,4],[4,3,2,1]) == -1
    assert macro._spearman([1,1,1],[0,1,2]) is None


def test_independent_permutation_is_reproducible_and_not_large_sample_theory():
    sample=[(i/20, 1-i/20) for i in range(20)]
    r1=macro._spearman_audit(sample,seed=11,nperm=199,nbootstrap=99)
    r2=macro._spearman_audit(sample,seed=11,nperm=199,nbootstrap=99)
    assert r1==r2
    assert r1["rho"] < -0.99
    assert r1["permutation_p_two_sided"] >= 1/200
    assert r1["bootstrap_valid"] > 80


def test_exact_species_macro_uses_individual_species_as_units(monkeypatch):
    glopl=fake_glopl_bytes()
    monkeypatch.setattr(macro,"UPSTREAM_BLOB_SHA",_git_blob_sha(glopl))
    monkeypatch.setattr(
        macro, "EXPECTED_BREEDING_SHA256",
        __import__("hashlib").sha256(fake_breeding_workbook()).hexdigest(),
    )
    traits=macro.extract_breeding_traits(fake_breeding_workbook())
    assert set(traits) >= {"Example alba","Example beta","Example ceras"}
    assert traits["Example beta"]["Autofertility_index_FS"] == 0.5
    result, rows=macro.analyze(glopl,fake_breeding_workbook())
    assert result["fruit_set_study_protocol_exact_species_overlap"] == 3
    assert result["species_with_both_SC_FS_and_AF_FS"] == 3
    assert len(rows)==3
    assert result["matched_strict_context_species_overlap"] == 1
    assert result["trait_coverage"]["af_fruit_set"] == 3
    assert result["species_level_rank_correlations"]["af_fruit_set"]["rho"] is None
    assert result["strict_context_association"]["af_vs_within_species_range"]["rho"] is None
    assert next(r for r in rows if r["species"]=="Example alba")["gopl_contexts"] == 2
