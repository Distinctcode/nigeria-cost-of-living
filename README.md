# 🇳🇬 Nigeria Selected Food Prices Dashboard

## Project Overview

This project uses Python and exploratory data analysis (EDA) to investigate selected food prices across Nigeria's six geopolitical zones.

The analysis examines price changes across three reporting periods, compares recorded prices between regions, and investigates how much prices vary across geopolitical zones.

An interactive dashboard was developed with Streamlit and Plotly to make the findings accessible through charts, summary statistics, tables, and downloadable datasets.

## Project Objectives

* Explore the prices of 42 selected food items.
* Examine month-on-month (MoM) and year-on-year (YoY) price changes.
* Compare recorded food prices across Nigeria's six geopolitical zones.
* Investigate regional price variability.
* Present analytical findings through an interactive dashboard.
* Make cleaned datasets available for further analysis.

## Tools and Technologies

* Python — programming and analysis.
* Pandas — data preparation and analysis.
* Jupyter Notebook — exploratory data analysis.
* Plotly — interactive visualisations.
* Streamlit — interactive dashboard development.
* Git and GitHub — version control and project publication.

## Dashboard Features

The dashboard contains five main sections:

1. Overview: Summary metrics, selected high-priced food items, and regional averages.
2. Food Price Analysis: Comparison of reporting periods and price changes.
3. Regional Comparison: Comparison of selected food items across six geopolitical zones.
4. Regional Variability: Examination of differences between regional prices.
5. Data Explorer: Search, inspect, and download cleaned datasets.

## Reporting Periods

The food-price analysis covers:

* May 2025
* April 2026
* May 2026

These are three reporting periods, not a complete continuous monthly time series.

## Key Findings

* The mean reported month-on-month price change across the selected items was approximately (+2.24%).
* The mean reported year-on-year change was approximately (−3.58%).
* The South East recorded the highest mean across the regional price columns, while the North West recorded the lowest.
* Regional price differences varied considerably by food item.

These findings apply only to the selected items in the supplied dataset.

## Project Structure

Nigeria-cost-of-living/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── notebooks/
│   └── 01_exploratory_analysis.ipynb
└── data/
    └── processed/
        ├── food_prices_cleaned.csv
        ├── regional_prices_cleaned.csv
        └── regional_variability.csv


## How to Run the Dashboard Locally

1. Clone or download this repository.

2. Open a terminal in the project folder.

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

5. Open the local address provided in the terminal.

Ensure that all three processed CSV files are available in `data/processed/`.

## Data Scope and Limitations

This project analyses selected food items; it does not measure every component of Nigeria's cost of living.

The reporting periods are limited to those supplied in the workbook. The original data source, currency, measurement units, and pack sizes should be confirmed before interpreting absolute prices or making direct comparisons between different food items.

Regional price differences describe the supplied observations and should not, on their own, be interpreted as evidence of the causes of those differences.

## Author

Developed as a data analytics project demonstrating data cleaning, exploratory analysis, regional comparisons, data visualisation, and interactive dashboard development.
