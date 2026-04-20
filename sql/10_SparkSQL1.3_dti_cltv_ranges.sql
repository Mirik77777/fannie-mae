-- Validate DTI and CLTV ranges and count high-risk populations
-- Confirms type casting worked and gives population sizes for Q1 risk groups
SELECT
    MIN(debt_to_income)  AS min_dti,
    MAX(debt_to_income)  AS max_dti,
    AVG(debt_to_income)  AS avg_dti,
    SUM(CASE WHEN debt_to_income > 43 THEN 1 ELSE 0 END) AS high_dti_count,
    MIN(original_cltv)   AS min_cltv,
    MAX(original_cltv)   AS max_cltv,
    AVG(original_cltv)   AS avg_cltv,
    SUM(CASE WHEN original_cltv > 80 THEN 1 ELSE 0 END) AS high_cltv_count
FROM cleaned;
