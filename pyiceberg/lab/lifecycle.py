"""Mỗi bài Iceberg tự tạo bảng trên MinIO rồi làm đúng một việc."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pyarrow as pa
from pyiceberg.catalog import load_catalog
from pyiceberg.partitioning import PartitionField, PartitionSpec
from pyiceberg.schema import Schema
from pyiceberg.transforms import IdentityTransform
from pyiceberg.types import DoubleType, LongType, NestedField, StringType

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
from plan import plan_compaction, snapshot_as_of

BASE_SCHEMA = Schema(
    NestedField(1, "trade_id", StringType(), required=True),
    NestedField(2, "symbol", StringType(), required=True),
    NestedField(3, "price", DoubleType(), required=True),
)


def catalog():
    return load_catalog(
        "lifecycle",
        **{
            "type": "sql",
            "uri": "sqlite:////tmp/it4931_pyiceberg_lifecycle.db",
            "warehouse": "s3://warehouse/pyiceberg/lifecycle",
            "s3.endpoint": "http://localhost:9000",
            "s3.access-key-id": "minioadmin",
            "s3.secret-access-key": "minioadmin",
            "s3.path-style-access": "true",
        },
    )


def _ice():
    ice = catalog()
    if "labcheck" not in {item[0] for item in ice.list_namespaces()}:
        ice.create_namespace("labcheck")
    return ice


def _replace(ice, name: str, partition_spec: PartitionSpec | None = None):
    identifier = f"labcheck.{name}"
    if ice.table_exists(identifier):
        ice.drop_table(identifier)
    kwargs = {"schema": BASE_SCHEMA}
    if partition_spec is not None:
        kwargs["partition_spec"] = partition_spec
    return ice.create_table(identifier, **kwargs)


def _arrow(rows: dict) -> pa.Table:
    fields = []
    for name, values in rows.items():
        kind = pa.float64() if isinstance(values[0], float) else pa.string()
        if isinstance(values[0], int) and not isinstance(values[0], bool):
            kind = pa.int64()
        fields.append(pa.field(name, kind, nullable=name == "quantity"))
    return pa.table(rows, schema=pa.schema(fields))


def _snapshots(table):
    found = []
    for snapshot in table.snapshots():
        committed = datetime.fromtimestamp(snapshot.timestamp_ms / 1000, tz=timezone.utc)
        found.append((snapshot.snapshot_id, committed))
    return found


def create_one_row() -> int:
    """Tạo bảng và đọc lại một dòng từ MinIO."""
    ice = _ice()
    table = _replace(ice, "created")
    table.append(_arrow({"trade_id": ["T1"], "symbol": ["FPT"], "price": [22.0]}))
    count = ice.load_table("labcheck.created").scan().to_arrow().num_rows
    if count != 1:
        raise AssertionError(count)
    return count


def partition_by_symbol() -> list[str]:
    """Hai mã thành hai file, path chứa symbol=."""
    ice = _ice()
    table = _replace(
        ice,
        "partitioned",
        PartitionSpec(PartitionField(source_id=2, field_id=1000, transform=IdentityTransform(), name="symbol")),
    )
    table.append(_arrow({"trade_id": ["T1"], "symbol": ["FPT"], "price": [22.0]}))
    table.append(_arrow({"trade_id": ["T2"], "symbol": ["VNM"], "price": [80.0]}))
    paths = [row["file_path"] for row in ice.load_table("labcheck.partitioned").inspect.files().to_pylist()]
    if not any("symbol=FPT" in path for path in paths) or not any("symbol=VNM" in path for path in paths):
        raise AssertionError(paths)
    return paths


def add_quantity_column() -> dict:
    """Thêm cột sau snapshot đầu. Snapshot cũ vẫn một dòng."""
    ice = _ice()
    table = _replace(ice, "evolved")
    table.append(_arrow({"trade_id": ["T1"], "symbol": ["FPT"], "price": [22.0]}))
    table = ice.load_table("labcheck.evolved")
    first = table.current_snapshot()
    with table.update_schema() as update:
        update.add_column("quantity", LongType(), required=False)
    table = ice.load_table("labcheck.evolved")
    table.append(_arrow({"trade_id": ["T2"], "symbol": ["VNM"], "price": [80.0], "quantity": [5]}))
    table = ice.load_table("labcheck.evolved")
    names = [field.name for field in table.schema().fields]
    historical = table.scan(snapshot_id=first.snapshot_id).to_arrow().num_rows
    current = table.scan().to_arrow().num_rows
    if "quantity" not in names or historical != 1 or current != 2:
        raise AssertionError((names, historical, current))
    return {"columns": names, "historical": historical, "current": current}


def compact_small_files() -> dict:
    """Hai file nhỏ hơn 1MiB được gom một nhóm."""
    ice = _ice()
    table = _replace(ice, "compacted")
    table.append(_arrow({"trade_id": ["T1"], "symbol": ["FPT"], "price": [22.0]}))
    table.append(_arrow({"trade_id": ["T2"], "symbol": ["VNM"], "price": [80.0]}))
    files = [
        (row["file_path"], int(row["file_size_in_bytes"]))
        for row in ice.load_table("labcheck.compacted").inspect.files().to_pylist()
    ]
    groups = plan_compaction(files, target_bytes=1024 * 1024)
    if len(files) < 2 or len(groups) != 1 or len(groups[0]) != len(files):
        raise AssertionError((files, groups))
    return {"files": len(files), "groups": groups}


def travel_to_first_snapshot() -> dict:
    """Đọc đúng snapshot lúc chỉ có T1."""
    ice = _ice()
    table = _replace(ice, "travel")
    table.append(_arrow({"trade_id": ["T1"], "symbol": ["FPT"], "price": [22.0]}))
    table = ice.load_table("labcheck.travel")
    first = table.current_snapshot()
    table.append(_arrow({"trade_id": ["T2"], "symbol": ["VNM"], "price": [80.0]}))
    table = ice.load_table("labcheck.travel")
    chosen = snapshot_as_of(_snapshots(table), datetime.fromtimestamp(first.timestamp_ms / 1000, tz=timezone.utc))
    historical = table.scan(snapshot_id=chosen).to_arrow().num_rows
    current = table.scan().to_arrow().num_rows
    if chosen != first.snapshot_id or historical != 1 or current != 2:
        raise AssertionError((chosen, first.snapshot_id, historical, current))
    return {"snapshot": chosen, "historical": historical, "current": current}


LESSONS = {
    "create": create_one_row,
    "partition": partition_by_symbol,
    "evolve": add_quantity_column,
    "compact": compact_small_files,
    "travel": travel_to_first_snapshot,
}


def run(lesson: str):
    if lesson not in LESSONS:
        raise ValueError(f"Bài không có: {lesson}. Chọn {sorted(LESSONS)}")
    return LESSONS[lesson]()


if __name__ == "__main__":
    import sys

    name = sys.argv[1] if len(sys.argv) > 1 else "all"
    chosen = LESSONS if name == "all" else {name: LESSONS[name]}
    for key, function in chosen.items():
        print(key, function())
