import pandas as pd
import matplotlib.pyplot as plt


# Load processed sales data
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "sales.csv"

df = pd.read_csv(DATA_PATH)

# Convert date
df["invoicedate"] = pd.to_datetime(df["invoicedate"])

print("Dataset shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nBasic statistics:")
print(df[["quantity", "unitprice", "revenue"]].describe())

print("\nUnique customers:", df["customerid"].nunique())
print("Unique products:", df["stockcode"].nunique())
print("Unique invoices:", df["invoiceno"].nunique())

# Top transactions by revenue
print("\nTop 10 transactions by revenue:")

top_revenue = (
    df[
        [
            "invoiceno",
            "stockcode",
            "description",
            "quantity",
            "unitprice",
            "customerid",
            "country",
            "revenue",
        ]
    ]
    .sort_values("revenue", ascending=False)
    .head(10)
)

print(top_revenue.to_string(index=False))

# Outlier thresholds
print("\nOutlier analysis:")

for column in ["quantity", "unitprice", "revenue"]:
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1

    upper_bound = q3 + (1.5 * iqr)

    outliers = df[df[column] > upper_bound]

    print(f"\n{column}")
    print(f"Q1: {q1:.2f}")
    print(f"Q3: {q3:.2f}")
    print(f"IQR: {iqr:.2f}")
    print(f"Upper bound: {upper_bound:.2f}")
    print(f"Outlier rows: {len(outliers):,}")

# Revenue distribution analysis
print("\nRevenue distribution:")

print(f"Mean revenue:   {df['revenue'].mean():.2f}")
print(f"Median revenue: {df['revenue'].median():.2f}")
print(f"Skewness:       {df['revenue'].skew():.2f}")
print(f"Kurtosis:       {df['revenue'].kurtosis():.2f}")

# Monthly revenue analysis

monthly_revenue = (
    df.set_index("invoicedate")
    .resample("ME")["revenue"]
    .sum()
    .reset_index()
)

print("\nMonthly revenue:")
print(monthly_revenue.to_string(index=False))

# Month-over-month revenue growth

monthly_revenue["mom_growth_pct"] = (
    monthly_revenue["revenue"]
    .pct_change()
    .mul(100)
)

print("\nMonthly revenue with MoM growth:")
print(
    monthly_revenue.to_string(
        index=False,
        formatters={
            "revenue": "{:,.2f}".format,
            "mom_growth_pct": "{:.2f}%".format,
        }
    )
)

# Monthly revenue visualization

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_revenue["invoicedate"],
    monthly_revenue["revenue"],
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    PROJECT_ROOT / "reports" / "monthly_revenue_trend.png",
    dpi=150
)

plt.show()

# Customer-level revenue analysis

customer_revenue = (
    df.groupby("customerid")["revenue"]
    .sum()
    .reset_index()
    .rename(columns={"revenue": "total_revenue"})
)

print("\nCustomer revenue statistics:")
print(customer_revenue["total_revenue"].describe())

print("\nTop 10 customers by revenue:")
print(
    customer_revenue
    .sort_values("total_revenue", ascending=False)
    .head(10)
    .to_string(index=False)
)

# Revenue concentration analysis

customer_revenue = customer_revenue.sort_values(
    "total_revenue",
    ascending=False
).reset_index(drop=True)

total_revenue = customer_revenue["total_revenue"].sum()

top_10_count = int(len(customer_revenue) * 0.10)

top_10_revenue = customer_revenue.head(top_10_count)["total_revenue"].sum()

top_10_percentage = (
    top_10_revenue / total_revenue
) * 100

print("\nRevenue concentration:")
print(f"Total customers: {len(customer_revenue):,}")
print(f"Top 10% customers: {top_10_count:,}")
print(f"Top 10% revenue: £{top_10_revenue:,.2f}")
print(f"Top 10% revenue share: {top_10_percentage:.2f}%")

# Pareto revenue analysis

customer_revenue["cumulative_revenue"] = (
    customer_revenue["total_revenue"].cumsum()
)

customer_revenue["cumulative_revenue_pct"] = (
    customer_revenue["cumulative_revenue"]
    / customer_revenue["total_revenue"].sum()
) * 100

customer_revenue["customer_pct"] = (
    (customer_revenue.index + 1)
    / len(customer_revenue)
) * 100

print("\nPareto analysis:")
print(
    customer_revenue[
        ["customer_pct", "cumulative_revenue_pct"]
    ].iloc[[99, 216, 432, 867, 2168, 4337]]
    .to_string(index=False)
)

# Pareto revenue visualization

plt.figure(figsize=(12, 6))

plt.plot(
    customer_revenue["customer_pct"],
    customer_revenue["cumulative_revenue_pct"]
)

plt.axhline(
    80,
    linestyle="--",
    label="80% Revenue"
)

plt.axvline(
    20,
    linestyle="--",
    label="20% Customers"
)

plt.title("Customer Revenue Concentration (Pareto Analysis)")
plt.xlabel("Cumulative % of Customers")
plt.ylabel("Cumulative % of Revenue")
plt.legend()
plt.tight_layout()

plt.savefig(
    PROJECT_ROOT / "reports" / "customer_revenue_pareto.png",
    dpi=150
)

plt.show()

# Customer purchase frequency analysis

customer_frequency = (
    df.groupby("customerid")["invoiceno"]
    .nunique()
    .reset_index()
    .rename(columns={"invoiceno": "purchase_frequency"})
)

print("\nCustomer purchase frequency:")
print(customer_frequency["purchase_frequency"].describe())

print("\nPurchase frequency distribution:")
print(
    customer_frequency["purchase_frequency"]
    .value_counts()
    .sort_index()
    .head(20)
)


# Purchase frequency visualization
# Focus on customers with up to 20 purchases
# while retaining all underlying data.

frequency_plot = (
    customer_frequency[
        customer_frequency["purchase_frequency"] <= 20
    ]["purchase_frequency"]
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(12, 6))

plt.bar(
    frequency_plot.index,
    frequency_plot.values
)

plt.title("Customer Purchase Frequency (Up to 20 Purchases)")
plt.xlabel("Number of Purchases")
plt.ylabel("Number of Customers")
plt.xticks(frequency_plot.index)

plt.tight_layout()

plt.savefig(
    PROJECT_ROOT / "reports" / "customer_purchase_frequency.png",
    dpi=150
)

plt.show()

# Load Customer 360 data from PostgreSQL export

CUSTOMER_360_PATH = PROJECT_ROOT / "data" / "processed" / "customer_360.csv"

customer_360 = pd.read_csv(CUSTOMER_360_PATH)

print("\nCustomer 360 shape:")
print(customer_360.shape)

print("\nCustomer 360 columns:")
print(customer_360.columns.tolist())

# Churn behavior analysis

churn_analysis = (
    customer_360
    .groupby("churn_status")
    .agg(
        customers=("customer_id", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_revenue=("total_revenue", "mean"),
        avg_orders=("total_orders", "mean"),
        avg_order_value=("average_order_value", "mean"),
    )
    .round(2)
)

print("\nChurn behavior analysis:")
print(churn_analysis)

# Prepare churn modeling dataset

model_df = customer_360.copy()

model_df["churn"] = (
    model_df["churn_status"] == "Churned"
).astype(int)

# Convert dates
model_df["first_purchase_date"] = pd.to_datetime(
    model_df["first_purchase_date"]
)

model_df["last_purchase_date"] = pd.to_datetime(
    model_df["last_purchase_date"]
)

# Customer lifetime
model_df["customer_lifetime_days"] = (
    model_df["last_purchase_date"]
    - model_df["first_purchase_date"]
).dt.days

print("\nChurn modeling dataset:")
print(model_df.shape)

print("\nChurn target distribution:")
print(model_df["churn"].value_counts())

print("\nChurn rate:")
print(
    f"{model_df['churn'].mean() * 100:.2f}%"
)

# Compare churned vs non-churned customers

feature_comparison = (
    model_df
    .groupby("churn")
    [
        [
            "recency",
            "frequency",
            "total_revenue",
            "total_orders",
            "total_items",
            "average_order_value",
            "customer_lifetime_days",
        ]
    ]
    .mean()
    .round(2)
)

print("\nFeature comparison: churned vs non-churned")
print(feature_comparison)

# Churn prediction model

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
)

features = [
    "recency",
    "frequency",
    "total_revenue",
    "total_items",
    "average_order_value",
    "customer_lifetime_days",
]

X = model_df[features]
y = model_df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression(
    random_state=42,
    max_iter=1000,
)

model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
y_probability = model.predict_proba(X_test_scaled)[:, 1]

print("\nChurn model results:")

print("\nClassification report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Not Churned", "Churned"],
    )
)

print("\nConfusion matrix:")
print(confusion_matrix(y_test, y_pred))

print(
    f"\nROC-AUC: {roc_auc_score(y_test, y_probability):.4f}"
)

# Time-based churn prediction dataset

CUTOFF_DATE = pd.Timestamp("2011-09-30")
PREDICTION_END = pd.Timestamp("2011-11-29")

historical = df[
    df["invoicedate"] <= CUTOFF_DATE
].copy()

future = df[
    (df["invoicedate"] > CUTOFF_DATE)
    & (df["invoicedate"] <= PREDICTION_END)
].copy()


# Historical customer features

historical_features = (
    historical
    .groupby("customerid")
    .agg(
        historical_orders=("invoiceno", "nunique"),
        historical_items=("quantity", "sum"),
        historical_revenue=("revenue", "sum"),
        first_purchase=("invoicedate", "min"),
        last_purchase=("invoicedate", "max"),
    )
    .reset_index()
)

historical_features["historical_recency"] = (
    CUTOFF_DATE
    - historical_features["last_purchase"]
).dt.days

historical_features["historical_aov"] = (
    historical_features["historical_revenue"]
    / historical_features["historical_orders"]
)

historical_features["historical_lifetime_days"] = (
    historical_features["last_purchase"]
    - historical_features["first_purchase"]
).dt.days


# Future customer activity

future_activity = (
    future
    .groupby("customerid")
    .agg(
        future_orders=("invoiceno", "nunique"),
        future_revenue=("revenue", "sum"),
    )
    .reset_index()
)


# Create target

model_temporal = historical_features.merge(
    future_activity,
    on="customerid",
    how="left",
)

model_temporal["future_orders"] = (
    model_temporal["future_orders"]
    .fillna(0)
)

model_temporal["future_revenue"] = (
    model_temporal["future_revenue"]
    .fillna(0)
)

model_temporal["future_churn"] = (
    model_temporal["future_orders"] == 0
).astype(int)


print("\nTime-based churn dataset:")
print(model_temporal.shape)

print("\nFuture churn distribution:")
print(
    model_temporal["future_churn"]
    .value_counts()
)

print("\nFuture churn rate:")
print(
    f"{model_temporal['future_churn'].mean() * 100:.2f}%"
)

# Leakage-free churn prediction model

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
)

model_features = [
    "historical_recency",
    "historical_orders",
    "historical_items",
    "historical_revenue",
    "historical_aov",
    "historical_lifetime_days",
]

X = model_temporal[model_features]
y = model_temporal["future_churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

temporal_model = LogisticRegression(
    random_state=42,
    max_iter=1000,
)

temporal_model.fit(
    X_train_scaled,
    y_train,
)

y_pred = temporal_model.predict(X_test_scaled)

y_probability = temporal_model.predict_proba(
    X_test_scaled
)[:, 1]

print("\nLeakage-free churn model results:")

print("\nClassification report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Retained",
            "Future Churn",
        ],
    )
)

print("\nConfusion matrix:")
print(
    confusion_matrix(
        y_test,
        y_pred,
    )
)

print(
    f"\nROC-AUC: "
    f"{roc_auc_score(y_test, y_probability):.4f}"
)

# Model feature importance

feature_importance = pd.DataFrame({
    "feature": model_features,
    "coefficient": temporal_model.coef_[0],
})

feature_importance["abs_coefficient"] = (
    feature_importance["coefficient"].abs()
)

feature_importance = (
    feature_importance
    .sort_values("abs_coefficient", ascending=False)
)

print("\nLogistic regression feature importance:")
print(
    feature_importance[
        ["feature", "coefficient"]
    ].to_string(index=False)
)

# Random Forest churn model

from sklearn.ensemble import RandomForestClassifier

rf_model = RandomForestClassifier(
    n_estimators=300,
    max_depth=8,
    min_samples_leaf=10,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1,
)

rf_model.fit(
    X_train,
    y_train,
)

rf_pred = rf_model.predict(X_test)

rf_probability = rf_model.predict_proba(
    X_test
)[:, 1]

print("\nRandom Forest churn model:")

print("\nClassification report:")
print(
    classification_report(
        y_test,
        rf_pred,
        target_names=[
            "Retained",
            "Future Churn",
        ],
    )
)

print("\nConfusion matrix:")
print(
    confusion_matrix(
        y_test,
        rf_pred,
    )
)

print(
    f"\nROC-AUC: "
    f"{roc_auc_score(y_test, rf_probability):.4f}"
)

# Churn threshold analysis

from sklearn.metrics import precision_score, recall_score, f1_score

threshold_results = []

for threshold in [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]:

    threshold_pred = (
        y_probability >= threshold
    ).astype(int)

    threshold_results.append({
        "threshold": threshold,
        "precision": precision_score(
            y_test,
            threshold_pred,
            zero_division=0,
        ),
        "recall": recall_score(
            y_test,
            threshold_pred,
            zero_division=0,
        ),
        "f1": f1_score(
            y_test,
            threshold_pred,
            zero_division=0,
        ),
    })

threshold_df = pd.DataFrame(threshold_results)

print("\nChurn threshold analysis:")
print(
    threshold_df.round(3).to_string(index=False)
)

# Customer retention scoring

X_all_scaled = scaler.transform(
    model_temporal[model_features]
    .fillna(0)
)

model_temporal["churn_probability"] = (
    temporal_model.predict_proba(
        X_all_scaled
    )[:, 1]
)

model_temporal["risk_level"] = pd.cut(
    model_temporal["churn_probability"],
    bins=[-float("inf"), 0.30, 0.40, 0.60, float("inf")],
    labels=[
        "Low Risk",
        "Moderate Risk",
        "High Risk",
        "Critical Risk",
    ],
)

print("\nRetention risk distribution:")
print(
    model_temporal["risk_level"]
    .value_counts()
    .sort_index()
)

print("\nTop 20 highest-risk customers:")
print(
    model_temporal[
        [
            "customerid",
            "historical_recency",
            "historical_orders",
            "historical_revenue",
            "churn_probability",
            "risk_level",
        ]
    ]
    .sort_values(
        "churn_probability",
        ascending=False,
    )
    .head(20)
    .to_string(index=False)
)

# Business-aware retention opportunity score

model_temporal["retention_opportunity_score"] = (
    model_temporal["churn_probability"]
    * model_temporal["historical_revenue"]
)

print("\nTop retention opportunities:")

print(
    model_temporal[
        [
            "customerid",
            "historical_recency",
            "historical_orders",
            "historical_revenue",
            "churn_probability",
            "retention_opportunity_score",
            "risk_level",
        ]
    ]
    .sort_values(
        "retention_opportunity_score",
        ascending=False,
    )
    .head(20)
    .to_string(index=False)
)

# Retention priority classification

def assign_priority(row):
    if row["churn_probability"] >= 0.40:
        if row["historical_revenue"] >= 5000:
            return "High Value - High Risk"
        else:
            return "Standard Retention"

    if row["historical_revenue"] >= 5000:
        return "High Value - Low Risk"

    return "Monitor"


model_temporal["retention_priority"] = (
    model_temporal.apply(
        assign_priority,
        axis=1,
    )
)

print("\nRetention priority distribution:")

print(
    model_temporal["retention_priority"]
    .value_counts()
)

# Export retention scoring dataset

scored_columns = [
    "customerid",
    "historical_recency",
    "historical_orders",
    "historical_items",
    "historical_revenue",
    "historical_aov",
    "historical_lifetime_days",
    "churn_probability",
    "risk_level",
    "retention_opportunity_score",
    "retention_priority",
    "future_churn",
]

retention_scoring = model_temporal[scored_columns].copy()

RETENTION_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "retention_scoring.csv"
)

retention_scoring.to_csv(
    RETENTION_PATH,
    index=False,
)

print("\nSaved retention scoring dataset:")
print(RETENTION_PATH)

print("\nRetention scoring shape:")
print(retention_scoring.shape)

# Model evaluation summary

from sklearn.metrics import accuracy_score

evaluation_summary = pd.DataFrame({
    "model": [
        "Logistic Regression",
        "Random Forest",
    ],
    "accuracy": [
        accuracy_score(y_test, y_pred),
        accuracy_score(y_test, rf_pred),
    ],
    "roc_auc": [
        roc_auc_score(y_test, y_probability),
        roc_auc_score(y_test, rf_probability),
    ],
})

EVALUATION_PATH = (
    PROJECT_ROOT
    / "reports"
    / "model_evaluation.csv"
)

evaluation_summary.to_csv(
    EVALUATION_PATH,
    index=False,
)

print("\nModel evaluation summary:")
print(evaluation_summary.round(4).to_string(index=False))

print(
    f"\nSaved model evaluation to: "
    f"{EVALUATION_PATH}"
)