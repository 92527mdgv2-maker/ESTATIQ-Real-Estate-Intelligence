import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load cleaned Zillow dataset
project_folder = Path(__file__).parent
file_path = project_folder / "data" / "zillow_cleaned.csv"

df = pd.read_csv(file_path)

# Cities we want to compare
cities = [
    "Dallas",
    "Houston",
    "Austin",
    "San Antonio",
    "Fort Worth"
]

# Select historical dates beginning in 2018
date_columns = [
    col for col in df.columns
    if col.startswith("20")
    and len(col) == 10
    and col >= "2018-01-01"
]

# Create the line graph
plt.figure(figsize=(12, 6))

for city in cities:
    city_data = df[
        (df["RegionName"] == city) &
        (df["State"] == "TX")
    ]

    if not city_data.empty:
        values = city_data.iloc[0][date_columns]
        values = pd.to_numeric(values, errors="coerce")

        plt.plot(
            pd.to_datetime(date_columns),
            values,
            label=city
        )

# Customize the graph
plt.title("Texas Housing Market Trends (2018-2026)")
plt.xlabel("Year")
plt.ylabel("Typical Home Value ($)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save the graph
charts_folder = project_folder / "charts"
charts_folder.mkdir(exist_ok=True)

plt.savefig(
    charts_folder / "texas_housing_trends.png",
    dpi=300
)

print("Housing market graph created successfully!")

plt.show()
# Step 6: Compare current housing values
print("\nCreating city comparison bar chart...")

latest_date = date_columns[-1]

city_names = []
home_values = []

for city in cities:
    city_data = df[
        (df["RegionName"] == city) &
        (df["State"] == "TX")
    ]

    if not city_data.empty:
        value = pd.to_numeric(
            city_data.iloc[0][latest_date],
            errors="coerce"
        )

        if pd.notna(value):
            city_names.append(city)
            home_values.append(value)

# Create the bar chart
plt.figure(figsize=(10, 6))

bars = plt.bar(city_names, home_values)

plt.title("Texas Home Values by City")
plt.xlabel("City")
plt.ylabel("Typical Home Value ($)")
plt.grid(axis="y", alpha=0.3)

# Add dollar amounts above each bar
for bar, value in zip(bars, home_values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"${value:,.0f}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

# Save the bar chart
plt.savefig(
    charts_folder / "texas_city_comparison.png",
    dpi=300
)

print("City comparison chart created successfully!")

plt.show()
# Step 7: Create housing value distribution histogram
print("\nCreating housing value distribution histogram...")

# Get valid home values from all cities
all_home_values = pd.to_numeric(
    df[latest_date],
    errors="coerce"
).dropna()

# Create histogram
plt.figure(figsize=(12, 6))

plt.hist(
    all_home_values,
    bins=50,
    edgecolor="black",
    alpha=0.8
)

plt.title("Distribution of U.S. City Home Values")
plt.xlabel("Typical Home Value ($)")
plt.ylabel("Number of Cities")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

# Save histogram
plt.savefig(
    charts_folder / "housing_value_distribution.png",
    dpi=300
)

print("Housing value histogram created successfully!")

plt.show()