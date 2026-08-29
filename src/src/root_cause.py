import sqlite3
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "database" / "sales.db"


def load_data():

    conn = sqlite3.connect(DB_FILE)

    df = pd.read_sql_query(
        "SELECT * FROM sales",
        conn
    )

    conn.close()

    return df


def analyze_root_cause(anomaly_date):

    df = load_data()

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"],
        errors="coerce"
    )

    anomaly_date = pd.to_datetime(anomaly_date)

    month_data = df[
        (df["Order_Date"].dt.year == anomaly_date.year)
        &
        (df["Order_Date"].dt.month == anomaly_date.month)
    ]

    if month_data.empty:
        return None

    product = (
        month_data.groupby("Product")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    region = (
        month_data.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    category = (
        month_data.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    return {
        "product": product,
        "region": region,
        "category": category
    }


if __name__ == "__main__":

    print("=" * 60)
    print("🧠 AI ROOT CAUSE ANALYSIS")
    print("=" * 60)

    df = load_data()

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"],
        errors="coerce"
    )

    monthly = (
        df.set_index("Order_Date")
        .resample("ME")["Sales"]
        .sum()
        .reset_index()
    )

    if not monthly.empty:

        latest_date = monthly.iloc[-1]["Order_Date"]

        result = analyze_root_cause(latest_date)

        if result:

            print("\n🏆 TOP PRODUCTS")

            print(
                result["product"]
                .to_string(index=False)
            )

            print("\n🌍 TOP REGIONS")

            print(
                result["region"]
                .to_string(index=False)
            )

            print("\n📦 TOP CATEGORIES")

            print(
                result["category"]
                .to_string(index=False)
            )

    print("\n" + "=" * 60)
    print("✅ ROOT CAUSE ANALYSIS COMPLETED")
    print("=" * 60)