-- Customer 360° & Churn Intelligence Platform
-- PostgreSQL analytical queries
--
-- Assumption:
-- The cleaned transactional table is named public.sales.
-- Adjust the table name if your PostgreSQL schema uses a different name.

-- ============================================================
-- 1. Customer 360° Summary
-- ============================================================

SELECT
    customerid AS customer_id,
    COUNT(DISTINCT invoiceno) AS total_orders,
    SUM(quantity) AS total_items,
    SUM(revenue) AS total_revenue,
    ROUND(SUM(revenue) / NULLIF(COUNT(DISTINCT invoiceno), 0), 2)
        AS average_order_value,
    MIN(invoicedate) AS first_purchase_date,
    MAX(invoicedate) AS last_purchase_date,
    CURRENT_DATE - MAX(invoicedate)::date AS recency
FROM public.sales
WHERE customerid IS NOT NULL
  AND is_valid_sale = TRUE
GROUP BY customerid
ORDER BY total_revenue DESC;


-- ============================================================
-- 2. Customer Revenue Ranking
-- ============================================================

SELECT
    customerid AS customer_id,
    SUM(revenue) AS total_revenue,
    RANK() OVER (ORDER BY SUM(revenue) DESC) AS revenue_rank
FROM public.sales
WHERE customerid IS NOT NULL
  AND is_valid_sale = TRUE
GROUP BY customerid
ORDER BY revenue_rank;


-- ============================================================
-- 3. RFM Base Metrics
-- ============================================================

WITH rfm_base AS (
    SELECT
        customerid AS customer_id,
        CURRENT_DATE - MAX(invoicedate)::date AS recency,
        COUNT(DISTINCT invoiceno) AS frequency,
        SUM(revenue) AS monetary
    FROM public.sales
    WHERE customerid IS NOT NULL
      AND is_valid_sale = TRUE
    GROUP BY customerid
)
SELECT *
FROM rfm_base
ORDER BY monetary DESC;


-- ============================================================
-- 4. RFM Scoring
-- ============================================================

WITH rfm_base AS (
    SELECT
        customerid AS customer_id,
        CURRENT_DATE - MAX(invoicedate)::date AS recency,
        COUNT(DISTINCT invoiceno) AS frequency,
        SUM(revenue) AS monetary
    FROM public.sales
    WHERE customerid IS NOT NULL
      AND is_valid_sale = TRUE
    GROUP BY customerid
),
rfm_scored AS (
    SELECT
        *,
        NTILE(5) OVER (ORDER BY recency DESC) AS recency_score,
        NTILE(5) OVER (ORDER BY frequency) AS frequency_score,
        NTILE(5) OVER (ORDER BY monetary) AS monetary_score
    FROM rfm_base
)
SELECT *
FROM rfm_scored
ORDER BY monetary DESC;


-- ============================================================
-- 5. Customer Segmentation
-- ============================================================

WITH rfm_base AS (
    SELECT
        customerid AS customer_id,
        CURRENT_DATE - MAX(invoicedate)::date AS recency,
        COUNT(DISTINCT invoiceno) AS frequency,
        SUM(revenue) AS monetary
    FROM public.sales
    WHERE customerid IS NOT NULL
      AND is_valid_sale = TRUE
    GROUP BY customerid
),
rfm_scored AS (
    SELECT
        *,
        NTILE(5) OVER (ORDER BY recency DESC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency) AS f_score,
        NTILE(5) OVER (ORDER BY monetary) AS m_score
    FROM rfm_base
)
SELECT
    *,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4
            THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3
            THEN 'Potential Loyalists'
        WHEN r_score >= 3 AND f_score >= 2
            THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2
            THEN 'New/Promising'
        WHEN r_score <= 2 AND f_score >= 3
            THEN 'At Risk'
        ELSE 'Lost Customers'
    END AS customer_segment
FROM rfm_scored;


-- ============================================================
-- 6. Revenue by Customer Segment
-- ============================================================

WITH segmented AS (
    WITH rfm_base AS (
        SELECT
            customerid AS customer_id,
            CURRENT_DATE - MAX(invoicedate)::date AS recency,
            COUNT(DISTINCT invoiceno) AS frequency,
            SUM(revenue) AS monetary
        FROM public.sales
        WHERE customerid IS NOT NULL
          AND is_valid_sale = TRUE
        GROUP BY customerid
    ),
    rfm_scored AS (
        SELECT
            *,
            NTILE(5) OVER (ORDER BY recency DESC) AS r_score,
            NTILE(5) OVER (ORDER BY frequency) AS f_score,
            NTILE(5) OVER (ORDER BY monetary) AS m_score
        FROM rfm_base
    )
    SELECT
        *,
        CASE
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4
                THEN 'Champions'
            WHEN r_score >= 3 AND f_score >= 3
                THEN 'Potential Loyalists'
            WHEN r_score >= 3 AND f_score >= 2
                THEN 'Loyal Customers'
            WHEN r_score >= 4 AND f_score <= 2
                THEN 'New/Promising'
            WHEN r_score <= 2 AND f_score >= 3
                THEN 'At Risk'
            ELSE 'Lost Customers'
        END AS customer_segment
    FROM rfm_scored
)
SELECT
    customer_segment,
    COUNT(*) AS customer_count,
    ROUND(SUM(monetary), 2) AS segment_revenue,
    ROUND(AVG(monetary), 2) AS average_customer_revenue
FROM segmented
GROUP BY customer_segment
ORDER BY segment_revenue DESC;


-- ============================================================
-- 7. Top 10% Customers by Revenue
-- ============================================================

WITH customer_revenue AS (
    SELECT
        customerid AS customer_id,
        SUM(revenue) AS total_revenue
    FROM public.sales
    WHERE customerid IS NOT NULL
      AND is_valid_sale = TRUE
    GROUP BY customerid
),
ranked AS (
    SELECT
        *,
        NTILE(10) OVER (ORDER BY total_revenue DESC) AS revenue_decile
    FROM customer_revenue
)
SELECT
    COUNT(*) AS top_10_customer_count,
    ROUND(SUM(total_revenue), 2) AS top_10_revenue,
    ROUND(
        100.0 * SUM(total_revenue)
        / NULLIF((SELECT SUM(total_revenue) FROM customer_revenue), 0),
        2
    ) AS revenue_share_percent
FROM ranked
WHERE revenue_decile = 1;


-- ============================================================
-- 8. Monthly Revenue Trend
-- ============================================================

SELECT
    DATE_TRUNC('month', invoicedate)::date AS month,
    ROUND(SUM(revenue), 2) AS monthly_revenue
FROM public.sales
WHERE is_valid_sale = TRUE
GROUP BY DATE_TRUNC('month', invoicedate)
ORDER BY month;


-- ============================================================
-- 9. Customer Churn Status Based on Recency
-- ============================================================

WITH customer_recency AS (
    SELECT
        customerid AS customer_id,
        CURRENT_DATE - MAX(invoicedate)::date AS recency
    FROM public.sales
    WHERE customerid IS NOT NULL
      AND is_valid_sale = TRUE
    GROUP BY customerid
)
SELECT
    customer_id,
    recency,
    CASE
        WHEN recency <= 60 THEN 'Active'
        WHEN recency <= 120 THEN 'At Risk'
        ELSE 'Churned'
    END AS churn_status
FROM customer_recency
ORDER BY recency DESC;


-- ============================================================
-- 10. Churn Status Distribution
-- ============================================================

WITH customer_recency AS (
    SELECT
        customerid AS customer_id,
        CURRENT_DATE - MAX(invoicedate)::date AS recency
    FROM public.sales
    WHERE customerid IS NOT NULL
      AND is_valid_sale = TRUE
    GROUP BY customerid
)
SELECT
    CASE
        WHEN recency <= 60 THEN 'Active'
        WHEN recency <= 120 THEN 'At Risk'
        ELSE 'Churned'
    END AS churn_status,
    COUNT(*) AS customer_count
FROM customer_recency
GROUP BY 1
ORDER BY customer_count DESC;
