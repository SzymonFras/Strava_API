SELECT
  DATE_TRUNC(DATE(start_date_local), MONTH) AS month,
  round(AVG(kudos_count)) AS avg_kudos
FROM `{project_id}.dataset.table_main`
GROUP BY month
ORDER BY month