#!/usr/bin/env bash
set -x

HADOOP_STREAMING_JAR=/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming.jar
HDFS_OUTPUT_DIR=tag_count

hdfs dfs -rm -r -skipTrash $HDFS_OUTPUT_DIR

yarn jar $HADOOP_STREAMING_JAR \
        -files count_mapper.py,sum_reducer.py \
        -D stream.num.map.output.key.fields=2 \
        -D stream.num.reduce.output.key.fields=2 \
        -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
        -D mapreduce.partition.keycomparator.options="-k1,1n -k2,2" \
        -D mapreduce.partition.keypartitioner.options=-k1,2 \
        -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
        -mapper 'python3 count_mapper.py' \
        -combiner 'python3 sum_reducer.py' \
        -reducer 'python3 sum_reducer.py' \
        -input /data/stackexchange_part/posts \
        -output $HDFS_OUTPUT_DIR

echo $?
