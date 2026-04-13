# Data Analysis Dashboard

## Overview
A professional, interactive web application for exploring, cleaning, and analyzing datasets (CSV or Excel files). Built with Streamlit, it provides automated insights, data quality scoring, and plain-English explanations of statistical results.

## Architecture
- **Framework:** Streamlit (Python)
- **Port:** 5000
- **Entry Point:** `app.py`

## Project Structure
```
/
├── app.py                # Main entry point
├── requirements.txt      # Python dependencies
├── sample_data.csv       # Example dataset
├── .streamlit/
│   └── config.toml       # Streamlit server config (port 5000, host 0.0.0.0)
└── src/
    ├── __init__.py
    ├── dashboard.py      # UI orchestration
    ├── data_manager.py   # Data loading, cleaning, quality scoring
    ├── stats_manager.py  # Statistical tests (normality, t-tests, correlations)
    └── visualizer.py     # Interactive Plotly charts
```

## Key Features
- Dataset health score (missing values, duplicates, outliers)
- Automated data cleaning with change tracking
- Statistical analysis: IQR outlier detection, Pearson correlation, Shapiro-Wilk normality tests
- Interactive Plotly visualizations (histograms, scatter plots, correlation matrices)
- Plain English explanations for all statistical findings

## Dependencies
- streamlit, pandas, numpy, scipy, plotly, openpyxl

## Running the App
```
streamlit run app.py
```
The app runs on port 5000 at 0.0.0.0.

## Deployment
Configured as autoscale deployment running `streamlit run app.py --server.port=5000 --server.address=0.0.0.0`.
