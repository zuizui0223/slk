from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


EFFECT_SCHEMA = "SLK_PEDICULARIS_G3_G5_EFFECT_FREEZE_V1"
PRECISION_FREEZE_SCHEMA = "SLK_PEDICULARIS_G3_G5_PRECISION_FREEZE_V1"
PRECISION_PLAN_SCHEMA = "SLK_PEDICULARIS_G3_G5_PRECISION_PLAN_V1"
PRECISION_PLAN_STATUS = "G3_G5_EFFECT_SAMPLE_SIZE_PROSPECTIVELY_PLANNED"
ROUTES = {"SAME_BLOCK_INTERNAL_IDENTITY", "INDEPENDENT_DIRECT_PHI_BLOCK"}


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _filled(value: object, label: str) -> str:
    out = str(value).strip()
    _need(bool(out) and "REQUIRED_BEFORE_USE" not in out, f"unfrozen {label}")
    return out


def compile_sampling(effect: dict, precision_freeze: dict, plan: dict) -> dict:
    _need(effect.get("schema_version") == EFFECT_SCHEMA, "wrong effect-freeze schema")
    _need(precision_freeze.get("schema_version") == PRECISION_FREEZE_SCHEMA, "wrong precision-freeze schema")
    _need(precision_freeze.get("status") == "FROZEN_CANDIDATE", "precision freeze must be FROZEN_CANDIDATE")
    _need(plan.get("schema_version") == PRECISION_PLAN_SCHEMA, "wrong precision-plan schema")
    _need(plan.get("status") == PRECISION_PLAN_STATUS, "precision plan is not ready")

    ectx = effect.get("context", {})
    fctx = precision_freeze.get("context", {})
    pctx = plan.get("context", {})
    _need(ectx.get("system") == "Pedicularis rex", "wrong effect system")
    for key in ("context_id", "population_id", "season_id", "fitness_scale_id", "time_horizon_id"):
        _filled(ectx.get(key), f"effect.context.{key}")
        _need(ectx.get(key) == fctx.get(key), f"effect/precision-freeze context mismatch: {key}")
        _need(ectx.get(key) == pctx.get(key), f"effect/precision-plan context mismatch: {key}")

    route = ectx.get("estimation_route")
    _need(route in ROUTES, "invalid or unfrozen effect estimation route")
    _need(ectx.get("frozen_before_g3_g5_outcomes") is False, "sampling must be compiled before final effect freeze")

    z_levels = effect.get("z_grid", {}).get("levels", [])
    target_z_count = precision_freeze.get("targets", {}).get("registered_z_levels")
    plan_z_count = plan.get("targets", {}).get("registered_z_levels")
    _need(isinstance(z_levels, list) and len(z_levels) >= 5, "effect z grid must already be specified")
    _need(len(z_levels) == target_z_count == plan_z_count, "z-level count mismatch across effect/precision contracts")

    pf_meta = precision_freeze.get("freeze_metadata", {})
    precision_commit = _filled(pf_meta.get("freeze_commit"), "precision freeze commit")
    _filled(pf_meta.get("d0_qualification_receipt_reference"), "D0 qualification receipt reference")
    _need(precision_freeze.get("context", {}).get("frozen_before_g3_g5_outcomes") is True, "precision freeze was not frozen before outcomes")

    targets = precision_freeze.get("targets", {})
    _need(plan.get("targets", {}).get("world_cell_mean_half_width") == targets.get("world_cell_mean_half_width"), "half-width target mismatch")
    _need(plan.get("targets", {}).get("minimum_recoverable_benefit_R") == targets.get("minimum_recoverable_benefit_R"), "R target mismatch")
    _need(plan.get("targets", {}).get("minimum_abs_architecture_value_Phi") == targets.get("minimum_abs_architecture_value_Phi"), "Phi target mismatch")

    decomp = plan.get("decomposition", {})
    direct = plan.get("independent_direct_phi", {})
    min_world = decomp.get("minimum_analyzable_plants_per_world")
    rec_world = decomp.get("recruitment_plants_per_world")
    _need(isinstance(min_world, int) and min_world > 0, "bad decomposition analyzable n")
    _need(isinstance(rec_world, int) and rec_world >= min_world, "bad decomposition recruitment n")

    out = copy.deepcopy(effect)
    sampling = out.setdefault("sampling", {})
    sampling["minimum_analyzable_plants_per_world"] = min_world
    sampling["recruitment_plants_per_world"] = rec_world
    if route == "INDEPENDENT_DIRECT_PHI_BLOCK":
        min_direct = direct.get("minimum_analyzable_plants_per_world")
        rec_direct = direct.get("recruitment_plants_per_world")
        _need(isinstance(min_direct, int) and min_direct > 0, "bad direct-block analyzable n")
        _need(isinstance(rec_direct, int) and rec_direct >= min_direct, "bad direct-block recruitment n")
        sampling["minimum_analyzable_plants_per_direct_world"] = min_direct
        sampling["recruitment_plants_per_direct_world"] = rec_direct
    else:
        sampling["minimum_analyzable_plants_per_direct_world"] = None
        sampling["recruitment_plants_per_direct_world"] = None

    _need(sampling.get("flowers_per_z_level_per_plant") == 1, "v1 flowers-per-z-level contract changed")
    sampling["sample_size_source"] = f"SLK_PEDICULARIS_G3_G5_PRECISION_PLAN_V1@{precision_commit}"
    sampling["sample_size_rationale"] = (
        "Maximum of simultaneous world-by-z cell precision, predeclared minimum R effect, and predeclared minimum |Phi| effect; "
        "variance imported for planning only from an independent D0 qualification partition with a frozen SD safety multiplier."
    )
    sampling["sample_size_compiled_from_precision_plan"] = True

    out.setdefault("freeze_metadata", {})["precision_plan_reference"] = (
        f"SLK_PEDICULARIS_G3_G5_PRECISION_PLAN_V1@{precision_commit}"
    )
    out["status"] = "SAMPLING_COMPILED_AWAITING_FINAL_EFFECT_FREEZE"
    out["context"]["frozen_before_g3_g5_outcomes"] = False
    out["compiler_claim_ceiling"] = (
        "SAMPLE_SIZE_FIELDS_COMPILED_ONLY; final effect freeze metadata, bootstrap settings, and all other registered fields must be frozen before layout generation."
    )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile Pedicularis G3-G5 precision plan into the final effect-freeze sampling block")
    parser.add_argument("effect_freeze_candidate_json", type=Path)
    parser.add_argument("precision_freeze_json", type=Path)
    parser.add_argument("precision_plan_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = compile_sampling(
        json.loads(args.effect_freeze_candidate_json.read_text(encoding="utf-8")),
        json.loads(args.precision_freeze_json.read_text(encoding="utf-8")),
        json.loads(args.precision_plan_json.read_text(encoding="utf-8")),
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
