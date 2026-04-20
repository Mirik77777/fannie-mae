-- Cure speed analysis: average duration of delinquency episodes that were cured
-- Uses window functions to identify episode starts, assign episode IDs,
-- measure duration, and filter to episodes that eventually returned to current status
-- Minimum 100 cured episodes required for inclusion
WITH flagged AS (
    SELECT
        loan_identifier,
        monthly_reporting_period,
        servicer_name,
        delinquency_status,
        LAG(delinquency_status, 1)
            OVER (PARTITION BY loan_identifier
                  ORDER BY monthly_reporting_period) AS prev_status
    FROM cleaned_q2
),
episode_starts AS (
    SELECT *,
        CASE WHEN delinquency_status >= 1
              AND (prev_status IS NULL OR prev_status = 0)
             THEN 1 ELSE 0
        END AS is_episode_start
    FROM flagged
),
with_episode_id AS (
    SELECT *,
        SUM(is_episode_start)
            OVER (PARTITION BY loan_identifier
                  ORDER BY monthly_reporting_period
                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
            AS episode_id
    FROM episode_starts
),
episode_summary AS (
    SELECT
        loan_identifier,
        episode_id,
        servicer_name,
        COUNT(*) AS duration_months,
        MAX(delinquency_status) AS max_severity
    FROM with_episode_id
    WHERE delinquency_status >= 1
    GROUP BY loan_identifier, episode_id, servicer_name
),
cured_episodes AS (
    SELECT DISTINCT w1.loan_identifier, w1.episode_id
    FROM with_episode_id w1
    INNER JOIN flagged w2
      ON  w2.loan_identifier = w1.loan_identifier
      AND w2.monthly_reporting_period > w1.monthly_reporting_period
      AND w2.delinquency_status = 0
    WHERE w1.delinquency_status >= 1
)
SELECT
    e.servicer_name,
    COUNT(*) AS cured_episodes,
    ROUND(AVG(e.duration_months), 2) AS avg_months_to_cure,
    PERCENTILE_APPROX(e.duration_months, 0.5) AS median_months_to_cure,
    ROUND(AVG(e.max_severity), 2) AS avg_max_severity
FROM episode_summary e
INNER JOIN cured_episodes c
  ON e.loan_identifier = c.loan_identifier
 AND e.episode_id = c.episode_id
GROUP BY e.servicer_name
HAVING COUNT(*) >= 100
ORDER BY avg_months_to_cure ASC;
