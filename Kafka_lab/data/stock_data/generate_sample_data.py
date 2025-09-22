# -*- coding: utf-8 -*-
import json
import random
from datetime import datetime, timedelta
import pandas as pd

# Stock symbols for the lab
STOCK_SYMBOLS = [
    "AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", 
    "META", "NVDA", "NFLX", "ADBE", "CRM"
]

# Base prices for each stock (approximate current prices)
BASE_PRICES = {
    "AAPL": 150.0,
    "GOOGL": 2800.0,
    "MSFT": 350.0,
    "TSLA": 250.0,
    "AMZN": 3200.0,
    "META": 300.0,
    "NVDA": 450.0,
    "NFLX": 400.0,
    "ADBE": 500.0,
    "CRM": 200.0
}

def generate_ohlcv_data(symbol, base_price, timestamp):
    """Generate realistic OHLCV data for a stock symbol"""
    
    # Generate random price movement (-2% to +2%)
    price_change = random.uniform(-0.02, 0.02)
    new_price = base_price * (1 + price_change)
    
    # Generate OHLCV
    open_price = round(new_price * random.uniform(0.998, 1.002), 2)
    close_price = round(new_price * random.uniform(0.998, 1.002), 2)
    
    high_price = round(max(open_price, close_price) * random.uniform(1.001, 1.005), 2)
    low_price = round(min(open_price, close_price) * random.uniform(0.995, 0.999), 2)
    
    # Generate volume (base volume varies by stock)
    base_volume = random.randint(100000, 1000000)
    volume = base_volume + random.randint(-50000, 50000)
    
    return {
        "symbol": symbol,
        "timestamp": timestamp.isoformat() + "Z",
        "open": open_price,
        "high": high_price,
        "low": low_price,
        "close": close_price,
        "volume": volume,
        "exchange": "NASDAQ"
    }

def generate_sample_data(num_records=1000):
    """Generate sample stock data for testing"""
    
    data = []
    start_time = datetime.now() - timedelta(hours=24)
    
    for i in range(num_records):
        # Pick random symbol
        symbol = random.choice(STOCK_SYMBOLS)
        base_price = BASE_PRICES[symbol]
        
        # Generate timestamp (every 1 minute)
        timestamp = start_time + timedelta(minutes=i)
        
        # Generate OHLCV data
        ohlcv = generate_ohlcv_data(symbol, base_price, timestamp)
        data.append(ohlcv)
    
    return data

if __name__ == "__main__":
    # Generate sample data
    print("Generating sample stock data...")
    sample_data = generate_sample_data(1000)
    
    # Save to JSON file
    with open('data/stock_data/sample_ohlcv.json', 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    # Save to CSV for easy viewing
    df = pd.DataFrame(sample_data)
    df.to_csv('data/stock_data/sample_ohlcv.csv', index=False)
    
    print("Generated {} records".format(len(sample_data)))
    print("Saved to data/stock_data/sample_ohlcv.json")
    print("Saved to data/stock_data/sample_ohlcv.csv")
    
    # Show sample
    print("\nSample data:")
    print(df.head())