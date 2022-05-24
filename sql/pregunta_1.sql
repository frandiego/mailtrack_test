WITH months AS (
  SELECT 
    TO_CHAR(time, 'yyyy-MM') AS yearmonth 
  FROM 
    generate_series(
      '2021-01-01', '2021-12-31' :: date, 
      '1 month'
    ) AS time
), 
user_connections AS (
  SELECT 
    TO_CHAR(timestamp, 'yyyy-MM') AS yearmonth, 
    user_id, 
    COUNT(*) AS n_connections 
  FROM 
    user_connections 
  GROUP BY 
    yearmonth, 
    user_id 
  HAVING 
    COUNT(*) >= 2
), 
active_users AS (
  SELECT 
    yearmonth, 
    COUNT(
      DISTINCT(user_id)
    ) as active_users 
  FROM 
    user_connections 
  GROUP BY 
    yearmonth
) 
SELECT 
  l.yearmonth, 
  CASE WHEN r.active_users IS NOT NULL THEN r.active_users ELSE 0 END AS active_users 
FROM 
  months AS l 
  LEFT JOIN active_users AS r USING(yearmonth) 
ORDER BY 
  yearmonth DESC
