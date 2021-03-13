#!/usr/bin/env bash
set -x

input_ids_hdfs_path=/data/ids
output_hdfs_path=hw2_mr_data_ids
job_name=random
HADOOP_STREAMING_JAR=/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming.jar

hdfs dfs -rm -r $OUT_DIR

yarn jar $HADOOP_STREAMING_JAR \
    -files mapper.py, reducer.py \
    -input $input_ids_hdfs_path \
    -output $output_hdfs_path \
    -mapper "python mapper.py" \
    -numReduceTasks 2 \
    -reducer "python reducer.py" \
     > hw2_mr_data_ids.out

echo $?
