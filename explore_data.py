import pandas as pd
from pathlib import Path

# Step 1: Load the Zillow housing dataset
file_path = Path(__file__).parent / "data" / "zillow_city.csv"
df = pd.read_csv(file_path)

# Step 2: Display dataset information
print("=== ZILLOW REAL ESTATE DATA ANALYSIS ===")

print("\nDataset Size:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.iloc[:5, :10])

print("\nColumn Names:")
print(df.columns[:10].tolist())

print("\nMissing Values:")
print(df.isnull().sum().sum())

print("\nDataset loaded successfully!")
# Step 3: Identify the latest housing data
date_columns = [
    col for col in df.columns
    if col.startswith("20") and len(col) == 10
]

latest_date = date_columns[-1]

print("\n=== HOUSING MARKET ANALYSIS ===")
print("Latest available month:", latest_date)

# Step 4: Find Dallas, Texas
dallas = df[
    (df["RegionName"] == "Dallas") &
    (df["State"] == "TX")
]

if not dallas.empty:
    latest_value = dallas.iloc[0][latest_date]
    print(f"Dallas typical home value: ${latest_value:,.2f}")
else:
    print("Dallas was not found.")

# Step 5: Check missing values in latest month
missing = df[latest_date].isnull().sum()

print("\nCities missing latest housing data:", missing)
print("Total city records:", len(df))
# Step 6: Clean the Zillow housing dataset
print("\n=== DATA CLEANING ===")

# Create a copy to preserve the original data
clean_df = df.copy()

# Record original number of rows
original_rows = len(clean_df)

# Remove duplicate cities using unique Zillow IDs
clean_df = clean_df.drop_duplicates(subset=["RegionID"])

# Convert latest housing values into numeric data
clean_df[latest_date] = pd.to_numeric(
    clean_df[latest_date],
    errors="coerce"
)

# Remove records missing essential information
clean_df = clean_df.dropna(
    subset=["RegionName", "State", latest_date]
)

# Remove invalid housing values
clean_df = clean_df[
    clean_df[latest_date] > 0
].copy()

# Create useful columns for our future dashboard
clean_df["CityState"] = (
    clean_df["RegionName"] + ", " + clean_df["State"]
)

clean_df["LatestHomeValue"] = clean_df[latest_date]

# Save the cleaned dataset
output_path = (
    Path(__file__).parent / "data" / "zillow_cleaned.csv"
)

clean_df.to_csv(output_path, index=False)

print("Original rows:", original_rows)
print("Cleaned rows:", len(clean_df))
print("Rows removed:", original_rows - len(clean_df))
print("Cleaned dataset saved successfully!")