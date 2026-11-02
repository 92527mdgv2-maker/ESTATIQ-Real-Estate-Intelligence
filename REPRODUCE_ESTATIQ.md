# ESTATIQ | Professor Reproduction Guide

**Project:** ESTATIQ — Real Estate Intelligence

**Purpose:** This guide explains how to download, install, reproduce, test, and run the ESTATIQ Python real estate analytics application.

**GitHub Repository:** Add repository URL here.

---

## 1. Project Overview

ESTATIQ is an interactive Python-based real estate intelligence dashboard developed as an academic project.

The application uses Zillow Home Value Index (ZHVI) data to analyze historical housing values across U.S. cities and states.

Major features include:

Executive housing market overview
Interactive U.S. housing market map
Historical housing value trends
City-to-city market comparisons
Market rankings and annual growth analysis
Machine learning prediction evaluation
Data quality and missing-value analysis
Downloadable analytical results

The application is developed using Python, Streamlit, Pandas, NumPy, Plotly, Matplotlib, and Scikit-learn.

## 2. Requirements

Before beginning, install:

Python 3.10 or newer
GitHub Desktop or Git
Visual Studio Code (recommended)
A modern web browser
An internet connection

The user must also obtain the Zillow source dataset separately.

## 3. Clone the GitHub Repository

The repository may be private. If so, the project owner must invite the professor as a GitHub collaborator.

### Using GitHub Desktop

Install and open GitHub Desktop.
Sign in to GitHub.
Select File > Clone Repository.
Find ESTATIQ-Real-Estate-Intelligence.
Select a new, empty local destination.
Click Clone.
Open the cloned repository in Visual Studio Code.

Alternatively, use the terminal:

```bash
git clone REPLACE_WITH_REPOSITORY_URL
cd ESTATIQ-Real-Estate-Intelligence
```

Replace the placeholder with the actual GitHub repository URL.

## 4. Set Up the Python Environment

Open the VS Code terminal inside the cloned ESTATIQ repository.

### macOS

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

### Windows PowerShell

Create a virtual environment:

```powershell
py -m venv .venv
```

Activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### Install the Required Libraries

Run:

```bash
python -m pip install -r requirements.txt
```

This installs the Python libraries required by ESTATIQ.

## 5. Download the Zillow Dataset

ESTATIQ uses publicly available data from Zillow Research.

Official data source:

https://www.zillow.com/research/data/

### Required Dataset

Locate the Zillow Home Value Index (ZHVI) dataset using these selections:

Geography: City
Home type: Single-Family Residences and Condominiums
Price tier: Middle Tier (33rd to 67th percentile)
Data frequency: Monthly
Adjustment: Seasonally Adjusted

The source filename is typically:

`City_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv`

### Prepare the File

Download the correct CSV dataset.
Rename it to `zillow_city.csv`.
Open the cloned ESTATIQ project folder.
Open the `data` folder.
Place `zillow_city.csv` inside the `data` folder.

Expected location:

```text
ESTATIQ-Real-Estate-Intelligence/
    data/
        zillow_city.csv
```

IMPORTANT:

The large Zillow datasets are intentionally excluded from GitHub to keep the repository manageable.

The original project used approximately 21,364 city records, with housing observations extending through September 2026.

Zillow periodically updates its data. A newer download may produce different housing values, record counts, or date ranges.

For exact numerical reproduction, the same historical dataset snapshot is required.

## 6. Run Zillow Data Preparation

In the VS Code terminal, execute:

```bash
python explore_data.py
```

This script loads and processes the original Zillow dataset.

It generates:

`data/zillow_cleaned.csv`

For the original project snapshot, approximately 21,364 city records were processed.

Confirm that the terminal reports successful data preparation before continuing.

## 7. Run Machine Learning Evaluation

After data preparation, execute:

```bash
python machine_learning_v2.py
```

The application evaluates three models:

Previous-month baseline model
Linear Regression
Random Forest Regression

The models are evaluated using historical housing value observations.

The project uses chronological training and testing, reserving the latest twelve months for historical evaluation.

Results are evaluated using:

Mean Absolute Error (MAE)
Root Mean Squared Error (RMSE)
R-squared (R²)

The script generates:

```text
data/model_results.csv
data/model_predictions.csv
```

The second file contains historical actual-versus-predicted results used by the dashboard.

IMPORTANT:

The model evaluation is a historical one-month-ahead backtest. It is not a validated long-term housing market forecast.

## 8. Run Automated Tests

ESTATIQ includes automated data-validation and integration checks.

Execute:

```bash
python -m unittest -v test_estatiq.py
```

Expected output for the verified project:

```text
Ran 7 tests

OK
```

The tests check basic dataset availability and structure, machine learning output files, and model evaluation data.

These tests do not cover every possible dashboard interaction.

## 9. Launch ESTATIQ

Start the Streamlit dashboard:

```bash
python -m streamlit run estatiq_dashboard_v7_us_market_map.py
```

The application should open automatically in a web browser.

If it does not, open:

http://localhost:8501

Keep the terminal running while using the dashboard.

To stop the application, press Control + C inside the terminal.

## 10. Explore the Dashboard

### Overview

Select a state and compare cities using historical housing value charts and market summary indicators.

Recommended example:

Texas
Dallas
Houston
Austin
San Antonio
Fort Worth

### US Market Map

Explore housing market conditions geographically.

Hover over states to view housing statistics and change the displayed market metric.

State-level visualization is available without additional geographic files.

Individual city markers require a separate verified city-coordinate dataset.

### Market Trends

Examine monthly housing value changes and historical patterns.

### City Comparison

Compare estimated housing values across selected cities.

### Market Rankings

Rank housing markets using home values, monthly changes, and year-over-year growth rates.

### Machine Learning

Review model evaluation metrics and actual-versus-predicted housing values.

Compare the baseline, Linear Regression, and Random Forest models.

### Data Quality

Review dataset coverage, missing observations, and data limitations.

## 11. Expected Project Structure

```text
ESTATIQ-Real-Estate-Intelligence/
|
|-- estatiq_dashboard_v7_us_market_map.py
|-- explore_data.py
|-- machine_learning_v2.py
|-- visualization.py
|-- test_estatiq.py
|-- requirements.txt
|-- README.md
|-- REPRODUCE_ESTATIQ.md
|
|-- charts/
|
|-- data/
|   |-- zillow_city.csv
|   |-- zillow_cleaned.csv
|   |-- model_results.csv
|   |-- model_predictions.csv
```

The original Zillow dataset must be downloaded separately.

The cleaned dataset and prediction results are generated by the Python scripts.

## 12. Troubleshooting

### Streamlit Is Not Installed

Activate the project's virtual environment and run:

```bash
python -m pip install -r requirements.txt
```

### Original Zillow Dataset Is Missing

Verify that the file exists at:

`data/zillow_city.csv`

If not, download and rename the correct city-level Zillow dataset.

### Cleaned Dataset Is Missing

Run:

```bash
python explore_data.py
```

### Machine Learning Results Are Missing

Run:

```bash
python machine_learning_v2.py
```

### Dashboard Shows a Connection Error

Restart Streamlit:

```bash
python -m streamlit run estatiq_dashboard_v7_us_market_map.py
```

Keep the terminal running.

### Dashboard Values Differ

Zillow updates and revises its datasets.

Results may differ when using a newer dataset version.

## 13. Reproduction Verification Checklist

[ ] Accessed the ESTATIQ GitHub repository
[ ] Successfully cloned the repository
[ ] Created and activated the Python environment
[ ] Installed dependencies from requirements.txt
[ ] Downloaded the correct Zillow city-level dataset
[ ] Ran explore_data.py successfully
[ ] Ran machine_learning_v2.py successfully
[ ] Regenerated the model results and predictions
[ ] Passed all seven automated tests
[ ] Launched the Streamlit dashboard
[ ] Verified the U.S. Market Map
[ ] Verified the Machine Learning section
[ ] Verified Market Rankings and Data Quality

## 14. Data Attribution and Limitations

Data source: Zillow Research — Zillow Home Value Index (ZHVI).

ZHVI represents estimated typical home values, not individual home sale prices.

The application analyzes historical housing data and is intended for academic and research purposes.

Machine learning results are historical model evaluations and do not guarantee future home prices.

ESTATIQ is an independent educational project and is not affiliated with or endorsed by Zillow.

---

**ESTATIQ | Real Estate Intelligence**

Python Midterm Project — Reproduction and Verification Documentation