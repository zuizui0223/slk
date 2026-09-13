from __future__ import annotations

import importlib.util
from math import isclose
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "adjudicate_pedicularis_structural_y_function.py"
spec = importlib.util.spec_from_file_location("ped_structural_y_scale", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def _records(y_scale: float, z_scale: float):
    base = [
        (0.0, 0.0),
        (1.0, 0.0),
        (0.0, 1.0),
        (1.0, 1.0),
        (2.0, 0.5),
    ]
    return [
        (y * y_scale, z * z_scale, 1.0 + 2.0 * y + 3.0 * z)
        for y, z in base
    ]


def test_two_predictor_fit_is_invariant_to_independent_predictor_units():
    reference = module._ols_y_z(_records(1.0, 1.0))
    assert reference is not None

    for y_scale, z_scale in (
        (1e-6, 1e6),
        (1e-4, 1e-4),
        (1.0, 1.0),
        (1e6, 1e-6),
        (1e6, 1e6),
    ):
        fit = module._ols_y_z(_records(y_scale, z_scale))
        assert fit is not None
        assert isclose(fit["intercept"], 1.0, rel_tol=1e-11, abs_tol=1e-11)
        assert isclose(fit["beta_y"], 2.0 / y_scale, rel_tol=1e-11, abs_tol=0.0)
        assert isclose(fit["beta_z"], 3.0 / z_scale, rel_tol=1e-11, abs_tol=0.0)
        assert isclose(
            fit["normalized_determinant"],
            reference["normalized_determinant"],
            rel_tol=1e-13,
            abs_tol=1e-13,
        )


def test_constant_predictor_still_fails_closed():
    records = [
        (1.0, 0.0, 1.0),
        (1.0, 1.0, 2.0),
        (1.0, 2.0, 3.0),
        (1.0, 3.0, 4.0),
    ]
    assert module._ols_y_z(records) is None


def test_exactly_collinear_predictors_still_fail_closed_at_all_scales():
    for y_scale, z_scale in ((1e-6, 1e6), (1.0, 1.0), (1e6, 1e-6)):
        records = [
            (value * y_scale, (2.0 * value + 1.0) * z_scale, 4.0 + value)
            for value in (0.0, 1.0, 2.0, 3.0)
        ]
        assert module._ols_y_z(records) is None
