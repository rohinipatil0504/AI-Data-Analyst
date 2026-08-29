import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "database" / "sales.db"

conn = sqlite3.connect(DB_FILE)

print("\n" + "=" * 50)
print("       SQL BUSINESS ANALYTICS")
print("=" * 50)


# 1. Total Sales
query = """
SELECT SUM(Sales) AS Total_Sales
FROM sales;
"""

print("\n💰 TOTAL SALES")
print(pd.read_sql_query(query, conn))


# 2. Total Profit
query = """
SELECT SUM(Profit) AS Total_Profit
FROM sales;
"""

print("\n📈 TOTAL PROFIT")
print(pd.read_sql_query(query, conn))


# 3. Total Orders
query = """
SELECT COUNT(DISTINCT Order_ID) AS Total_Orders
FROM sales;
"""

print("\n🛒 TOTAL ORDERS")
print(pd.read_sql_query(query, conn))


# 4. Top 10 Products by Sales
query = """
SELECT
    Product,
    SUM(Sales) AS Total_Sales
FROM sales
GROUP BY Product
ORDER BY Total_Sales DESC
LIMIT 10;
"""

print("\n🏆 TOP 10 PRODUCTS BY SALES")
print(pd.read_sql_query(query, conn))


# 5. Profit by Region
query = """
SELECT
    Region,
    SUM(Profit) AS Total_Profit
FROM sales
GROUP BY Region
ORDER BY Total_Profit DESC;
"""

print("\n🌍 PROFIT BY REGION")
print(pd.read_sql_query(query, conn))


# 6. Sales by Category
query = """
SELECT
    Category,
    SUM(Sales) AS Total_Sales
FROM sales
GROUP BY Category
ORDER BY Total_Sales DESC;
"""

print("\n📦 SALES BY CATEGORY")
print(pd.read_sql_query(query, conn))


# 7. Sales by Customer Type
query = """
SELECT
    Customer_Type,
    SUM(Sales) AS Total_Sales
FROM sales
GROUP BY Customer_Type
ORDER BY Total_Sales DESC;
"""

print("\n👥 SALES BY CUSTOMER TYPE")
print(pd.read_sql_query(query, conn))


# 8. Payment Mode Analysis
query = """
SELECT
    Payment_Mode,
    COUNT(*) AS Number_of_Orders
FROM sales
GROUP BY Payment_Mode
ORDER BY Number_of_Orders DESC;
"""

print("\n💳 PAYMENT MODE ANALYSIS")
print(pd.read_sql_query(query, conn))


# 9. Top Cities
query = """
SELECT
    City,
    SUM(Sales) AS Total_Sales
FROM sales
GROUP BY City
ORDER BY Total_Sales DESC
LIMIT 10;
"""

print("\n🏙️ TOP 10 CITIES")
print(pd.read_sql_query(query, conn))


# 10. Monthly Sales
query = """
SELECT
    strftime('%Y-%m', Order_Date) AS Month,
    SUM(Sales) AS Total_Sales
FROM sales
GROUP BY Month
ORDER BY Month;
"""

print("\n📅 MONTHLY SALES")
print(pd.read_sql_query(query, conn))


conn.close()

print("\n" + "=" * 50)
print("✅ SQL ANALYSIS COMPLETED")
print("=" * 50)
