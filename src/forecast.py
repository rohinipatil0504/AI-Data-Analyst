import sqlite3
import pandas as pd
from pathlib import Path
from sklearn.linear_model import LinearRegression


# =====================================================
# PROJECT PATH
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "database" / "sales.db"


# =====================================================
# LOAD MONTHLY SALES
# =====================================================

def get_monthly_sales():

    conn = sqlite3.connect(DB_FILE)

    query = """
    SELECT
        strftime('%Y-%m', Order_Date) AS Month,
        SUM(Sales) AS Sales
    FROM sales
    GROUP BY Month
    ORDER BY Month
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


# =====================================================
# SALES FORECAST
# =====================================================

def forecast_sales(months=6):

    df = get_monthly_sales()

    if df.empty:
        return None

    df["Month"] = pd.to_datetime(df["Month"])

    # Time index
    df["Time_Index"] = range(len(df))

    X = df[["Time_Index"]]
    y = df["Sales"]

    # Machine Learning Model
    model = LinearRegression()

    model.fit(X, y)

    # Future months
    future_index = list(
        range(
            len(df),
            len(df) + months
        )
    )

    future_sales = model.predict(
        pd.DataFrame({
            "Time_Index": future_index
        })
    )

    future_dates = pd.date_range(
        start=df["Month"].iloc[-1]
        + pd.DateOffset(months=1),
        periods=months,
        freq="MS"
    )

    forecast_df = pd.DataFrame({
        "Month": future_dates,
        "Predicted_Sales": future_sales
    })

    # Negative prediction ko zero karna
    forecast_df["Predicted_Sales"] = (
        forecast_df["Predicted_Sales"].clip(lower=0)
    )

    return forecast_df


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    print("\n" + "=" * 50)
    print("        AI SALES FORECAST")
    print("=" * 50)

    result = forecast_sales(6)

    if result is not None:

        print("\n🔮 NEXT 6 MONTHS FORECAST\n")

        print(
            result.to_string(index=False)
        )

        print("\n" + "=" * 50)
        print("✅ FORECASTING COMPLETED")
        print("=" * 50)

    else:

        print("❌ No sales data found.")