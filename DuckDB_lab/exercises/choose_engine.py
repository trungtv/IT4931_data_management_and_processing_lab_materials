"""Khi một phép aggregate của gold không cần cụm Spark.

Thân hàm giữa EXERCISE_START và EXERCISE_END là lời giải.
"""

from __future__ import annotations

LAPTOP_ROW_LIMIT = 50_000_000


def engine_for_aggregate(rows: int, concurrent_writers: int, streaming_sink: bool) -> str:
    """duckdb hoặc spark. DuckDB chỉ khi một writer, không phải sink streaming, và vừa laptop."""
    # EXERCISE_START
    if rows < 0 or concurrent_writers < 1:
        raise ValueError("rows và concurrent_writers không hợp lệ")
    if streaming_sink or concurrent_writers > 1 or rows > LAPTOP_ROW_LIMIT:
        return "spark"
    return "duckdb"
    # EXERCISE_END
