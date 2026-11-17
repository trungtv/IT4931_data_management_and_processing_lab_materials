"""Đọc lại message khi consumer đóng trước commit. Replication factor của topic là 1."""

from __future__ import annotations

import json
import uuid

from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic

BOOTSTRAP = "localhost:9092"


def consume_once(topic: str, group: str, max_records: int, commit: bool) -> list[int]:
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=BOOTSTRAP,
        group_id=group,
        enable_auto_commit=False,
        auto_offset_reset="earliest",
        consumer_timeout_ms=8000,
        value_deserializer=lambda raw: json.loads(raw.decode("utf-8")),
    )
    seen: list[int] = []
    for record in consumer:
        seen.append(record.value["n"])
        if len(seen) >= max_records:
            break
    if commit and seen:
        consumer.commit()
    consumer.close()
    return seen


def run() -> tuple[list[int], list[int]]:
    topic = "offset-drill-" + uuid.uuid4().hex[:8]
    group = "drill-" + uuid.uuid4().hex[:8]
    admin = KafkaAdminClient(bootstrap_servers=BOOTSTRAP)
    admin.create_topics([NewTopic(name=topic, num_partitions=1, replication_factor=1)])
    admin.close()
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    )
    for number in range(6):
        producer.send(topic, {"n": number})
    producer.flush()
    producer.close()
    first = consume_once(topic, group, max_records=3, commit=False)
    second = consume_once(topic, group, max_records=3, commit=True)
    if first != second or first != [0, 1, 2]:
        raise AssertionError((first, second))
    return first, second


if __name__ == "__main__":
    print(run())
