import yfinance as yf
import pandas as pd

class VendorFeed:
    def get_market_data(self, tickers, period="2y"):
        """
        Fetch adjusted close prices for multiple tickers.
        Returns a DataFrame with dates as index, columns = tickers.
        """
        data = yf.download(tickers, period=period, auto_adjust=True)['Close']
        return data
    
    def get_single_ticker(self, ticker, period="2y"):
        data = yf.download(ticker, period=period, auto_adjust=True)
        data = data.reset_index()
        data["ticker"] = ticker
        return data[["Date", "ticker", "Close", "Volume"]]