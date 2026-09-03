import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Customer 360° & Churn Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    .main-title {
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 2px;
    }

    .subtitle {
        font-size: 15px;
        color: #6b7280;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 650;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    div[data-testid="stMetric"] {
    border: 1px solid #374151;
    border-radius: 10px;
    padding: 15px;
    background-color: #111827;
    }

    div[data-testid="stMetricLabel"] {
    color: #d1d5db !important;
    }

    div[data-testid="stMetricValue"] {
    color: #ffffff !important;
    }

    .insight-box {
    padding: 18px;
    border-radius: 10px;
    border: 1px solid #374151;
    background-color: #111827;
    color: #ffffff !important;
    margin-top: 10px;
    }

    .insight-box b {
    color: #ffffff !important;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    customer = pd.read_csv(
        "data/processed/customer_360.csv"
    )

    retention = pd.read_csv(
        "data/processed/retention_scoring.csv"
    )

    monthly_revenue = pd.read_csv(
    "data/processed/monthly_revenue.csv"
    )

    try:
        model = pd.read_csv(
            "reports/model_evaluation.csv"
        )
    except FileNotFoundError:
        model = pd.DataFrame()

    return customer, retention, monthly_revenue, model


customer, retention, monthly_revenue, model = load_data()


# =========================================================
# DATA CLEANING
# =========================================================

customer["first_purchase_date"] = pd.to_datetime(
    customer["first_purchase_date"],
    errors="coerce"
)

customer["last_purchase_date"] = pd.to_datetime(
    customer["last_purchase_date"],
    errors="coerce"
)

retention["churn_probability"] = pd.to_numeric(
    retention["churn_probability"],
    errors="coerce"
)

retention["historical_revenue"] = pd.to_numeric(
    retention["historical_revenue"],
    errors="coerce"
)

retention["retention_opportunity_score"] = pd.to_numeric(
    retention["retention_opportunity_score"],
    errors="coerce"
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">'
    'Customer 360° & Churn Intelligence Platform'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Customer Analytics • Churn Prediction • Retention Intelligence • Revenue Insights'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# TOP NAVIGATION
# =========================================================

pages = [
    "Executive Overview",
    "Customer & Churn",
    "Retention Intelligence",
    "ML Performance",
    "Customer Explorer"
]

page = st.radio(
    "Navigation",
    pages,
    horizontal=True,
    label_visibility="collapsed"
)

st.divider()


# =========================================================
# PAGE 1 — EXECUTIVE OVERVIEW
# =========================================================

if page == "Executive Overview":

    st.markdown(
        '<div class="section-title">Executive Overview</div>',
        unsafe_allow_html=True
    )

    total_revenue = customer["total_revenue"].sum()
    total_customers = customer["customer_id"].nunique()
    total_orders = customer["total_orders"].sum()

    churned = customer.loc[
        customer["churn_status"] == "Churned",
        "customer_id"
    ].nunique()

    at_risk = customer.loc[
        customer["churn_status"] == "At Risk",
        "customer_id"
    ].nunique()

    future_churn = retention.loc[
        retention["future_churn"] == 1,
        "customerid"
    ].nunique()

    churn_rate = churned / total_customers

    future_churn_rate = (
        future_churn /
        retention["customerid"].nunique()
    )

    revenue_at_risk = customer.loc[
        customer["churn_status"] == "At Risk",
        "total_revenue"
    ].sum()

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    c1.metric(
        "Total Revenue",
        f"£{total_revenue:,.0f}"
    )

    c2.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

    c3.metric(
        "Churn Rate",
        f"{churn_rate:.2%}"
    )

    c4.metric(
        "At Risk Customers",
        f"{at_risk:,}"
    )

    c5.metric(
        "Future Churn Rate",
        f"{future_churn_rate:.2%}"
    )

    c6.metric(
        "Revenue from At Risk",
        f"£{revenue_at_risk:,.0f}"
    )

    st.divider()

    # Monthly revenue

    monthly = monthly_revenue.copy()

    fig = px.line(
        monthly,
        x="month",
        y="revenue",
        markers=True,
        title="Monthly Revenue Trend"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (£)",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:

        churn_distribution = (
            customer["churn_status"]
            .value_counts()
            .reset_index()
        )

        churn_distribution.columns = [
            "churn_status",
            "customers"
        ]

        fig = px.pie(
            churn_distribution,
            names="churn_status",
            values="customers",
            hole=0.55,
            title="Customer Churn Status"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        risk_distribution = (
            retention["risk_level"]
            .value_counts()
            .reset_index()
        )

        risk_distribution.columns = [
            "risk_level",
            "customers"
        ]

        fig = px.bar(
            risk_distribution,
            x="risk_level",
            y="customers",
            title="Retention Risk Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# PAGE 2 — CUSTOMER & CHURN
# =========================================================

elif page == "Customer & Churn":

    st.markdown(
        '<div class="section-title">Customer & Churn Analysis</div>',
        unsafe_allow_html=True
    )

    churn_rate = (
        customer["churn_status"]
        .eq("Churned")
        .mean()
    )

    future_churn_rate = (
        retention["future_churn"]
        .mean()
    )

    revenue_at_risk = customer.loc[
        customer["churn_status"] == "At Risk",
        "total_revenue"
    ].sum()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Churn Rate",
        f"{churn_rate:.2%}"
    )

    c2.metric(
        "Revenue from At Risk",
        f"£{revenue_at_risk:,.0f}"
    )

    c3.metric(
        "Future Churn Rate",
        f"{future_churn_rate:.2%}"
    )

    st.divider()

    fig = px.scatter(
        customer,
        x="total_orders",
        y="total_revenue",
        color="churn_status",
        hover_data=[
            "customer_id",
            "average_order_value"
        ],
        title="Customer Revenue vs Order Frequency"
    )

    fig.update_layout(
        xaxis_title="Total Orders",
        yaxis_title="Total Revenue (£)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:

        risk = (
            retention
            .groupby("risk_level")
            .size()
            .reset_index(name="customers")
        )

        fig = px.bar(
            risk,
            x="risk_level",
            y="customers",
            title="Retention Risk Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        priority = (
            retention["retention_priority"]
            .value_counts()
            .reset_index()
        )

        priority.columns = [
            "retention_priority",
            "customers"
        ]

        fig = px.bar(
            priority,
            y="retention_priority",
            x="customers",
            orientation="h",
            title="Retention Priority"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# PAGE 3 — RETENTION INTELLIGENCE
# =========================================================

elif page == "Retention Intelligence":

    st.markdown(
        '<div class="section-title">'
        'Retention & Revenue Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    total_opportunity = retention[
        "retention_opportunity_score"
    ].sum()

    critical = retention.loc[
        retention["risk_level"] == "Critical Risk",
        "customerid"
    ].nunique()

    high_risk = retention.loc[
        retention["risk_level"] == "High Risk",
        "customerid"
    ].nunique()

    high_risk_opportunity = retention.loc[
        retention["risk_level"] == "High Risk",
        "retention_opportunity_score"
    ].sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Retention Opportunity",
        f"£{total_opportunity:,.0f}"
    )

    c2.metric(
        "Critical Risk Customers",
        f"{critical:,}"
    )

    c3.metric(
        "High Risk Customers",
        f"{high_risk:,}"
    )

    c4.metric(
        "High Risk Opportunity",
        f"£{high_risk_opportunity:,.0f}"
    )

    st.divider()

    opportunity = (
        retention
        .groupby("risk_level", as_index=False)
        ["retention_opportunity_score"]
        .sum()
    )

    fig = px.bar(
        opportunity,
        x="risk_level",
        y="retention_opportunity_score",
        title="Retention Opportunity by Risk Level"
    )

    fig.update_layout(
        yaxis_title="Retention Opportunity (£)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Top 15 Retention Opportunities"
    )

    top15 = (
        retention
        .sort_values(
            "retention_opportunity_score",
            ascending=False
        )
        .head(15)
        [
            [
                "customerid",
                "risk_level",
                "churn_probability",
                "historical_revenue",
                "retention_opportunity_score",
                "retention_priority"
            ]
        ]
    )

    st.dataframe(
        top15.style.format({
            "churn_probability": "{:.1%}",
            "historical_revenue": "£{:,.2f}",
            "retention_opportunity_score": "£{:,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    high_value = (
        retention[
            retention["risk_level"].isin(
                ["High Risk", "Critical Risk"]
            )
        ]
        .sort_values(
            "historical_revenue",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        high_value,
        x="historical_revenue",
        y="customerid",
        orientation="h",
        title="Top High-Value At-Risk Customers"
    )

    fig.update_layout(
        xaxis_title="Historical Revenue (£)",
        yaxis_title="Customer ID"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# PAGE 4 — ML PERFORMANCE
# =========================================================

elif page == "ML Performance":

    st.markdown(
        '<div class="section-title">ML Model Performance</div>',
        unsafe_allow_html=True
    )

    if model.empty:

        st.warning(
            "Model evaluation file was not found."
        )

    else:

        logistic = model[
            model["model"]
            .str.contains(
                "Logistic",
                case=False,
                na=False
            )
        ]

        if not logistic.empty:

            accuracy = logistic.iloc[0]["accuracy"]
            roc_auc = logistic.iloc[0]["roc_auc"]

            c1, c2 = st.columns(2)

            c1.metric(
                "Accuracy",
                f"{accuracy:.2%}"
            )

            c2.metric(
                "ROC-AUC",
                f"{roc_auc:.2%}"
            )

        st.divider()

        comparison = model.melt(
            id_vars="model",
            value_vars=[
                "accuracy",
                "roc_auc"
            ],
            var_name="metric",
            value_name="score"
        )

        comparison["metric"] = (
            comparison["metric"]
            .str.replace(
                "_",
                " ",
                regex=False
            )
            .str.title()
        )

        fig = px.bar(
            comparison,
            x="model",
            y="score",
            color="metric",
            barmode="group",
            text="score",
            title="Model Performance Comparison"
        )

        fig.update_traces(
            texttemplate="%{text:.2%}",
            textposition="outside"
        )

        fig.update_layout(
            yaxis_tickformat=".0%",
            yaxis_title="Score"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown(
            """
            <div class="insight-box">
            <b>Model Insight</b><br><br>
            Logistic Regression achieved <b>68.79% accuracy</b>
            and <b>73.54% ROC-AUC</b>, providing a strong
            baseline for identifying customers at risk of
            future churn.
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# PAGE 5 — CUSTOMER EXPLORER
# =========================================================

elif page == "Customer Explorer":

    st.markdown(
        '<div class="section-title">Customer Explorer</div>',
        unsafe_allow_html=True
    )

    customer_ids = sorted(
        customer["customer_id"]
        .dropna()
        .unique()
    )

    selected_customer = st.selectbox(
        "Select Customer",
        customer_ids
    )

    customer_row = customer[
        customer["customer_id"] == selected_customer
    ]

    retention_row = retention[
        retention["customerid"] == selected_customer
    ]

    if not customer_row.empty:

        row = customer_row.iloc[0]

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Total Revenue",
            f"£{row['total_revenue']:,.2f}"
        )

        c2.metric(
            "Total Orders",
            f"{row['total_orders']:,}"
        )

        c3.metric(
            "Average Order Value",
            f"£{row['average_order_value']:,.2f}"
        )

        c4.metric(
            "Recency",
            f"{row['recency']} days"
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Customer Status")

            st.write(
                f"**Churn Status:** "
                f"{row['churn_status']}"
            )

            st.write(
                f"**Country:** "
                f"{row['country']}"
            )

            st.write(
                f"**First Purchase:** "
                f"{row['first_purchase_date'].date()}"
            )

            st.write(
                f"**Last Purchase:** "
                f"{row['last_purchase_date'].date()}"
            )

        with col2:

            if not retention_row.empty:

                r = retention_row.iloc[0]

                st.subheader(
                    "Retention Intelligence"
                )

                st.write(
                    f"**Risk Level:** "
                    f"{r['risk_level']}"
                )

                st.write(
                    f"**Churn Probability:** "
                    f"{r['churn_probability']:.2%}"
                )

                st.write(
                    f"**Retention Opportunity:** "
                    f"£{r['retention_opportunity_score']:,.2f}"
                )

                st.write(
                    f"**Priority:** "
                    f"{r['retention_priority']}"
                )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Customer 360° & Churn Intelligence Platform • "
    "Python • SQL • PostgreSQL • Machine Learning • "
    "Power BI • Streamlit"
)
