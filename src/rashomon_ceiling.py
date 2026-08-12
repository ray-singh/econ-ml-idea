"""Experiment 1: constrained-flip optimizer (the "adversarial ceiling").

For a given accuracy tolerance epsilon, compute the maximum extractable
surplus by optimally reclassifying boundary individuals of the canonical
model r_hat*, without leaving the Rashomon set R_epsilon.

See README.md section 5 and 6.2.
"""

import numpy as np

# README.md section 6.2.
DEFAULT_EPSILON_GRID = [0.001, 0.005, 0.01, 0.02, 0.05]


def adversarial_ceiling(
    y_true: np.ndarray,
    canonical_pred: np.ndarray,
    profit_gain: np.ndarray,
    epsilon: float,
) -> dict:
    """Flip up to epsilon * n predictions of the canonical model to
    maximize profit, subject to an accuracy-loss budget of epsilon.

    Implements Proposition 1 (paper/theory_draft.md): restricts flips to
    individuals currently at the low tier (canonical_pred == 0), sorts
    them by profit_gain descending (equivalently, elasticity ascending),
    and flips the top floor(epsilon * n) of them, but only while
    profit_gain remains positive (Assumption A2 — never flip an
    unprofitable individual just to spend budget).

    `profit_gain` is b_i = pi_1 * (1 - w_i) - pi_0, precomputed per
    individual (see src/metrics.py).
    """
    y_true = np.asarray(y_true)
    canonical_pred = np.asarray(canonical_pred)
    profit_gain = np.asarray(profit_gain, dtype=float)
    n = len(canonical_pred)
    budget = int(np.floor(epsilon * n))

    eligible = np.flatnonzero(canonical_pred == 0)
    ranked = eligible[np.argsort(-profit_gain[eligible])]
    candidates = ranked[:budget]
    flip_idx = candidates[profit_gain[candidates] > 0]

    new_pred = canonical_pred.copy()
    new_pred[flip_idx] = 1

    return {
        "epsilon": epsilon,
        "budget": budget,
        "n_flipped": int(len(flip_idx)),
        "surplus": float(profit_gain[flip_idx].sum()),
        "flipped_indices": flip_idx,
        "new_pred": new_pred,
    }


def sweep_epsilon(
    y_true: np.ndarray,
    canonical_pred: np.ndarray,
    profit_gain: np.ndarray,
    epsilons: list[float] = DEFAULT_EPSILON_GRID,
) -> dict:
    """Run adversarial_ceiling over a grid of epsilon values.

    Default grid from README.md section 6.2: {0.1%, 0.5%, 1%, 2%, 5%}.
    """
    return {eps: adversarial_ceiling(y_true, canonical_pred, profit_gain, eps) for eps in epsilons}
