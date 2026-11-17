from pyspark.sql import SparkSession

from settings import (
    ICEBERG_PACKAGES,
    WAREHOUSE,
    minio_access_key,
    minio_endpoint,
    minio_secret_key,
    spark_master,
)


def build_spark(app_name: str) -> SparkSession:
    return (
        SparkSession.builder.appName(app_name)
        .master(spark_master())
        .config("spark.jars.packages", ICEBERG_PACKAGES)
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
        .config("spark.sql.catalog.lake", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.lake.type", "hadoop")
        .config("spark.sql.catalog.lake.warehouse", WAREHOUSE)
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.hadoop.fs.s3a.endpoint", minio_endpoint())
        .config("spark.hadoop.fs.s3a.access.key", minio_access_key())
        .config("spark.hadoop.fs.s3a.secret.key", minio_secret_key())
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .config(
            "spark.hadoop.fs.s3a.aws.credentials.provider",
            "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
        )
        .getOrCreate()
    )


def ensure_namespace(spark: SparkSession) -> None:
    spark.sql("CREATE NAMESPACE IF NOT EXISTS lake.lab")
