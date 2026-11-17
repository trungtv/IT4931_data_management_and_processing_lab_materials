import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "Data_Lakehouse_lab" / "pipeline"))

from same_function import clean_all_at_once, duplicate_ids_when_cleaned_per_batch
from transforms import clean_trades


def _trade(trade_id):
    return {
        "trade_id": trade_id,
        "symbol": "fpt",
        "side": "buy",
        "price": 22,
        "quantity": 10,
        "event_time": "2026-11-17 09:00:00+00:00",
    }


def _clean(frame):
    return clean_trades(frame, as_of=pd.Timestamp("2026-11-17 12:00:00+00:00"))


def test_per_batch_clean_keeps_a_key_that_arrives_twice():
    first = pd.DataFrame([_trade("T1"), _trade("T2")])
    second = pd.DataFrame([_trade("T1")])
    assert duplicate_ids_when_cleaned_per_batch([first, second], _clean) == ["T1"]
    once = clean_all_at_once([first, second], _clean)
    assert once["trade_id"].tolist() == ["T1", "T2"]
