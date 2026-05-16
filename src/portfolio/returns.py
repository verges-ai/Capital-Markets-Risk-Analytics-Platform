import pandas as pd


class ReturnEngine:


    def calculate_returns(
        self,
        pnl_series,
        exposure_series
    ):

        return (
            pnl_series
            /
            exposure_series
        )