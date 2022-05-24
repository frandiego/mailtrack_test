WITH months AS (
  SELECT 
    TO_CHAR(time, 'yyyy-MM') AS yearmonth 
  FROM 
    generate_series(
      '2021-01-01', '2021-12-31' :: date, 
      '1 month'
    ) AS time
), 
cross_months_countries AS (
  SELECT 
    yearmonth, 
    r.id as country_id, 
    r.name 
  FROM 
    months l CROSS 
    JOIN countries r
), 
user_active_connections AS (
  SELECT 
    DISTINCT TO_CHAR(timestamp, 'yyyy-MM') AS yearmonth, 
    user_id 
  FROM 
    user_connections 
  GROUP BY 
    yearmonth, 
    user_id 
  HAVING 
    COUNT(*) >= 2
), 
country_users_active AS (
  SELECT 
    l.yearmonth, 
    r.country_id, 
    COUNT(
      DISTINCT(l.user_id)
    ) as active_users 
  FROM 
    user_active_connections l 
    LEFT JOIN users r ON l.user_id = r.id 
  GROUP BY 
    l.yearmonth, 
    r.country_id
), 
country_users_active_full AS (
  SELECT 
    l.yearmonth, 
    l.country_id, 
    l.name, 
    CASE WHEN r.active_users IS NOT NULL THEN r.active_users ELSE 0 END as active_users 
  FROM 
    cross_months_countries l 
    LEFT JOIN country_users_active r USING(yearmonth, country_id) 
  ORDER BY 
    yearmonth, 
    name
), 
country_users_active_full_prev AS (
  SELECT 
    yearmonth, 
    name, 
    active_users, 
    lag(active_users) over (
      partition by name 
      order by 
        yearmonth
    ) as active_users_prev 
  FROM 
    country_users_active_full
) 
SELECT 
  yearmonth, 
  name, 
  active_users, 
  CASE WHEN active_users_prev = 0 THEN 0 
  WHEN active_users_prev IS NULL THEN NULL 
  ELSE ROUND(
    (
      active_users :: decimal - active_users_prev :: decimal
    )/ active_users_prev :: decimal * 100, 
    2
  ) END AS growth 
FROM 
  country_users_active_full_prev 
ORDER BY 
  name ASC, 
  yearmonth DESC
