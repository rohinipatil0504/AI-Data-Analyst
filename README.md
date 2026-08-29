# AI-Data-Analyst
AI-powered Sales Analytics and Business Intelligence Dashboard
# 🤖 AI Data Analyst

An AI-powered Sales Analytics and Business Intelligence dashboard that transforms raw sales data into actionable business insights using **Python, SQL, Machine Learning, and Streamlit**.

The project combines traditional data analytics with AI/ML techniques to identify unusual sales patterns, analyze business risks, discover possible root causes, and support data-driven decision making.

## 🚀 Key Features

### 📊 Interactive Sales Dashboard

* Total Sales, Profit, and Orders KPIs
* Sales analysis by product, category, and region
* Monthly sales trends
* Interactive visualizations
* Business performance overview

### 🤖 AI Anomaly Detection

* Detects unusual monthly sales patterns
* Uses **Isolation Forest**
* Identifies abnormal product performance
* Generates anomaly summaries

### 🔍 AI Root Cause Analysis

* Investigates abnormal sales periods
* Identifies top-performing products
* Analyzes regions contributing to sales
* Analyzes category-level performance

### ⚠️ AI Sales Risk Analysis

* Calculates product-level risk scores
* Uses profit margin and sales volatility
* Classifies products into:

  * High Risk
  * Medium Risk
  * Low Risk
* Generates business recommendations

### 📈 Sales Forecasting

* Analyzes historical sales trends
* Generates future sales predictions
* Helps with business planning and decision making

### 🗄️ SQL Business Analytics

* SQLite database integration
* SQL-based business queries
* Product, region, category and sales analysis

### 🧹 Data Cleaning & Processing

* Handles missing/invalid values
* Converts and processes dates
* Prepares data for analytics and ML

## 🧠 Machine Learning

The project uses machine learning for business intelligence tasks, including:

* **Isolation Forest** — anomaly detection
* **Scikit-learn** — machine learning workflows
* Feature-based sales risk analysis
* Predictive sales analysis

## 🛠️ Tech Stack

| Technology       | Usage                   |
| ---------------- | ----------------------- |
| Python           | Data analysis and ML    |
| Pandas           | Data processing         |
| NumPy            | Numerical operations    |
| Matplotlib       | Data visualization      |
| Plotly           | Interactive charts      |
| Scikit-learn     | Machine Learning        |
| SQLite           | Database                |
| SQL              | Business analytics      |
| Streamlit        | Interactive dashboard   |
| Flask            | Backend/API development |
| Jupyter Notebook | Data exploration        |

## 📁 Project Structure

```text
AI-Data-Analyst/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│   └── sales.db
│
├── dashboard/
│   ├── app.py
│   └── dashboard.py
│
├── models/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_analysis.ipynb
│
├── reports/
│   └── figures/
│
├── src/
│   ├── ai_assistant.py
│   ├── analysis.py
│   ├── anomaly_detection.py
│   ├── data_cleaning.py
│   ├── forecast.py
│   ├── root_cause.py
│   ├── sales_prediction.py
│   ├── sales_risk.py
│   ├── sql_analysis.py
│   ├── sql_queries.py
│   └── visualization.py
│
├── requirements.txt
└── README.md
```

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/rohinipatil0504/AI-Data-Analyst.git
cd AI-Data-Analyst
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the dashboard

```bash
streamlit run dashboard/app.py
```

## 📊 Business Problems Solved

This project is designed to answer practical business questions such as:

* Which products are performing poorly?
* Which products have higher business risk?
* When did unusual sales activity occur?
* Which products, regions, or categories contributed to an anomaly?
* What are the historical sales trends?
* What sales patterns can help future planning?
* Where should management focus attention?

## 💡 Project Highlights

**AI + Data Analytics + Business Intelligence**

Instead of only displaying charts, the system attempts to move from:

**Raw Data → Analysis → ML Detection → Root Cause → Risk → Business Recommendation**

This makes the project more than a basic dashboard and demonstrates an end-to-end data analytics workflow.

## 🎯 Skills Demonstrated

* Python
* Data Analysis
* Data Cleaning
* SQL
* Machine Learning
* Anomaly Detection
* Predictive Analytics
* Business Intelligence
* Data Visualization
* Streamlit Dashboard Development
* Database Management
* Git & GitHub

## 👩‍💻 Author

**Rohini Rajesh Patil**

B.Tech Computer Science Engineering
AI / ML & Data Science Enthusiast

---

⭐ If you find this project useful, consider giving the repository a star!
