"""Section 6.5 robustness check: does a group-fairness constraint close
the discriminatory-surplus gap?

Adds an equalized-odds constraint w.r.t. a synthetic protected attribute
that is uncorrelated with elasticity w_i, then re-runs the Experiment 1/2
comparison to show the gap persists.

See README.md section 6.5.
"""

import numpy as np
import pandas as pd


def synthesize_protected_attribute(df: pd.DataFrame, seed: int | None = None) -> np.ndarray:
    """Synthesize a protected attribute independent of elasticity w_i."""
    raise NotImplementedError


def fit_equalized_odds_model(X: pd.DataFrame, y: np.ndarray, protected: np.ndarray):
    """Fit a model subject to an equalized-odds constraint w.r.t. `protected`."""
    raise NotImplementedError
