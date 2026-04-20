servicer_results = spark.sql("""
    WITH events AS (
        SELECT
            prev_servicer AS servicer,
            loan_identifier,
            CASE WHEN prev_status >= 1 THEN 1 ELSE 0 END
                AS was_delinquent,
            CASE WHEN prev_status >= 1 AND delinquency_status = 0
                 THEN 1 ELSE 0 END
                AS is_cure,
            CASE WHEN prev_status BETWEEN 1 AND 2 THEN 1 ELSE 0 END
                AS was_early_delinquent,
            CASE WHEN prev_status BETWEEN 1 AND 2
                  AND delinquency_status >= 3
                 THEN 1 ELSE 0 END
                AS is_roll
        FROM transitions
        WHERE prev_status IS NOT NULL
          AND prev_servicer IS NOT NULL
    )
    SELECT
        servicer,
        COUNT(DISTINCT loan_identifier)     AS unique_loans,
        SUM(was_delinquent)                 AS delinquent_months,
        SUM(is_cure)                        AS cure_events,
        ROUND(SUM(is_cure) * 100.0
              / SUM(was_delinquent), 2)     AS cure_rate_pct,
        SUM(was_early_delinquent)           AS early_delinq_months,
        SUM(is_roll)                        AS roll_events,
        ROUND(SUM(is_roll) * 100.0
              / NULLIF(SUM(was_early_delinquent), 0), 2)
                                            AS roll_rate_pct
    FROM events
    GROUP BY servicer
    HAVING SUM(was_delinquent) >= 1000
    ORDER BY cure_rate_pct DESC
""")
servicer_results.show(30, truncate=False)
