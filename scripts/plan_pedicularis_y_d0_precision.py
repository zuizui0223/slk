from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import NormalDist


DEFAULT_ALPHA = 0.05
DEFAULT_POWER = 0.80
DEFAULT_ATTRITION = 0.15


def _finite_pos(x: float, label: str, allow_zero: bool = False) -> float:
    if not isinstance(x, (int, float)) or isinstance(x, bool) or not math.isfinite(x):
        raise ValueError(f"{label} must be finite numeric")
    if allow_zero:
        if x < 0:
            raise ValueError(f"{label} must be >= 0")
    elif x <= 0:
        raise ValueError(f"{label} must be > 0")
    return float(x)


def _z(p: float) -> float:
    if not 0 < p < 1:
        raise ValueError("probability must be in (0,1)")
    return NormalDist().inv_cdf(p)


def inflate_for_attrition(n: int, attrition: float = DEFAULT_ATTRITION) -> int:
    _finite_pos(n, "n")
    attrition = _finite_pos(attrition, "attrition", allow_zero=True)
    if attrition >= 1:
        raise ValueError("attrition must be < 1")
    return math.ceil(n / (1 - attrition))


def n_paired_equivalence(sd_diff: float, margin: float, alpha: float = DEFAULT_ALPHA,
                         power: float = DEFAULT_POWER) -> int:
    sd_diff = _finite_pos(sd_diff, "sd_diff")
    margin = _finite_pos(margin, "margin")
    zsum = _z(1 - alpha) + _z(power)
    return max(2, math.ceil((zsum * sd_diff / margin) ** 2))


def n_two_group_equivalence(sd: float, margin: float, alpha: float = DEFAULT_ALPHA,
                            power: float = DEFAULT_POWER) -> int:
    sd = _finite_pos(sd, "sd")
    margin = _finite_pos(margin, "margin")
    zsum = _z(1 - alpha) + _z(power)
    # Equal allocation. Returned n is independent plants PER GROUP.
    return max(2, math.ceil(2 * (zsum * sd / margin) ** 2))


def n_paired_superiority(sd_diff: float, min_effect: float, alpha: float = DEFAULT_ALPHA,
                         power: float = DEFAULT_POWER, directional: bool = False) -> int:
    sd_diff = _finite_pos(sd_diff, "sd_diff")
    min_effect = _finite_pos(min_effect, "min_effect")
    za = _z(1 - alpha) if directional else _z(1 - alpha / 2)
    zsum = za + _z(power)
    return max(2, math.ceil((zsum * sd_diff / min_effect) ** 2))


def n_two_group_superiority(sd: float, min_effect: float, alpha: float = DEFAULT_ALPHA,
                            power: float = DEFAULT_POWER, directional: bool = False) -> int:
    sd = _finite_pos(sd, "sd")
    min_effect = _finite_pos(min_effect, "min_effect")
    za = _z(1 - alpha) if directional else _z(1 - alpha / 2)
    zsum = za + _z(power)
    return max(2, math.ceil(2 * (zsum * sd / min_effect) ** 2))


def n_mean_precision(sd: float, half_width: float, alpha: float = DEFAULT_ALPHA) -> int:
    sd = _finite_pos(sd, "sd")
    half_width = _finite_pos(half_width, "half_width")
    return max(2, math.ceil((_z(1 - alpha / 2) * sd / half_width) ** 2))


def plan_endpoint(spec: dict, defaults: dict | None = None) -> dict:
    defaults = defaults or {}
    alpha = float(spec.get("alpha", defaults.get("alpha", DEFAULT_ALPHA)))
    power = float(spec.get("power", defaults.get("power", DEFAULT_POWER)))
    attrition = float(spec.get("attrition", defaults.get("attrition", DEFAULT_ATTRITION)))
    kind = spec.get("kind")

    if kind == "paired_equivalence":
        raw = n_paired_equivalence(spec["sd_diff"], spec["margin"], alpha, power)
        n_unit = "paired_plants_total"
    elif kind == "two_group_equivalence":
        raw = n_two_group_equivalence(spec["sd"], spec["margin"], alpha, power)
        n_unit = "plants_per_group"
    elif kind == "paired_superiority":
        raw = n_paired_superiority(
            spec["sd_diff"], spec["min_effect"], alpha, power,
            bool(spec.get("directional", False)),
        )
        n_unit = "paired_plants_total"
    elif kind == "two_group_superiority":
        raw = n_two_group_superiority(
            spec["sd"], spec["min_effect"], alpha, power,
            bool(spec.get("directional", False)),
        )
        n_unit = "plants_per_group"
    elif kind == "mean_precision":
        raw = n_mean_precision(spec["sd"], spec["half_width"], alpha)
        n_unit = "plants_total"
    else:
        raise ValueError(f"unsupported kind: {kind}")

    inflated = inflate_for_attrition(raw, attrition)
    out = {
        "endpoint_id": spec.get("endpoint_id", "UNNAMED"),
        "kind": kind,
        "alpha": alpha,
        "power": None if kind == "mean_precision" else power,
        "attrition": attrition,
        "raw_required_n": raw,
        "inflated_required_n": inflated,
        "n_unit": n_unit,
    }
    for key in ("sd", "sd_diff", "margin", "min_effect", "half_width", "directional"):
        if key in spec:
            out[key] = spec[key]
    return out


def plan_manifest(manifest: dict) -> dict:
    defaults = manifest.get("defaults", {})
    endpoints = manifest.get("endpoints", [])
    if not endpoints:
        raise ValueError("no endpoints supplied")

    results = [plan_endpoint(x, defaults) for x in endpoints]
    maxima_by_unit: dict[str, dict] = {}
    for row in results:
        unit = row["n_unit"]
        n = row["inflated_required_n"]
        if unit not in maxima_by_unit or n > maxima_by_unit[unit]["inflated_required_n"]:
            maxima_by_unit[unit] = {
                "inflated_required_n": n,
                "driving_endpoints": [row["endpoint_id"]],
            }
        elif n == maxima_by_unit[unit]["inflated_required_n"]:
            maxima_by_unit[unit]["driving_endpoints"].append(row["endpoint_id"])

    return {
        "planner_schema_version": "SLK_PEDICULARIS_Y_D0_PRECISION_PLAN_V1",
        "status": "PLANNING_ONLY_NOT_A_BIOLOGICAL_RECEIPT",
        "results": results,
        "maxima_by_allocation_unit": maxima_by_unit,
        "allocation_rule": (
            "Do not take one numeric maximum across incompatible units. "
            "paired_plants_total, plants_total, and plants_per_group must be translated into the frozen field allocation separately."
        ),
        "anti_peeking": (
            "Inputs must come from independent calibration, literature, or prospectively justified margins/effects; "
            "never from unblinded confirmatory outcomes."
        ),
        "approximation_boundary": (
            "Normal-approximation planning assumes the equivalence target difference is near zero and uses independent-plant scale SD inputs. "
            "Final analysis may use the registered cluster/bootstrap model, but sample-size inputs must remain prospective."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Prospective Pedicularis structural-y/D0 precision planner")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.manifest.read_text())
    result = plan_manifest(payload)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
