SELECT
  DATE_TRUNC(DATE(start_date_local), MONTH) AS month,
  round(AVG(weighted_average_watts)) AS avg_power
FROM `project-bedff666-ec4c-42c0-ba7.strava.activities_v1`
WHERE weighted_average_watts IS NOT NULL
GROUP BY month
ORDER BY month