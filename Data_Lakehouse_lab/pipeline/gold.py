"""Ghi bảng gold bằng đúng aggregate_trades đã dùng cho batch."""

from pyspark.sql.types import DoubleType, LongType, StringType, StructField, StructType

from session import build_spark, ensure_namespace
from settings import GOLD_LOCATION
from transforms import GOLD_COLUMNS, aggregate_trades

GOLD_SCHEMA = StructType(
    [
        StructField("symbol", StringType(), False),
        StructField("trade_count", LongType(), False),
        StructField("total_quantity", LongType(), False),
        StructField("notional", DoubleType(), False),
        StructField("vwap", DoubleType(), False),
    ]
)


def ensure_gold(spark) -> None:
    ensure_namespace(spark)
    spark.sql(
        f"""
        CREATE TABLE IF NOT EXISTS lake.lab.gold_symbol_stats (
            symbol string,
            trade_count bigint,
            total_quantity bigint,
            notional double,
            vwap double
        ) USING iceberg
        LOCATION '{GOLD_LOCATION}'
        """
    )


def main() -> None:
    spark = build_spark("gold-symbol-stats")
    ensure_gold(spark)
    silver = spark.table("lake.lab.silver_trades").select("symbol", "price", "quantity").toPandas()
    aggregated = aggregate_trades(silver)
    spark.createDataFrame(aggregated.loc[:, GOLD_COLUMNS], schema=GOLD_SCHEMA).write.format(
        "iceberg"
    ).mode("overwrite").save("lake.lab.gold_symbol_stats")
    count = spark.table("lake.lab.gold_symbol_stats").count()
    print(f"gold_symbol_stats: {count} dòng")
    spark.table("lake.lab.gold_symbol_stats").show(truncate=False)
    spark.stop()


if __name__ == "__main__":
    main()
