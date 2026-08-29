import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

# Number of records
n = 2000

# Products and prices
products = {
    "Laptop": 55000,
    "Smartphone": 25000,
    "Tablet": 22000,
    "Monitor": 15000,
    "Printer": 12000,
    "Keyboard": 1500,
    "Mouse": 800,
    "Headphones": 3000,
    "Smartwatch": 6000,
    "Power Bank": 1800,
    "Office Chair": 9000,
    "Office Desk": 12000,
    "Bookshelf": 7000,
    "Backpack": 1800,
    "Webcam": 3500,
    "USB Drive": 900,
    "Router": 2500,
    "External Hard Drive": 6500,
    "Bluetooth Speaker": 3000,
    "Gaming Mouse": 2200
}

categories = {
    "Laptop": "Electronics",
    "Smartphone": "Electronics",
    "Tablet": "Electronics",
    "Monitor": "Electronics",
    "Printer": "Electronics",
    "Keyboard": "Accessories",
    "Mouse": "Accessories",
    "Headphones": "Accessories",
    "Smartwatch": "Accessories",
    "Power Bank": "Accessories",
    "Office Chair": "Furniture",
    "Office Desk": "Furniture",
    "Bookshelf": "Furniture",
    "Backpack": "Accessories",
    "Webcam": "Electronics",
    "USB Drive": "Accessories",
    "Router": "Electronics",
    "External Hard Drive": "Electronics",
    "Bluetooth Speaker": "Accessories",
    "Gaming Mouse": "Accessories"
}

regions = ["North", "South", "East", "West", "Central"]

cities = {
    "North": ["Delhi", "Jaipur", "Lucknow", "Chandigarh"],
    "South": ["Bengaluru", "Hyderabad", "Chennai"],
    "East": ["Kolkata", "Bhubaneswar", "Patna"],
    "West": ["Mumbai", "Pune", "Ahmedabad", "Surat"],
    "Central": ["Indore", "Bhopal", "Nagpur"]
}

customer_types = ["New", "Regular", "Premium"]

payment_modes = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash",
    "Net Banking"
]

# Generate basic data
product_list = np.random.choice(list(products.keys()), n)

region_list = np.random.choice(
    regions,
    n,
    p=[0.20, 0.20, 0.15, 0.25, 0.20]
)

city_list = [
    np.random.choice(cities[region])
    for region in region_list
]

quantity = np.random.randint(1, 11, n)

discount = np.random.choice(
    [0, 5, 10, 15, 20, 25],
    n,
    p=[0.15, 0.20, 0.30, 0.20, 0.10, 0.05]
)

customer_type = np.random.choice(
    customer_types,
    n,
    p=[0.30, 0.55, 0.15]
)

payment_mode = np.random.choice(
    payment_modes,
    n
)

# Random dates between 2024 and 2025
dates = pd.date_range(
    start="2024-01-01",
    end="2025-12-31",
    periods=n
)

# Unit price with small variation
unit_price = [
    round(products[p] * np.random.uniform(0.90, 1.10), 2)
    for p in product_list
]

# Sales calculation
sales = [
    round(q * price * (1 - d / 100), 2)
    for q, price, d in zip(quantity, unit_price, discount)
]

# Cost and profit
cost = [
    round(s * np.random.uniform(0.60, 0.85), 2)
    for s in sales
]

profit = [
    round(s - c, 2)
    for s, c in zip(sales, cost)
]

# Create DataFrame
df = pd.DataFrame({
    "Order_ID": [f"ORD{1001 + i}" for i in range(n)],
    "Order_Date": dates,
    "Product": product_list,
    "Category": [categories[p] for p in product_list],
    "Region": region_list,
    "City": city_list,
    "Quantity": quantity,
    "Unit_Price": unit_price,
    "Discount": discount,
    "Sales": sales,
    "Cost": cost,
    "Profit": profit,
    "Customer_Type": customer_type,
    "Payment_Mode": payment_mode
})

# Add some missing values for data-cleaning practice
df.loc[np.random.choice(df.index, 20, replace=False), "City"] = np.nan
df.loc[np.random.choice(df.index, 10, replace=False), "Discount"] = np.nan

# Add duplicate records
duplicates = df.sample(15, random_state=42)
df = pd.concat([df, duplicates], ignore_index=True)

# Create folder if it doesn't exist
output_folder = Path("data/raw")
output_folder.mkdir(parents=True, exist_ok=True)

# Save CSV
output_file = output_folder / "sales_data.csv"
df.to_csv(output_file, index=False)

print("Dataset created successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"File saved at: {output_file}")