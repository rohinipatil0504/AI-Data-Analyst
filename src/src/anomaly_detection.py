import sqlite3
import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest


# =====================================================
# DATABASE
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
# MONTHLY ANOMALY DETECTION
# =====================================================

def detect_monthly_anomalies():

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

    model = IsolationForest(
        contamination=0.15,
        random_state=42
    )

    monthly["Anomaly"] = model.fit_predict(
        monthly[["Sales"]]
    )

    monthly["Status"] = monthly["Anomaly"].map({
        1: "Normal",
        -1: "🚨 Anomaly"
    })

    return monthly


# =====================================================
# PRODUCT ANOMALY DETECTION
# =====================================================

def detect_product_anomalies():

    df = load_data()

    product_sales = (
        df.groupby("Product")["Sales"]
        .sum()
        .reset_index()
    )

    model = IsolationForest(
        contamination=0.15,
        random_state=42
    )

    product_sales["Anomaly"] = model.fit_predict(
        product_sales[["Sales"]]
    )

    product_sales["Status"] = product_sales["Anomaly"].map({
        1: "Normal",
        -1: "🚨 Anomaly"
    })

    return product_sales


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    print("=" * 60)
    print("🚨 AI ANOMALY DETECTION")
    print("=" * 60)

    print("\n📅 MONTHLY SALES ANOMALIES\n")

    monthly = detect_monthly_anomalies()

    print(
        monthly[
            [
                "Order_Date",
                "Sales",
                "Status"
            ]
        ].to_string(index=False)
    )

    print("\n" + "=" * 60)

    print("\n📦 PRODUCT ANOMALIES\n")

    products = detect_product_anomalies()

    print(
        products[
            [
                "Product",
                "Sales",
                "Status"
            ]
        ].to_string(index=False)
    )

    print("\n" + "=" * 60)
    print("✅ ANOMALY DETECTION COMPLETED")
    print("=" * 60)
    print("🚨 ANOMALY DETECTION FILE WORKING!")