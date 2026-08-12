"""Profit, surplus, and exploitability-alignment metrics.

See README.md section 6.3.
"""

import numpy as np


def profit(y_pred: np.ndarray, premium_schedule: dict, retention_prob: np.ndarray) -> float:
    """Total profit under a fixed premium schedule keyed by predicted class.

    Tier-0 individuals are always retained (normalized baseline);
    tier-1 individuals are retained with probability `retention_prob[i]`
    and otherwise contribute zero (they leave for a competitor).
    """
    y_pred = np.asarray(y_pred)
    pi0, pi1 = premium_schedule[0], premium_schedule[1]
    per_individual = np.where(y_pred == 1, pi1 * retention_prob, pi0)
    return float(per_individual.sum())


def discriminatory_surplus(profit_model: float, profit_canonical: float) -> float:
    """Surplus extracted over the canonical (validation-loss-minimizing) model."""
    return profit_model - profit_canonical


def exploitability_alignment(y_pred: np.ndarray, w: np.ndarray, theta: np.ndarray) -> float:
    """rho_m = corr(r_hat_m(X_i), w_i | theta_i): how well a model's
    predictions align with unobserved elasticity, conditional on true risk.

    Computed as the size-weighted average of the Pearson correlation
    within each true-risk subgroup (theta=0, theta=1).
    """
    y_pred, w, theta = np.asarray(y_pred, dtype=float), np.asarray(w, dtype=float), np.asarray(theta)
    corrs, weights = [], []
    for t in np.unique(theta):
        mask = theta == t
        if mask.sum() > 1 and y_pred[mask].std() > 0 and w[mask].std() > 0:
            corrs.append(np.corrcoef(y_pred[mask], w[mask])[0, 1])
            weights.append(mask.sum())
    if not corrs:
        return 0.0
    return float(np.average(corrs, weights=weights))
