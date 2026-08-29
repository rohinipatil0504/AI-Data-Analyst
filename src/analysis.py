import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/processed/cleaned_sales_data.csv")

# Basic information
print("\n===== DATASET INFO =====")
print(df.info())

print("\n===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== BASIC STATISTICS =====")
print(df.describe())

# Total Sales
total_sales = df["Sales"].sum()

# Total Cost
total_cost = df["Cost"].sum()

# Total Profit
total_profit = df["Profit"].sum()

# Total Quantity
total_quantity = df["Quantity"].sum()

print("\n===== BUSINESS SUMMARY =====")
print("Total Sales:", round(total_sales, 2))
print("Total Cost:", round(total_cost, 2))
print("Total Profit:", round(total_profit, 2))
print("Total Quantity Sold:", total_quantity)

# Best products
print("\n===== TOP PRODUCTS BY SALES =====")
product_sales = (
    df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(product_sales)

# Sales by region
print("\n===== SALES BY REGION =====")
region_sales = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(region_sales)

# Profit by category
print("\n===== PROFIT BY CATEGORY =====")
category_profit = (
    df.groupby("Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print(category_profit)

# Customer analysis
print("\n===== SALES BY CUSTOMER TYPE =====")
customer_sales = (
    df.groupby("Customer_Type")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(customer_sales)