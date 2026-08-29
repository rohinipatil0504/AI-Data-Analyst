import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pathlib import Path
import sys
from sklearn.linear_model import LinearRegression

# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

DATA_FILE = BASE_DIR / "data" / "processed" / "cleaned_sales_data.csv"

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="🤖",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("🤖 AI Data Analyst")
st.subheader("📊 AI-Powered Sales Intelligence Dashboard")

st.write(
    "Python • Pandas • SQL • Machine Learning • Plotly • Streamlit • AI"
)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(DATA_FILE)

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"],
        errors="coerce"
    )

    return df


df = load_data()

# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔎 Dashboard Filters")

# Region
regions = ["All"] + sorted(
    df["Region"].dropna().unique().tolist()
)

selected_region = st.sidebar.selectbox(
    "🌍 Region",
    regions
)

# Category
categories = ["All"] + sorted(
    df["Category"].dropna().unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "📦 Category",
    categories
)

# Customer Type
customers = ["All"] + sorted(
    df["Customer_Type"].dropna().unique().tolist()
)

selected_customer = st.sidebar.selectbox(
    "👥 Customer Type",
    customers
)

# Payment Mode
payments = ["All"] + sorted(
    df["Payment_Mode"].dropna().unique().tolist()
)

selected_payment = st.sidebar.selectbox(
    "💳 Payment Mode",
    payments
)

# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()

if selected_region != "All":

    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if selected_category != "All":

    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

if selected_customer != "All":

    filtered_df = filtered_df[
        filtered_df["Customer_Type"] == selected_customer
    ]

if selected_payment != "All":

    filtered_df = filtered_df[
        filtered_df["Payment_Mode"] == selected_payment
    ]


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_orders = filtered_df["Order_ID"].nunique()

total_quantity = filtered_df["Quantity"].sum()

average_order = (
    filtered_df["Sales"].mean()
    if len(filtered_df) > 0
    else 0
)

# =========================================================
# BUSINESS OVERVIEW
# =========================================================

st.markdown("## 📌 Business Overview")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "💰 Total Sales",
    f"₹{total_sales:,.0f}"
)

c2.metric(
    "📈 Total Profit",
    f"₹{total_profit:,.0f}"
)

c3.metric(
    "🛒 Orders",
    f"{total_orders:,}"
)

c4.metric(
    "📦 Quantity",
    f"{total_quantity:,}"
)

c5.metric(
    "🧾 Avg Order",
    f"₹{average_order:,.0f}"
)

st.divider()

# =========================================================
# FILTER STATUS
# =========================================================

st.info(
    f"Showing {len(filtered_df):,} orders "
    f"out of {len(df):,} total orders."
)

# =========================================================
# ML SALES FORECAST
# =========================================================

st.header("🔮 AI Sales Forecast")

if len(filtered_df) >= 2:

    monthly = (
        filtered_df
        .groupby(
            filtered_df["Order_Date"].dt.to_period("M")
        )["Sales"]
        .sum()
        .reset_index()
    )

    monthly["Month"] = monthly["Order_Date"].astype(str)

    monthly["Month_Number"] = np.arange(
        1,
        len(monthly) + 1
    )

    X = monthly[["Month_Number"]]

    y = monthly["Sales"]

    model = LinearRegression()

    model.fit(X, y)

    next_month_number = (
        monthly["Month_Number"].max() + 1
    )

    predicted_sales = model.predict(
        [[next_month_number]]
    )[0]

    r2_score = model.score(X, y)

    last_sales = y.iloc[-1]

    if predicted_sales >= last_sales:
        trend = "📈 Increasing"
    else:
        trend = "📉 Decreasing"

    f1, f2, f3 = st.columns(3)

    f1.metric(
        "🔮 Predicted Next Month Sales",
        f"₹{predicted_sales:,.0f}"
    )

    f2.metric(
        "📊 Expected Trend",
        trend
    )

    f3.metric(
        "🎯 Model R² Score",
        f"{r2_score:.2f}"
    )

else:

    st.warning(
        "Not enough data for sales prediction."
    )


# =========================================================
# TOP PRODUCTS
# =========================================================

st.header("🏆 Top Products by Sales")

top_products = (
    filtered_df
    .groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
    .head(10)
)

fig_products = px.bar(
    top_products,
    x="Product",
    y="Sales",
    title="Top 10 Products by Sales"
)

fig_products.update_layout(
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)

# =========================================================
# REGION + CATEGORY
# =========================================================

c1, c2 = st.columns(2)

with c1:

    st.subheader("🌍 Profit by Region")

    region_data = (
        filtered_df
        .groupby("Region")["Profit"]
        .sum()
        .reset_index()
        .sort_values(
            "Profit",
            ascending=False
        )
    )

    fig_region = px.bar(
        region_data,
        x="Region",
        y="Profit",
        title="Profit by Region"
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )


with c2:

    st.subheader("📦 Sales by Category")

    category_data = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig_category = px.pie(
        category_data,
        names="Category",
        values="Sales",
        title="Sales by Category"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

# =========================================================
# MONTHLY SALES
# =========================================================

st.header("📅 Monthly Sales Trend")

monthly_sales = (
    filtered_df
    .groupby(
        filtered_df["Order_Date"].dt.to_period("M")
    )["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Month"] = (
    monthly_sales["Order_Date"].astype(str)
)

fig_monthly = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)

# =========================================================
# CUSTOMER ANALYSIS
# =========================================================

st.header("👥 Customer Analysis")

customer_data = (
    filtered_df
    .groupby("Customer_Type")["Sales"]
    .sum()
    .reset_index()
)

fig_customer = px.pie(
    customer_data,
    names="Customer_Type",
    values="Sales",
    title="Sales by Customer Type"
)

st.plotly_chart(
    fig_customer,
    use_container_width=True
)

# =========================================================
# PAYMENT MODE
# =========================================================

st.header("💳 Payment Mode Analysis")

payment_data = (
    filtered_df["Payment_Mode"]
    .value_counts()
    .reset_index()
)

payment_data.columns = [
    "Payment_Mode",
    "Orders"
]

fig_payment = px.bar(
    payment_data,
    x="Payment_Mode",
    y="Orders",
    title="Orders by Payment Mode"
)

st.plotly_chart(
    fig_payment,
    use_container_width=True
)

# =========================================================
# TOP CITIES
# =========================================================

st.header("🏙️ Top Cities by Sales")

city_data = (
    filtered_df
    .groupby("City")["Sales"]
    .sum()
    .reset_index()
    .sort_values(
        "Sales",
        ascending=False
    )
    .head(10)
)

fig_city = px.bar(
    city_data,
    x="City",
    y="Sales",
    title="Top 10 Cities"
)

fig_city.update_layout(
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig_city,
    use_container_width=True
)

# =========================================================
# AI DATA ANALYST
# =========================================================

st.divider()

st.header("🤖 Ask AI Data Analyst")

st.write(
    "Ask questions about your business data."
)

question = st.text_input(
    "💬 Your Question",
    placeholder="Which product has the highest sales?"
)

if st.button("🚀 Ask AI"):

    if question.strip():

        try:

            from src.ai_assistant import ask_question

            answer = ask_question(question)

            st.success(answer)

        except Exception as e:

            st.error(
                "AI Assistant error"
            )

            st.code(str(e))

    else:

        st.warning(
            "Please enter a question."
        )

# =========================================================
# DATA TABLE
# =========================================================

st.divider()

st.header("📋 Filtered Sales Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# =========================================================
# DOWNLOAD
# =========================================================

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv_data,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AI Data Analyst | Python • Pandas • SQL • ML • Plotly • Streamlit • AI"
)