"""Quyết định compaction và snapshot time travel.

Thân hàm giữa EXERCISE_START và EXERCISE_END là lời giải.
"""

from __future__ import annotations

from datetime import datetime


def plan_compaction(files: list[tuple[str, int]], target_bytes: int) -> list[list[str]]:
    """Gom file nhỏ thành nhóm không vượt target. File đã đủ lớn đứng một mình."""
    # EXERCISE_START
    if target_bytes <= 0:
        raise ValueError("target_bytes phải dương")
    groups: list[list[str]] = []
    current: list[str] = []
    current_size = 0
    for name, size in files:
        if size <= 0:
            raise ValueError(f"Kích thước file không hợp lệ: {name}")
        if size >= target_bytes:
            if current:
                groups.append(current)
                current = []
                current_size = 0
            groups.append([name])
            continue
        if current and current_size + size > target_bytes:
            groups.append(current)
            current = []
            current_size = 0
        current.append(name)
        current_size += size
    if current:
        groups.append(current)
    return groups
    # EXERCISE_END


def snapshot_as_of(snapshots: list[tuple[int, datetime]], as_of: datetime) -> int:
    """Snapshot mới nhất có committed_at <= as_of. Hòa thời điểm thì lấy id lớn hơn."""
    # EXERCISE_START
    chosen: tuple[datetime, int] | None = None
    for snapshot_id, committed_at in snapshots:
        if committed_at > as_of:
            continue
        if chosen is None or committed_at > chosen[0] or (
            committed_at == chosen[0] and snapshot_id > chosen[1]
        ):
            chosen = (committed_at, snapshot_id)
    if chosen is None:
        raise ValueError("Không có snapshot nào tại thời điểm này")
    return chosen[1]
    # EXERCISE_END
