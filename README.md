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

´´´
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
´´´


**Tech stack**:
- **Frontend / dashboard**: Streamlit
- **Data manipulation**: Pandas, NumPy
- **Visualisation**: Plotly
- **Statistics**: SciPy
- **Testing**: Pytest
- **Data sources**: Synthetic (or plug‑in yfinance for live data)

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/capital-markets-risk-analytics-platform.git
   cd capital-markets-risk-analytics-platform

2.   **Create a virtual environment**

   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows

3.   **Install dependencies**

   pip install -r requirements.txt

4.   **Generate initial data (synthetic market prices, positions, benchmark)**

   python -c "from src.market_data.data_loader import generate_and_save_data; generate_and_save_data()"

5.  **Usage**

   streamlit run dashboard/app.py

6. **Testing**

   pytest tests/


## 🌐 Live Demo   
   
Copy the entire block above into your `README.md`. Then replace `https://your-dashboard-url.com` with your actual deployment link (e.g., `https://capital-markets-risk.streamlit.app`).
