SELECT
  DATE_TRUNC(DATE(start_date_local), MONTH) AS month,
  round(AVG(weighted_average_watts)) AS avg_power
FROM `{project_id}.dataset.table_main`
WHERE weighted_average_watts IS NOT NULL
GROUP BY month
ORDER BY month