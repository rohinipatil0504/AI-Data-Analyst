import sqlite3
import pandas as pd
from pathlib import Path

from sklearn.linear_model import LinearRegression


# =====================================================
# PATH
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
# FORECAST
# =====================================================

def forecast_sales(months=6):

    df = get_monthly_sales()

    if len(df) < 3:
        return None

    df["Month"] = pd.to_datetime(df["Month"])

    df["Time_Index"] = range(len(df))

    X = df[["Time_Index"]]
    y = df["Sales"]

    model = LinearRegression()

    model.fit(X, y)

    future_index = range(
        len(df),
        len(df) + months
    )

    future_sales = model.predict(
        pd.DataFrame({
            "Time_Index": list(future_index)
        })
    )

    future_dates = pd.date_range(
        start=df["Month"].iloc[-1] + pd.DateOffset(months=1),
        periods=months,
        freq="MS"
    )

    forecast_df = pd.DataFrame({
        "Month": future_dates,
        "Predicted_Sales": future_sales
    })

    return forecast_df


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    result = forecast_sales(6)

    print("\n===== SALES FORECAST =====")
    print(result)