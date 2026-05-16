from src.market_data.data_loader import MarketDataLoader


loader = MarketDataLoader()


positions = loader.load_positions()

print(positions)


market = loader.load_market_universe()

print(
    market["DAX"].head()
)