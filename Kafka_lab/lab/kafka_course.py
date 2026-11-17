"""Năm bài Kafka trên broker localhost:9092. Topic mới có replication factor 1."""

from __future__ import annotations

import json
import uuid
import zlib

from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic

BOOTSTRAP = "localhost:9092"


def symbol_partition(symbol: str, partition_count: int) -> int:
    """Cùng mã luôn vào một partition. Partition count phải dương."""
    cleaned = symbol.strip().upper()
    if not cleaned or partition_count < 1:
        raise ValueError("symbol và partition_count không hợp lệ")
    return zlib.crc32(cleaned.encode()) % partition_count


def _topic(prefix: str, partitions: int) -> str:
    name = f"{prefix}-{uuid.uuid4().hex[:8]}"
    admin = KafkaAdminClient(bootstrap_servers=BOOTSTRAP)
    admin.create_topics([NewTopic(name=name, num_partitions=partitions, replication_factor=1)])
    admin.close()
    return name


def _producer(**kwargs) -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        **kwargs,
    )


def _read(topic: str, group: str | None, commit: bool, limit: int) -> list[dict]:
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=BOOTSTRAP,
        group_id=group,
        enable_auto_commit=False,
        auto_offset_reset="earliest",
        consumer_timeout_ms=8000,
        value_deserializer=lambda raw: json.loads(raw.decode("utf-8")),
    )
    rows = []
    for record in consumer:
        rows.append({"partition": record.partition, **record.value})
        if len(rows) >= limit:
            break
    if commit and rows:
        consumer.commit()
    consumer.close()
    return rows


def produce_and_consume(trades: list[dict]) -> list[dict]:
    """Lab 1: producer gửi hết, consumer đọc lại đủ trade_id."""
    topic = _topic("basics", 1)
    producer = _producer()
    for trade in trades:
        producer.send(topic, trade)
    producer.flush()
    producer.close()
    seen = _read(topic, group=None, commit=False, limit=len(trades))
    if sorted(row["trade_id"] for row in seen) != sorted(trade["trade_id"] for trade in trades):
        raise AssertionError(seen)
    return seen


def group_keeps_the_commit(trades: list[dict]) -> tuple[int, int]:
    """Lab 2: một partition, consumer commit xong thì consumer sau cùng group không đọc lại."""
    topic = _topic("group", 1)
    producer = _producer()
    for trade in trades:
        producer.send(topic, trade)
    producer.flush()
    producer.close()
    group = "group-" + uuid.uuid4().hex[:8]
    first = _read(topic, group=group, commit=True, limit=len(trades))
    second = _read(topic, group=group, commit=False, limit=len(trades))
    if len(first) != len(trades) or second:
        raise AssertionError((first, second))
    return len(first), len(second)


def same_symbol_same_partition(trades: list[dict], partition_count: int) -> dict[str, int]:
    """Lab 3: partitioner theo mã. Mọi bản ghi của một mã nằm một partition."""
    topic = _topic("part", partition_count)

    def partitioner(key, all_partitions, available):
        del available
        return symbol_partition(key.decode("utf-8"), len(all_partitions))

    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP,
        key_serializer=lambda value: value.encode("utf-8"),
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        partitioner=partitioner,
    )
    for trade in trades:
        producer.send(topic, key=trade["symbol"], value=trade)
    producer.flush()
    producer.close()
    seen = _read(topic, group=None, commit=False, limit=len(trades))
    placed: dict[str, int] = {}
    for row in seen:
        symbol = row["symbol"]
        if symbol in placed and placed[symbol] != row["partition"]:
            raise AssertionError(seen)
        placed[symbol] = row["partition"]
        if placed[symbol] != symbol_partition(symbol, partition_count):
            raise AssertionError(placed)
    return placed


def notional_by_symbol(trades: list[dict]) -> dict[str, float]:
    """Lab 5: cộng price * quantity theo mã trên message đã đọc."""
    rows = produce_and_consume(trades)
    totals: dict[str, float] = {}
    for row in rows:
        totals[row["symbol"]] = totals.get(row["symbol"], 0.0) + row["price"] * row["quantity"]
    return totals
