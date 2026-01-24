"""
Data Analysis Dashboard - Main Application Entry Point

This is a professional, interactive web application for exploring and analyzing datasets.
Built with Streamlit, it provides automatic data cleaning, statistical analysis, and
interactive visualizations suitable for both technical and non-technical users.

Features:
- Dataset health scoring and quality assessment
- Plain English explanations for statistical findings
- Transparent data cleaning with detailed change tracking
- Statistical validity warnings for hypothesis tests
- Interactive visualizations (histograms, scatter plots, correlations, etc.)
- Comprehensive statistical analysis tools

Usage:
    Run the application from the command line:
    
    $ streamlit run app.py
    
    Then upload a CSV or Excel file through the sidebar to begin analysis.

Author: Antigravity
Date: 2025-11-24
Version: 1.0.0
"""

import streamlit as st
from src.dashboard import DashboardApp

# Application entry point
if __name__ == "__main__":
    # Initialize and run the dashboard application
    app = DashboardApp()
    app.run()
