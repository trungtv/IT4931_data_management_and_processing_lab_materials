"""Bài Mongo, Neo4j, Redis và cách chọn store. Không bật Postgres."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))

from model_choice import QueryNeed, choose_store, latest_price_key
from trades_roundtrip import mongo_trade, neo4j_holder, redis_price


def mongo_counts(database, trades: list[dict]) -> dict[str, int]:
    """Ghi document và đếm theo symbol."""
    for trade in trades:
        mongo_trade(database, trade)
    rows = database.trades.aggregate([{"$group": {"_id": "$symbol", "n": {"$sum": 1}}}])
    return {row["_id"]: row["n"] for row in rows}


def redis_latest(client, symbol: str, price: float, ttl_seconds: int) -> tuple[str, int]:
    """Giá mới nhất có TTL. Key chia shard để tránh một hot key."""
    key = redis_price(client, symbol, price)
    client.expire(key, ttl_seconds)
    ttl = client.ttl(key)
    if ttl <= 0:
        raise AssertionError(ttl)
    if key != latest_price_key(symbol, shard_count=8):
        raise AssertionError(key)
    return key, ttl


def coholders(session, left: str, right: str, symbol: str) -> list[str]:
    """Hai account cùng nắm một mã. Câu hỏi đi qua hai cạnh."""
    session.run(
        "MERGE (a:Account {id: $left}) "
        "MERGE (b:Account {id: $right}) "
        "MERGE (s:Symbol {ticker: $symbol}) "
        "MERGE (a)-[:HOLDS]->(s) "
        "MERGE (b)-[:HOLDS]->(s)",
        left=left,
        right=right,
        symbol=symbol,
    )
    rows = session.run(
        "MATCH (a:Account {id: $left})-[:HOLDS]->(:Symbol {ticker: $symbol})<-[:HOLDS]-(other) "
        "RETURN other.id AS id",
        left=left,
        symbol=symbol,
    )
    found = sorted(record["id"] for record in rows)
    if right not in found:
        raise AssertionError(found)
    return found


def store_for(pattern: str, hops: int, ttl_seconds: int | None) -> str:
    return choose_store(QueryNeed(pattern=pattern, hops=hops, ttl_seconds=ttl_seconds))


def run() -> dict:
    from neo4j import GraphDatabase
    from pymongo import MongoClient
    import redis

    database = MongoClient("mongodb://admin:password123@localhost:27017")["trades"]
    counts = mongo_counts(
        database,
        [
            {"trade_id": "T1", "symbol": "FPT", "side": "BUY", "price": 22.0, "quantity": 10},
            {"trade_id": "T2", "symbol": "FPT", "side": "SELL", "price": 23.0, "quantity": 4},
        ],
    )
    cache = redis.Redis(host="localhost", port=6379, decode_responses=True)
    key, ttl = redis_latest(cache, "FPT", 22.0, 30)
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password123"))
    with driver.session() as session:
        neo4j_holder(session, "ACC1", "FPT")
        others = coholders(session, "ACC1", "ACC2", "FPT")
    driver.close()
    stores = {
        "price": store_for("point", 0, 30),
        "document": store_for("document", 0, None),
        "graph": store_for("document", 2, None),
        "federate": store_for("federate", 0, None),
    }
    if counts.get("FPT", 0) < 2 or stores != {
        "price": "redis",
        "document": "mongodb",
        "graph": "neo4j",
        "federate": "trino",
    }:
        raise AssertionError((counts, stores))
    return {"counts": counts, "key": key, "ttl": ttl, "coholders": others, "stores": stores}


if __name__ == "__main__":
    print(run())
