-- Validate delinquency status distribution after cleaning
-- Confirms field parsed correctly and shows portfolio is dominated by performing loans
SELECT delinquency_status, COUNT(*) AS cnt
FROM cleaned
GROUP BY delinquency_status
ORDER BY delinquency_status;
