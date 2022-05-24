WITH rank_timestamp AS (
  SELECT 
    l.timestamp, 
    r.*, 
    rank() OVER (
      PARTITION BY r.country_id 
      ORDER BY 
        timestamp DESC
    ) 
  FROM 
    user_connections l 
    LEFT JOIN users r ON l.user_id = r.id
) 
SELECT 
  l.email, 
  r.name as country_name, 
  l.timestamp 
FROM 
  rank_timestamp l 
  LEFT JOIN countries r ON l.country_id = r.id 
WHERE 
  rank <= 10 
ORDER BY 
  country_name ASC, 
  timestamp DESC
