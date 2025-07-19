FROM bitnami/spark:3

WORKDIR /jars

RUN spark-submit --packages io.delta:delta-core_2.12:2.4.0,org.apache.hadoop:hadoop-aws:3.3.4,org.elasticsearch:elasticsearch-spark-30_2.12:8.5.1
