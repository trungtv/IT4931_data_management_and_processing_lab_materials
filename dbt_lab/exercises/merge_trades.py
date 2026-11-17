"""Merge incremental theo trade_id.

Thân hàm giữa EXERCISE_START và EXERCISE_END là lời giải.
"""

from __future__ import annotations

import pandas as pd

COLUMNS = ["trade_id", "symbol", "side", "price", "quantity", "event_time"]


def merge_trades(existing: pd.DataFrame, incoming: pd.DataFrame) -> pd.DataFrame:
    """Incoming thắng khi event_time mới hơn hoặc bằng bản đang có."""
    # EXERCISE_START
    for name, frame in (("existing", existing), ("incoming", incoming)):
        missing = [column for column in COLUMNS if column not in frame.columns]
        if missing:
            raise ValueError(f"{name} thiếu cột: {missing}")

    frames = []
    for frame in (existing, incoming):
        current = frame.loc[:, COLUMNS].copy()
        current["event_time"] = pd.to_datetime(current["event_time"], utc=True)
        current["_rank"] = 0 if frame is existing else 1
        frames.append(current)
    combined = pd.concat(frames, ignore_index=True)
    combined = combined.sort_values(["trade_id", "event_time", "_rank"], kind="mergesort")
    kept = combined.drop_duplicates("trade_id", keep="last").drop(columns="_rank")
    return kept.sort_values("trade_id", kind="mergesort").reset_index(drop=True)
    # EXERCISE_END
