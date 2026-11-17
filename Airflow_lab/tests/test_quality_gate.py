import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "Data_Lakehouse_lab" / "pipeline"))

from quality_gate import assess, object_key, publish_symbols, staged_trades


def test_a_dated_batch_publishes_three_symbols_and_rejects_the_bad_key():
    report = assess(staged_trades("2026-11-17"), "2026-11-17")
    assert report["branch"] == "publish"
    assert report["rejected"] == ["T4"]
    assert [row["symbol"] for row in publish_symbols(report["clean"])] == ["FPT", "HPG", "VNM"]
    assert object_key(report["output_uri"], "symbols.json") == (
        "airflow/trade_quality_gate/publish/logical_date=2026-11-17/symbols.json"
    )


def test_an_empty_clean_set_is_quarantine_and_publish_refuses_it():
    empty = staged_trades("2026-11-17").iloc[0:0]
    report = assess(empty, "2026-11-17")
    assert report["branch"] == "quarantine"
    with pytest.raises(ValueError, match="schema"):
        publish_symbols(report["clean"])
