"""Áp clean_trades cho batch (đọc bronze) và cho stream (đọc Kafka), ghi cùng bảng silver."""

import argparse

from pyspark.sql.functions import col, from_json
from pyspark.sql.types import DoubleType, LongType, StringType, StructField, StructType, TimestampType

from bronze_stream import RAW_SCHEMA
from session import build_spark, ensure_namespace
from settings import SILVER_LOCATION, SILVER_STREAM_CHECKPOINT, TOPIC, kafka_bootstrap
from transforms import clean_trades

SILVER_SCHEMA = StructType(
    [
        StructField("trade_id", StringType()),
        StructField("symbol", StringType()),
        StructField("side", StringType()),
        StructField("price", DoubleType()),
        StructField("quantity", LongType()),
        StructField("event_time", TimestampType()),
    ]
)


def ensure_silver(spark) -> None:
    ensure_namespace(spark)
    spark.sql(
        f"""
        CREATE TABLE IF NOT EXISTS lake.lab.silver_trades (
            trade_id string,
            symbol string,
            side string,
            price double,
            quantity bigint,
            event_time timestamp
        ) USING iceberg
        LOCATION '{SILVER_LOCATION}'
        """
    )


def write_silver(spark_df, mode: str) -> None:
    cleaned = clean_trades(spark_df.toPandas())
    writer = spark_df.sparkSession.createDataFrame(cleaned, schema=SILVER_SCHEMA).write
    writer.format("iceberg").mode(mode).save("lake.lab.silver_trades")


def run_batch(spark) -> None:
    ensure_silver(spark)
    bronze = spark.table("lake.lab.bronze_trades")
    write_silver(bronze, "overwrite")


def run_stream(spark) -> None:
    ensure_silver(spark)
    parsed = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", kafka_bootstrap())
        .option("subscribe", TOPIC)
        .option("startingOffsets", "earliest")
        .load()
        .select(from_json(col("value").cast("string"), RAW_SCHEMA).alias("trade"))
        .select("trade.*")
    )

    def write_batch(batch_df, _epoch_id) -> None:
        if batch_df.limit(1).count() == 0:
            return
        write_silver(batch_df, "append")

    query = (
        parsed.writeStream.foreachBatch(write_batch)
        .option("checkpointLocation", SILVER_STREAM_CHECKPOINT)
        .trigger(availableNow=True)
        .start()
    )
    query.awaitTermination()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["batch", "stream"], required=True)
    args = parser.parse_args()
    spark = build_spark(f"silver-{args.mode}")
    if args.mode == "batch":
        run_batch(spark)
    else:
        run_stream(spark)
    count = spark.table("lake.lab.silver_trades").count()
    print(f"silver_trades ({args.mode}): {count} dòng")
    spark.stop()


if __name__ == "__main__":
    main()
