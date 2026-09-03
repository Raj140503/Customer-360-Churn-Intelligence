# Customer 360° & Churn Intelligence Platform

An end-to-end **Data Analytics, Data Engineering, Business Intelligence, and Machine Learning** platform that transforms retail transaction data into customer-level insights, churn predictions, retention priorities, and actionable revenue intelligence.

## 🚀 Live Demo

**Streamlit App:** https://customer-360-churn-intelligence.streamlit.app/

**GitHub Repository:** https://github.com/Raj140503/Customer-360-Churn-Intelligence

---

## 📌 Project Overview

Customer churn is not only a customer-service problem—it is a revenue problem.

This project builds a complete customer intelligence workflow from raw transaction data to business action:

**Raw Data → ETL → Customer 360° → RFM & Churn Analysis → ML Prediction → Retention Scoring → Power BI / Streamlit**

The platform helps answer questions such as:

- Who are the most valuable customers?
- Which customers are at risk of churning?
- How concentrated is revenue among high-value customers?
- Which customers should retention teams contact first?
- How accurately can future churn be predicted?
- What revenue is potentially exposed to churn?

---

## 🎯 Business Objectives

1. Build a reliable transaction-level data pipeline.
2. Create a unified **Customer 360°** analytical dataset.
3. Analyze customer behavior using **RFM concepts**.
4. Identify active, at-risk, and churned customers.
5. Predict future churn using machine learning.
6. Quantify customer retention opportunities using revenue-weighted scoring.
7. Present insights through interactive BI and web dashboards.
8. Translate analytical results into practical retention actions.

---

## 🧰 Tech Stack

| Area | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Visualization | Plotly, Matplotlib |
| BI | Microsoft Power BI |
| Web Dashboard | Streamlit |
| Database / SQL | PostgreSQL, SQL |
| ETL | Python |
| Data Source | UCI Online Retail Dataset |
| Version Control | Git, GitHub |

---

## 📊 Dataset

The project uses the **UCI Online Retail Dataset**, containing transactional records from a UK-based online retailer.

- **541,909** raw transaction records
- **8** original columns
- Transaction period: **December 2010 – December 2011**
- Customer and product transaction information
- Returns and invalid transactions handled during ETL

Source: https://archive.ics.uci.edu/

---

# 🔄 Data Engineering & ETL

The ETL pipeline cleans and transforms raw transaction data into an analytics-ready sales dataset.

### Pipeline

```text
Raw Online Retail Data
        ↓
Column Standardization
        ↓
Duplicate Removal
        ↓
Revenue Calculation
        ↓
Transaction Classification
        ↓
Invalid Sale Filtering
        ↓
Processed Sales Dataset
        ↓
Customer / ML / BI Analytics
```

### Key transformations

- Standardized column names
- Converted customer IDs to nullable integers
- Removed duplicate records
- Calculated:

```text
Revenue = Quantity × Unit Price
```

- Classified transactions as `SALE` or `RETURN`
- Removed invalid sales with:
  - Missing customer ID
  - Non-positive quantity
  - Non-positive unit price
  - Return transactions

### ETL Output

The pipeline produces:

```text
data/processed/sales.csv
```

The deployed Streamlit application uses lightweight processed outputs so the application can run efficiently without requiring the large transaction-level CSV.

---

# 👤 Customer 360°

The Customer 360° dataset consolidates customer behavior into a single analytical view.

### Customer-level metrics

- Total Orders
- Total Items
- Total Revenue
- Average Order Value
- First Purchase Date
- Last Purchase Date
- Recency
- Frequency
- Churn Status
- Country

### Customer churn classification

| Status | Recency |
|---|---:|
| Active | 0–60 days |
| At Risk | 61–120 days |
| Churned | 121+ days |

---

# 📈 RFM & Customer Segmentation

Customers are segmented based on purchasing behavior.

### Segments

- Champions
- Potential Loyalists
- Loyal Customers
- New / Promising
- At Risk
- Lost Customers

### Key finding

**Champions generated approximately £5.73M, representing 64.48% of customer revenue.**

This demonstrates the strong revenue contribution of high-value customers.

---

# 💰 Revenue Intelligence

The analysis highlights substantial revenue concentration.

### Pareto analysis

| Customer Segment | Revenue Contribution |
|---|---:|
| Top 2.3% | 40.61% |
| Top 5% | 50.46% |
| Top 10% | 61.41% |
| Top 20% | 74.68% |
| Top 50% | 92.19% |

### Key insight

The **top 10% of customers generated approximately 61.41% of total customer revenue**.

This makes high-value customer retention a major business priority.

---

# 🤖 Machine Learning — Churn Prediction

A leakage-free supervised ML workflow was developed to predict whether a customer would churn in a future period.

### Models evaluated

- Logistic Regression
- Random Forest

### Evaluation

| Model | Accuracy | ROC-AUC |
|---|---:|---:|
| Logistic Regression | 68.79% | **73.54%** |
| Random Forest | 67.82% | 73.10% |

### Selected model

**Logistic Regression**

It achieved the highest ROC-AUC and provides interpretable feature coefficients, making it useful for explaining customer churn drivers.

### Important churn signals

The model indicates that customer behavior such as:

- Lower historical order frequency
- Higher recency
- Lower historical revenue
- Customer lifetime characteristics

plays an important role in future churn risk.

---

# 🎯 Retention Intelligence

The project goes beyond simply predicting churn.

Customers are prioritized using:

```text
Retention Opportunity Score
=
Historical Revenue × Churn Probability
```

This combines:

**Customer Value + Churn Risk**

so retention teams can focus on customers where churn could have the greatest financial impact.

### Risk distribution

| Risk Level | Customers |
|---|---:|
| Low Risk | 551 |
| Moderate Risk | 308 |
| High Risk | 1,007 |
| Critical Risk | 1,738 |

### Highest retention opportunity

The highest identified opportunity was:

- Customer: `12346`
- Historical Revenue: **£77,183.60**
- Churn Probability: **99.92%**
- Retention Opportunity Score: approximately **£77.1K**
- Risk Level: **Critical**

---

# 📊 Power BI Dashboard

The Power BI report contains **5 analytical pages**.

### 1. Executive Overview

Provides:

- Revenue KPIs
- Customer KPIs
- Monthly revenue trend
- Revenue concentration
- High-level business insights

### 2. Customer & Churn Analysis

Provides:

- Customer segmentation
- Churn status
- Recency analysis
- Customer behavior
- Revenue by customer segment

### 3. Retention & Revenue Intelligence

Provides:

- Retention risk
- Revenue at risk
- Retention opportunities
- High-value customer identification
- Priority analysis

### 4. ML Model Performance

Provides:

- Model comparison
- Accuracy
- ROC-AUC
- Logistic Regression performance
- Model interpretation

### 5. Actionable Retention Insights

Provides:

- Priority customer groups
- Retention recommendations
- Revenue-risk interpretation
- Business actions

---

# 🌐 Streamlit Application

The Streamlit version provides an interactive web interface for exploring the analytical outputs.

### Application sections

- **Executive Overview**
- **Customer & Churn**
- **Retention Intelligence**
- **ML Performance**
- **Customer Explorer**

The deployed application uses lightweight analytical datasets such as:

```text
customer_360.csv
retention_scoring.csv
monthly_revenue.csv
model_evaluation.csv
```

This avoids requiring the large transaction-level `sales.csv` file during cloud deployment.

---

# 🗄️ SQL Analytics

PostgreSQL / SQL analysis was used to perform customer-level analytical queries.

Examples include:

- Customer revenue analysis
- RFM segmentation
- Customer ranking
- Revenue concentration
- Churn analysis
- Retention opportunity analysis
- Customer behavior aggregation

SQL scripts are available in:

```text
sql/
```

---

# 📁 Repository Structure

```text
Customer-360-Churn-Intelligence/
│
├── analysis/
│   └── Exploratory analysis notebooks
│
├── data/
│   ├── raw/
│   │   └── Online Retail.xlsx
│   │
│   └── processed/
│       ├── customer_360.csv
│       ├── retention_scoring.csv
│       ├── monthly_revenue.csv
│       └── sales.csv
│
├── etl/
│   ├── pipeline.py
│   ├── transform.py
│   └── test_read.py
│
├── reports/
│   ├── Customer_360_Churn_Intelligence.pbix
│   └── model_evaluation.csv
│
├── sql/
│   └── customer_analysis.sql
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

> `sales.csv` is the large transaction-level ETL output used locally for analysis. The deployed Streamlit application does not depend on it.

---

# ▶️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Raj140503/Customer-360-Churn-Intelligence.git
cd Customer-360-Churn-Intelligence
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scriptsctivate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit application

```bash
streamlit run app.py
```

The application will open in your browser.

---

# ⚙️ Run the ETL Pipeline

From the project root:

```bash
python etl/pipeline.py
```

Expected output:

```text
Starting ETL pipeline...
Successfully extracted 541,909 rows.
Valid sales records: 392,692
Saved processed data to data/processed/sales.csv
ETL pipeline completed successfully.
```

---

# 📌 Key Business Findings

### Customer concentration

The top 10% of customers contribute approximately **61.41% of revenue**, creating a strong business case for VIP retention programs.

### Churn exposure

The future churn dataset contains approximately **53.02% future churn**, providing a meaningful classification problem for retention modeling.

### Customer health

Current Customer 360° segmentation identifies:

- **2,410 Active**
- **713 At Risk**
- **1,215 Churned**

### Retention strategy

The strongest retention strategy is not to target every high-risk customer equally.

Instead:

```text
High Churn Probability
        +
High Historical Revenue
        ↓
High Retention Priority
```

This converts a predictive model into a practical revenue-protection framework.

---

# 💡 Recommended Business Actions

### Champions
- VIP treatment
- Loyalty rewards
- Early product access
- Personalized offers

### High-value At-Risk Customers
- Immediate retention outreach
- Personalized incentives
- Re-engagement campaigns
- Account-level monitoring

### Low-value High-risk Customers
- Automated email campaigns
- Low-cost reactivation offers
- Marketing automation

### Churned Customers
- Win-back campaigns
- Customer feedback collection
- Reactivation incentives

---

# 📈 Why This Project Stands Out

This project demonstrates more than dashboard creation.

It combines:

**Data Engineering**
→ ETL pipeline and data transformation

**Data Analytics**
→ Customer behavior, RFM, revenue concentration

**SQL**
→ Analytical customer segmentation and ranking

**Machine Learning**
→ Leakage-free churn prediction

**Business Intelligence**
→ Power BI dashboard

**Application Development**
→ Streamlit interactive platform

**Business Strategy**
→ Revenue-weighted retention prioritization

The result is an end-to-end **Customer Intelligence & Revenue Retention Platform**.

---

# 👨‍💻 Author

**Raj**

Computer Engineering | Data Analytics | Data Engineering | Machine Learning

### Portfolio

- GitHub: https://github.com/Raj140503
- Project Repository: https://github.com/Raj140503/Customer-360-Churn-Intelligence
- Live Application: https://customer-360-churn-intelligence.streamlit.app/

---

## 📜 License & Dataset Attribution

This project is intended for educational and portfolio purposes.

The Online Retail dataset is provided by the **UCI Machine Learning Repository** under **CC BY 4.0**.

Dataset source: https://archive.ics.uci.edu/
