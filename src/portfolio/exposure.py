import pandas as pd

class ExposureCalculator:
    @staticmethod
    def by_asset_class(prices: pd.Series, positions: pd.DataFrame) -> dict:
        """Exposure aggregated by asset class."""
        exposure = {}
        for _, row in positions.iterrows():
            asset = row['asset']
            asset_class = row['asset_class']
            qty = row['quantity']
            if asset in prices:
                val = qty * prices[asset]
                exposure[asset_class] = exposure.get(asset_class, 0) + val
        return exposure
    
    @staticmethod
    def top_exposures(prices: pd.Series, positions: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
        """Return top N exposures as DataFrame."""
        exposures = []
        for _, row in positions.iterrows():
            asset = row['asset']
            qty = row['quantity']
            if asset in prices:
                exposures.append({'asset': asset, 'exposure': qty * prices[asset]})
        df = pd.DataFrame(exposures).sort_values('exposure', ascending=False)
        return df.head(top_n)