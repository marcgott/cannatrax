# Get current height/span of all plants
sql = "SELECT DISTINCT(plant_ID),max(height) as maxheight ,max(span) as maxspan FROM `log` group by plant_ID"

#get plant height/span history
sql = "SELECT logdate,height,span FROM `log` where plant_ID=%s"

"""
SELECT a.*
    FROM log a,
            (
                SELECT plant_ID, MAX(logdate) as logdate
                    FROM log
                 WHERE height <> 0
                 GROUP BY plant_ID
            ) b
 WHERE a.plant_ID = b.plant_ID
   AND a.logdate = b.logdate

select plant_ID,logdate,span,height FROM log WHERE (height<>0 OR span<>0) AND plant_ID=18
"""
