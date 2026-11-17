"""Chứng minh clean theo từng micro-batch không bằng clean một lần.

Thân hàm giữa EXERCISE_START và EXERCISE_END là lời giải.
"""

from __future__ import annotations

from collections.abc import Callable

import pandas as pd


def duplicate_ids_when_cleaned_per_batch(
    frames: list[pd.DataFrame],
    clean_fn: Callable[[pd.DataFrame], pd.DataFrame],
) -> list[str]:
    """Dedupe bên trong từng batch rồi nối lại. Trả về trade_id còn trùng."""
    # EXERCISE_START
    if not frames:
        return []
    cleaned = [clean_fn(frame) for frame in frames]
    combined = pd.concat(cleaned, ignore_index=True)
    duplicated = combined.loc[combined["trade_id"].duplicated(keep=False), "trade_id"]
    return sorted(duplicated.dropna().unique())
    # EXERCISE_END


def clean_all_at_once(
    frames: list[pd.DataFrame],
    clean_fn: Callable[[pd.DataFrame], pd.DataFrame],
) -> pd.DataFrame:
    """Cùng hàm clean, nhưng trên toàn bộ dòng."""
    # EXERCISE_START
    if not frames:
        raise ValueError("Không có batch nào")
    return clean_fn(pd.concat(frames, ignore_index=True))
    # EXERCISE_END
