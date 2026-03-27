SELECT
  DATE_TRUNC(DATE(start_date_local), MONTH) AS month,
  round(AVG(kudos_count)) AS avg_kudos
FROM `project-bedff666-ec4c-42c0-ba7.strava.activities_v1`
GROUP BY month
ORDER BY month