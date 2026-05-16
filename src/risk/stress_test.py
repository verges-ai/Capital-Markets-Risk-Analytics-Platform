import pandas as pd
import numpy as np

class StressTest:
    @staticmethod
    def apply_shock(prices: pd.Series, factors: pd.Series, positions: pd.DataFrame,
                    shock_factors: dict) -> tuple:
        """
        Apply shocks to risk factors and compute shocked portfolio value.
        Returns (pnl_change, shocked_prices_series).
        """
        shocked_prices = prices.copy()
        for asset in prices.index:
            # Determine factor exposure (simplified mapping)
            if 'Equity' in asset or 'ETF' in asset:
                factor_return = shock_factors.get('equity_idx', 0)
            elif 'Bond' in asset:
                factor_return = shock_factors.get('bond_yield', 0) * (-5)  # duration approx -5
            elif 'OIL' in asset:
                factor_return = shock_factors.get('oil_price', 0)
            elif 'VIX' in asset:
                factor_return = shock_factors.get('vix', 0)
            else:
                factor_return = 0
            shocked_prices[asset] = prices[asset] * (1 + factor_return)
        
        # Compute original and shocked portfolio values
        orig_value = 0.0
        shocked_value = 0.0
        for _, row in positions.iterrows():
            asset = row['asset']
            qty = row['quantity']
            if asset in prices:
                orig_value += qty * prices[asset]
                shocked_value += qty * shocked_prices[asset]
        
        pnl_change = shocked_value - orig_value
        return pnl_change, shocked_prices