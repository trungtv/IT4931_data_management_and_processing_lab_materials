"""Spark đọc message từ một topic Kafka mới. Không dùng checkpoint bronze."""

from __future__ import annotations

import json
import uuid

from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

BOOTSTRAP = "kafka:29092"
PACKAGES = "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0"


def run() -> list[str]:
    topic = "spark-read-" + uuid.uuid4().hex[:8]
    admin = KafkaAdminClient(bootstrap_servers=BOOTSTRAP)
    admin.create_topics([NewTopic(name=topic, num_partitions=1, replication_factor=1)])
    admin.close()
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    )
    for trade in ({"trade_id": "T1", "symbol": "FPT"}, {"trade_id": "T2", "symbol": "VNM"}):
        producer.send(topic, trade)
    producer.flush()
    producer.close()
    spark = (
        SparkSession.builder.appName("spark-read-kafka")
        .master("local[1]")
        .config("spark.jars.packages", PACKAGES)
        .getOrCreate()
    )
    try:
        rows = (
            spark.read.format("kafka")
            .option("kafka.bootstrap.servers", BOOTSTRAP)
            .option("subscribe", topic)
            .option("startingOffsets", "earliest")
            .option("endingOffsets", "latest")
            .load()
            .select(col("value").cast("string").alias("value"))
            .collect()
        )
    finally:
        spark.stop()
    values = [row.value for row in rows]
    if sorted(values) != sorted(
        [json.dumps({"trade_id": "T1", "symbol": "FPT"}), json.dumps({"trade_id": "T2", "symbol": "VNM"})]
    ):
        raise AssertionError(values)
    return values


if __name__ == "__main__":
    print(run())
