"""Cấu hình Spark catalog Iceberg trùng capstone.

Notebook 05 để catalog trong comment và ghi JAR 1.4.0, warehouse /tmp.
Hàm này là cấu hình được dùng khi chạy.
"""

from __future__ import annotations

ICEBERG_PACKAGE = "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.6.1"
WAREHOUSE = "s3a://warehouse/iceberg"


def iceberg_configs(s3_endpoint: str) -> dict[str, str]:
    """Hadoop catalog trên MinIO. Endpoint rỗng thì dừng, không đổi sang đĩa local."""
    # EXERCISE_START
    if not s3_endpoint:
        raise ValueError("Thiếu endpoint MinIO")
    return {
        "spark.sql.catalog.lake": "org.apache.iceberg.spark.SparkCatalog",
        "spark.sql.catalog.lake.type": "hadoop",
        "spark.sql.catalog.lake.warehouse": WAREHOUSE,
        "spark.sql.catalog.lake.io-impl": "org.apache.iceberg.aws.s3.S3FileIO",
        "spark.hadoop.fs.s3a.endpoint": s3_endpoint,
        "spark.hadoop.fs.s3a.path.style.access": "true",
        "spark.hadoop.fs.s3a.connection.ssl.enabled": "false",
    }
    # EXERCISE_END
