from datetime import datetime, timedelta, timezone

import pandas as pd
import pytest

from transforms import aggregate_trades, clean_trades

AS_OF = pd.Timestamp("2026-11-17T09:00:00Z")


def trade(**overrides) -> dict:
    row = {
        "trade_id": "T1",
        "symbol": "vnm",
        "side": "buy",
        "price": 20,
        "quantity": 10,
        "event_time": "2026-11-17T08:00:00+00:00",
        "extra": "bỏ cột này",
    }
    row.update(overrides)
    return row


def test_drops_null_price():
    cleaned = clean_trades(pd.DataFrame([trade(), trade(trade_id="T2", price=None)]), as_of=AS_OF)
    assert cleaned["trade_id"].tolist() == ["T1"]


def test_drops_late_event():
    late = (datetime(2026, 11, 17, 9, tzinfo=timezone.utc) - timedelta(days=8)).isoformat()
    cleaned = clean_trades(
        pd.DataFrame([trade(), trade(trade_id="LATE", event_time=late)]),
        as_of=AS_OF,
    )
    assert cleaned["trade_id"].tolist() == ["T1"]


def test_drops_duplicate_trade_id_and_keeps_first():
    cleaned = clean_trades(
        pd.DataFrame([trade(price=20), trade(price=99, symbol="fpt")]),
        as_of=AS_OF,
    )
    assert len(cleaned) == 1
    assert cleaned.loc[0, "price"] == 20
    assert cleaned.loc[0, "symbol"] == "VNM"


def test_missing_column_raises():
    frame = pd.DataFrame([{"trade_id": "T1", "symbol": "VNM"}])
    with pytest.raises(ValueError, match="Thiếu cột"):
        clean_trades(frame, as_of=AS_OF)


def test_aggregate_vwap():
    frame = pd.DataFrame(
        [
            {"symbol": "VNM", "price": 10.0, "quantity": 2},
            {"symbol": "VNM", "price": 20.0, "quantity": 2},
            {"symbol": "FPT", "price": 5.0, "quantity": 4},
        ]
    )
    aggregated = aggregate_trades(frame)
    vnm = aggregated.set_index("symbol").loc["VNM"]
    assert int(vnm["trade_count"]) == 2
    assert int(vnm["total_quantity"]) == 4
    assert vnm["notional"] == 60
    assert vnm["vwap"] == 15


def test_aggregate_missing_column_raises():
    with pytest.raises(ValueError, match="Thiếu cột"):
        aggregate_trades(pd.DataFrame([{"symbol": "VNM"}]))
