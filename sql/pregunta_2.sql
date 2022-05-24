WITH user_connections AS (
  SELECT 
    TO_CHAR(timestamp, 'yyyy-MM') AS yearmonth, 
    user_id, 
    COUNT(*) AS n_connections 
  FROM 
    user_connections 
  WHERE 
    TO_CHAR(timestamp, 'yyyy-MM') = '2021-04' 
  GROUP BY 
    yearmonth, 
    user_id 
  HAVING 
    COUNT(*) >= 2
), 
domain_connections AS (
  SELECT 
    l.yearmonth, 
    l.user_id, 
    l.n_connections, 
    split_part(r.email, '@', 2) AS domain 
  FROM 
    user_connections l 
    LEFT JOIN users r ON r.id = l.user_id
), 
domain_active_users AS (
  SELECT 
    yearmonth, 
    domain, 
    COUNT(
      DISTINCT(user_id)
    ) AS active_users 
  FROM 
    domain_connections 
  GROUP BY 
    yearmonth, 
    domain
) 
SELECT 
  * 
FROM 
  domain_active_users 
WHERE 
  active_users = (
    SELECT 
      MAX(active_users) 
    FROM 
      domain_active_users
  )
