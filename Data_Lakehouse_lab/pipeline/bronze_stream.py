"""Đọc Kafka và ghi nguyên bản vào Iceberg bronze. Query dừng khi hết dữ liệu đang có."""

from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StringType, StructField, StructType

from session import build_spark, ensure_namespace
from settings import BRONZE_CHECKPOINT, BRONZE_LOCATION, TOPIC, kafka_bootstrap

RAW_SCHEMA = StructType(
    [
        StructField("trade_id", StringType()),
        StructField("symbol", StringType()),
        StructField("side", StringType()),
        StructField("price", StringType()),
        StructField("quantity", StringType()),
        StructField("event_time", StringType()),
    ]
)


def ensure_bronze(spark) -> None:
    ensure_namespace(spark)
    spark.sql(
        f"""
        CREATE TABLE IF NOT EXISTS lake.lab.bronze_trades (
            trade_id string,
            symbol string,
            side string,
            price string,
            quantity string,
            event_time string
        ) USING iceberg
        LOCATION '{BRONZE_LOCATION}'
        """
    )


def main() -> None:
    spark = build_spark("bronze-trades")
    ensure_bronze(spark)
    parsed = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", kafka_bootstrap())
        .option("subscribe", TOPIC)
        .option("startingOffsets", "earliest")
        .load()
        .select(from_json(col("value").cast("string"), RAW_SCHEMA).alias("trade"))
        .select("trade.*")
    )

    def write_batch(batch_df, epoch_id) -> None:
        count = batch_df.count()
        print(f"bronze epoch {epoch_id}: {count} dòng")
        if count == 0:
            return
        batch_df.write.format("iceberg").mode("append").save("lake.lab.bronze_trades")

    query = (
        parsed.writeStream.foreachBatch(write_batch)
        .option("checkpointLocation", BRONZE_CHECKPOINT)
        .trigger(availableNow=True)
        .start()
    )
    query.awaitTermination()
    count = spark.table("lake.lab.bronze_trades").count()
    print(f"bronze_trades: {count} dòng")
    spark.stop()


if __name__ == "__main__":
    main()
