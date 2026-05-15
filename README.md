# Capital Markets Risk Analytics Platform

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🏦 Business Context

Investment banks and asset managers (HSBC, DZ BANK, ODDO BHF) face a critical challenge:

> Market data, portfolio positions, and risk calculations are fragmented across Bloomberg/Reuters, internal trading systems, Excel reports, and SQL databases.

This fragmentation leads to:
- Data inconsistencies
- Manual, error‑prone reporting
- Delayed risk decisions
- Regulatory audit risks (Basel III, CRR III, EMIR, MiFID II, ICAAP)

## 🎯 Project Goal

Build a **centralised risk analytics platform** that:

1. **Ingests** data from multiple sources (vendor feeds, internal positions, benchmarks)
2. **Validates** data quality (missing prices, stale data, duplicates, anomalies)
3. **Calculates** portfolio exposure, P&L, and advanced risk metrics:
   - Value at Risk (Historical & Parametric)
   - Expected Shortfall
   - Monte Carlo Simulation
   - Stress Testing (custom scenarios)
   - Tracking Error vs benchmark
4. **Visualises** results in an interactive dashboard for portfolio managers, risk controllers, and management.
5. **Audits** every calculation for regulatory compliance.

## 🏗️ Architecture

The platform follows a modular, production‑ready structure:
Capital Markets Risk Analytics Platform/
│
├── data/ # CSV data (generated once)
├── dashboard/ # Streamlit frontend (app.py)
├── src/ # Core business logic
│ ├── audit/ # Audit trail logging
│ ├── market_data/ # Vendor feed & internal data loaders
│ ├── quality/ # Data validation
│ ├── storage/ # In‑memory database (CSV caching)
│ ├── portfolio/ # Positions, exposure, P&L
│ └── risk/ # VaR, ES, Monte Carlo, stress tests
├── tests/ # Unit tests (pytest)
├── notebooks/ # Jupyter exploratory analysis
├── requirements.txt
└── README.md
