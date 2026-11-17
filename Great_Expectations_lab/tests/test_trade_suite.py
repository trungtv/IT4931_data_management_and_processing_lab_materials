import pandas as pd
import pytest

from trade_suite import checkpoint, failed_expectations


def _frame(trade_id, side, price):
    return {"trade_id": trade_id, "side": side, "price": price}


def test_a_clean_batch_passes():
    frame = pd.DataFrame([_frame("T1", "BUY", 22.0), _frame("T2", "SELL", 21.5)])
    assert failed_expectations(frame) == []


def test_duplicate_hold_and_non_positive_price_fail_closed():
    frame = pd.DataFrame([_frame("T1", "BUY", 22.0), _frame("T1", "HOLD", 0)])
    failed = failed_expectations(frame)
    assert "expect_column_values_to_be_unique" in failed
    assert "expect_column_values_to_be_in_set" in failed
    assert "expect_column_values_to_be_between" in failed
    assert "expect_column_values_to_not_be_null" not in failed
    with pytest.raises(RuntimeError, match="Checkpoint thất bại"):
        checkpoint(frame)
