state_multipliers = spark.sql("""
    WITH state_rates AS (
        SELECT property_state, risk_group, COUNT(*) AS n,
               AVG(is_90plus_delinquent) AS rate
        FROM q1_risk GROUP BY property_state, risk_group
    ),
    pivoted AS (
        SELECT property_state,
            MAX(CASE WHEN risk_group='Low DTI & Low CLTV' THEN rate END) AS baseline,
            MAX(CASE WHEN risk_group='High DTI & Low CLTV' THEN rate END) AS dti_only,
            MAX(CASE WHEN risk_group='Low DTI & High CLTV' THEN rate END) AS cltv_only,
            MAX(CASE WHEN risk_group='High DTI & High CLTV' THEN rate END) AS combined,
            MAX(CASE WHEN risk_group='Low DTI & Low CLTV' THEN n END) AS baseline_n,
            MAX(CASE WHEN risk_group='High DTI & High CLTV' THEN n END) AS combined_n
        FROM state_rates GROUP BY property_state
    )
    SELECT property_state,
        ROUND(baseline*100,4) AS baseline_pct,
        ROUND(dti_only*100,4) AS dti_only_pct,
        ROUND(cltv_only*100,4) AS cltv_only_pct,
        ROUND(combined*100,4) AS combined_pct,
        ROUND(combined/baseline,2) AS multiplier,
        baseline_n, combined_n
    FROM pivoted
    WHERE baseline > 0 AND combined_n >= 1000
    ORDER BY multiplier DESC
""")
state_multipliers.show(60, truncate=False)
