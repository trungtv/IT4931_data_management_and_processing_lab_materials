"""Đối chiếu VWAP: hàm gold, Spark SQL local, DuckDB.

Chạy: python DuckDB_lab/lab/compare_aggregate.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import duckdb
import pandas as pd
from pyspark.sql import SparkSession


def pipeline_dir() -> Path:
    configured = os.environ.get("LAKEHOUSE_PIPELINE")
    if configured:
        folder = Path(configured)
    else:
        folder = Path(__file__).resolve().parents[2] / "Data_Lakehouse_lab" / "pipeline"
    if not folder.is_dir():
        raise RuntimeError(f"Không thấy pipeline: {folder}")
    return folder


sys.path.insert(0, str(pipeline_dir()))

from transforms import aggregate_trades


def sample_trades() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"symbol": "VNM", "price": 10.0, "quantity": 2},
            {"symbol": "VNM", "price": 20.0, "quantity": 2},
            {"symbol": "FPT", "price": 5.0, "quantity": 4},
            {"symbol": "FPT", "price": 15.0, "quantity": 4},
        ]
    )


def spark_aggregate(trades: pd.DataFrame) -> pd.DataFrame:
    spark = SparkSession.builder.appName("duckdb-compare").master("local[1]").getOrCreate()
    try:
        spark.createDataFrame(trades).createOrReplaceTempView("trades")
        return spark.sql(
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


def duckdb_aggregate(trades: pd.DataFrame) -> pd.DataFrame:
    connection = duckdb.connect()
    connection.register("trades", trades)
    return connection.sql(
        """
        SELECT symbol,
               count(*)::BIGINT AS trade_count,
               sum(quantity)::BIGINT AS total_quantity,
               sum(price * quantity) AS notional,
               sum(price * quantity) / sum(quantity) AS vwap
        FROM trades
        GROUP BY symbol
        ORDER BY symbol
        """
    ).df()


def compare(trades: pd.DataFrame | None = None) -> pd.DataFrame:
    frame = sample_trades() if trades is None else trades
    by_function = aggregate_trades(frame).sort_values("symbol").reset_index(drop=True)
    by_spark = spark_aggregate(frame).sort_values("symbol").reset_index(drop=True)
    by_duck = duckdb_aggregate(frame).sort_values("symbol").reset_index(drop=True)
    pandas_aligned = by_function.copy()
    for column in ("trade_count", "total_quantity"):
        pandas_aligned[column] = pandas_aligned[column].astype("int64")
        by_spark[column] = by_spark[column].astype("int64")
        by_duck[column] = by_duck[column].astype("int64")
    for column in ("notional", "vwap"):
        pandas_aligned[column] = pandas_aligned[column].astype("float64")
        by_spark[column] = by_spark[column].astype("float64")
        by_duck[column] = by_duck[column].astype("float64")
    pd.testing.assert_frame_equal(pandas_aligned, by_spark, check_dtype=False)
    pd.testing.assert_frame_equal(pandas_aligned, by_duck, check_dtype=False)
    return pandas_aligned


if __name__ == "__main__":
    print(compare().to_string(index=False))
