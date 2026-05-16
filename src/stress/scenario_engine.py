import pandas as pd


class ScenarioEngine:


    def equity_crash(
        self,
        portfolio_df,
        shock=-0.20
    ):

        stressed = portfolio_df.copy()

        stressed["market_value"] = (
            stressed["market_value"]
            *
            (1+shock)
        )

        return stressed


    def rate_shock(
        self,
        portfolio_df,
        shock=-0.05
    ):

        stressed = portfolio_df.copy()

        stressed["market_value"] = (
            stressed["market_value"]
            *
            (1+shock)
        )

        return stressed