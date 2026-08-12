"""Experiment 2: train a realistic Rashomon set and measure exploitability.

Trains ~100-300 models varying algorithm (logistic regression, random
forest, gradient-boosted trees, shallow MLP), hyperparameters, and seeds.
Keeps only models within each epsilon band of best validation AUC, then
computes profit and exploitability alignment (rho_m) for each.

See README.md section 6.3.
"""

import numpy as np
import pandas as pd

MODEL_GRID = {
    "logistic_regression": {},
    "random_forest": {},
    "gradient_boosted_trees": {},
    "mlp": {},
}


def train_model_sweep(X: pd.DataFrame, y: np.ndarray, seeds: list[int]) -> list[dict]:
    """Train the full model x hyperparameter x seed grid.

    Returns a list of dicts, one per trained model, containing the
    fitted model, its validation AUC, and its predictions.
    """
    raise NotImplementedError


def filter_rashomon_set(models: list[dict], epsilon: float) -> list[dict]:
    """Keep only models within epsilon of the best validation AUC/loss."""
    raise NotImplementedError


def best_exploiter(rashomon_set: list[dict], w: np.ndarray, theta: np.ndarray) -> dict:
    """Find the profit-maximizing model within a realistic Rashomon set
    and report how much of the Experiment-1 ceiling it captures.
    """
    raise NotImplementedError
