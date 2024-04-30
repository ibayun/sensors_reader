def exctract_data_query(*, interval, start_date, end_date):
  return  f"""
SELECT
    trunc(avg(t), 2) AS avg_temp,
    trunc(max(t), 2) as max_temp,
    trunc(min(t), 2) as min_temp,
    
    trunc(avg(moist), 2) AS avg_moist,
    trunc(max(moist), 2) as max_moist,
    trunc(min(moist), 2) as min_moist,

    trunc(avg(gray), 2) AS avg_gray,
    trunc(max(gray), 2) as max_gray,
    trunc(min(gray), 2) as min_gray,

    trunc(avg(co2), 2) AS avg_co2,
    trunc(max(co2), 2) as max_co2,
    trunc(min(co2), 2) as min_co2,

    toStartOfInterval(tm, toIntervalMinute({interval})) aS h
FROM
(
    SELECT
        toFloat32OrNull(datas.temperature) AS t,
        toFloat32OrNull(datas.moisture) AS moist,
        toFloat32OrNull(datas.gray) AS gray,
        toFloat32OrNull(datas.co2) AS co2,
        timestamp AS tm
    FROM device_data
    WHERE t IS NOT NULL
)
WHERE date(tm) between '{start_date}' and '{end_date}'
GROUP BY h
ORDER BY h ASC

""" 
