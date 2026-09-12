import math

SCHEMA = "SLK_PEDICULARIS_G1_G5_RECEIPT_V1"
SCALE = "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER"


def _need(ok, msg):
    if not ok:
        raise ValueError(msg)


def _est(x, label):
    p, lo, hi = x.get("point"), x.get("lower_95"), x.get("upper_95")
    for v in (p, lo, hi):
        _need(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v), f"bad {label}")
    _need(lo <= p <= hi, f"bad interval {label}")
    return float(p), float(lo), float(hi)


def _close(a, b):
    return math.isclose(a, b, rel_tol=1e-8, abs_tol=1e-8)


def _all_true(x, keys):
    return all(x.get(k) is True for k in keys)


def _phi_class(lo, hi):
    if lo > 0:
        return "DIFFERENTIATION_FAVORED"
    if hi < 0:
        return "PERSISTENT_COMPROMISE"
    return "CRITICAL_OR_UNRESOLVED"


def adjudicate(r):
    _need(r.get("receipt_schema_version") == SCHEMA, "wrong schema")
    c = r.get("context", {})
    _need(c.get("system") == "Pedicularis rex", "wrong system")
    _need(c.get("fitness_scale_id") == SCALE, "wrong fitness scale")
    for k in ("context_id", "population_id", "season_id", "time_horizon_id", "z_trait_id", "y_trait_id"):
        v = c.get(k)
        _need(isinstance(v, str) and v and "REQUIRED_BEFORE_USE" not in v, f"unfrozen {k}")

    up = r.get("upstream_g1_g2", {})
    anti = up.get("anti_circularity", {})
    _need(anti.get("water_used_as_sch_antagonist_G") is False, "water-as-G forbidden")
    _need(anti.get("independent_predator_exposure_used") is True, "independent G required")
    _need(anti.get("water_y_held_fixed_during_sch_surface") is True, "water-y not fixed")
    upstream_ok = up.get("g1") == "DIRECT_PASS" and up.get("g2") == "DIRECT_PASS" and up.get("g2_detail") == "G2_DIRECT_PASS_POSITIVE"
    if not upstream_ok:
        return {"status": "G1_G2_READY_ONLY", "claim_ceiling": "UPSTREAM_NOT_CLOSED"}
    L, Llo, _ = _est(up.get("conflict_load", {}), "L")
    _need(Llo > 0, "G2 lower95 must exceed zero")

    sy = r.get("structural_y", {})
    ykeys = ["Y0_repeatable_variation", "Y1_x_y_independence_audited", "Y2_preferential_loading", "Y2_pollination_cross_effect_bounded", "Y3_intervention_or_natural_experiment"]
    if sy.get("status") != "QUALIFIED" or not _all_true(sy, ykeys):
        state = r.get("functional_state_lane", {}).get("status")
        return {"status": "FUNCTIONAL_STATE_RELEASE_ONLY" if state == "DIRECT_PASS" else "G1_G2_READY_ONLY", "L": L, "claim_ceiling": "NO_STRUCTURAL_G3_G5"}

    w = r.get("worlds", {})
    for key in ("S", "D"):
        _need(w.get(key, {}).get("registered_prospectively") is True, f"unregistered {key}")
    WS, _, _ = _est(w["S"]["optimized_fitness"], "WS")
    WD, _, _ = _est(w["D"]["optimized_fitness"], "WD")
    direct = r.get("g5_Phi", {}).get("direct", {})
    _need(direct.get("status") == "IDENTIFIED", "direct Phi open")
    P, Plo, Phi = _est(direct, "Phi_direct")
    _need(_close(P, WD - WS), "direct Phi identity failed")

    q = r.get("d0_qualification", {})
    qkeys = ["D0_Q1_z_preserved", "D0_Q2_functional_benefit_matched", "D0_Q3_pollination_facing_equivalent", "D0_Q4_antagonist_channel_fidelity", "D0_Q5_apparatus_burden_accounted", "D0_Q6_common_horizon"]
    if q.get("status") != "QUALIFIED" or not _all_true(q, qkeys):
        return {"status": "STRUCTURAL_DIRECT_PHI_IDENTIFIED", "L": L, "Phi_direct": P, "Phi_class": _phi_class(Plo, Phi), "claim_ceiling": "DIRECT_ARCHITECTURE_VALUE_ONLY"}

    _need(w.get("D0", {}).get("registered_prospectively") is True, "unregistered D0")
    WD0, _, _ = _est(w["D0"]["optimized_fitness"], "WD0")
    g3 = r.get("g3_R", {})
    g4 = r.get("g4_K", {})
    _need(g3.get("status") == "RECOVERABLE_ARCHITECTURE_BENEFIT_IDENTIFIED", "R open")
    _need(g4.get("status") == "ARCHITECTURE_COST_IDENTIFIED" and g4.get("double_counting_audit_pass") is True, "K open")
    R, Rlo, Rhi = _est(g3, "R")
    K, _, _ = _est(g4, "K")
    _need(_close(R, WD0 - WS), "R identity failed")
    _need(_close(K, WD0 - WD), "K identity failed")

    dec = r["g5_Phi"]["decomposed"]
    _need(dec.get("status") == "IDENTIFIED", "decomposed Phi open")
    Pd, _, _ = _est(dec, "Phi_decomp")
    _need(_close(Pd, R - K), "decomposed Phi identity failed")
    b, blo, bhi = _est(r["g5_Phi"]["bridge_residual"], "bridge")
    _need(_close(b, P - Pd), "bridge identity failed")
    rule = r["g5_Phi"]["bridge_concordance"]
    _need(rule.get("frozen_before_confirmatory_outcomes") is True, "bridge rule not frozen")
    tol = rule.get("max_abs_point")
    _need(isinstance(tol, (int, float)) and tol >= 0, "bad bridge tolerance")
    concordant = abs(b) <= tol and blo <= 0 <= bhi
    out = {"status": "STRUCTURAL_G1_G5_CLOSED_CONCORDANT" if concordant else "STRUCTURAL_G1_G5_DECOMPOSED", "L": L, "R": R, "K": K, "Phi_direct": P, "Phi_decomp": Pd, "Phi_class": _phi_class(Plo, Phi), "bridge_residual": b, "bridge_concordant": concordant, "claim_ceiling": "SAME_SYSTEM_G1_G5" if concordant else "G1_G5_MEASURED_BRIDGE_NOT_CONCORDANT"}
    if Llo > 0 and Rlo > 0 and Phi < 0:
        out["diagnostic_pattern"] = "CONFLICT_REAL_RECOVERABLE_BUT_ARCHITECTURE_NOT_WORTH_COST"
    return out
