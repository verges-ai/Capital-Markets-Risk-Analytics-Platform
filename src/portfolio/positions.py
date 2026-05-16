import pandas as pd

class PositionManager:
    @staticmethod
    def get_current_value(prices: pd.Series, positions: pd.DataFrame) -> float:
        """Compute total current portfolio value."""
        total = 0.0
        for _, row in positions.iterrows():
            asset = row['asset']
            qty = row['quantity']
            if asset in prices:
                total += qty * prices[asset]
        return total
    
    @staticmethod
    def get_weights(prices: pd.Series, positions: pd.DataFrame) -> dict:
        """Compute portfolio weights as dict {asset: weight}."""
        values = {}
        total = 0.0
        for _, row in positions.iterrows():
            asset = row['asset']
            qty = row['quantity']
            if asset in prices:
                val = qty * prices[asset]
                values[asset] = val
                total += val
        if total == 0:
            return {asset: 0 for asset in values}
        return {asset: val/total for asset, val in values.items()}