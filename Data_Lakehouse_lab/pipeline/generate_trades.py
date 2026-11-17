"""Đẩy một lô giao dịch chứng khoán, gồm cả bản ghi bẩn, vào Kafka."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic

from settings import TOPIC, kafka_bootstrap


def sample_trades(now: datetime | None = None) -> list[dict]:
    clock = now or datetime.now(timezone.utc)
    trades = []
    for index in range(30):
        trades.append(
            {
                "trade_id": f"T{index:04d}",
                "symbol": ["vnm", "fpt", "hpg"][index % 3],
                "side": "buy" if index % 2 == 0 else "sell",
                "price": 20 + (index % 5),
                "quantity": 10 * ((index % 4) + 1),
                "event_time": (clock - timedelta(minutes=index)).isoformat(),
            }
        )
    trades.extend(
        [
            {
                "trade_id": "BADNULL",
                "symbol": "VNM",
                "side": "BUY",
                "price": None,
                "quantity": 10,
                "event_time": clock.isoformat(),
            },
            {
                "trade_id": "T0001",
                "symbol": "VNM",
                "side": "BUY",
                "price": 99,
                "quantity": 1,
                "event_time": clock.isoformat(),
            },
            {
                "trade_id": "LATE",
                "symbol": "FPT",
                "side": "BUY",
                "price": 10,
                "quantity": 10,
                "event_time": (clock - timedelta(days=10)).isoformat(),
            },
            {
                "trade_id": "BADSIDE",
                "symbol": "HPG",
                "side": "HOLD",
                "price": 10,
                "quantity": 10,
                "event_time": clock.isoformat(),
            },
        ]
    )
    return trades


def ensure_topic(bootstrap: str) -> None:
    admin = KafkaAdminClient(bootstrap_servers=bootstrap)
    try:
        if TOPIC not in admin.list_topics():
            admin.create_topics([NewTopic(name=TOPIC, num_partitions=3, replication_factor=1)])
    finally:
        admin.close()


def publish(trades: list[dict], bootstrap: str | None = None) -> int:
    servers = bootstrap or kafka_bootstrap()
    ensure_topic(servers)
    producer = KafkaProducer(
        bootstrap_servers=servers,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    )
    for trade in trades:
        producer.send(TOPIC, trade)
    producer.flush()
    producer.close()
    return len(trades)


def main() -> None:
    count = publish(sample_trades())
    print(f"Đã gửi {count} giao dịch tới topic {TOPIC} ({kafka_bootstrap()})")


if __name__ == "__main__":
    main()
