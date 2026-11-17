"""Biến đổi giao dịch dùng chung cho batch và streaming.

Thân hàm giữa EXERCISE_START và EXERCISE_END là lời giải. Đợt sau chỉ thay
đoạn đó bằng NotImplementedError.
"""

from __future__ import annotations

import pandas as pd

REQUIRED_TRADE_COLUMNS = ["trade_id", "symbol", "side", "price", "quantity", "event_time"]
SILVER_COLUMNS = REQUIRED_TRADE_COLUMNS
GOLD_COLUMNS = ["symbol", "trade_count", "total_quantity", "notional", "vwap"]


def _as_utc(value: pd.Timestamp) -> pd.Timestamp:
    stamp = pd.Timestamp(value)
    if stamp.tzinfo is None:
        return stamp.tz_localize("UTC")
    return stamp.tz_convert("UTC")


def clean_trades(df: pd.DataFrame, as_of: pd.Timestamp | None = None) -> pd.DataFrame:
    """Giữ giao dịch hợp lệ: khóa, chiều, giá, khối lượng, và cửa sổ thời gian."""
    # EXERCISE_START
    missing = [column for column in REQUIRED_TRADE_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Thiếu cột bắt buộc: {missing}")

    out = df.loc[:, REQUIRED_TRADE_COLUMNS].copy()
    out["trade_id"] = out["trade_id"].astype("string").str.strip()
    out["symbol"] = out["symbol"].astype("string").str.strip().str.upper()
    out["side"] = out["side"].astype("string").str.strip().str.upper()
    out["price"] = pd.to_numeric(out["price"], errors="coerce")
    out["quantity"] = pd.to_numeric(out["quantity"], errors="coerce")
    out["event_time"] = pd.to_datetime(out["event_time"], utc=True, errors="coerce")

    as_of_utc = _as_utc(pd.Timestamp.now(tz="UTC") if as_of is None else as_of)
    late_before = as_of_utc - pd.Timedelta(days=7)
    future_after = as_of_utc + pd.Timedelta(hours=1)
    valid = (
        out["trade_id"].notna()
        & (out["trade_id"] != "")
        & out["symbol"].notna()
        & (out["symbol"] != "")
        & out["side"].isin(["BUY", "SELL"])
        & out["price"].notna()
        & (out["price"] > 0)
        & out["quantity"].notna()
        & (out["quantity"] > 0)
        & out["event_time"].notna()
        & (out["event_time"] >= late_before)
        & (out["event_time"] <= future_after)
    )
    out = out.loc[valid].drop_duplicates(subset=["trade_id"], keep="first")
    out["quantity"] = out["quantity"].astype("int64")
    out["price"] = out["price"].astype("float64")
    out["event_time"] = out["event_time"].dt.tz_convert("UTC").dt.tz_localize(None)
    return out.reset_index(drop=True)
    # EXERCISE_END


def aggregate_trades(df: pd.DataFrame) -> pd.DataFrame:
    """Gom giao dịch đã sạch theo mã: số lệnh, khối lượng, notional, VWAP."""
    required = ["symbol", "price", "quantity"]
    # EXERCISE_START
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Thiếu cột bắt buộc: {missing}")

    work = df.loc[:, required].copy()
    work["price"] = pd.to_numeric(work["price"], errors="coerce")
    work["quantity"] = pd.to_numeric(work["quantity"], errors="coerce")
    if work[["price", "quantity"]].isna().any().any():
        raise ValueError("price hoặc quantity không phải số")
    if ((work["price"] <= 0) | (work["quantity"] <= 0)).any():
        raise ValueError("price và quantity phải dương")

    work["notional"] = work["price"] * work["quantity"]
    grouped = work.groupby("symbol", as_index=False).agg(
        trade_count=("quantity", "size"),
        total_quantity=("quantity", "sum"),
        notional=("notional", "sum"),
    )
    grouped["trade_count"] = grouped["trade_count"].astype("int64")
    grouped["total_quantity"] = grouped["total_quantity"].astype("int64")
    grouped["notional"] = grouped["notional"].astype("float64")
    grouped["vwap"] = grouped["notional"] / grouped["total_quantity"]
    return grouped.loc[:, GOLD_COLUMNS].sort_values("symbol").reset_index(drop=True)
    # EXERCISE_END
