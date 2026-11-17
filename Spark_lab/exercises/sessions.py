"""Session window trên giao dịch của một mã.

Thân hàm giữa EXERCISE_START và EXERCISE_END là lời giải.
"""

from __future__ import annotations

import pandas as pd


def sessionize(event_times: list[pd.Timestamp], gap: pd.Timedelta) -> list[tuple[pd.Timestamp, pd.Timestamp, int]]:
    """Tách session khi khoảng cách hai sự kiện liên tiếp lớn hơn gap.

    Kết quả là (bắt đầu, sự kiện cuối, số sự kiện). Đầu vào không cần đã sắp xếp.
    """
    # EXERCISE_START
    if gap <= pd.Timedelta(0):
        raise ValueError("gap phải dương")
    if not event_times:
        return []
    ordered = sorted(pd.Timestamp(value) for value in event_times)
    sessions: list[tuple[pd.Timestamp, pd.Timestamp, int]] = []
    start = ordered[0]
    last = ordered[0]
    count = 1
    for current in ordered[1:]:
        if current - last > gap:
            sessions.append((start, last, count))
            start = current
            count = 1
        else:
            count += 1
        last = current
    sessions.append((start, last, count))
    return sessions
    # EXERCISE_END
