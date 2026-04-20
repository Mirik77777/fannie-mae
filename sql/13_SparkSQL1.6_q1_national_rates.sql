-- Aggregating delinquency rates across the 2x2 risk matrix
-- This provides the national baseline for risk layering analysis
SELECT
    risk_group,
    COUNT(*)                         AS total_records,
    SUM(is_90plus_delinquent)        AS delinquent_90plus,
    ROUND(AVG(is_90plus_delinquent) * 100, 4) AS delinquency_rate_pct,
    COUNT(DISTINCT loan_identifier)  AS unique_loans
FROM q1_risk
GROUP BY risk_group
ORDER BY risk_group;
