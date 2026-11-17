import os


def kafka_bootstrap() -> str:
    return os.environ.get("KAFKA_BOOTSTRAP", "kafka:29092")


def minio_endpoint() -> str:
    return os.environ.get("MINIO_ENDPOINT", "http://minio:9000")


def minio_access_key() -> str:
    return os.environ.get("MINIO_ACCESS_KEY", "minioadmin")


def minio_secret_key() -> str:
    return os.environ.get("MINIO_SECRET_KEY", "minioadmin")


def spark_master() -> str:
    return os.environ.get("SPARK_MASTER", "local[*]")


TOPIC = "trades"
WAREHOUSE = "s3a://warehouse/iceberg"
BRONZE_LOCATION = "s3a://warehouse/iceberg/lab/bronze_trades"
SILVER_LOCATION = "s3a://warehouse/iceberg/lab/silver_trades"
GOLD_LOCATION = "s3a://warehouse/iceberg/lab/gold_symbol_stats"
BRONZE_CHECKPOINT = "s3a://warehouse/checkpoints/bronze"
SILVER_STREAM_CHECKPOINT = "s3a://warehouse/checkpoints/silver_stream"
ICEBERG_PACKAGES = ",".join(
    [
        "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.6.1",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0",
        "org.apache.hadoop:hadoop-aws:3.3.4",
        "com.amazonaws:aws-java-sdk-bundle:1.12.262",
    ]
)
