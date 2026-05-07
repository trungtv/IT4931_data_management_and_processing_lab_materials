# Kafka Lab - Real-time Stock Market Data Streaming

## 🎯 Overview

This lab series focuses on Apache Kafka fundamentals using real-world stock market data (OHLCV). Students will learn consumer groups, partitioning strategies, offset management, and real-time analytics through hands-on exercises.

## 📚 Lab Structure

### **Lab 1: Kafka Basics**
- **Focus**: Topics, Partitions, Producers, Consumers
- **Skills**: Message serialization, basic producer/consumer patterns
- **Use Case**: Simple stock data streaming

### **Lab 2: Consumer Groups and Load Balancing**
- **Focus**: Consumer group coordination, partition assignment
- **Skills**: Load balancing, consumer group management
- **Use Case**: Multiple consumers processing stock data

### **Lab 3: Advanced Partitioning Strategies**
- **Focus**: Custom partitioners, data routing
- **Skills**: Partition-aware routing, performance optimization
- **Use Case**: Stock data partitioned by symbol/volume

### **Lab 4: Offset Management and Exactly-Once Processing**
- **Focus**: Offset commits, exactly-once semantics
- **Skills**: Reliable message processing, failure recovery
- **Use Case**: Reliable stock data processing

### **Lab 5: Real-time Stock Analytics**
- **Focus**: Stream processing, real-time analytics
- **Skills**: Multiple consumer groups, real-time dashboards
- **Use Case**: Live stock analysis and alerts

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Install dependencies
./setup_kafka_lab.sh

# Start Kafka cluster
docker compose up -d

# Verify services
docker compose ps
```

### 2. Access Web UIs
- **AKHQ (Modern Kafka UI)**: http://localhost:8080
- **Schema Registry**: http://localhost:8081
- **Kafka Connect**: http://localhost:8083

### 3. Start Jupyter Lab
```bash
jupyter lab
```

### 4. Run Labs
Open notebooks in order:
1. `01_kafka_basics.ipynb`
2. `02_consumer_groups.ipynb`
3. `03_partitioning.ipynb`
4. `04_offset_management.ipynb`
5. `05_stock_analytics.ipynb`

## 🏗️ Architecture

### **Services Included:**
- **Kafka Broker**: Port 9092 (Message streaming with KRaft mode)
- **Schema Registry**: Port 8081 (Schema management)
- **Kafka Connect**: Port 8083 (Data integration)
- **AKHQ**: Port 8080 (Modern Kafka UI - better than provectus/kafka-ui)
- **Redis**: Port 6379 (Caching)

### **KRaft Mode Benefits:**
- ✅ **No Zookeeper**: Simplified architecture - no external coordination service
- ✅ **Better Performance**: Reduced network hops and latency
- ✅ **Future-proof**: Zookeeper will be deprecated in future Kafka versions
- ✅ **Easier Management**: Fewer components to maintain and monitor
- ✅ **Simplified Deployment**: Single node can act as both broker and controller

### **Data Flow:**
```
Stock Data Generator → Kafka Producer → Stock Data Topic
                                                      ↓
                                              Multiple Consumer Groups
                                                      ↓
                                            Analytics, Alerts, Storage
```

## 📊 Sample Data

### **Stock Symbols:**
- AAPL, GOOGL, MSFT, TSLA, AMZN
- META, NVDA, NFLX, ADBE, CRM

### **Data Structure:**
```json
{
  "symbol": "AAPL",
  "timestamp": "2025-01-21T10:30:00Z",
  "open": 150.25,
  "high": 151.50,
  "low": 149.80,
  "close": 151.20,
  "volume": 1250000,
  "exchange": "NASDAQ"
}
```

## 🔧 Configuration

### **Kafka Settings:**
- **Bootstrap Servers**: localhost:9092
- **Topic**: stock-data
- **Partitions**: 3 (configurable, applied by default for newly auto-created topics)
- **Replication Factor**: 1 (single broker)

### **Consumer Groups:**
- **stock-analytics-group**: Real-time analytics
- **stock-alerts-group**: Price/volume alerts
- **stock-storage-group**: Data persistence

## 🐛 Troubleshooting

### **Common Issues:**

1. **Kafka won't start**:
   ```bash
   # Check logs
   docker compose logs kafka
   
   # Restart services
   docker compose restart
   ```

2. **Can't connect to Kafka**:
   ```bash
   # Check if Kafka is running
   docker compose ps kafka
   
   # Test connection
   docker exec -it kafka_broker kafka-topics --bootstrap-server localhost:9092 --list
   ```

3. **`stock-data` chỉ có 1 partition thay vì 3**:
   - `KAFKA_NUM_PARTITIONS=3` chỉ áp dụng cho topic mới được auto-create
   - Nếu `stock-data` đã được tạo trước đó với 1 partition, hãy xóa và tạo lại:
   ```bash
   docker exec -it kafka_broker kafka-topics --bootstrap-server localhost:9092 --delete --topic stock-data
   docker exec -it kafka_broker kafka-topics --bootstrap-server localhost:9092 --create --topic stock-data --partitions 3 --replication-factor 1
   docker exec -it kafka_broker kafka-topics --bootstrap-server localhost:9092 --describe --topic stock-data
   ```

4. **Consumer group issues**:
   - Check consumer group status in Kafka UI
   - Verify partition assignments
   - Check for consumer lag

### **Performance Tuning:**
- Increase batch size for producers
- Tune consumer fetch settings
- Optimize partition count
- Monitor consumer lag

## 📚 Learning Resources

- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [Kafka Consumer Groups](https://kafka.apache.org/documentation/#consumerconfigs)
- [Kafka Partitioning](https://kafka.apache.org/documentation/#producerconfigs)
- [Kafka Offset Management](https://kafka.apache.org/documentation/#consumerconfigs)

## 🎯 Learning Outcomes

After completing this lab series, students will be able to:

1. **Kafka Fundamentals**:
   - Understand topics, partitions, producers, consumers
   - Implement basic producer/consumer patterns
   - Use Kafka UI for monitoring

2. **Consumer Groups**:
   - Manage consumer group coordination
   - Implement load balancing strategies
   - Handle consumer group rebalancing

3. **Partitioning**:
   - Design custom partitioning strategies
   - Optimize for data locality
   - Handle partition rebalancing

4. **Offset Management**:
   - Implement reliable offset commits
   - Handle exactly-once processing
   - Manage consumer failures

5. **Real-time Analytics**:
   - Build real-time data pipelines
   - Implement multiple consumer groups
   - Create real-time dashboards

## 📋 Assessment Criteria

### **Beginner Level**:
- Complete Lab 1 and 2
- Understand basic Kafka concepts
- Implement simple producer/consumer

### **Intermediate Level**:
- Complete Labs 1-4
- Understand consumer groups and partitioning
- Implement reliable message processing

### **Advanced Level**:
- Complete all labs
- Build real-time analytics pipeline
- Optimize for performance and reliability

---

**Happy Streaming! 🚀**

