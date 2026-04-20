spark.sql("""
CREATE OR REPLACE TEMP VIEW transitions AS
SELECT
    loan_identifier,
    monthly_reporting_period,
    servicer_name,
    delinquency_status,
    LAG(delinquency_status, 1)
        OVER (PARTITION BY loan_identifier ORDER BY monthly_reporting_period)
        AS prev_status,
    LAG(servicer_name, 1)
        OVER (PARTITION BY loan_identifier ORDER BY monthly_reporting_period)
        AS prev_servicer
FROM cleaned_q2
""")
spark.sql("SELECT COUNT(*) AS transition_records FROM transitions WHERE prev_status IS NOT NULL").show()
