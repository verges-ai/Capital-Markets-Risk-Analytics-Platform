import pandas as pd
import numpy as np
from datetime import datetime
import os

# Get the project root directory (two levels up from this file: src/market_data/ -> root)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# ---------------------------
# Data Generation Functions
# ---------------------------
def generate_market_prices():
    """Generate synthetic daily market prices for last 252 days."""
    dates = pd.date_range(end=datetime.today(), periods=252, freq='B')
    # Risk factors
    factors = pd.DataFrame(index=dates)
    factors['equity_idx'] = 100 * np.exp(np.random.normal(0, 0.01, 252).cumsum())
    factors['bond_yield'] = 0.02 + np.random.normal(0, 0.0005, 252).cumsum()
    factors['oil_price'] = 70 + np.random.normal(0, 0.01, 252).cumsum()
    factors['vix'] = 15 + np.random.gamma(2, 0.5, 252).cumsum()
    
    assets = {
        'AAPL Equity': {'factor': 'equity_idx', 'beta': 1.2, 'base_price': 150},
        'MSFT Equity': {'factor': 'equity_idx', 'beta': 1.1, 'base_price': 280},
        'TLT Bond': {'factor': 'bond_yield', 'beta': -5.0, 'base_price': 95},
        'SPY ETF': {'factor': 'equity_idx', 'beta': 1.0, 'base_price': 400},
        'OIL Future': {'factor': 'oil_price', 'beta': 1.0, 'base_price': 70},
        'VIX Call': {'factor': 'vix', 'beta': 0.8, 'base_price': 2.5}
    }
    
    prices = pd.DataFrame(index=dates)
    for asset, params in assets.items():
        factor_returns = factors[params['factor']].pct_change()
        asset_returns = params['beta'] * factor_returns + np.random.normal(0, 0.005, len(factor_returns))
        prices[asset] = params['base_price'] * (1 + asset_returns.fillna(0)).cumprod()
    
    os.makedirs(DATA_DIR, exist_ok=True)
    prices.to_csv(os.path.join(DATA_DIR, "market_prices.csv"))
    factors.to_csv(os.path.join(DATA_DIR, "risk_factors.csv"))
    return prices, factors

def generate_positions():
    """Generate synthetic portfolio positions."""
    positions = pd.DataFrame({
        'asset': ['AAPL Equity', 'MSFT Equity', 'TLT Bond', 'SPY ETF', 'OIL Future', 'VIX Call'],
        'quantity': [1000, 500, 20000, 300, 5000, 10000],
        'currency': ['USD', 'USD', 'USD', 'USD', 'USD', 'USD'],
        'asset_class': ['Equity', 'Equity', 'Bond', 'ETF', 'Derivative', 'Derivative']
    })
    positions.to_csv(os.path.join(DATA_DIR, "positions.csv"), index=False)
    return positions

def generate_benchmark():
    """Generate benchmark weights."""
    benchmark = pd.DataFrame({
        'asset': ['SPY ETF', 'TLT Bond'],
        'weight': [0.6, 0.4]
    })
    benchmark.to_csv(os.path.join(DATA_DIR, "benchmark.csv"), index=False)
    return benchmark

def generate_and_save_data():
    """Generate all data files."""
    generate_market_prices()
    generate_positions()
    generate_benchmark()
    print(f"Data generated and saved to '{DATA_DIR}' directory.")

# ---------------------------
# Data Loading Functions
# ---------------------------
def load_market_prices():
    """Load market prices from CSV."""
    path = os.path.join(DATA_DIR, "market_prices.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Market prices file not found at {path}. Run generate_and_save_data() first.")
    return pd.read_csv(path, index_col=0, parse_dates=True)

def load_risk_factors():
    """Load risk factors from CSV."""
    path = os.path.join(DATA_DIR, "risk_factors.csv")
    return pd.read_csv(path, index_col=0, parse_dates=True)

def load_positions():
    """Load portfolio positions from CSV."""
    path = os.path.join(DATA_DIR, "positions.csv")
    return pd.read_csv(path)

def load_benchmark():
    """Load benchmark weights from CSV."""
    path = os.path.join(DATA_DIR, "benchmark.csv")
    return pd.read_csv(path)

# Optional: Load real data from vendor feed (if needed)
def load_real_market_prices(tickers=None):
    """
    Alternative loader using yfinance via VendorFeed.
    Requires yfinance installed. Kept separate to avoid dependency issues.
    """
    if tickers is None:
        tickers = ["AAPL", "MSFT", "TLT", "SPY", "CL=F", "^VIX"]
    from src.market_data.vendor_feed import VendorFeed
    vf = VendorFeed()
    prices = vf.get_market_data(tickers)
    return prices