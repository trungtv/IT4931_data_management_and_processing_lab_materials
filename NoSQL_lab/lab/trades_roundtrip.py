"""Một lệnh trên Mongo, Redis và Neo4j cho cùng một giao dịch."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))

from model_choice import latest_price_key


def mongo_trade(database, trade: dict) -> dict:
    database.trades.replace_one({"trade_id": trade["trade_id"]}, trade, upsert=True)
    found = database.trades.find_one({"trade_id": trade["trade_id"]}, {"_id": 0})
    if found != trade:
        raise AssertionError(found)
    return found


def redis_price(client, symbol: str, price: float) -> str:
    key = latest_price_key(symbol, shard_count=8)
    client.set(key, str(price), ex=30)
    stored = client.get(key)
    if stored is None or float(stored) != price:
        raise AssertionError(stored)
    return key


def neo4j_holder(session, account: str, symbol: str) -> list[str]:
    session.run(
        "MERGE (a:Account {id: $account}) "
        "MERGE (s:Symbol {ticker: $symbol}) "
        "MERGE (a)-[:HOLDS]->(s)",
        account=account,
        symbol=symbol,
    )
    rows = session.run(
        "MATCH (a:Account {id: $account})-[:HOLDS]->(s:Symbol) RETURN s.ticker AS ticker",
        account=account,
    )
    tickers = sorted(record["ticker"] for record in rows)
    if symbol not in tickers:
        raise AssertionError(tickers)
    return tickers


def run() -> tuple[str, str, list[str]]:
    from neo4j import GraphDatabase
    from pymongo import MongoClient
    import redis

    trade = {"trade_id": "T1", "symbol": "FPT", "side": "BUY", "price": 22.0, "quantity": 10}
    found = mongo_trade(MongoClient("mongodb://admin:password123@localhost:27017")["trades"], trade)
    key = redis_price(redis.Redis(host="localhost", port=6379, decode_responses=True), "FPT", 22.0)
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password123"))
    with driver.session() as session:
        tickers = neo4j_holder(session, "ACC1", "FPT")
    driver.close()
    return found["trade_id"], key, tickers


if __name__ == "__main__":
    print(run())
