spark.sql("""
CREATE OR REPLACE TEMP VIEW cleaned_q2 AS
SELECT
    loan_identifier,
    monthly_reporting_period,
    delinquency_status,
    CASE
        WHEN UPPER(TRIM(servicer_name)) LIKE '%NATIONSTAR%'
        THEN 'Nationstar Mortgage LLC'
        ELSE servicer_name
    END AS servicer_name
FROM cleaned
WHERE servicer_name IS NOT NULL
  AND TRIM(servicer_name) <> ''
  AND delinquency_status IS NOT NULL
  AND monthly_reporting_period IS NOT NULL
""")
print("Q2 cleaned view created (Nationstar merged).")
