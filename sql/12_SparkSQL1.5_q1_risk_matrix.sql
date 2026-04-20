-- Categorizing loans into a 2x2 risk matrix for interaction analysis
CREATE OR REPLACE TEMP VIEW q1_risk AS
SELECT
    loan_identifier,
    property_state,
    debt_to_income,
    original_cltv,
    delinquency_status,
    -- Binary flags for risk indicators
    CASE WHEN debt_to_income > 43 THEN 1 ELSE 0 END AS high_dti,
    CASE WHEN original_cltv  > 80 THEN 1 ELSE 0 END AS high_cltv,
    -- Stratification into 4 distinct risk groups
    CASE
        WHEN debt_to_income <= 43 AND original_cltv <= 80
            THEN 'Low DTI & Low CLTV'
        WHEN debt_to_income <= 43 AND original_cltv >  80
            THEN 'Low DTI & High CLTV'
        WHEN debt_to_income >  43 AND original_cltv <= 80
            THEN 'High DTI & Low CLTV'
        WHEN debt_to_income >  43 AND original_cltv >  80
            THEN 'High DTI & High CLTV'
    END AS risk_group,
    -- Identifying Serious Delinquency (90+ Days)
    CASE WHEN delinquency_status >= 3 THEN 1 ELSE 0 END AS is_90plus_delinquent
FROM cleaned
WHERE debt_to_income IS NOT NULL
  AND original_cltv  IS NOT NULL
  AND delinquency_status IS NOT NULL;
