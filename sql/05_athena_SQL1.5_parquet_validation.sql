-- Validate column mapping by inspecting key analytical fields
SELECT loan_identifier, servicer_name, debt_to_income,
       original_cltv, property_state, current_loan_delinquency_status
FROM individual_cw.fannie_parquet
LIMIT 10;
