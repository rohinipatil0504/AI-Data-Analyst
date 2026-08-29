import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "database" / "sales.db"


def load_data():

    conn = sqlite3.connect(DB_FILE)

    df = pd.read_sql_query(
        "SELECT * FROM sales",
        conn
    )

    conn.close()

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"],
        errors="coerce"
    )

    return df


def calculate_risk():

    df = load_data()

    # ---------------------------------------------
    # Product level statistics
    # ---------------------------------------------

    product = (
        df.groupby("Product")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique")
        )
        .reset_index()
    )

    # ---------------------------------------------
    # Profit Margin
    # ---------------------------------------------

    product["Profit_Margin"] = (
        product["Profit"] /
        product["Sales"].replace(0, np.nan)
    ) * 100

    product["Profit_Margin"] = (
        product["Profit_Margin"]
        .fillna(0)
    )

    # ---------------------------------------------
    # Monthly sales volatility
    # ---------------------------------------------

    monthly = (
        df.groupby(
            [
                "Product",
                df["Order_Date"].dt.to_period("M")
            ]
        )["Sales"]
        .sum()
        .reset_index()
    )

    volatility = (
        monthly
        .groupby("Product")["Sales"]
        .std()
        .fillna(0)
        .reset_index()
    )

    volatility.columns = [
        "Product",
        "Sales_Volatility"
    ]

    product = product.merge(
        volatility,
        on="Product",
        how="left"
    )

    # ---------------------------------------------
    # Normalize metrics
    # ---------------------------------------------

    scaler = MinMaxScaler()

    metrics = scaler.fit_transform(
        product[
            [
                "Sales",
                "Profit",
                "Orders",
                "Sales_Volatility"
            ]
        ]
    )

    normalized = pd.DataFrame(
        metrics,
        columns=[
            "Sales_N",
            "Profit_N",
            "Orders_N",
            "Volatility_N"
        ]
    )

    product = pd.concat(
        [
            product.reset_index(drop=True),
            normalized
        ],
        axis=1
    )

    # ---------------------------------------------
    # Risk calculation
    # ---------------------------------------------

    product["Risk_Score"] = (
        (1 - product["Sales_N"]) * 30
        +
        (1 - product["Profit_N"]) * 30
        +
        (1 - product["Orders_N"]) * 20
        +
        product["Volatility_N"] * 20
    )

    product["Risk_Score"] = (
        product["Risk_Score"]
        .clip(0, 100)
        .round(2)
    )

    # ---------------------------------------------
    # Risk Level
    # ---------------------------------------------

    def risk_level(score):

        if score >= 70:
            return "High Risk"

        elif score >= 40:
            return "Medium Risk"

        else:
            return "Low Risk"

    product["Risk_Level"] = (
        product["Risk_Score"]
        .apply(risk_level)
    )

    # ---------------------------------------------
    # Recommendation
    # ---------------------------------------------

    def recommendation(row):

        if row["Risk_Level"] == "High Risk":
            return "Needs immediate attention"

        elif row["Risk_Level"] == "Medium Risk":
            return "Monitor performance"

        return "Performing well"

    product["Recommendation"] = product.apply(
        recommendation,
        axis=1
    )

    return product.sort_values(
        "Risk_Score",
        ascending=False
    )


if __name__ == "__main__":

    print("=" * 70)
    print("🎯 AI SALES RISK ANALYSIS")
    print("=" * 70)

    result = calculate_risk()

    print(
        result[
            [
                "Product",
                "Sales",
                "Profit",
                "Orders",
                "Profit_Margin",
                "Sales_Volatility",
                "Risk_Score",
                "Risk_Level",
                "Recommendation"
            ]
        ].to_string(index=False)
    )

    print("=" * 70)
    print("✅ AI SALES RISK ANALYSIS COMPLETED")
    print("=" * 70)