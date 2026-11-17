"""Cổng chất lượng trước khi publish aggregate theo mã.

Thân hàm giữa EXERCISE_START và EXERCISE_END là lời giải.
"""

from __future__ import annotations

import pandas as pd
from transforms import aggregate_trades, clean_trades

from idempotency import task_output_uri


def staged_trades(logical_date: str) -> pd.DataFrame:
    """Một batch cố định cho logical date: lệnh sạch, một bản trùng, một side bẩn."""
    # EXERCISE_START
    if len(logical_date) != 10:
        raise ValueError("logical_date phải là YYYY-MM-DD")
    event_time = f"{logical_date}T09:00:00+00:00"
    rows = [
        ("T1", "FPT", "BUY", 22.0, 10),
        ("T2", "VNM", "SELL", 80.0, 5),
        ("T3", "HPG", "BUY", 26.0, 8),
        ("T1", "FPT", "BUY", 22.0, 10),
        ("T4", "FPT", "HOLD", 22.0, 10),
    ]
    return pd.DataFrame(
        [
            {
                "trade_id": trade_id,
                "symbol": symbol,
                "side": side,
                "price": price,
                "quantity": quantity,
                "event_time": event_time,
            }
            for trade_id, symbol, side, price, quantity in rows
        ]
    )
    # EXERCISE_END


def assess(frame: pd.DataFrame, logical_date: str) -> dict:
    """clean_trades một lần. Còn dòng sạch thì publish, hết thì quarantine."""
    # EXERCISE_START
    as_of = pd.Timestamp(logical_date).tz_localize("UTC") + pd.Timedelta(hours=12)
    cleaned = clean_trades(frame, as_of=as_of)
    kept = set(cleaned["trade_id"].astype(str))
    rejected = sorted(set(frame["trade_id"].astype(str)) - kept)
    records = cleaned.assign(event_time=cleaned["event_time"].astype(str)).to_dict(orient="records")
    return {
        "logical_date": logical_date,
        "branch": "publish" if records else "quarantine",
        "clean": records,
        "rejected": rejected,
        "output_uri": task_output_uri("trade_quality_gate", "publish", logical_date),
    }
    # EXERCISE_END


def object_key(uri_prefix: str, name: str) -> str:
    """Key trong bucket warehouse. Retry ghi đè đúng key này."""
    # EXERCISE_START
    prefix = "s3://warehouse/"
    if not uri_prefix.startswith(prefix) or not uri_prefix.endswith("/"):
        raise ValueError("uri_prefix phải là s3://warehouse/.../")
    if not name or "/" in name:
        raise ValueError("name không hợp lệ")
    return uri_prefix.removeprefix(prefix) + name
    # EXERCISE_END


def publish_symbols(clean_records: list[dict]) -> list[dict]:
    """Aggregate từng mã. Hết dòng sạch thì lỗi schema, không publish rỗng."""
    # EXERCISE_START
    if not clean_records:
        raise ValueError("schema")
    frame = pd.DataFrame(clean_records)
    stats = aggregate_trades(frame)
    published = []
    for row in stats.to_dict(orient="records"):
        published.append(
            {
                "symbol": row["symbol"],
                "trade_count": int(row["trade_count"]),
                "total_quantity": int(row["total_quantity"]),
                "notional": float(row["notional"]),
                "vwap": float(row["vwap"]),
            }
        )
    return published
    # EXERCISE_END
