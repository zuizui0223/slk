from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.shared import RGBColor

from scripts.build_anonymous_review_bundle import build
from scripts.build_amnat_distribution_zip import build_distribution
from scripts.build_amnat_editorial_manager_kit import build_upload_kit
from scripts.format_amnat_review_docx import format_document
from scripts.verify_amnat_claims import verify


def test_registered_slk_claims_recompute() -> None:
    receipt = verify()
    assert receipt["all_checks_pass"] is True
    inv = receipt["checks"]["INV1_fixation_occupancy_invariant"]
    assert inv["comparisons"] == 336
    assert inv["derived_from_moran_process"] is True
    assert inv["derived_from_rare_mutation_chain"] is True
    assert inv["max_relative_error"] < 1e-10
    turnover = receipt["checks"]["UTA1_4c_environmental_barrier_turnover"]
    assert turnover["E_V"] < turnover["E_A"] < turnover["E_I"]
    assert turnover["value_limited_example"]["Phi"] < 0
    assert turnover["accessibility_limited_example"]["Phi"] > 0
    assert turnover["accessibility_limited_example"]["g0"] < 0
    assert turnover["establishment_limited_example"]["Phi"] > 0
    assert turnover["establishment_limited_example"]["g0"] > 0
    assert turnover["establishment_limited_example"]["Delta_R"] < 0
    assert receipt["checks"]["CANONICAL_MAPPING_GUARD"]["guard_raised"] is True
    diag = receipt["checks"]["UTA1_10_persistent_integration_gate_localization"]
    assert diag["negative_architecture_value"]["Phi"] < 0
    assert diag["local_release_barrier"]["Phi"] > 0
    assert diag["local_release_barrier"]["g0"] < 0
    assert diag["rare_establishment_barrier"]["Phi"] > 0
    assert diag["rare_establishment_barrier"]["g0"] > 0
    assert diag["rare_establishment_barrier"]["Delta_R"] < 0
    assert diag["mechanism_identified"] is False
    interval_diag = receipt["checks"]["UTA1_11_interval_compatible_state_set"]
    assert interval_diag["nested_refinement_monotone"] is True
    assert interval_diag["narrow_states"] == ["EARLY_GATES_PASSED"]
    assert set(interval_diag["medium_states"]) < set(interval_diag["wide_states"])
    assert interval_diag["marginal_box_is_conservative_outer_set"] is True
    assert interval_diag["exact_joint_feasibility_supported"] is False
    assert interval_diag["statistical_partial_identification_novelty_claimed"] is False
    assert diag["boundary_policy"] == {
        "Phi=0": "ARCHITECTURE_VALUE_BOUNDARY_UNRESOLVED",
        "g0=0": "LOCAL_RELEASE_BOUNDARY_UNRESOLVED",
        "Delta_R=0": "RARE_INVASION_BOUNDARY_UNRESOLVED",
    }
    early = diag["early_gates_passed"]
    assert early["state"] == "EARLY_GATES_PASSED"
    assert early["Phi"] > 0
    assert early["g0"] > 0
    assert early["Delta_R"] > 0
    assert early["realized_differentiation_implied"] is False
    assert early["excluded_failure_modes"] == [
        "negative_architecture_value",
        "downhill_initial_release",
        "rare_invasion_failure",
    ]


def test_anonymous_bundle_is_curated_and_scanned(tmp_path: Path) -> None:
    out = build(tmp_path / "reviewer_bundle")
    assert (out / "README.md").is_file()
    assert (out / "MANUSCRIPT_SOURCE.md").is_file()
    assert (out / "CLAIM_VERIFICATION_RECEIPT.json").is_file()
    assert (out / "scripts" / "slk_threshold_atlas.py").is_file()
    assert (out / "tests" / "test_moran_process_invariant.py").is_file()
    assert (out / "docs" / "INV1_EXECUTABLE_VALIDATION_V1.md").is_file()
    assert (out / "ANONYMITY_AUDIT.txt").read_text(encoding="utf-8").startswith("identity_scan=PASS")
    assert (out / "SHA256SUMS.txt").is_file()
    readme = (out / "README.md").read_text(encoding="utf-8")
    assert "not a byte-for-byte reproducibility target" in readme
    assert "one-ULP JSON difference" in readme
    assert not (out / ".git").exists()


def test_formatter_adds_line_and_page_number_fields() -> None:
    doc = Document()
    doc.add_heading("Anonymous review manuscript", level=1)
    doc.add_paragraph("A test paragraph.")
    format_document(doc, line_numbers=True)

    sect_pr = doc.sections[0]._sectPr
    assert sect_pr.find(qn("w:lnNumType")) is not None
    footer_xml = doc.sections[0].footer._element.xml
    assert " PAGE " in footer_xml
    assert "w:suppressLineNumbers" in footer_xml
    assert doc.styles["Normal"].paragraph_format.line_spacing == 2
    assert doc.styles["Heading 1"].font.color.rgb == RGBColor(0, 0, 0)


def test_reviewer_distribution_zip_is_byte_reproducible(tmp_path: Path) -> None:
    first_dir = tmp_path / "first_bundle"
    second_dir = tmp_path / "second_bundle"
    first_zip = tmp_path / "first.zip"
    second_zip = tmp_path / "second.zip"
    first_receipt = tmp_path / "first_receipt.json"
    second_receipt = tmp_path / "second_receipt.json"

    first = build_distribution(
        bundle_dir=first_dir,
        output_zip=first_zip,
        receipt_path=first_receipt,
        rebuild_bundle=True,
    )
    second = build_distribution(
        bundle_dir=second_dir,
        output_zip=second_zip,
        receipt_path=second_receipt,
        rebuild_bundle=True,
    )

    assert first_zip.read_bytes() == second_zip.read_bytes()
    assert first["reviewer_zip_sha256"] == second["reviewer_zip_sha256"]
    assert first["reviewer_zip_file_count"] == 17
    assert first["cache_files_included"] is False
    assert first["bundle_identity_audit"] == "identity_scan=PASS"
    assert first["sorted_paths"] is True


def test_editorial_manager_upload_kit_is_deterministic(tmp_path: Path) -> None:
    generated = tmp_path / "generated"
    rendered = generated / "rendered"
    rendered.mkdir(parents=True)

    fake_files = {
        generated / "SLK_AMNAT_REVIEW_MANUSCRIPT.docx": b"manuscript-docx",
        generated / "SLK_AMNAT_ANONYMOUS_TITLE_PAGE.docx": b"title-docx",
        rendered / "SLK_AMNAT_REVIEW_MANUSCRIPT.pdf": b"manuscript-pdf",
        rendered / "SLK_AMNAT_ANONYMOUS_TITLE_PAGE.pdf": b"title-pdf",
        generated / "SLK_AMNAT_REVIEWER_DATA_CODE_BUNDLE_FINAL.zip": b"reviewer-zip",
        generated / "AMNAT_REVIEW_PACKAGE_QA.txt": b"qa-pass",
    }
    for path, payload in fake_files.items():
        path.write_bytes(payload)

    first = build_upload_kit(
        generated_dir=generated,
        staging_dir=tmp_path / "stage1",
        output_zip=tmp_path / "kit1.zip",
        receipt_path=tmp_path / "kit1.json",
    )
    second = build_upload_kit(
        generated_dir=generated,
        staging_dir=tmp_path / "stage2",
        output_zip=tmp_path / "kit2.zip",
        receipt_path=tmp_path / "kit2.json",
    )

    assert (tmp_path / "kit1.zip").read_bytes() == (tmp_path / "kit2.zip").read_bytes()
    assert first["kit_sha256"] == second["kit_sha256"]
    assert first["kit_file_count"] == 8
    assert first["reviewer_bundle_sha256"] == second["reviewer_bundle_sha256"]
    assert first["internal_sha256_manifest_passed"] is True
