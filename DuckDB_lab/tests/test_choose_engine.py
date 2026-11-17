import pytest

from choose_engine import engine_for_aggregate


def test_one_writer_on_a_laptop_uses_duckdb():
    assert engine_for_aggregate(rows=1_000, concurrent_writers=1, streaming_sink=False) == "duckdb"


def test_a_second_writer_or_a_stream_uses_spark():
    assert engine_for_aggregate(rows=1_000, concurrent_writers=2, streaming_sink=False) == "spark"
    assert engine_for_aggregate(rows=1_000, concurrent_writers=1, streaming_sink=True) == "spark"


def test_invalid_writer_count_raises():
    with pytest.raises(ValueError):
        engine_for_aggregate(rows=1, concurrent_writers=0, streaming_sink=False)
