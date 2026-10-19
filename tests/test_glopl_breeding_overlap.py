"""Synthetic XLSX/plant binomial parsing; no network in routine pytest."""

import io
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_glopl_breeding_overlap import (
    normalize_species,
    read_xlsx,
    _column_number,
)


def _minimal_excel_bytes() -> bytes:
    workbook = io.BytesIO()
    sheet = """<?xml version="1.0" encoding="UTF-8"?>
    <worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
      <sheetData>
        <row r="1">
          <c r="A1" t="s"><v>0</v></c>
          <c r="B1" t="inlineStr"><is><t>Autofertility</t></is></c>
        </row>
        <row r="2">
          <c r="A2" t="s"><v>1</v></c>
          <c r="B2"><v>0.7</v></c>
        </row>
        <row r="3">
          <c r="A3" t="s"><v>2</v></c>
          <c r="B3"><v>0.3</v></c>
        </row>
      </sheetData>
    </worksheet>"""
    shared = """<?xml version="1.0" encoding="UTF-8"?>
    <sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
      <si><t>Species</t></si>
      <si><t>Primula farinosa</t></si>
      <si><r><t>Clarkia </t></r><r><t>xantiana</t></r></si>
    </sst>"""
    with zipfile.ZipFile(workbook, "w", compression=zipfile.ZIP_DEFLATED) as f:
        f.writestr("xl/workbook.xml", "<workbook/>")
        f.writestr("xl/sharedStrings.xml", shared)
        f.writestr("xl/worksheets/sheet1.xml", sheet)
    return workbook.getvalue()


def test_xlsx_reads_shared_and_inline_strings_and_numerics():
    wb = read_xlsx(_minimal_excel_bytes())
    assert "xl/worksheets/sheet1.xml" in wb
    assert wb["xl/worksheets/sheet1.xml"] == [
        ["Species", "Autofertility"],
        ["Primula farinosa", "0.7"],
        ["Clarkia xantiana", "0.3"],
    ]


def test_binomial_matching_is_exact_and_does_not_merge_subspecies():
    assert normalize_species("Primula_farinosa") == "Primula farinosa"
    assert normalize_species("Clarkia   xantiana") == "Clarkia xantiana"
    assert normalize_species("Clarkia xantiana var. xantiana") is None
    assert normalize_species("Rosa cf. canina") is None
    assert normalize_species("Primula") is None
    assert normalize_species("Cirsium irumtiense") == "Cirsium irumtiense"


def test_column_coordinate_converter_and_non_xlsx_guard():
    assert [_column_number(x) for x in ("A1", "Z25", "AA1", "AC9")] == [0, 25, 26, 28]
    try:
        read_xlsx(b"not an XLSX")
    except ValueError as err:
        assert "not an XLSX" in str(err)
    else:
        assert False, "bad binary input must fail"
