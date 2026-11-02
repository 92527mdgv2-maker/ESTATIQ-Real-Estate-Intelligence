
# ESTATIQ | Real Estate Intelligence

**An interactive U.S. housing market analytics platform powered by Python, Zillow housing data, and machine learning.**

ESTATIQ is a Python-based real estate intelligence dashboard designed to help users explore historical housing market trends, compare property values across U.S. cities, evaluate regional market performance, and analyze machine learning predictions.

The application combines data science, geographic visualization, and predictive analytics in a professional, interactive web interface.

> **Academic Project:** ESTATIQ was developed as a Python midterm project to demonstrate data processing, visualization, machine learning, and interactive application development.

---

## 1. Project Overview

The U.S. real estate market contains large amounts of historical data that can be difficult to interpret without analytical tools.

ESTATIQ addresses this challenge by transforming Zillow housing market data into accessible, interactive visualizations and statistical insights.

The primary objectives are to:

- Analyze historical housing value trends.
- Compare estimated home values across U.S. cities.
- Identify market growth and decline.
- Visualize regional housing patterns geographically.
- Evaluate machine learning models using historical data.
- Provide an intuitive interface for exploring housing market information.

## 2. Dashboard Features

### Executive Market Overview

The main dashboard provides a high-level summary of housing market conditions.

Features include:

- Total cities represented in the dataset.
- Selected state and cities.
- Average estimated home values.
- Interactive historical housing value charts.
- Comparisons between selected cities.

### Interactive U.S. Market Map

ESTATIQ includes an interactive geographic visualization of the United States.

Users can:

- Explore housing market statistics by state.
- View geographic differences in estimated housing values.
- Compare annual housing value growth.
- Hover over states to inspect market information.
- Download state-level market summaries.

The state-level map uses Zillow city data to calculate regional summaries.

Individual city markers require an additional verified geographic coordinate dataset.

### Historical Market Trends

The Market Trends section allows users to explore changes in estimated home values over time.

Users can select cities and examine historical patterns through interactive line charts.

### City Comparison

The City Comparison section enables users to evaluate housing market differences between selected cities.

Comparisons include estimated home values and annual changes.

### Market Rankings

The Market Rankings section identifies cities based on selected market statistics.

Users can rank cities by:

- Estimated home values.
- Year-over-year percentage changes.
- Month-over-month percentage changes.

Results can be filtered and downloaded as CSV files.

### Machine Learning Intelligence

ESTATIQ evaluates multiple machine learning approaches to predicting historical monthly housing values.

The application compares:

1. Previous-month baseline model.
2. Linear Regression.
3. Random Forest Regression.

Users can examine:

- Model performance metrics.
- Actual versus predicted housing values.
- Monthly prediction errors.
- Historical model comparisons.
- City-specific prediction results.

### Data Quality Analysis

The Data Quality section provides information about the underlying dataset.

It examines:

- Historical data coverage.
- Missing observations.
- Duplicate region identifiers.
- Availability of monthly housing estimates.

This helps users understand the reliability and limitations of the analysis.

---

## 3. Technologies Used

ESTATIQ is developed using the Python programming language.

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive dashboard development |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical calculations |
| Plotly | Interactive charts and geographic maps |
| Scikit-learn | Machine learning models and evaluation |
| Matplotlib | Supplementary data visualizations |
| Git | Version control |
| GitHub | Repository hosting and development history |
| Visual Studio Code | Development environment |

---

## 4. Data Source

### Zillow Home Value Index (ZHVI)

The project uses housing market data provided by Zillow Research.

Official source:

https://www.zillow.com/research/data/

The dataset contains monthly Zillow Home Value Index estimates for U.S. cities.

Dataset type:

**City-level ZHVI — Single-Family Residences and Condominiums, Middle Price Tier, Seasonally Adjusted, Monthly.**

Original dataset filename:

`City_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv`

The project's historical dataset contains approximately 21,364 city or region records and monthly data extending through September 2026.

### Important Data Interpretation

The Zillow Home Value Index represents estimated typical housing values.

It does not represent:

- Individual property appraisals.
- Actual transaction prices for every home.
- Guaranteed future housing prices.

State-level summaries calculated by ESTATIQ are based on available city observations and are not population-weighted Zillow state indexes.

---

## 5. Project Structure

```text
ESTATIQ-Real-Estate-Intelligence/
|
|-- estatiq_dashboard_v7_us_market_map.py
|-- explore_data.py
|-- machine_learning_v2.py
|-- visualization.py
|-- requirements.txt
|-- README.md
|
|-- charts/
|   |-- housing_value_distribution.png
|   |-- texas_city_comparison.png
|   |-- texas_housing_trends.png
|
|-- data/
    |-- zillow_city.csv
    |-- zillow_cleaned.csv
    |-- model_results.csv
    |-- model_predictions.csv
```

The large CSV files are stored locally and excluded from GitHub using `.gitignore`.

---

## 6. Installation Instructions

### Step 1: Obtain the Project

Clone or download the ESTATIQ GitHub repository.

Open the project folder in Visual Studio Code.

### Step 2: Create a Virtual Environment

Open the VS Code terminal and execute:

```bash
python3 -m venv .venv
```

Activate the environment on macOS:

```bash
source .venv/bin/activate
```

### Step 3: Install Dependencies

Run:

```bash
python -m pip install -r requirements.txt
```

This installs the Python libraries needed for the dashboard, data analysis, and machine learning.

### Step 4: Download the Zillow Dataset

Visit:

https://www.zillow.com/research/data/

Download the city-level monthly ZHVI dataset for the middle housing price tier.

Create a folder named `data` if one does not already exist.

Rename the downloaded CSV file:

`zillow_city.csv`

Place it inside the project's `data` folder.

**Note:** Zillow may update its historical data. A newer download may produce results different from the original project snapshot.

### Step 5: Prepare the Dataset

Run:

```bash
python explore_data.py
```

This processes the Zillow housing dataset and creates:

`data/zillow_cleaned.csv`

### Step 6: Run Machine Learning Evaluation

Execute:

```bash
python machine_learning_v2.py
```

This evaluates the machine learning models and generates:

- `data/model_results.csv`
- `data/model_predictions.csv`

### Step 7: Launch the Dashboard

Run:

```bash
python -m streamlit run estatiq_dashboard_v7_us_market_map.py
```

Streamlit will launch the dashboard in a web browser.

The default local address is typically:

http://localhost:8501

Keep the terminal running while using the application.

---

## 7. Machine Learning Methodology

ESTATIQ implements supervised machine learning to evaluate historical monthly housing value predictions.

### Data Preparation

The Zillow dataset is processed into chronological observations suitable for machine learning.

The model uses preceding monthly home value estimates to predict the following month's estimated value.

### Model Training and Testing

The project uses a chronological training and testing approach.

Earlier observations are used for training, while the final 12 calendar months are reserved for testing.

This approach helps avoid using future observations to train models evaluated on earlier periods.

### Models

**Previous-Month Baseline**

Uses the preceding month's estimated housing value as a simple prediction.

This provides a benchmark for evaluating whether more sophisticated models improve predictive performance.

**Linear Regression**

Uses a linear relationship between historical inputs and the target housing value.

**Random Forest Regression**

Uses an ensemble of decision trees to model more complex patterns in historical housing values.

### Evaluation Metrics

Model performance is evaluated using:

**Mean Absolute Error (MAE)**

Measures the average absolute difference between actual and predicted housing values.

**Root Mean Squared Error (RMSE)**

Measures prediction error while assigning greater weight to larger errors.

**R-squared (R²)**

Measures the proportion of variation explained by the model on the evaluated dataset.

### Machine Learning Limitations

The current evaluation is a historical one-month-ahead backtest.

It is not a validated long-term housing market forecasting service.

Housing values change gradually over time, so very high R² scores should not be interpreted as proof of accurate long-term forecasts.

Model performance should be evaluated against the baseline and through actual prediction errors.

---

## 8. Data Quality and Limitations

ESTATIQ uses a historical Zillow dataset rather than live housing market data.

Several limitations should be considered:

- Some cities contain missing historical observations.
- Zillow can revise previously published estimates.
- Estimates do not represent individual home sale prices.
- Historical performance does not guarantee future market behavior.
- State-level aggregations are calculated from available city observations.
- Individual city coordinates are not included in the original Zillow CSV.
- Machine learning evaluation does not establish reliable long-term forecasts.

These limitations are important when interpreting dashboard results.

---

## 9. Running a Project Demonstration

A recommended demonstration of ESTATIQ includes:

1. Introduce the project and its objectives.
2. Explain the Zillow Home Value Index dataset.
3. Demonstrate the Executive Market Overview.
4. Compare major Texas housing markets.
5. Explore geographic differences using the U.S. Market Map.
6. Identify market growth and decline through Market Rankings.
7. Demonstrate machine learning model comparisons.
8. Explain MAE, RMSE, and R².
9. Show the Data Quality section.
10. Discuss challenges, limitations, and future improvements.

---

## 10. Future Enhancements

Possible future developments include:

- Automated housing data updates.
- Additional geographic data for individual city map markers.
- More advanced forecasting models.
- Additional machine learning evaluation methods.
- Housing affordability analytics.
- Downloadable market research reports.
- More extensive automated testing.
- Expanded regional and national market comparisons.

---

## 11. Troubleshooting

**Problem: Streamlit is not installed**

Solution:

```bash
python -m pip install -r requirements.txt
```

**Problem: Missing Zillow dataset**

Verify that `zillow_city.csv` exists inside the `data` folder.

Run:

```bash
python explore_data.py
```

**Problem: Missing machine learning prediction data**

Run:

```bash
python machine_learning_v2.py
```

**Problem: Streamlit connection error**

Restart the dashboard:

```bash
python -m streamlit run estatiq_dashboard_v7_us_market_map.py
```

Keep the terminal running while using the application.

---

## 12. Academic Purpose and Attribution

ESTATIQ was developed as an educational Python and data science project.

The application demonstrates the integration of:

- Data collection and preparation.
- Data analysis.
- Interactive visualization.
- Machine learning evaluation.
- Web application development.
- Software documentation and version control.

**Data attribution:** Zillow Research — Zillow Home Value Index (ZHVI).

ESTATIQ is an independent academic project and is not affiliated with or endorsed by Zillow.

The platform is intended for education and research, not professional financial or investment advice.
