import pandas as pd
from src.market_data.data_loader import load_positions

class InternalFeed:
    """Simulates internal trading system positions."""
    @staticmethod
    def get_positions():
        return load_positions()