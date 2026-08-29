# 🤖 AI Data Analyst

An AI-powered Sales Analytics and Business Intelligence application that helps businesses understand sales performance, detect unusual patterns, identify possible root causes, predict future sales, and generate AI-based business insights.

## 🚀 Project Overview

**AI Data Analyst** converts raw sales data into meaningful business insights using data analysis, SQL, machine learning, forecasting, and a local LLM-based AI assistant.

The application provides an interactive Streamlit dashboard where users can explore sales data and ask questions in natural language.

## ✨ Key Features

### 📊 Business Dashboard

* Total Sales
* Total Profit
* Total Orders
* Quantity Sold
* Profit Margin
* Interactive filters

### 🤖 AI Data Analyst

Ask questions in natural language, such as:

* Which product has the highest sales?
* Which product has the highest profit?
* Which region has the highest sales?
* Which category is performing best?
* What are the business recommendations?

### 🚨 AI Anomaly Detection

Uses **Isolation Forest** to identify unusual sales periods and unusual product-level sales behaviour.

### 🧠 Root Cause Analysis

Analyzes an unusual sales period using:

* Product performance
* Regional performance
* Category performance

### 🎯 AI Sales Risk Analysis

Calculates product-level risk using:

* Sales
* Profit
* Number of orders
* Profit margin
* Sales volatility

Products are classified as:

* 🔴 High Risk
* 🟡 Medium Risk
* 🟢 Low Risk

### 🔮 Sales Forecasting

Uses historical sales data to generate future sales predictions.

### 🧠 AI Executive Summary

Automatically summarizes:

* Overall sales performance
* Best product
* Best region
* Best category
* Detected anomalies
* High-risk products
* Recommended business actions

### 💡 Business Recommendations

Generates actionable recommendations based on sales performance and detected business patterns.

### 📈 Interactive Visualizations

The dashboard includes:

* Sales trends
* Product comparison
* Regional analysis
* Category analysis
* Customer analysis
* Payment analysis
* City analysis
* Profit analysis
* Risk visualization
* Forecast visualization

## 🛠️ Technologies Used

* **Python**
* **Pandas**
* **NumPy**
* **SQLite**
* **SQL**
* **Scikit-learn**
* **Plotly**
* **Streamlit**
* **Ollama / Llama**
* **Machine Learning**

## 🧠 Machine Learning

The project uses machine learning for:

**Anomaly Detection**

* Isolation Forest

**Sales Risk Analysis**

* Risk scoring based on business metrics

**Sales Forecasting**

* Historical sales-based prediction

## 📁 Project Structure

```text
AI_Data_Analyst/
│
├── dashboard/
│   └── dashboard.py
│
├── database/
│   └── sales.db
│
├── data/
│   └── raw/
│       └── sales_data.csv
│
├── src/
│   ├── analysis.py
│   ├── ai_assistant.py
│   ├── anomaly_detection.py
│   ├── create_dataset.py
│   ├── data_cleaning.py
│   ├── forecast.py
│   ├── root_cause.py
│   ├── sales_prediction.py
│   ├── sales_risk.py
│   ├── sql_analysis.py
│   ├── sql_queries.py
│   └── visualization.py
│
├── README.md
└── requirements.txt
```

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/rohinipatil0504/AI-Data-Analyst.git
```

### 2. Open the project

```bash
cd AI-Data-Analyst
```

### 3. Create virtual environment

```bash
python -m venv venv
```

### 4. Activate virtual environment

Windows:

```powershell
.\venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the dashboard

```bash
streamlit run dashboard/dashboard.py
```

The application will open in your browser.

## 🤖 AI Assistant

The project integrates a local LLM through **Ollama** to provide natural-language business analysis.

Example:

**User:**

> Which product has the highest sales?

**AI Analyst:**

> Laptop has the highest sales based on the available sales data.

## 📊 Example Business Insights

The system can identify:

* Best-performing products
* Weak-performing products
* High-risk products
* Unusual sales periods
* Strong-performing regions
* High-performing categories
* Future sales trends

## 🎯 Project Goal

The goal of this project is to build an AI-powered business analytics system that goes beyond traditional dashboards by combining:

**Data Analytics + SQL + Machine Learning + Forecasting + Generative AI**

into a single application.

## 🔮 Future Improvements

* Automated PDF business reports
* Advanced forecasting models
* Customer churn prediction
* Sales recommendation engine
* Real-time data integration
* Automated email alerts for anomalies
* Cloud deployment
* Role-based dashboard access

## 👩‍💻 Author

**Rohini Rajesh Patil**

B.Tech Computer Science Engineering

Interested in **AI/ML, Data Science and Business Analytics**.

---

⭐ If you find this project useful, consider giving the repository a star!
