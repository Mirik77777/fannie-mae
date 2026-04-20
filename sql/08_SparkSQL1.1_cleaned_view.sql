-- Create cleaned view with proper type casting and data quality filters
-- All columns from Parquet are STRING (inherited from CSV)
-- Numeric fields are cast to DOUBLE or INT
-- Delinquency status uses regex to filter valid numeric codes before casting
-- Records with null loan identifiers or anomalous loan_age (-1) are excluded
CREATE OR REPLACE TEMP VIEW cleaned AS
SELECT
    loan_identifier,
    monthly_reporting_period,
    channel,
    seller_name,
    servicer_name,
    property_state,
    loan_purpose,
    origination_date,
    modification_flag,
    zero_balance_code,
    CAST(original_interest_rate AS DOUBLE)  AS original_interest_rate,
    CAST(current_interest_rate  AS DOUBLE)  AS current_interest_rate,
    CAST(original_upb           AS DOUBLE)  AS original_upb,
    CAST(current_actual_upb     AS DOUBLE)  AS current_actual_upb,
    CAST(original_loan_term     AS INT)     AS original_loan_term,
    CAST(loan_age               AS INT)     AS loan_age,
    CAST(original_ltv           AS DOUBLE)  AS original_ltv,
    CAST(original_cltv          AS DOUBLE)  AS original_cltv,
    CAST(debt_to_income         AS DOUBLE)  AS debt_to_income,
    CAST(borrower_credit_score  AS INT)     AS borrower_credit_score,
    CASE
        WHEN TRIM(current_loan_delinquency_status) RLIKE '^[0-9]+$'
        THEN CAST(TRIM(current_loan_delinquency_status) AS INT)
        ELSE NULL
    END AS delinquency_status
FROM raw_fannie
WHERE loan_identifier IS NOT NULL
  AND TRIM(loan_identifier) <> ''
  AND (CAST(loan_age AS INT) >= 0 OR loan_age IS NULL)
SELECT COUNT(*) AS cleaned_records FROM cleaned;
