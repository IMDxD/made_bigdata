set hive.auto.convert.join=false;
set mapreduce.job.reduces=8;

SELECT
    l.user_agent,
    SUM(IF(u.sex = "male", 1, 0)),
    SUM(IF(u.sex = "male", 0, 1)) FROM (
    logs as l JOIN users u ON u.ip = l.ip
    )
GROUP BY l.user_agent
LIMIT 10;