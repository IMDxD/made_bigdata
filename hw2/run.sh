#!/usr/bin/env bash
set -x

input_ids_hdfs_path=/data/ids
output_hdfs_path=hw2_mr_data_ids
job_name=random
HADOOP_STREAMING_JAR=/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming.jar

hdfs dfs -rm -r $output_hdfs_path

yarn jar $HADOOP_STREAMING_JAR \
    -files mapper.py,reducer.py \
    -input $input_ids_hdfs_path \
    -output $output_hdfs_path \
    -mapper "mapper.py" \
    -numReduceTasks 2 \
    -reducer "reducer.py"

hdfs dfs -cat $output_hdfs_path/part-00000 | head -50

