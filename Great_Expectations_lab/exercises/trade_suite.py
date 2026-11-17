"""Suite Great Expectations 1.x cho giao dịch, chạy trên context ephemeral.

Thân hàm giữa EXERCISE_START và EXERCISE_END là lời giải.
"""

from __future__ import annotations

import pandas as pd


def failed_expectations(df: pd.DataFrame) -> list[str]:
    """Tên expectation không đạt. Batch sạch trả về danh sách rỗng."""
    # EXERCISE_START
    import great_expectations as gx
    from great_expectations.expectations import (
        ExpectColumnValuesToBeBetween,
        ExpectColumnValuesToBeInSet,
        ExpectColumnValuesToBeUnique,
        ExpectColumnValuesToNotBeNull,
    )

    context = gx.get_context(mode="ephemeral")
    source = context.data_sources.add_pandas("trades")
    asset = source.add_dataframe_asset("trades")
    batch_definition = asset.add_batch_definition_whole_dataframe("all")
    suite = context.suites.add(gx.ExpectationSuite(name="trade_suite"))
    suite.add_expectation(ExpectColumnValuesToNotBeNull(column="trade_id"))
    suite.add_expectation(ExpectColumnValuesToBeUnique(column="trade_id"))
    suite.add_expectation(ExpectColumnValuesToBeInSet(column="side", value_set=["BUY", "SELL"]))
    suite.add_expectation(
        ExpectColumnValuesToBeBetween(column="price", min_value=0, strict_min=True)
    )
    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})
    result = batch.validate(suite)
    return [item.expectation_config.type for item in result.results if not item.success]
    # EXERCISE_END


def suite_rules() -> list[dict]:
    """Hợp đồng của suite. Data Docs của lab này là danh sách rule này, không phải file HTML in sẵn."""
    return [
        {"column": "trade_id", "rule": "not_null"},
        {"column": "trade_id", "rule": "unique"},
        {"column": "side", "rule": "in_set", "values": ["BUY", "SELL"]},
        {"column": "price", "rule": "greater_than_zero"},
    ]


def checkpoint(df: pd.DataFrame) -> None:
    """Dừng batch khi còn expectation fail. Batch sạch thì đi tiếp."""
    # EXERCISE_START
    failed = failed_expectations(df)
    if failed:
        raise RuntimeError("Checkpoint thất bại: " + ", ".join(failed))
    # EXERCISE_END
