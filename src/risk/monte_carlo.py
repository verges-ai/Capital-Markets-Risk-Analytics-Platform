import numpy as np

def monte_carlo_var(pnl_series: np.ndarray, n_sim: int = 10000,
                    horizon: int = 1, confidence: float = 0.95) -> float:
    """Monte Carlo VaR assuming normal distribution of daily P&L."""
    mu = pnl_series.mean()
    sigma = pnl_series.std()
    simulated_pnl = np.random.normal(mu * horizon, sigma * np.sqrt(horizon), n_sim)
    var = np.percentile(simulated_pnl, (1 - confidence) * 100)
    return var