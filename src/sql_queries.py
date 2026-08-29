import sqlite3
import pandas as pd
from pathlib import Path


# =====================================================
# DATABASE PATH
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DB_FILE = BASE_DIR / "database" / "sales.db"


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_connection():
    return sqlite3.connect(DB_FILE)


# =====================================================
# TOTAL SALES
# =====================================================

def get_total_sales():

    conn = get_connection()

    query = """
    SELECT SUM(Sales) AS Total_Sales
    FROM sales
    """

    result = pd.read_sql_query(query, conn)

    conn.close()

    return result.iloc[0]["Total_Sales"]


# =====================================================
# TOTAL PROFIT
# =====================================================

def get_total_profit():

    conn = get_connection()

    query = """
    SELECT SUM(Profit) AS Total_Profit
    FROM sales
    """

    result = pd.read_sql_query(query, conn)

    conn.close()

    return result.iloc[0]["Total_Profit"]


# =====================================================
# TOTAL ORDERS
# =====================================================

def get_total_orders():

    conn = get_connection()

    query = """
    SELECT COUNT(DISTINCT Order_ID) AS Total_Orders
    FROM sales
    """

    result = pd.read_sql_query(query, conn)

    conn.close()

    return int(result.iloc[0]["Total_Orders"])


# =====================================================
# TOTAL QUANTITY
# =====================================================

def get_total_quantity():

    conn = get_connection()

    query = """
    SELECT SUM(Quantity) AS Total_Quantity
    FROM sales
    """

    result = pd.read_sql_query(query, conn)

    conn.close()

    return int(result.iloc[0]["Total_Quantity"])


# =====================================================
# AVERAGE ORDER VALUE
# =====================================================

def get_average_order_value():

    conn = get_connection()

    query = """
    SELECT AVG(Sales) AS Average_Order_Value
    FROM sales
    """

    result = pd.read_sql_query(query, conn)

    conn.close()

    return result.iloc[0]["Average_Order_Value"]


# =====================================================
# TOP PRODUCTS BY SALES
# =====================================================

def get_top_products(limit=10):

    conn = get_connection()

    query = f"""
    SELECT
        Product,
        SUM(Sales) AS Total_Sales
    FROM sales
    GROUP BY Product
    ORDER BY Total_Sales DESC
    LIMIT {limit}
    """

    result = pd.read_sql_query(query, conn)

    conn.close()

    return result


# =====================================================
# PROFIT BY REGION
# =====================================================

def get_profit_by_region():

    conn = get_connection()

    query = """
    SELECT
        Region,
        SUM(Profit) AS Total_Profit
    FROM sales
    GROUP BY Region
    ORDER BY Total_Profit DESC
    """

    result = pd.read_sql_query(query, conn)

    conn.close()

    return result


# =====================================================
# SALES BY REGION
# =====================================================

def get_sales_by_region():

    conn = get_connection()

    query = """
    SELECT
        Region,
        SUM(Sales) AS Total_Sales
    FROM sales
    GROUP BY Region
    ORDER BY Total_Sales DESC
    """

    result = pd.read_sql_query(query, conn)

    conn.close()

    return result


# =====================================================
# SALES BY CATEGORY
# =====================================================

def get_sales_by_category():

    conn = get_connection()

    query = """
    SELECT
        Category,
        SUM(Sales) AS Total_Sales
    FROM sales
    GROUP BY Category
    ORDER BY Total_Sales DESC
    """

    result = pd.read_sql_query(query, conn)

    conn.close()

    return result


# =====================================================
# PROFIT BY CATEGORY
# =====================================================

def get_profit_by_category():

    conn = get_connection()

    query = """
    SELECT
        Category,
        SUM(Profit) AS Total_Profit
    FROM sales
    GROUP BY Category
    ORDER BY Total_Profit DESC
    """

    result = pd.read_sql_query(query, conn)

    conn.close()

    return result


# =====================================================
# SALES BY CUSTOMER TYPE
# =====================================================

def get_sales_by_customer():

    conn = get_connection()

    query = """
    SELECT
        Customer_Type,
        SUM(Sales) AS Total_Sales
    FROM sales
    GROUP BY Customer_Type
    ORDER BY Total_Sales DESC
    """

    result = pd.read_sql_query(query, conn)

    conn.close()

    return result


# =====================================================
# PAYMENT MODE
# =====================================================

def get_payment_analysis():

    conn = get_connection()

    query = """
    SELECT
        Payment_Mode,
        COUNT(*) AS Number_of_Orders
    FROM sales
    GROUP BY Payment_Mode
    ORDER BY Number_of_Orders DESC
    """

    result = pd.read_sql_query(query, conn)

    conn.close()

    return result


# =====================================================
# TOP CITIES
# =====================================================

def get_top_cities(limit=10):

    conn = get_connection()

    query = f"""
    SELECT
        City,
        SUM(Sales) AS Total_Sales
    FROM sales
    GROUP BY City
    ORDER BY Total_Sales DESC
    LIMIT {limit}
    """

    result = pd.read_sql_query(query, conn)

    conn.close()

    return result


# =====================================================
# MONTHLY SALES
# =====================================================

def get_monthly_sales():

    conn = get_connection()

    query = """
    SELECT
        strftime('%Y-%m', Order_Date) AS Month,
        SUM(Sales) AS Total_Sales
    FROM sales
    GROUP BY Month
    ORDER BY Month
    """

    result = pd.read_sql_query(query, conn)

    conn.close()

    return result


# =====================================================
# MONTHLY PROFIT
# =====================================================

def get_monthly_profit():

    conn = get_connection()

    query = """
    SELECT
        strftime('%Y-%m', Order_Date) AS Month,
        SUM(Profit) AS Total_Profit
    FROM sales
    GROUP BY Month
    ORDER BY Month
    """

    result = pd.read_sql_query(query, conn)

    conn.close()

    return result


# =====================================================
# MOST SOLD PRODUCTS
# =====================================================

def get_most_sold_products(limit=10):

    conn = get_connection()

    query = f"""
    SELECT
        Product,
        SUM(Quantity) AS Total_Quantity
    FROM sales
    GROUP BY Product
    ORDER BY Total_Quantity DESC
    LIMIT {limit}
    """

    result = pd.read_sql_query(query, conn)

    conn.close()

    return result


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    print("=" * 50)
    print("       SQL QUERY TEST")
    print("=" * 50)

    print("\n💰 Total Sales:")
    print(get_total_sales())

    print("\n📈 Total Profit:")
    print(get_total_profit())

    print("\n🛒 Total Orders:")
    print(get_total_orders())

    print("\n📦 Total Quantity:")
    print(get_total_quantity())

    print("\n🧾 Average Order Value:")
    print(get_average_order_value())

    print("\n🏆 Top Products:")
    print(get_top_products())

    print("\n🌍 Profit by Region:")
    print(get_profit_by_region())

    print("\n📊 Sales by Category:")
    print(get_sales_by_category())

    print("\n👥 Sales by Customer:")
    print(get_sales_by_customer())

    print("\n💳 Payment Analysis:")
    print(get_payment_analysis())

    print("\n🏙️ Top Cities:")
    print(get_top_cities())

    print("\n📅 Monthly Sales:")
    print(get_monthly_sales())

    print("\n📈 Monthly Profit:")
    print(get_monthly_profit())

    print("\n📦 Most Sold Products:")
    print(get_most_sold_products())

    print("\n" + "=" * 50)
    print("✅ SQL QUERIES COMPLETED")
    print("=" * 50)