import pandas as pd
import os
from src.market_data.data_loader import load_market_prices, load_positions, load_benchmark, load_risk_factors

class Database:
    """Simple in-memory storage with optional CSV persistence."""
    _prices = None
    _positions = None
    _benchmark = None
    _factors = None
    
    @classmethod
    def get_prices(cls):
        if cls._prices is None:
            cls._prices = load_market_prices()
        return cls._prices
    
    @classmethod
    def get_positions(cls):
        if cls._positions is None:
            cls._positions = load_positions()
        return cls._positions
    
    @classmethod
    def get_benchmark(cls):
        if cls._benchmark is None:
            cls._benchmark = load_benchmark()
        return cls._benchmark
    
    @classmethod
    def get_factors(cls):
        if cls._factors is None:
            cls._factors = load_risk_factors()
        return cls._factors
    
    @classmethod
    def refresh(cls):
        """Reload all data from CSV."""
        cls._prices = load_market_prices()
        cls._positions = load_positions()
        cls._benchmark = load_benchmark()
        cls._factors = load_risk_factors()