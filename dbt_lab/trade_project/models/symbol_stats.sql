select
    symbol,
    count(*) as trade_count,
    sum(quantity) as total_quantity,
    {{ vwap('price', 'quantity') }} as vwap
from {{ ref('trades') }}
group by symbol
