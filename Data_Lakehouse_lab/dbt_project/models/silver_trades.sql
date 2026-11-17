select
    trade_id,
    symbol,
    side,
    price,
    quantity,
    event_time
from iceberg_scan('s3://warehouse/iceberg/lab/silver_trades')
