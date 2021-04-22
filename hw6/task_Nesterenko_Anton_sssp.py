"""
Made BigData hw6
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

END = 34
COUNT = 0


spark = SparkSession.builder.appName("classifier").getOrCreate()

df = (
    spark
    .read
    .format("csv")
    .options(header=False, inferSchema=True, sep="\t")
    .load("hdfs:///data/twitter/twitter.txt")
)

df = df.select(col("_c0").alias("to"), col("_c1").alias("from"))

used = {12}
get_set = {12}

while len(get_set) > 0:
    get_set = (
        df
        .filter(col("from").isin(get_set))
        .select(col("to"))
        .dropDuplicates()
        .collect()
    )
    COUNT += 1
    get_set = {t["to"] for t in get_set}
    if END in get_set:
        break
    get_set -= used
    used |= get_set

print(COUNT)
