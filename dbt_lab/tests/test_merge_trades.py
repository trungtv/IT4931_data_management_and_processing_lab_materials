import pandas as pd

from merge_trades import merge_trades


def _row(trade_id, event_time, price):
    return {
        "trade_id": trade_id,
        "symbol": "FPT",
        "side": "BUY",
        "price": price,
        "quantity": 10,
        "event_time": event_time,
    }


def test_newer_incoming_replaces_and_equal_timestamp_keeps_incoming():
    existing = pd.DataFrame([_row("T1", "2026-11-17 09:00:00+00:00", 20), _row("T2", "2026-11-17 09:00:00+00:00", 21)])
    incoming = pd.DataFrame([_row("T1", "2026-11-17 09:05:00+00:00", 22), _row("T2", "2026-11-17 09:00:00+00:00", 23)])
    merged = merge_trades(existing, incoming)
    assert merged.set_index("trade_id").loc["T1", "price"] == 22
    assert merged.set_index("trade_id").loc["T2", "price"] == 23


def test_older_incoming_does_not_overwrite():
    existing = pd.DataFrame([_row("T1", "2026-11-17 09:05:00+00:00", 22)])
    incoming = pd.DataFrame([_row("T1", "2026-11-17 09:00:00+00:00", 20)])
    merged = merge_trades(existing, incoming)
    assert merged.loc[0, "price"] == 22
