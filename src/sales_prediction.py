import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import LinearRegression

# =====================================================
# PROJECT PATH
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "cleaned_sales_data.csv"
)


# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(DATA_FILE)

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)


# =====================================================
# MONTHLY SALES
# =====================================================

monthly_sales = (
    df.groupby(
        df["Order_Date"].dt.to_period("M")
    )["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Month_Number"] = np.arange(
    1,
    len(monthly_sales) + 1
)


# =====================================================
# MACHINE LEARNING MODEL
# =====================================================

X = monthly_sales[
    ["Month_Number"]
]

y = monthly_sales[
    "Sales"
]


model = LinearRegression()

model.fit(X, y)


# =====================================================
# NEXT MONTH PREDICTION
# =====================================================

next_month_number = (
    monthly_sales["Month_Number"].max() + 1
)

prediction = model.predict(
    [[next_month_number]]
)[0]


# =====================================================
# MODEL SCORE
# =====================================================

r2_score = model.score(
    X,
    y
)


# =====================================================
# RESULT
# =====================================================

print("=" * 55)

print("        🔮 AI SALES PREDICTION")

print("=" * 55)

print()

print(
    f"📊 Historical Months: "
    f"{len(monthly_sales)}"
)

print(
    f"💰 Predicted Next Month Sales: "
    f"₹{prediction:,.2f}"
)

print(
    f"🎯 Model R² Score: "
    f"{r2_score:.2f}"
)

print()

if prediction > monthly_sales["Sales"].iloc[-1]:

    print(
        "📈 Expected Trend: INCREASING"
    )

else:

    print(
        "📉 Expected Trend: DECREASING"
    )

print()

print("=" * 55)