import numpy as np
from scipy.stats import norm

def calculate_var_historical(pnl_series, confidence=0.95):
    """Historical VaR."""
    pnl_sorted = pnl_series.sort_values()
    idx = int((1 - confidence) * len(pnl_sorted))
    var = pnl_sorted.iloc[idx]
    return var

def calculate_var_parametric(pnl_series, confidence=0.95):
    """Parametric VaR assuming normal distribution."""
    mu = pnl_series.mean()
    sigma = pnl_series.std()
    z = norm.ppf(1 - confidence)
    var = mu + z * sigma
    return var