import numpy as np

def calculate_expected_shortfall(pnl_series, confidence=0.95):
    """Historical Expected Shortfall (average of worst (1-confidence)% losses)."""
    pnl_sorted = pnl_series.sort_values()
    idx = int((1 - confidence) * len(pnl_sorted))
    es = pnl_sorted.iloc[:idx+1].mean()
    return es