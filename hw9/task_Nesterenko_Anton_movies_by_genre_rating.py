"""hw9 movies_by_genre"""
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    explode,
    expr,
    mean,
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

rating_df = (
    spark.read.format("csv")
    .options(header=True, inferSchema=True, sep=",")
    .load("hdfs:///data/movielens/ratings.csv")
)

rating_df = rating_df.groupBy("movieId").agg(mean("rating").alias("rating"))

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
df = df.alias("l").join(
    rating_df.alias("r"),
    on="movieId",
    how="inner"
).select(
    col("l.movieId").alias("movieid"),
    col("l.title").alias("title"),
    col("l.year").alias("year"),
    col("l.genres").alias("genres"),
    col("r.rating").alias("rating"),
)
df = df.withColumn("genre", explode("genres"))
df = df.select(col("genre"), col("year"), col("movieid"), col("rating"), col("title"))

(
    df.write.format("org.apache.spark.sql.cassandra")
    .options(table="movies_by_genre_rating", keyspace=keyspace)
    .mode("append")
    .save()
)
