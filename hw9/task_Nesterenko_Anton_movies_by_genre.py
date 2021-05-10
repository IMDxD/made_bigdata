"""hw9 movies_by_genre"""
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    explode,
    expr,
    regexp_replace,
    rtrim,
    split,
    substring,
)
from pyspark.sql.types import IntegerType

YEAR_PATTERN = r".*\(\d{4}\)$"

spark = SparkSession.builder.appName("hw9").getOrCreate()

keyspace = sys.argv[1]

df = (
    spark.read.format("csv")
    .options(header=True, inferSchema=True, sep=",")
    .load("hdfs:///data/movielens/movies.csv")
)

df = df.withColumn("title", regexp_replace(col("title"), "\xa0", ""))

df = df.withColumn("title", regexp_replace(col("title"), r"\(\D+\)$", ""))
df = df.withColumn("title", regexp_replace(col("title"), '"+', '"'))
df = df.withColumn("title", regexp_replace(col("title"), r"\)+", ")"))
df = df.withColumn("title", regexp_replace(col("title"), '^"', ""))
df = df.withColumn("title", regexp_replace(col("title"), '"$', ""))
df = df.withColumn("title", rtrim(col("title"))).filter(
    col("title").rlike(YEAR_PATTERN)
)
df = df.withColumn("year", substring(col("title"), -5, 4).cast(IntegerType()))
df = df.withColumn("title", expr("substring(title, 1, length(title)-6)"))
df = df.filter(rtrim(col("title")).rlike(".+"))
df = df.filter(col("title").isNotNull())
df = df.filter(col("genres") != "(no genres listed)")
df = df.withColumn("genres", split(df["genres"], r"\|"))
genre_df = df.withColumn("genre", explode(col("genres")))
genre_df = genre_df.select(
    col("genre"), col("year"), col("movieId").alias("movieid"), col("title")
)

(
    genre_df.write.format("org.apache.spark.sql.cassandra")
    .options(table="movies_by_genre", keyspace=keyspace)
    .mode("append")
    .save()
)
