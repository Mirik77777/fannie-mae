-- Identify top servicers by volume to confirm servicer field is populated
-- and assess data adequacy for Q2 servicer-level analysis
SELECT servicer_name, COUNT(*) AS cnt
FROM cleaned
WHERE servicer_name IS NOT NULL AND TRIM(servicer_name) <> ''
GROUP BY servicer_name
ORDER BY cnt DESC
LIMIT 15;
