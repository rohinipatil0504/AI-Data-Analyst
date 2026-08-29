import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Load cleaned data
df = pd.read_csv("data/processed/cleaned_sales_data.csv")

# Create figures folder
Path("reports/figures").mkdir(parents=True, exist_ok=True)

# Convert date
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# 1. Sales by Product
product_sales = df.groupby("Product")["Sales"].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
product_sales.plot(kind="bar")
plt.title("Sales by Product")
plt.xlabel("Product")
plt.ylabel("Sales")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("reports/figures/sales_by_product.png")
plt.close()

# 2. Profit by Category
category_profit = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
category_profit.plot(kind="bar")
plt.title("Profit by Category")
plt.xlabel("Category")
plt.ylabel("Profit")
plt.tight_layout()
plt.savefig("reports/figures/profit_by_category.png")
plt.close()

# 3. Sales by Region
region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
region_sales.plot(kind="bar")
plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("reports/figures/sales_by_region.png")
plt.close()

# 4. Monthly Sales Trend
monthly_sales = (
    df.groupby(df["Order_Date"].dt.to_period("M"))["Sales"]
    .sum()
)

monthly_sales.index = monthly_sales.index.astype(str)

plt.figure(figsize=(12, 6))
monthly_sales.plot(kind="line", marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("reports/figures/monthly_sales_trend.png")
plt.close()

# 5. Correlation Heatmap
numeric_columns = [
    "Quantity",
    "Unit_Price",
    "Discount",
    "Sales",
    "Cost",
    "Profit"
]

plt.figure(figsize=(8, 6))
sns.heatmap(
    df[numeric_columns].corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Sales & Profit Correlation")
plt.tight_layout()
plt.savefig("reports/figures/correlation_heatmap.png")
plt.close()

print("All visualizations created successfully!")
print("Check: reports/figures/")