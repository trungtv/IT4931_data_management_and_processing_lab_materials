import pytest

from model_choice import QueryNeed, choose_store, latest_price_key


def test_latest_price_is_redis_and_a_two_hop_document_is_still_a_graph():
    assert choose_store(QueryNeed("point", hops=0, ttl_seconds=30)) == "redis"
    assert choose_store(QueryNeed("document", hops=2)) == "neo4j"


def test_trade_document_and_cross_store_sql():
    assert choose_store(QueryNeed("document", hops=0)) == "mongodb"
    assert choose_store(QueryNeed("federate", hops=0)) == "trino"


def test_latest_price_key_is_stable_and_sharded():
    assert latest_price_key("fpt", 8) == latest_price_key(" FPT ", 8)
    assert latest_price_key("fpt", 1) == "price:0:FPT"
    shard = int(latest_price_key("hpg", 8).split(":")[1])
    assert 0 <= shard < 8


def test_point_read_without_ttl_is_rejected():
    with pytest.raises(ValueError):
        choose_store(QueryNeed("point", hops=0))
