import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

# =========================================================
# PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "raw" / "sales_data.csv"

sys.path.append(str(BASE_DIR))


# =========================================================
# PROJECT MODULES
# =========================================================

from src.ai_assistant import ask_llama, generate_recommendations
from src.forecast import forecast_sales
from src.anomaly_detection import (
    detect_monthly_anomalies,
    detect_product_anomalies
)
from src.root_cause import analyze_root_cause
from src.sales_risk import calculate_risk


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("🤖 AI Data Analyst")

st.subheader(
    "AI Powered Sales Intelligence Dashboard"
)

st.caption(
    "Python • Pandas • SQL • Machine Learning • "
    "Llama • Forecasting • Anomaly Detection • "
    "Root Cause Analysis • Risk Scoring"
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


try:

    df = load_data()

except Exception as e:

    st.error(f"❌ Data loading error: {e}")
    st.stop()


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.title("🔎 Dashboard Filters")


regions = sorted(
    df["Region"].dropna().unique()
)

selected_regions = st.sidebar.multiselect(
    "🌍 Region",
    regions,
    default=regions
)


categories = sorted(
    df["Category"].dropna().unique()
)

selected_categories = st.sidebar.multiselect(
    "📦 Category",
    categories,
    default=categories
)


customers = sorted(
    df["Customer_Type"].dropna().unique()
)

selected_customers = st.sidebar.multiselect(
    "👥 Customer Type",
    customers,
    default=customers
)


payments = sorted(
    df["Payment_Mode"].dropna().unique()
)

selected_payments = st.sidebar.multiselect(
    "💳 Payment Mode",
    payments,
    default=payments
)


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df[
    df["Region"].isin(selected_regions)
    &
    df["Category"].isin(selected_categories)
    &
    df["Customer_Type"].isin(selected_customers)
    &
    df["Payment_Mode"].isin(selected_payments)
]


if filtered_df.empty:

    st.warning(
        "⚠️ No data available for selected filters."
    )

    st.stop()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_orders = filtered_df["Order_ID"].nunique()

total_quantity = filtered_df["Quantity"].sum()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)


# =========================================================
# BUSINESS OVERVIEW
# =========================================================

st.markdown("---")

st.header("📊 Business Overview")


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
    "🛒 Total Orders",
    f"{total_orders:,}"
)


c4.metric(
    "📦 Quantity Sold",
    f"{total_quantity:,}"
)


c5.metric(
    "📊 Profit Margin",
    f"{profit_margin:.2f}%"
)


# =========================================================
# 🧠 AI EXECUTIVE SUMMARY
# =========================================================

st.markdown("---")

st.header("🧠 AI Executive Summary")


try:

    best_product_data = (
        filtered_df
        .groupby("Product")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    best_product = best_product_data.index[0]

    best_product_sales = best_product_data.iloc[0]


    best_region_data = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    best_region = best_region_data.index[0]


    best_category_data = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    best_category = best_category_data.index[0]


    risk_data = calculate_risk()

    high_risk_count = len(
        risk_data[
            risk_data["Risk_Level"] == "High Risk"
        ]
    )


    anomaly_data = detect_monthly_anomalies()

    anomaly_count = len(
        anomaly_data[
            anomaly_data["Status"] == "Anomaly"
        ]
    )


    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "🏆 Best Product",
        best_product
    )


    c2.metric(
        "🌍 Best Region",
        best_region
    )


    c3.metric(
        "📦 Best Category",
        best_category
    )


    c4.metric(
        "🚨 Anomalies",
        anomaly_count
    )


    st.subheader("🤖 Business Intelligence")


    if anomaly_count > 0:

        anomaly_message = (
            f"⚠️ {anomaly_count} unusual sales period(s) "
            "were detected."
        )

    else:

        anomaly_message = (
            "✅ No major sales anomalies detected."
        )


    if high_risk_count > 0:

        risk_message = (
            f"🎯 {high_risk_count} product(s) "
            "are classified as High Risk."
        )

    else:

        risk_message = (
            "✅ No High Risk products detected."
        )


    st.info(
        f"""
### 📊 Overall Performance

Your business generated **₹{total_sales:,.2f}**
in sales and **₹{total_profit:,.2f}** profit.

### 🏆 Top Product

**{best_product}** is the highest-selling product
with sales of **₹{best_product_sales:,.2f}**.

### 🌍 Regional Insight

**{best_region}** is the strongest-performing region.

### 📦 Category Insight

**{best_category}** is the leading sales category.

### 🚨 Risk Monitoring

{risk_message}

### 🔍 Anomaly Monitoring

{anomaly_message}

### 💡 Recommended Action

Focus on high-performing products while investigating
high-risk products and unusual sales periods.
"""
    )


except Exception as e:

    st.error(
        f"❌ Executive Summary Error: {e}"
    )


# =========================================================
# 🏆 TOP PRODUCTS
# =========================================================

st.markdown("---")

st.header("🏆 Top Products")


product_sales = (
    filtered_df
    .groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)


fig = px.bar(
    product_sales,
    x="Sales",
    y="Product",
    orientation="h",
    title="Top 10 Products by Sales"
)


fig.update_layout(
    yaxis=dict(
        categoryorder="total ascending"
    )
)


st.plotly_chart(
    fig,
    width="stretch"
)


# =========================================================
# 🌍 REGION + CATEGORY
# =========================================================

c1, c2 = st.columns(2)


with c1:

    st.subheader("🌍 Sales by Region")


    region_sales = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )


    fig = px.pie(
        region_sales,
        names="Region",
        values="Sales",
        title="Regional Sales Distribution"
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


with c2:

    st.subheader("📦 Sales by Category")


    category_sales = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )


    fig = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        title="Category Sales"
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


# =========================================================
# 👥 CUSTOMER ANALYSIS
# =========================================================

st.markdown("---")

st.header("👥 Customer Analysis")


customer_sales = (
    filtered_df
    .groupby("Customer_Type")["Sales"]
    .sum()
    .reset_index()
)


fig = px.pie(
    customer_sales,
    names="Customer_Type",
    values="Sales",
    title="Sales by Customer Type"
)


st.plotly_chart(
    fig,
    width="stretch"
)


# =========================================================
# 📅 MONTHLY SALES
# =========================================================

st.markdown("---")

st.header("📅 Monthly Sales Trend")


monthly_sales = (
    filtered_df
    .set_index("Order_Date")
    .resample("ME")["Sales"]
    .sum()
    .reset_index()
)


fig = px.line(
    monthly_sales,
    x="Order_Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)


st.plotly_chart(
    fig,
    width="stretch"
)


# =========================================================
# 🚨 ANOMALY DETECTION
# =========================================================

st.markdown("---")

st.header("🚨 AI Anomaly Detection")


st.write(
    "Isolation Forest identifies unusual sales behaviour."
)


try:

    anomalies = detect_monthly_anomalies()


    if anomalies.empty:

        st.info(
            "Not enough data for anomaly detection."
        )

        anomaly_rows = pd.DataFrame()

    else:

        anomaly_rows = anomalies[
            anomalies["Status"] == "Anomaly"
        ]


        if anomaly_rows.empty:

            st.success(
                "✅ No major sales anomalies detected."
            )

        else:

            st.warning(
                f"⚠️ {len(anomaly_rows)} unusual "
                "sales period(s) detected."
            )


        fig = px.line(
            anomalies,
            x="Order_Date",
            y="Sales",
            markers=True,
            title="Monthly Sales Anomaly Detection"
        )


        if not anomaly_rows.empty:

            fig.add_scatter(
                x=anomaly_rows["Order_Date"],
                y=anomaly_rows["Sales"],
                mode="markers",
                marker=dict(
                    size=16,
                    symbol="x"
                ),
                name="🚨 Anomaly"
            )


        st.plotly_chart(
            fig,
            width="stretch"
        )


        st.subheader("🚨 Detected Anomalies")


        if anomaly_rows.empty:

            st.info(
                "No unusual periods found."
            )

        else:

            st.dataframe(
                anomaly_rows[
                    [
                        "Order_Date",
                        "Sales",
                        "Status"
                    ]
                ],
                width="stretch"
            )


except Exception as e:

    st.error(
        f"❌ Anomaly Detection Error: {e}"
    )

    anomaly_rows = pd.DataFrame()


# =========================================================
# 📦 PRODUCT ANOMALY
# =========================================================

st.subheader(
    "📦 Product Anomaly Analysis"
)


try:

    product_anomalies = detect_product_anomalies()


    product_alerts = product_anomalies[
        product_anomalies["Status"] == "Anomaly"
    ]


    if product_alerts.empty:

        st.success(
            "✅ No unusual product sales detected."
        )

    else:

        st.warning(
            f"⚠️ {len(product_alerts)} unusual "
            "product(s) detected."
        )


        st.dataframe(
            product_alerts[
                [
                    "Product",
                    "Sales",
                    "Status"
                ]
            ],
            width="stretch"
        )


except Exception as e:

    st.error(
        f"❌ Product Anomaly Error: {e}"
    )


# =========================================================
# 🧠 ROOT CAUSE
# =========================================================

st.markdown("---")

st.header("🧠 AI Root Cause Analysis")


st.write(
    "Find the products, regions and categories "
    "responsible for unusual sales behaviour."
)


try:

    if not anomaly_rows.empty:

        selected_anomaly = st.selectbox(
            "📅 Select anomaly period",
            anomaly_rows["Order_Date"].tolist()
        )


        if st.button(
            "🔍 Analyze Root Cause"
        ):

            with st.spinner(
                "🧠 Analyzing..."
            ):

                result = analyze_root_cause(
                    selected_anomaly
                )


            if result is None:

                st.warning(
                    "No data found."
                )

            else:

                st.success(
                    "✅ Root Cause Analysis Completed"
                )


                c1, c2, c3 = st.columns(3)


                with c1:

                    st.subheader("🏆 Top Products")

                    st.dataframe(
                        result["product"],
                        width="stretch"
                    )


                with c2:

                    st.subheader("🌍 Top Regions")

                    st.dataframe(
                        result["region"],
                        width="stretch"
                    )


                with c3:

                    st.subheader("📦 Top Categories")

                    st.dataframe(
                        result["category"],
                        width="stretch"
                    )


    else:

        st.info(
            "Root Cause Analysis will appear "
            "when an anomaly is detected."
        )


except Exception as e:

    st.error(
        f"❌ Root Cause Error: {e}"
    )


# =========================================================
# 🎯 AI SALES RISK
# =========================================================

st.markdown("---")

st.header("🎯 AI Sales Risk Score")


st.write(
    "AI-based risk scoring uses sales, profit, "
    "orders and sales volatility."
)


try:

    risk_data = calculate_risk()


    if risk_data.empty:

        st.info(
            "No risk data available."
        )

    else:

        high_risk = len(
            risk_data[
                risk_data["Risk_Level"] == "High Risk"
            ]
        )


        medium_risk = len(
            risk_data[
                risk_data["Risk_Level"] == "Medium Risk"
            ]
        )


        low_risk = len(
            risk_data[
                risk_data["Risk_Level"] == "Low Risk"
            ]
        )


        c1, c2, c3 = st.columns(3)


        c1.metric(
            "🔴 High Risk",
            high_risk
        )


        c2.metric(
            "🟡 Medium Risk",
            medium_risk
        )


        c3.metric(
            "🟢 Low Risk",
            low_risk
        )


        risk_chart = risk_data[
            [
                "Product",
                "Risk_Score"
            ]
        ].sort_values(
            "Risk_Score",
            ascending=True
        )


        st.subheader(
            "📊 Product Risk Score"
        )


        fig = px.bar(
            risk_chart,
            x="Risk_Score",
            y="Product",
            orientation="h",
            title="AI Product Risk Score"
        )


        fig.update_xaxes(
            range=[0, 100]
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


        st.subheader(
            "📋 Risk Analysis"
        )


        display_risk = risk_data[
            [
                "Product",
                "Sales",
                "Profit",
                "Orders",
                "Profit_Margin",
                "Risk_Score",
                "Risk_Level",
                "Recommendation"
            ]
        ].copy()


        display_risk["Sales"] = (
            display_risk["Sales"].round(2)
        )


        display_risk["Profit"] = (
            display_risk["Profit"].round(2)
        )


        display_risk["Profit_Margin"] = (
            display_risk["Profit_Margin"].round(2)
        )


        st.dataframe(
            display_risk,
            width="stretch"
        )


        highest_risk = risk_data.iloc[0]


        st.warning(
            f"🚨 Highest Risk Product: "
            f"**{highest_risk['Product']}** "
            f"with Risk Score "
            f"**{highest_risk['Risk_Score']}/100**"
        )


        st.info(
            f"💡 Recommendation: "
            f"{highest_risk['Recommendation']}"
        )


except Exception as e:

    st.error(
        f"❌ Sales Risk Error: {e}"
    )


# =========================================================
# 💰 PROFIT BY REGION
# =========================================================

st.markdown("---")

st.header("💰 Profit by Region")


region_profit = (
    filtered_df
    .groupby("Region")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)


fig = px.bar(
    region_profit,
    x="Region",
    y="Profit",
    title="Regional Profit"
)


st.plotly_chart(
    fig,
    width="stretch"
)


# =========================================================
# 💳 PAYMENT ANALYSIS
# =========================================================

st.markdown("---")

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


fig = px.bar(
    payment_data,
    x="Payment_Mode",
    y="Orders",
    title="Orders by Payment Mode"
)


st.plotly_chart(
    fig,
    width="stretch"
)


# =========================================================
# 🏙️ CITY ANALYSIS
# =========================================================

st.markdown("---")

st.header("🏙️ Top Cities")


city_sales = (
    filtered_df
    .groupby("City")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)


fig = px.bar(
    city_sales,
    x="Sales",
    y="City",
    orientation="h",
    title="Top 10 Cities by Sales"
)


fig.update_layout(
    yaxis=dict(
        categoryorder="total ascending"
    )
)


st.plotly_chart(
    fig,
    width="stretch"
)


# =========================================================
# 🔮 FORECAST
# =========================================================

st.markdown("---")

st.header("🔮 AI Sales Forecast")


try:

    forecast = forecast_sales(6)


    if forecast is not None:

        fig = px.line(
            forecast,
            x="Month",
            y="Predicted_Sales",
            markers=True,
            title="Next 6 Months Sales Forecast"
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


        st.dataframe(
            forecast,
            width="stretch"
        )


    else:

        st.warning(
            "Forecast data unavailable."
        )


except Exception as e:

    st.error(
        f"❌ Forecast Error: {e}"
    )


# =========================================================
# 🤖 LLAMA AI ANALYST
# =========================================================

st.markdown("---")

st.header("🤖 Ask AI Data Analyst")


st.write(
    "Ask questions about your sales data using natural language."
)


question = st.text_input(
    "💬 Enter your question",
    placeholder="Which product has the highest sales?"
)


if st.button(
    "🚀 Ask AI"
):

    if question.strip():

        with st.spinner(
            "🤖 Llama is analyzing your data..."
        ):

            try:

                answer = ask_llama(
                    question
                )


                st.success(
                    "AI Analysis Completed!"
                )


                st.markdown(
                    answer
                )


            except Exception as e:

                st.error(
                    f"❌ AI Error: {e}"
                )

    else:

        st.warning(
            "Please enter a question."
        )


# =========================================================
# 💡 AI RECOMMENDATIONS
# =========================================================

st.markdown("---")

st.header(
    "💡 AI Business Recommendations"
)


if st.button(
    "🚀 Generate Recommendations"
):

    with st.spinner(
        "🤖 Generating business insights..."
    ):

        try:

            recommendations = (
                generate_recommendations()
            )


            st.success(
                "Recommendations Generated!"
            )


            st.markdown(
                recommendations
            )


        except Exception as e:

            st.error(
                f"❌ Recommendation Error: {e}"
            )


# =========================================================
# 💭 EXAMPLE QUESTIONS
# =========================================================

st.markdown("---")

st.header(
    "💭 Example AI Questions"
)


questions = [

    "Which product has the highest sales?",

    "Which product has the highest profit?",

    "Which region has the highest profit?",

    "Which category has the highest sales?",

    "Which city has the highest sales?",

    "Which payment mode is most popular?",

    "What are the total sales?",

    "What are the total profits?",

    "Give me business recommendations.",

    "Why did sales change?"

]


for q in questions:

    st.write(
        "• " + q
    )


# =========================================================
# 📥 BUSINESS REPORT
# =========================================================

st.markdown("---")

st.header(
    "📥 Download Business Report"
)


report = f"""
AI DATA ANALYST BUSINESS REPORT
================================

BUSINESS OVERVIEW
-----------------

Total Sales   : ₹{total_sales:,.2f}

Total Profit  : ₹{total_profit:,.2f}

Total Orders  : {total_orders:,}

Quantity Sold : {total_quantity:,}

Profit Margin : {profit_margin:.2f}%


AI FEATURES
-----------

Llama AI Analyst

Sales Forecasting

Isolation Forest Anomaly Detection

AI Root Cause Analysis

AI Sales Risk Scoring

AI Executive Summary

Business Recommendations


TECHNOLOGY
----------

Python

Pandas

NumPy

SQL

Scikit-learn

Plotly

Streamlit

Llama / Ollama

Machine Learning
"""


st.download_button(
    label="📥 Download Report",
    data=report,
    file_name="AI_Business_Report.txt",
    mime="text/plain"
)


# =========================================================
# 📋 DATA PREVIEW
# =========================================================

st.markdown("---")

st.header(
    "📋 Sales Data"
)


st.dataframe(
    filtered_df,
    width="stretch",
    height=400
)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "AI Data Analyst | Python • Pandas • SQL • ML • "
    "Llama • Forecasting • Anomaly Detection • "
    "Root Cause Analysis • Risk Scoring"
)