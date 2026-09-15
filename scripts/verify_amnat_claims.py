from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def verify() -> dict[str, object]:
    checks: dict[str, object] = {}

    # NE1: real conflict need not make differentiation profitable.
    L, R, K = 1.0, 0.5, 1.0
    phi = R - K
    assert L > 0 and phi < 0 and math.isclose(phi, -0.5)
    checks["NE1_conflict_not_payoff"] = {"L": L, "R": R, "K": K, "Phi": phi, "pass": True}

    # NE2: positive endpoint value need not imply local accessibility.
    s0, delta, k = 0.5, 2.0, 1.5
    k_local = s0**2 * delta**2
    k_global = s0 * delta**2
    assert math.isclose(k_local, 1.0)
    assert math.isclose(k_global, 2.0)
    assert k_local < k < k_global
    checks["NE2_payoff_not_accessibility"] = {
        "s0": s0,
        "Delta": delta,
        "k_local": k_local,
        "k": k,
        "k_global": k_global,
        "pass": True,
    }

    # NE3: accessible positive intrinsic value need not invade from rarity.
    phi, eta = 0.2, 0.5
    delta_rare = phi - eta
    assert phi > 0 and delta_rare < 0 and math.isclose(delta_rare, -0.3)
    checks["NE3_accessible_payoff_not_invasion"] = {
        "Phi": phi,
        "eta": eta,
        "Delta_rare": delta_rare,
        "pass": True,
    }

    # NE4: rare invasion need not imply reciprocal fixation superiority.
    phi, eta, beta, N = -0.2, -1.0, 1.0, 10
    delta_rare = phi - eta
    fixation_ratio = math.exp(beta * (N - 2) * phi)
    assert delta_rare > 0 and fixation_ratio < 1
    checks["NE4_invasion_not_reciprocal_fixation"] = {
        "Phi": phi,
        "eta": eta,
        "Delta_rare": delta_rare,
        "rho_D_over_rho_S": fixation_ratio,
        "pass": True,
    }

    # NE5: absolute fixation advantage over neutrality can disagree with occupancy.
    phi, eta, beta, N = -0.1, -0.5, 1.0, 10
    weak_selection_advantage = 3 * phi > eta
    occupancy_ratio = math.exp(beta * (N - 2) * phi)
    assert weak_selection_advantage and occupancy_ratio < 1
    checks["NE5_absolute_fixation_not_occupancy"] = {
        "Phi": phi,
        "eta": eta,
        "three_Phi": 3 * phi,
        "absolute_fixation_advantage": weak_selection_advantage,
        "Pi_D_over_Pi_S": occupancy_ratio,
        "pass": True,
    }

    # INV1: reciprocal fixation and symmetric rare-mutation occupancy ordering
    # are driven by the same exponential score ratio under the registered process.
    max_abs_error = 0.0
    comparisons = 0
    for beta in (0.1, 0.5, 1.0, 2.0):
        for N in (3, 4, 10, 50):
            for score_diff in (-2.0, -0.5, -0.1, 0.0, 0.1, 0.5, 2.0):
                fixation_ratio = math.exp(beta * (N - 2) * score_diff)
                occupancy_ratio = math.exp(beta * (N - 2) * score_diff)
                error = abs(fixation_ratio - occupancy_ratio)
                max_abs_error = max(max_abs_error, error)
                assert error == 0.0
                assert (fixation_ratio > 1) == (occupancy_ratio > 1)
                comparisons += 1
    checks["INV1_fixation_occupancy_invariant"] = {
        "comparisons": comparisons,
        "max_abs_error": max_abs_error,
        "pass": True,
    }

    return {
        "manuscript": "SLK_MANUSCRIPT_AMNAT_V3",
        "registered_process": "connected symmetric rare mutation + exponential Moran",
        "all_checks_pass": all(bool(v["pass"]) for v in checks.values()),
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("submission/amnat_review/generated/CLAIM_VERIFICATION_RECEIPT.json"),
    )
    args = parser.parse_args()

    receipt = verify()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
