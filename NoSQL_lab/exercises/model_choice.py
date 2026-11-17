"""Chọn store cho một nhu cầu truy vấn giao dịch.

Thân hàm giữa EXERCISE_START và EXERCISE_END là lời giải.
"""

from __future__ import annotations

import zlib
from dataclasses import dataclass


@dataclass(frozen=True)
class QueryNeed:
    pattern: str
    hops: int
    ttl_seconds: int | None = None


def choose_store(need: QueryNeed) -> str:
    """redis, mongodb, neo4j, hoặc trino.

    Đi qua ít nhất hai cạnh thì là đồ thị, kể cả khi người gọi ghi nhầm pattern
    document. Truy vấn liên store là Trino. Redis chỉ cho đọc điểm có TTL.
    """
    # EXERCISE_START
    if need.hops < 0:
        raise ValueError("hops phải không âm")
    if need.ttl_seconds is not None and need.ttl_seconds <= 0:
        raise ValueError("ttl_seconds phải dương")
    if need.pattern not in {"point", "document", "traverse", "federate"}:
        raise ValueError(f"pattern không hỗ trợ: {need.pattern}")
    if need.pattern == "federate":
        return "trino"
    if need.pattern == "traverse" or need.hops >= 2:
        return "neo4j"
    if need.pattern == "point" and need.ttl_seconds is not None:
        return "redis"
    if need.pattern == "document" and need.hops <= 1:
        return "mongodb"
    raise ValueError("Need không đủ để chọn store")
    # EXERCISE_END


def latest_price_key(symbol: str, shard_count: int) -> str:
    """Chia giá mới nhất theo symbol. Một key price duy nhất là hot key."""
    # EXERCISE_START
    cleaned = symbol.strip().upper()
    if not cleaned or shard_count < 1:
        raise ValueError("symbol và shard_count không hợp lệ")
    shard = zlib.crc32(cleaned.encode()) % shard_count
    return f"price:{shard}:{cleaned}"
    # EXERCISE_END
