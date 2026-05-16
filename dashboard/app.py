import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.storage.database import Database
from src.quality.validator import DataValidator
from src.portfolio.positions import PositionManager
from src.portfolio.exposure import ExposureCalculator
from src.portfolio.pnl import PnLCalculator
from src.risk.var import calculate_var_historical, calculate_var_parametric
from src.risk.expected_shortfall import calculate_expected_shortfall
from src.risk.stress_test import StressTest
from src.risk.monte_carlo import monte_carlo_var
from src.audit.logger import AuditLogger

st.set_page_config(page_title="Capital Markets Risk Analytics", layout="wide")
st.title("📊 Capital Markets Risk Analytics Platform")
st.markdown("### Centralized portfolio risk & performance dashboard")

# Load data
prices = Database.get_prices()
positions = Database.get_positions()
benchmark = Database.get_benchmark()
factors = Database.get_factors()

# Data validation
issues = DataValidator.validate(prices, positions)
if issues:
    st.warning("Data Quality Issues Detected")
    for issue in issues:
        st.write(f"⚠️ {issue}")
else:
    st.success("All data quality checks passed")
AuditLogger.log("Dashboard loaded – data validation completed")

# Portfolio overview
latest_prices = prices.iloc[-1]
total_value = PositionManager.get_current_value(latest_prices, positions)
weights = PositionManager.get_weights(latest_prices, positions)

st.sidebar.header("Portfolio Summary")
st.sidebar.metric("Total Portfolio Value (USD)", f"${total_value:,.0f}")

# Exposure pie chart
exposure_by_class = ExposureCalculator.by_asset_class(latest_prices, positions)
if exposure_by_class:
    fig = px.pie(names=list(exposure_by_class.keys()),
                 values=list(exposure_by_class.values()),
                 title="Exposure by Asset Class")
    st.plotly_chart(fig, use_container_width=True)

# Top exposures table
top_exposures = ExposureCalculator.top_exposures(latest_prices, positions)
st.subheader("Top 5 Exposures")
st.dataframe(top_exposures)

# P&L history
pnl_series = PnLCalculator.daily_pnl(prices, positions)
st.subheader("📈 Historical Daily P&L")
fig_pnl = px.line(pnl_series, title="Portfolio Daily Profit & Loss")
st.plotly_chart(fig_pnl, use_container_width=True)

# Risk analytics
st.subheader("📉 Risk Analytics")
confidence = st.slider("Confidence Level", 0.90, 0.99, 0.95, 0.01)

var_hist = calculate_var_historical(pnl_series, confidence)
var_par = calculate_var_parametric(pnl_series, confidence)
es = calculate_expected_shortfall(pnl_series, confidence)
mc_var = monte_carlo_var(pnl_series.values, confidence=confidence)

col1, col2, col3, col4 = st.columns(4)
col1.metric(f"Historical VaR ({confidence:.0%})", f"${var_hist:,.0f}")
col2.metric(f"Parametric VaR", f"${var_par:,.0f}")
col3.metric(f"Expected Shortfall", f"${es:,.0f}")
col4.metric(f"Monte Carlo VaR", f"${mc_var:,.0f}")

# Tracking error (simplified)
portfolio_returns = pnl_series / total_value
benchmark_assets = benchmark['asset'].tolist()
bm_prices = prices[benchmark_assets].copy()
bm_returns = bm_prices.pct_change().dot(benchmark.set_index('asset')['weight'])
common_idx = portfolio_returns.index.intersection(bm_returns.index)
excess = portfolio_returns.loc[common_idx] - bm_returns.loc[common_idx]
tracking_error = excess.std() * np.sqrt(252)
st.metric("Tracking Error (annualized)", f"{tracking_error:.2%}")

# Stress testing
st.subheader("💥 Stress Testing & Scenario Analysis")
with st.expander("Apply a shock scenario"):
    shock_equity = st.slider("Equity shock (%)", -30, 30, 0) / 100
    shock_oil = st.slider("Oil price shock (%)", -30, 30, 20) / 100
    shock_yield = st.slider("Bond yield change (bps)", -200, 200, 0) / 10000
    shock_vix = st.slider("VIX change (%)", -30, 30, 0) / 100
    
    if st.button("Run Stress Test"):
        shocks = {
            'equity_idx': shock_equity,
            'oil_price': shock_oil,
            'bond_yield': shock_yield,
            'vix': shock_vix
        }
        pnl_shock, shocked_prices = StressTest.apply_shock(latest_prices, factors.iloc[-1], positions, shocks)
        # Compute stressed VaR on shocked portfolio returns (approximation)
        # For demo, shift the historical PnL by the shock impact distributed across days
        shocked_pnl = pnl_series + (pnl_shock / len(pnl_series))
        shock_var = calculate_var_historical(shocked_pnl, confidence)
        shock_es = calculate_expected_shortfall(shocked_pnl, confidence)
        st.write(f"**Shock P&L:** ${pnl_shock:,.0f}")
        st.write(f"**VaR after shock ({confidence:.0%}):** ${shock_var:,.0f}")
        st.write(f"**ES after shock:** ${shock_es:,.0f}")
        AuditLogger.log(f"Stress test applied: shocks {shocks}")

# Audit trail
with st.expander("📋 Audit Log (last 5 entries)"):
    for entry in AuditLogger.get_last_n(5):
        st.write(entry)

# Business summary
st.markdown("---")
st.markdown("### 🎯 Business Value Summary")
st.info("""
**Capital Markets Risk Analytics Platform**  
- **Business Problem:** Fragmented market data, manual Excel workflows, delayed risk decisions.  
- **Solution:** Centralized ingestion, validation, exposure calculation, and advanced risk metrics (VaR, ES, Monte Carlo, stress testing, tracking error).  
- **Outcome:** Real‑time transparency, regulatory compliance, faster decision‑making (seconds vs. hours), full auditability.  
""")