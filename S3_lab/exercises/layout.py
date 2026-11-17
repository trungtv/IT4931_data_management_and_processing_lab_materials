"""Layout object và multipart trên bucket warehouse.

Thân hàm giữa EXERCISE_START và EXERCISE_END là lời giải.
"""

from __future__ import annotations

MIN_PART_BYTES = 5 * 1024 * 1024
MAX_PARTS = 10000


def multipart_plan(size_bytes: int, part_size: int) -> list[tuple[int, int]]:
    """Danh sách (offset, độ dài). Part giữa phải đủ 5MiB. Tối đa 10000 part."""
    # EXERCISE_START
    if size_bytes <= 0 or part_size <= 0:
        raise ValueError("size_bytes và part_size phải dương")
    if size_bytes <= part_size:
        return [(0, size_bytes)]
    if part_size < MIN_PART_BYTES:
        raise ValueError("Part không phải part cuối phải >= 5MiB")
    part_count = (size_bytes + part_size - 1) // part_size
    if part_count > MAX_PARTS:
        raise ValueError("Quá 10000 part")
    parts: list[tuple[int, int]] = []
    for index in range(part_count):
        offset = index * part_size
        length = min(part_size, size_bytes - offset)
        parts.append((offset, length))
    return parts
    # EXERCISE_END


def metadata_key(table: str, snapshot_id: int) -> str:
    """Object metadata của một snapshot. List prefix không thay được key này."""
    # EXERCISE_START
    if not table or snapshot_id < 0:
        raise ValueError("table và snapshot_id không hợp lệ")
    return f"iceberg/lab/{table}/metadata/snap-{snapshot_id}.avro"
    # EXERCISE_END


def current_snapshot_readable_by(method: str) -> bool:
    """Chỉ metadata Iceberg trả lời snapshot hiện tại."""
    # EXERCISE_START
    if method == "iceberg_metadata":
        return True
    if method == "list_objects":
        return False
    raise ValueError(f"method không hỗ trợ: {method}")
    # EXERCISE_END
