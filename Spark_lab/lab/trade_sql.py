"""VWAP bằng Spark SQL local, cùng số với aggregate_trades."""

from __future__ import annotations

import sys

import pandas as pd
from pyspark.sql import SparkSession

sys.path.insert(0, "/opt/airflow/pipeline")
from transforms import aggregate_trades


def trades() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"symbol": "FPT", "price": 22.0, "quantity": 10},
            {"symbol": "HPG", "price": 26.0, "quantity": 8},
            {"symbol": "VNM", "price": 80.0, "quantity": 5},
        ]
    )


def run() -> pd.DataFrame:
    frame = trades()
    expected = aggregate_trades(frame).sort_values("symbol").reset_index(drop=True)
    spark = SparkSession.builder.appName("trade-sql").master("local[1]").getOrCreate()
    try:
        spark.createDataFrame(frame).createOrReplaceTempView("trades")
        actual = spark.sql(
            """
            SELECT symbol,
                   count(*) AS trade_count,
                   sum(quantity) AS total_quantity,
                   sum(price * quantity) AS notional,
                   sum(price * quantity) / sum(quantity) AS vwap
            FROM trades
            GROUP BY symbol
            ORDER BY symbol
            """
        ).toPandas()
    finally:
        spark.stop()
    actual = actual.sort_values("symbol").reset_index(drop=True)
    for column in ("trade_count", "total_quantity"):
        actual[column] = actual[column].astype("int64")
    pd.testing.assert_frame_equal(
        expected[["symbol", "trade_count", "total_quantity", "vwap"]],
        actual[["symbol", "trade_count", "total_quantity", "vwap"]],
        check_dtype=False,
    )
    return actual


if __name__ == "__main__":
    print(run().to_string(index=False))
