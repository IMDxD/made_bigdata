#!/usr/bin/env bash
set -x

HADOOP_STREAMING_JAR=/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming.jar
HDFS_INPUT_DIR=$1
HDFS_OUTPUT_DIR=$2
JOB_NAME=$3

hdfs dfs -rm -r -skipTrash $HDFS_OUTPUT_DIR

( yarn jar $HADOOP_STREAMING_JAR \
        -files count_mapper.py,sum_reducer.py \
        -D mapreduce.job.name="Tag count calculate" \
        -D stream.num.map.output.key.fields=2 \
        -D stream.num.reduce.output.key.fields=2 \
        -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
        -D mapreduce.partition.keycomparator.options="-k1,1n -k2,2" \
        -D mapreduce.partition.keypartitioner.options=-k1,2 \
        -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
        -mapper 'python3 count_mapper.py' \
        -combiner 'python3 sum_reducer.py' \
        -reducer 'python3 sum_reducer.py' \
        -input $HDFS_INPUT_DIR \
        -output ${HDFS_OUTPUT_DIR}_tmp &&

yarn jar $HADOOP_STREAMING_JAR \
    -files top_reducer.py,top_mapper.py \
    -D mapreduce.job.name="Tag count highest" \
    -D stream.num.map.output.key.fields=2 \
    -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
    -D mapreduce.partition.keycomparator.options="-k1,1n -k2,2nr" \
    -mapper 'python3 top_mapper.py' \
    -reducer 'python3 top_reducer.py' \
    -numReduceTasks 1 \
    -input ${HDFS_OUTPUT_DIR}_tmp \
    -output ${HDFS_OUTPUT_DIR}
) || echo "Error happens"

hdfs dfs -rm -r -skipTrash ${HDFS_OUTPUT_DIR}_tmp

hdfs dfs -cat ${HDFS_OUTPUT_DIR}/*
