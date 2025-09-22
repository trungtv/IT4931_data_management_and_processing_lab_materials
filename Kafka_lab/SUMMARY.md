# Kafka Lab - Summary

## 🎉 Kafka Lab đã được tạo thành công!

### 📁 Cấu trúc thư mục:
```
Kafka_lab/
├── docker-compose.yml          # Kafka cluster với Zookeeper, Schema Registry, Kafka Connect, Kafka UI
├── requirements.txt            # Python dependencies
├── setup_kafka_lab.sh         # Setup script
├── test_kafka.py              # Test script
├── README.md                  # Hướng dẫn chi tiết
├── notebooks/                 # 5 Jupyter notebooks
│   ├── 01_kafka_basics.ipynb
│   ├── 02_consumer_groups.ipynb
│   ├── 03_partitioning.ipynb
│   ├── 04_offset_management.ipynb
│   └── 05_stock_analytics.ipynb
└── data/
    └── stock_data/
        ├── generate_sample_data.py
        └── sample_ohlcv.json
```

### 🚀 Cách sử dụng:

#### 1. Setup Environment:
```bash
cd Kafka_lab
./setup_kafka_lab.sh
```

#### 2. Start Kafka Cluster:
```bash
docker compose up -d
```

#### 3. Test Connection:
```bash
python test_kafka.py
```

#### 4. Start Jupyter Lab:
```bash
jupyter lab
```

#### 5. Run Notebooks:
- Mở `notebooks/01_kafka_basics.ipynb`
- Chạy từng cell để học Kafka fundamentals

### 🌐 Web UIs:
- **Kafka UI**: http://localhost:8080
- **Schema Registry**: http://localhost:8081
- **Kafka Connect**: http://localhost:8083

### 📊 Lab Content:

#### **Lab 1: Kafka Basics**
- Topics, Partitions, Producers, Consumers
- Message serialization với JSON
- Basic producer/consumer patterns
- Kafka UI monitoring

#### **Lab 2: Consumer Groups**
- Consumer group coordination
- Partition assignment strategies
- Load balancing across consumers
- Consumer group monitoring

#### **Lab 3: Advanced Partitioning**
- Custom partitioners
- Partition-aware data routing
- Partition rebalancing
- Performance optimization

#### **Lab 4: Offset Management**
- Offset commit strategies
- Exactly-once processing
- Consumer failure recovery
- Manual offset management

#### **Lab 5: Real-time Stock Analytics**
- Multiple consumer groups
- Stream processing patterns
- Real-time dashboards
- High-throughput data streams

### 🎯 Learning Outcomes:
Sau khi hoàn thành lab series này, sinh viên sẽ có thể:

1. **Kafka Fundamentals**: Hiểu topics, partitions, producers, consumers
2. **Consumer Groups**: Quản lý consumer group coordination và load balancing
3. **Partitioning**: Thiết kế custom partitioning strategies
4. **Offset Management**: Implement reliable offset commits và exactly-once processing
5. **Real-time Analytics**: Xây dựng real-time data pipelines với multiple consumer groups

### 🔧 Tech Stack:
- **Apache Kafka**: Message streaming platform
- **Zookeeper**: Coordination service
- **Schema Registry**: Schema management
- **Kafka Connect**: Data integration
- **Kafka UI**: Monitoring và management
- **Python**: kafka-python, pandas, matplotlib
- **Docker**: Containerized environment

### 📈 Use Case: Stock Market Data Streaming
- **Data**: OHLCV stock data (Open, High, Low, Close, Volume)
- **Symbols**: AAPL, GOOGL, MSFT, TSLA, AMZN, META, NVDA, NFLX, ADBE, CRM
- **Real-time**: Live stock data processing
- **Analytics**: Moving averages, price alerts, volume analysis
- **Multiple Consumers**: Analytics, alerts, storage, dashboard

---

**Kafka Lab đã sẵn sàng để sử dụng! 🚀**
