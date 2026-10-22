# Data Analysis Dashboard

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://saudmonsour-data-analysis-dashboard-app-uu96ud.streamlit.app/)

A professional, interactive web application for exploring and analyzing your data. Built with Streamlit and designed for both technical and non-technical users.

## What This Does

This dashboard helps you understand your data through automatic analysis and interactive visualizations. Upload a CSV or Excel file, and the application will clean your data, calculate statistics, detect patterns, and create charts to help you make sense of it all.

## Key Features

**Dataset Health Score**
Get an instant assessment of your data quality. The dashboard calculates a score from 0 to 100 based on missing values, duplicates, outliers, and data consistency.

**Plain English Insights**
Statistical jargon can be confusing. This tool explains what's happening in your data using simple language.

**Data Cleaning Transparency**
When you upload data, the dashboard automatically cleans it by removing duplicates and filling in missing values. A detailed summary shows exactly what was changed.

**Statistical Validity Warnings**
Running statistical tests on small samples can give misleading results. The dashboard warns you when your sample size is too small or when groups are unbalanced.

**Interactive Visualizations**
Create histograms, scatter plots, line charts, box plots, and bar charts. All charts are interactive, allowing you to zoom, pan, and hover for details.

**Correlation Analysis**
Discover relationships between variables with an interactive heatmap and ranked list of the strongest correlations in your dataset.

**Outlier Detection**
Automatically identify unusual values using the IQR method.

**Hypothesis Testing**
Test your assumptions with built-in normality tests and t-tests.

## How to Use

Upload a CSV or Excel file through the sidebar and explore the different sections and tabs to see various analyses. A sample dataset is included in `sample_data.csv` if you want to try the dashboard right away.

## Project Structure

```text
data-analysis-dashboard/
├── app.py                # Application entry point
├── requirements.txt      # Python dependencies
├── sample_data.csv       # Example dataset
└── src/
    ├── dashboard.py      # Main UI and orchestration
    ├── data_manager.py   # Data loading and cleaning
    ├── stats_manager.py  # Statistical calculations
    └── visualizer.py     # Chart creation
```


## Technical Details

The application uses an object-oriented architecture with clear separation of concerns. All calculations use industry-standard methods including IQR for outlier detection, Pearson's correlation coefficient, and Shapiro-Wilk normality tests.



## Requirements

* **Python:** 3.8+
* **Framework:** Streamlit
* **Data Libraries:** pandas, numpy, scipy
* **Visualization:** plotly
* **Excel Support:** openpyxl
