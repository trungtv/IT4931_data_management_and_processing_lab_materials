select
    symbol,
    trade_count,
    total_quantity,
    notional,
    vwap
from iceberg_scan('s3://warehouse/iceberg/lab/gold_symbol_stats')
