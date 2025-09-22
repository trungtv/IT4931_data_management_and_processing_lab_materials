#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError

# Configuration
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC_NAME = 'stock-data'

# Stock symbols
STOCK_SYMBOLS = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
BASE_PRICES = {
    "AAPL": 150.0,
    "GOOGL": 2800.0,
    "MSFT": 350.0,
    "TSLA": 250.0,
    "AMZN": 3200.0
}

def generate_stock_data(symbol):
    """Generate sample stock data"""
    base_price = BASE_PRICES[symbol]
    price_change = random.uniform(-0.02, 0.02)
    new_price = base_price * (1 + price_change)
    
    return {
        "symbol": symbol,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "open": round(new_price * random.uniform(0.998, 1.002), 2),
        "high": round(new_price * random.uniform(1.001, 1.005), 2),
        "low": round(new_price * random.uniform(0.995, 0.999), 2),
        "close": round(new_price * random.uniform(0.998, 1.002), 2),
        "volume": random.randint(100000, 1000000),
        "exchange": "NASDAQ"
    }

def test_kafka_connection():
    """Test basic Kafka connectivity"""
    print("Testing Kafka connection...")
    
    try:
        # Test producer
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None
        )
        
        # Send test message
        test_data = generate_stock_data("AAPL")
        future = producer.send(TOPIC_NAME, key="AAPL", value=test_data)
        record_metadata = future.get(timeout=10)
        
        print(f"✅ Producer test successful!")
        print(f"📊 Sent message to partition {record_metadata.partition}")
        
        producer.close()
        
        # Test consumer
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='latest',
            consumer_timeout_ms=5000
        )
        
        print("✅ Consumer test successful!")
        consumer.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Kafka test failed: {e}")
        return False

if __name__ == "__main__":
    print("Kafka Lab Test Script")
    print("=" * 50)
    
    if test_kafka_connection():
        print("\n🎉 Kafka cluster is working correctly!")
        print("You can now run the Jupyter notebooks.")
    else:
        print("\n💡 Make sure Kafka cluster is running:")
        print("   docker compose up -d")
        print("   docker compose ps")
