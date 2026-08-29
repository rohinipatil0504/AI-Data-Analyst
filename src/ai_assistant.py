import requests
import sqlite3
import pandas as pd
from pathlib import Path


# =====================================================
# PROJECT PATH
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DB_FILE = BASE_DIR / "database" / "sales.db"


# =====================================================
# LOAD DATA
# =====================================================

def load_data():

    conn = sqlite3.connect(DB_FILE)

    df = pd.read_sql_query(
        "SELECT * FROM sales",
        conn
    )

    conn.close()

    return df


# =====================================================
# ASK LLAMA
# =====================================================

def ask_llama(question):

    df = load_data()

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order_ID"].nunique()

    top_product = (
        df.groupby("Product")["Sales"]
        .sum()
        .idxmax()
    )

    top_region = (
        df.groupby("Region")["Profit"]
        .sum()
        .idxmax()
    )

    prompt = f"""
You are an expert AI Data Analyst.

Analyze this business data and answer the user's question.

BUSINESS DATA:

Total Sales: ₹{total_sales:,.2f}
Total Profit: ₹{total_profit:,.2f}
Total Orders: {total_orders:,}

Highest Sales Product:
{top_product}

Highest Profit Region:
{top_region}

User Question:
{question}

Instructions:
- Give a clear answer.
- Use the provided data.
- Explain the insight.
- Give a short business recommendation when useful.
- Do not invent numbers.
"""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",

            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },

            timeout=120
        )

        response.raise_for_status()

        return response.json()["response"]

    except Exception as e:

        return f"❌ Llama Error: {e}"


# =====================================================
# BUSINESS RECOMMENDATIONS
# =====================================================

def generate_recommendations():

    df = load_data()

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order_ID"].nunique()

    # Top product
    product_sales = (
        df.groupby("Product")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    top_product = product_sales.index[0]
    top_product_sales = product_sales.iloc[0]

    # Top profit product
    product_profit = (
        df.groupby("Product")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    best_profit_product = product_profit.index[0]
    best_product_profit = product_profit.iloc[0]

    # Best region
    region_profit = (
        df.groupby("Region")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    best_region = region_profit.index[0]
    best_region_profit = region_profit.iloc[0]

    # Best category
    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    best_category = category_sales.index[0]

    prompt = f"""
You are a professional Business Analyst.

Analyze the following company performance:

Total Sales:
₹{total_sales:,.2f}

Total Profit:
₹{total_profit:,.2f}

Total Orders:
{total_orders:,}

Highest Sales Product:
{top_product}
Sales:
₹{top_product_sales:,.2f}

Most Profitable Product:
{best_profit_product}
Profit:
₹{best_product_profit:,.2f}

Highest Profit Region:
{best_region}
Profit:
₹{best_region_profit:,.2f}

Best Sales Category:
{best_category}

Generate 5 practical business recommendations.

For every recommendation:
1. Give the business insight.
2. Explain why it matters.
3. Give an actionable suggestion.

Use ONLY the provided information.
Do not invent statistics.

Keep the answer professional and easy to understand.
"""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",

            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },

            timeout=120
        )

        response.raise_for_status()

        return response.json()["response"]

    except Exception as e:

        return f"❌ Recommendation Error: {e}"


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    print("=" * 50)

    print("AI DATA ANALYST TEST")

    print("=" * 50)

    print(
        ask_llama(
            "Which product has the highest sales?"
        )
    )

    print("\n")

    print("BUSINESS RECOMMENDATIONS")

    print("=" * 50)

    print(
        generate_recommendations()
    )