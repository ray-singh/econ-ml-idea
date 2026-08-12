"""Load and clean "Give Me Some Credit", synthesize the elasticity signal w_i.

See README.md section 6.1.
"""

import numpy as np
import pandas as pd

RAW_PATH = "data/cs-training.csv"

# Known top-coded sentinel values in this dataset's delinquency counters
# (96/98) — not real counts, drop them rather than treat as legitimate data.
_DELINQUENCY_COLS = [
    "NumberOfTime30-59DaysPastDueNotWorse",
    "NumberOfTime60-89DaysPastDueNotWorse",
    "NumberOfTimes90DaysLate",
]


def load_credit_data(path: str = RAW_PATH) -> pd.DataFrame:
    """Load and clean the "Give Me Some Credit" training set.

    Returns a DataFrame with the original features and a binary
    default outcome column `y`, with rows containing missing/invalid
    values dropped or imputed.
    """
    df = pd.read_csv(path, index_col=0)
    df = df.rename(columns={"SeriousDlqin2yrs": "y"})

    df["MonthlyIncome"] = df["MonthlyIncome"].fillna(df["MonthlyIncome"].median())
    df["NumberOfDependents"] = df["NumberOfDependents"].fillna(df["NumberOfDependents"].median())

    for col in _DELINQUENCY_COLS:
        df = df[df[col] < 90]

    return df.reset_index(drop=True)


def synthesize_elasticity(
    df: pd.DataFrame,
    z_col: str,
    beta: float,
    noise_std: float = 1.0,
    seed: int | None = None,
) -> np.ndarray:
    """Synthesize elasticity w_i = logit^-1(beta * Z_i + noise).

    `z_col` should be a real, legitimately-used feature that is
    economically plausible as an elasticity proxy (e.g. number of
    existing credit lines). `beta` controls corr(w, Z), the
    experimental knob described in README.md section 6.1.

    Z_i is standardized before applying beta so that a given beta has
    a comparable effect on corr(w, Z) regardless of the raw feature's
    scale.
    """
    rng = np.random.default_rng(seed)
    z = df[z_col].to_numpy(dtype=float)
    z = (z - z.mean()) / (z.std() + 1e-9)
    noise = rng.normal(0.0, noise_std, size=len(z))
    return 1.0 / (1.0 + np.exp(-(beta * z + noise)))
