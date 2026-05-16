import pandas as pd
import numpy as np

class PnLCalculator:
    @staticmethod
    def daily_pnl(prices: pd.DataFrame, positions: pd.DataFrame) -> pd.Series:
        """Compute daily P&L assuming constant positions."""
        # Ensure we have only assets in positions
        assets = positions['asset'].tolist()
        asset_prices = prices[assets].copy()
        quantities = positions.set_index('asset')['quantity']
        # Daily changes multiplied by quantity
        daily_changes = asset_prices.diff()
        pnl = daily_changes.multiply(quantities, axis=1).sum(axis=1)
        return pnl.dropna()
    
    @staticmethod
    def cumulative_pnl(pnl_series: pd.Series) -> pd.Series:
        return pnl_series.cumsum()