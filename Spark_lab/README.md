# Spark Lab - Big Data Processing with Apache Spark

VWAP chạy được nằm ở `lab/trade_sql.py` và notebook `01_spark_batch_processing.ipynb`: Spark SQL trong scheduler, cùng số với `aggregate_trades`. Catalog Iceberg của lab là runtime `1.6.1`, warehouse `s3a://warehouse/iceberg`. Session window vẫn ở `exercises/sessions.py`.

## 🎯 Overview
This lab provides hands-on experience with Apache Spark for big data processing, including batch processing, streaming, and machine learning.

## 🏗️ Architecture
- **Spark Cluster**: Master + 2 Workers (distributed processing)
- **Kafka**: KRaft mode for streaming data ingestion
- **PostgreSQL**: Structured data storage
- **Redis**: Caching and real-time data
- **Jupyter Lab**: Interactive development environment

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.8+ (for local development)
- Git
- Conda environment (datalab)

### Setup
```bash
# Navigate to Spark lab
cd Spark_lab

# Run setup script
chmod +x setup_spark_lab.sh
./setup_spark_lab.sh

# Start the cluster
docker-compose up -d

# Wait for services to be ready (30-60 seconds)
sleep 30

# Test connectivity
python test_spark_connectivity.py

# Check cluster status
docker-compose ps
```

### Access Points
- **Spark Master UI**: http://localhost:8080
- **Jupyter Lab**: http://localhost:8888
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **Kafka**: localhost:9092

## 📚 Lab Structure

### Lab 1: Spark Batch Processing ✅
**File**: `notebooks/01_spark_batch_processing.ipynb`

**Topics Covered**:
- DataFrame operations (select, filter, groupBy, join)
- Aggregations and window functions
- Multi-table joins and data integration
- Performance optimization (caching, partitioning, broadcast joins)
- Data persistence and export (Parquet, JSON, CSV)

**Sample Datasets**:
- Sales transactions (1000 records)
- Customer demographics (8 customers)
- Product catalog (8 products)

**Exercises**:
1. Basic DataFrame Operations
2. Aggregations and Grouping
3. Joins and Data Integration
4. Performance Optimization
5. Data Persistence and Export

### Lab 2: Spark Streaming ✅
**File**: `notebooks/02_spark_streaming.ipynb`

**Topics Covered**:
- Event-time vs Processing-time
- Tumbling windows (fixed, non-overlapping)
- Sliding windows (overlapping windows)
- Watermarking for late data handling
- Advanced window operations
- Output modes (Append, Update, Complete)
- Real-world streaming pipelines

**Sample Datasets**:
- Event streams with timestamps
- Late-arriving data scenarios
- User activity events

**Exercises**:
1. Event-Time vs Processing-Time
2. Tumbling Windows (Fixed Windows)
3. Sliding Windows (Overlapping Windows) ⭐
4. Watermarking for Late Data
5. Advanced Window Operations
6. Output Modes with Windows
7. Real-World Streaming Pipeline

### Lab 3: Spark MLlib ✅
**File**: `notebooks/03_spark_ml.ipynb`

**Topics Covered**:
- Feature engineering with Spark ML
- Classification (Random Forest)
- ML pipeline creation
- Model evaluation metrics
- Customer segmentation

**Sample Datasets**:
- Customer classification (1000 records)
- Sales regression (800 records)
- Customer clustering (600 records)

**Exercises**:
1. Customer Classification (Random Forest)
2. Sales Regression (Linear Regression)
3. Customer Clustering (K-means)
4. Model Evaluation and Tuning
5. Feature Engineering Pipeline

### Lab 4: Spark SQL ✅
**File**: `notebooks/04_spark_sql.ipynb`

**Topics Covered**:
- Spark SQL basics (spark.sql())
- Register DataFrames as temporary views
- JOIN operations with SQL syntax
- Window functions with SQL
- CREATE VIEW and CREATE TABLE
- User Defined Functions (UDFs)
- Catalog management

**Sample Datasets**:
- Sales transactions (1000 records)
- Customer demographics (8 customers)

**Exercises**:
1. Basic Spark SQL Queries
2. JOIN Operations with SQL
3. Window Functions with SQL
4. CREATE VIEW
5. CREATE TABLE (Managed and External)
6. User Defined Functions (UDF)
7. Catalog Management

### Lab 5: Spark + Iceberg Integration ✅
**File**: `notebooks/05_spark_iceberg_integration.ipynb`

**Topics Covered**:
- Spark session configuration with Iceberg extensions
- Read and write Iceberg tables from Spark
- Schema evolution with Spark
- Time travel queries
- Partitioning strategies
- Integration best practices

**Sample Datasets**:
- Sales transactions with timestamps (1000 records)

**Exercises**:
1. Create Sample Data and Setup
2. Write to Iceberg Table
3. Read from Iceberg Table
4. Schema Evolution
5. Time Travel Queries
6. Partitioning Strategies
7. Integration Best Practices

**Note**: Full Iceberg functionality requires Iceberg Spark runtime JAR. The notebook includes examples and patterns that work when the JAR is available.

### Lab 6: Spark + Kafka Integration ✅
**File**: `notebooks/06_spark_kafka_integration.ipynb`

**Topics Covered**:
- Kafka topic setup and configuration
- Kafka producer (Python) to send events
- Spark reading from Kafka topics
- Schema parsing (JSON messages)
- Windowed aggregations với real Kafka streams
- Sliding windows với Kafka data
- Writing results back to Kafka
- Kafka consumer to verify results
- Continuous producer for testing

**Sample Datasets**:
- Real-time events sent to Kafka topics
- User activity events (clicks, views, purchases)

**Exercises**:
1. Setup Kafka Topics
2. Create Kafka Producer
3. Read from Kafka với Spark
4. Windowed Aggregations với Kafka Stream
5. Sliding Windows với Kafka
6. Write Results to Kafka
7. Consume Results from Kafka
8. Continuous Producer (Background Thread)

**Prerequisites**:
- Kafka running (via docker-compose.yml)
- Kafka topics created
- Kafka Python library installed

## 🔧 Configuration

### Environment Variables
The lab uses the following configuration (see `.env` file):
```bash
# Spark Configuration
SPARK_MASTER_URL=spark://spark-master:7077
SPARK_APP_NAME=SparkLab

# Database Configuration
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=spark_lab
POSTGRES_USER=spark_user
POSTGRES_PASSWORD=spark_password

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=kafka:29092
KAFKA_TOPIC_PREFIX=spark_lab

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
```

### Spark Configuration
- **Master**: 1 core, 1GB RAM
- **Workers**: 2 cores, 2GB RAM each
- **Total Cluster**: 5 cores, 5GB RAM

## 📊 Sample Data Generation

### Batch Data
```python
# Generate sales data
python scripts/generate_sales_data.py

# Generate customer data
python scripts/generate_customer_data.py
```

### Streaming Data
```python
# Start IoT sensor simulator
python scripts/iot_sensor_simulator.py

# Start web click simulator
python scripts/web_click_simulator.py
```

## 🛠️ Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Connect to Spark cluster
export SPARK_MASTER_URL=spark://localhost:7077

# Run Python scripts
python code/batch_processing/sales_analysis.py
```

### Jupyter Development
1. Access Jupyter Lab at http://localhost:8888
2. Use the provided notebooks in `notebooks/` directory
3. Spark context is automatically configured

## 📈 Monitoring

### Spark UI
- **Master**: http://localhost:8080
- **Application**: http://localhost:4040 (when running)

### Kafka Monitoring
- **Topics**: Use Kafka CLI tools
- **Consumer Groups**: Monitor via Spark UI

### Database Monitoring
- **PostgreSQL**: Connect via psql or GUI tools
- **Redis**: Use redis-cli or GUI tools

## 🔍 Troubleshooting

### Common Issues

1. **Spark Master not accessible**
   ```bash
   docker-compose logs spark-master
   ```

2. **Kafka connection issues**
   ```bash
   docker-compose logs kafka
   ```

3. **Jupyter not connecting to Spark**
   - Check SPARK_MASTER_URL in Jupyter environment
   - Verify network connectivity

### Logs
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f spark-master
docker-compose logs -f kafka
```

## 📝 Best Practices

### Performance
- Use appropriate partitioning strategies
- Cache frequently accessed DataFrames
- Optimize shuffle operations
- Use broadcast joins for small tables

### Development
- Use Jupyter notebooks for exploration
- Move to Python scripts for production
- Implement proper error handling
- Use logging for debugging

### Data Management
- Use Parquet format for storage
- Implement data validation
- Use schema evolution strategies
- Monitor data quality

## 🎓 Learning Objectives

After completing this lab, you will be able to:
- Process large datasets with Spark DataFrames
- Implement real-time data processing with Structured Streaming
- Build machine learning pipelines with Spark MLlib
- Use Spark SQL for querying data with SQL syntax
- Integrate Spark with Apache Iceberg for data lakehouse storage
- Create and manage tables, views, and UDFs
- Optimize Spark applications for performance
- Integrate Spark with various data sources
- Monitor and debug Spark applications

## 📚 Additional Resources

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Structured Streaming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [MLlib Guide](https://spark.apache.org/docs/latest/ml-guide.html)

## 🤝 Contributing

Feel free to contribute improvements, additional exercises, or bug fixes to this lab.

## 📄 License

This lab is provided for educational purposes. Please refer to the individual component licenses for more details.
