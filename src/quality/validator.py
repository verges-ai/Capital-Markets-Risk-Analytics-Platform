import pandas as pd
import numpy as np

class DataValidator:
    @staticmethod
    def validate(prices: pd.DataFrame, positions: pd.DataFrame) -> list:
        issues = []
        # Missing prices
        if prices.isnull().any().any():
            issues.append("Missing prices detected")
        # Duplicate positions
        if positions['asset'].duplicated().any():
            issues.append("Duplicate positions found")
        # Negative quantities
        neg_qty = positions[positions['quantity'] < 0]
        if not neg_qty.empty:
            issues.append(f"Negative quantities: {neg_qty['asset'].tolist()}")
        # Stale data (price unchanged for >5 days)
        stale = prices.apply(lambda col: (col == col.shift(1)).sum() > 5)
        if stale.any():
            stale_assets = stale[stale].index.tolist()
            issues.append(f"Stale prices for: {stale_assets}")
        # Price anomalies (e.g., >3 std from mean)
        for col in prices.columns:
            mean = prices[col].mean()
            std = prices[col].std()
            latest = prices[col].iloc[-1]
            if abs(latest - mean) > 3 * std:
                issues.append(f"Price anomaly for {col}: latest {latest:.2f} vs mean {mean:.2f}")
        return issues