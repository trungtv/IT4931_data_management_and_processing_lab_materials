# Data Lakehouse Lab - End-to-End Data Pipeline Integration

## 📋 Overview

Hệ thống bài lab tổng hợp tích hợp tất cả các công nghệ Data Engineering đã học:
- **Kafka**: Real-time data ingestion
- **Spark**: Big data processing
- **Iceberg**: Data lakehouse storage
- **dbt**: Data transformations
- **Great Expectations**: Data quality
- **Airflow**: Workflow orchestration

## 🎯 Learning Objectives

Sau khi hoàn thành lab này, bạn sẽ có thể:

- ✅ Thiết kế và implement complete data lakehouse architecture
- ✅ Tích hợp multiple technologies trong một pipeline
- ✅ Build end-to-end data pipelines từ ingestion đến analytics
- ✅ Implement data quality checks ở mọi stage
- ✅ Orchestrate complex workflows với Airflow
- ✅ Apply best practices cho production pipelines

## 🏗️ Lab Architecture

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌──────────┐     ┌─────────┐
│  Kafka  │────▶│  Spark   │────▶│ Iceberg │────▶│   dbt    │────▶│   GE    │
│(Ingest) │     │(Process) │     │(Store)  │     │(Transform)│     │(Quality)│
└─────────┘     └─────────┘     └─────────┘     └──────────┘     └─────────┘
     │                │                │                │                │
     └────────────────┴────────────────┴────────────────┴────────────────┘
                                    │
                                    ▼
                            ┌─────────────┐
                            │   Airflow   │
                            │(Orchestrate)│
                            └─────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker và Docker Compose
- Python 3.10+
- Conda hoặc Miniconda
- Hoàn thành các labs trước:
  - Kafka Lab
  - Spark Lab
  - Airflow Lab
  - dbt Lab
  - Great Expectations Lab

### Setup Steps

1. **Clone và navigate:**
```bash
cd Data_Lakehouse_lab
```

2. **Run setup script:**
```bash
chmod +x setup_lakehouse_lab.sh
./setup_lakehouse_lab.sh
```

3. **Start all services:**
```bash
export AIRFLOW_UID=$(id -u)
docker compose -f ../platform/docker-compose.yml --profile lakehouse up -d --build
```

4. **Wait for services to be ready:**
```bash
# Check services
docker-compose ps

# Check Airflow UI: http://localhost:8080
# Check Spark Master UI: http://localhost:8081
```

5. **Open Jupyter:**
```bash
conda activate lakehouse_lab
jupyter notebook
```

## 📚 Lab Content

### Lab 1: Architecture Overview
- Data Lakehouse architecture
- Technology stack overview
- Integration patterns
- Best practices

### Lab 2: Data Ingestion với Kafka
- Ingest data từ multiple sources
- Kafka producers và consumers
- Schema registry
- Data validation at ingestion

### Lab 3: Processing với Spark + Iceberg
- Spark Structured Streaming từ Kafka
- Write to Iceberg tables
- Batch processing với Spark
- Schema evolution với Iceberg

### Lab 4: Transformation với dbt
- dbt models trên Iceberg tables
- Staging → Intermediate → Marts
- dbt transformations
- dbt tests

### Lab 5: Data Quality với Great Expectations
- GE expectations trên processed data
- Checkpoints và validations
- Data quality monitoring
- Alerts và notifications

### Lab 6: Orchestration với Airflow
- Airflow DAGs cho complete pipeline
- Task dependencies
- Error handling và retries
- Monitoring và alerting

### Lab 7: End-to-End Pipeline
- Complete pipeline từ start to finish
- Integration testing
- Performance optimization
- Production best practices

## 🐳 Docker Services

Lab này chạy các services sau:

- **Kafka**: Port 9092
- **Zookeeper**: Port 2181
- **Spark Master**: Port 8081 (UI) - Changed from 8080 to avoid conflict
- **Spark Worker**: Connected to master
- **PostgreSQL**: Port 5432 (Airflow metadata + dbt)
- **Redis**: Port 6379 (Airflow Celery broker)
- **Airflow Webserver**: Port 8080
- **Airflow Scheduler**: Background
- **Airflow Worker**: Background

## 📖 Pipeline Flow

```
1. Data Sources → Kafka (Ingestion)
2. Kafka → Spark Streaming (Real-time processing)
3. Spark → Iceberg Tables (Storage)
4. Iceberg → dbt (Transformations)
5. dbt Models → Great Expectations (Validation)
6. All → Airflow (Orchestration)
```

## 🔗 Integration Points

- **Kafka → Spark**: Structured Streaming
- **Spark → Iceberg**: Write operations
- **Iceberg → dbt**: Read từ Iceberg tables
- **dbt → GE**: Validate dbt outputs
- **All → Airflow**: Orchestrate entire pipeline

## 🐛 Troubleshooting

### Service Issues

1. **Check all services:**
```bash
docker-compose ps
```

2. **Check logs:**
```bash
docker-compose logs <service_name>
```

3. **Restart services:**
```bash
docker-compose restart <service_name>
```

### Connection Issues

- Ensure all services are healthy before starting
- Check port conflicts
- Verify network connectivity between containers

## 📝 Notes

- This lab requires significant resources (RAM, CPU)
- Start services gradually if needed
- Monitor resource usage
- Some services may take time to initialize

## 🎓 Next Steps

Sau khi hoàn thành lab này, bạn có thể:

1. Deploy similar architecture to production
2. Optimize pipeline performance
3. Scale individual components
4. Add monitoring và alerting
5. Implement CI/CD for data pipelines

---

**Happy Building! 🏗️**

