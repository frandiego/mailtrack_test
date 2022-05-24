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
country_active AS (
  SELECT 
    DISTINCT l.yearmonth, 
    r.country_id, 
    1 AS remove 
  FROM 
    user_active_connections l 
    LEFT JOIN users r ON l.user_id = r.id
), 
country_not_active AS (
  SELECT 
    l.yearmonth, 
    l.country_id, 
    trim(l.name) as name, 
    r.remove 
  FROM 
    cross_months_countries l 
    LEFT JOIN country_active r USING(country_id, yearmonth) 
  WHERE 
    remove IS NULL
) 
select 
  yearmonth, 
  STRING_AGG(
    name, 
    ',' 
    order by 
      name asc
  ) 
FROM 
  country_not_active 
GROUP BY 
  yearmonth 
ORDER BY 
  yearmonth DESC
