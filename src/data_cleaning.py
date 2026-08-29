import pandas as pd
from pathlib import Path

# File paths
input_file = "data/raw/sales_data.csv"
output_file = "data/processed/cleaned_sales_data.csv"

# Load data
df = pd.read_csv(input_file)

print("Original shape:", df.shape)

# Remove duplicate rows
df = df.drop_duplicates()

# Convert date
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

# Fill missing City
df["City"] = df["City"].fillna("Unknown")

# Fill missing Discount with 0
df["Discount"] = df["Discount"].fillna(0)

# Make sure numeric columns are numeric
numeric_columns = [
    "Quantity",
    "Unit_Price",
    "Discount",
    "Sales",
    "Cost",
    "Profit"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Remove rows with missing important values
df = df.dropna(
    subset=[
        "Order_ID",
        "Order_Date",
        "Product",
        "Sales",
        "Cost",
        "Profit"
    ]
)

# Recalculate Sales and Profit
df["Sales"] = (
    df["Quantity"]
    * df["Unit_Price"]
    * (1 - df["Discount"] / 100)
).round(2)

df["Profit"] = (df["Sales"] - df["Cost"]).round(2)

# Create processed folder
Path("data/processed").mkdir(parents=True, exist_ok=True)

# Save cleaned data
df.to_csv(output_file, index=False)

print("Cleaning completed!")
print("Cleaned shape:", df.shape)
print("Saved to:", output_file)