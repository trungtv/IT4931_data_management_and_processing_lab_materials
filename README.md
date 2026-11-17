# Big Data Engineering - Course Materials

## Nền lab

Lệnh một dòng cho capstone (MinIO, Postgres, Kafka KRaft, Spark, Airflow):

```bash
export AIRFLOW_UID=$(id -u)
docker compose -f platform/docker-compose.yml --profile lakehouse up -d --build
```

Cổng host cố định:

| Dịch vụ | Cổng |
| --- | --- |
| MinIO API / console | 9000 / 9001 |
| Postgres | 5432 |
| Kafka (từ máy host) | 9092 |
| Schema Registry | 8081 |
| Kafka Connect | 8083 |
| AKHQ | 8088 |
| Spark master UI / RPC | 8082 / 7077 |
| Airflow | 8080 (airflow / airflow) |

Profile riêng: `core`, `kafka`, `spark`, `airflow`, `lakehouse`. File [`docker-compose.yml`](docker-compose.yml) ở gốc repo include cùng file này. Không còn Kafka wurstmeister và Zookeeper.

Capstone có đáp án nằm ở [`Data_Lakehouse_lab/pipeline`](Data_Lakehouse_lab/pipeline). Hàm `clean_trades` và `aggregate_trades` có mốc `EXERCISE_START` / `EXERCISE_END`. DAG Airflow gọi các script đó, không gọi `echo`.

### Lộ trình chính

1. Docker, S3/MinIO — buổi chuẩn bị
2. Kafka, Spark, PyIceberg — bài lõi
3. DuckDB — một buổi đối chiếu khi không cần cụm (`DuckDB_lab/01_when_not_spark.ipynb`)
4. dbt, Airflow
5. Data Lakehouse — pipeline thật trên MinIO

### Tùy chọn, không tính vào capstone

- NoSQL, Kubernetes
- Great Expectations (chất lượng dữ liệu của capstone là dbt test)
- `archive/` — slide, PDF Hortonworks, và mirror sách Spark. Không phải bài làm

## 📋 Overview

Repository này chứa toàn bộ tài liệu và bài lab cho khóa học **Big Data Engineering**, bao gồm các công nghệ và công cụ hiện đại trong Data Engineering stack. Tất cả các labs được thiết kế để học viên có thể thực hành từ cơ bản đến nâng cao với các use cases thực tế.

## 🎯 Learning Objectives

Sau khi hoàn thành các labs trong repository này, học viên sẽ có thể:

- ✅ Hiểu và sử dụng các công nghệ Big Data phổ biến
- ✅ Xây dựng data pipelines end-to-end
- ✅ Xử lý real-time và batch data processing
- ✅ Quản lý data quality và orchestration
- ✅ Thiết kế và implement data lakehouse architecture
- ✅ Làm việc với NoSQL databases và data formats

## 📚 Lab Structure

Repository được tổ chức thành các labs độc lập, mỗi lab tập trung vào một công nghệ cụ thể:

### 🔴 Core Labs (Bắt buộc)

#### 1. **Kafka Lab** - Real-time Data Streaming
- **Mục tiêu**: Apache Kafka fundamentals với stock market data
- **Nội dung**: Topics, partitions, consumer groups, offset management, real-time analytics
- **Số notebooks**: 6 labs
- **Tech Stack**: Kafka, Zookeeper, Schema Registry, Kafka Connect, AKHQ, Redis
- **📁 Thư mục**: `Kafka_lab/`

#### 2. **Spark Lab** - Big Data Processing
- **Mục tiêu**: Apache Spark cho batch và streaming processing
- **Nội dung**: DataFrames, Structured Streaming, MLlib
- **Số notebooks**: 8 notebooks trong `Spark_lab/` (lab 7 gọi chung `clean_trades` với capstone, lab 8 là session window). Thư mục sách Spark nằm ở `archive/spark-lab/`
- **Tech Stack**: Spark, Spark SQL, Structured Streaming
- **📁 Thư mục**: `Spark_lab/`

#### 3. **Airflow Lab** - Workflow Orchestration
- **Mục tiêu**: Apache Airflow 3.1.1 cho data pipeline orchestration
- **Nội dung**: DAGs, Tasks, Operators, Hooks, XCom, Scheduling, Integration
- **Số notebooks**: 8 labs
- **Tech Stack**: Airflow 3.1.1, PostgreSQL, Redis, Celery
- **📁 Thư mục**: `Airflow_lab/`

### 🟡 Data Transformation & Quality Labs

#### 4. **dbt Lab** - Data Transformation
- **Mục tiêu**: dbt (Data Build Tool) cho data transformations
- **Nội dung**: Models, Jinja templating, Testing, Documentation, Macros, Airflow integration
- **Số notebooks**: 6 labs
- **Tech Stack**: dbt-core, dbt-postgres, PostgreSQL
- **📁 Thư mục**: `dbt_lab/`

#### 5. **Great Expectations Lab** - Data Quality
- **Mục tiêu**: Great Expectations cho data validation và quality checks
- **Nội dung**: Expectations, Checkpoints, Data Docs, dbt integration, Airflow integration
- **Số notebooks**: 7 labs
- **Tech Stack**: Great Expectations, PostgreSQL, dbt-expectations
- **📁 Thư mục**: `Great_Expectations_lab/`

### 🟢 Data Storage & Lakehouse Labs

#### 6. **PyIceberg Lab** - Data Lakehouse Format
- **Mục tiêu**: Apache Iceberg cho data lakehouse storage
- **Nội dung**: Schema evolution, Data partitioning, Compaction, Time travel
- **Số notebooks**: 6 labs
- **Tech Stack**: PyIceberg, Apache Iceberg
- **📁 Thư mục**: `pyiceberg/`

#### 7. **NoSQL Lab** - Multi-model Databases
- **Mục tiêu**: Các loại NoSQL databases phổ biến
- **Nội dung**: MongoDB (Document), Neo4j (Graph), Redis (Key-Value), Trino (SQL on everything)
- **Số notebooks**: 7 labs
- **Tech Stack**: MongoDB, Neo4j, Redis, Trino, PostgreSQL
- **📁 Thư mục**: `NoSQL_lab/`

### 🔵 Integration Lab (Tổng hợp)

#### 8. **Data Lakehouse Lab** - End-to-End Integration
- **Mục tiêu**: Tích hợp tất cả các công nghệ trong một pipeline hoàn chỉnh
- **Nội dung**: Complete data lakehouse architecture từ ingestion đến analytics
- **Số notebooks**: 7 labs
- **Tech Stack**: Kafka + Spark + Iceberg + dbt + Great Expectations + Airflow
- **📁 Thư mục**: `Data_Lakehouse_lab/`

### 🟢 Infrastructure Lab

#### 9. **K8s Basics Lab** - Container Orchestration
- **Mục tiêu**: Học Kubernetes fundamentals cho container orchestration
- **Nội dung**: Pods, Deployments, Services, ConfigMaps, Secrets, Storage, Scaling
- **Số notebooks**: 8 labs
- **Tech Stack**: Kubernetes, kubectl, minikube/kind
- **📁 Thư mục**: `K8s_Basics_lab/`

## 🗺️ Learning Paths

### Path 1: Real-time Data Processing (Streaming Focus)
**Mục tiêu**: Xây dựng real-time data pipelines
```
1. Kafka Lab (Real-time ingestion)
2. Spark Lab (Streaming processing)
3. PyIceberg Lab (Stream storage)
4. Airflow Lab (Orchestration)
5. Data Lakehouse Lab (Integration)
```
**Thời gian**: ~50-60 hours | **Độ khó**: Intermediate → Advanced

### Path 2: Data Transformation & Quality (ETL Focus)
**Mục tiêu**: Xây dựng data warehouse và quality pipelines
```
1. Spark Lab (Batch processing)
2. PyIceberg Lab (Data lake storage)
3. dbt Lab (Transformation)
4. Great Expectations Lab (Data quality)
5. Airflow Lab (Orchestration)
6. Data Lakehouse Lab (Integration)
```
**Thời gian**: ~60-70 hours | **Độ khó**: Intermediate → Advanced

### Path 3: Data Storage & Lakehouse (Storage Focus)
**Mục tiêu**: Hiểu về data storage và lakehouse architecture
```
1. PyIceberg Lab (Lakehouse format)
2. Spark Lab (Processing trên Iceberg)
3. dbt Lab (Transformations)
4. Great Expectations Lab (Quality)
5. Airflow Lab (Orchestration)
6. NoSQL Lab (Multi-model databases)
7. Data Lakehouse Lab (Complete architecture)
```
**Thời gian**: ~60-70 hours | **Độ khó**: Intermediate → Advanced

### Path 4: Complete Data Engineer (Recommended - Full Stack)
**Mục tiêu**: Trở thành Data Engineer đầy đủ kỹ năng
```
1. Kafka Lab (Ingestion)
2. Spark Lab (Processing - Batch & Streaming)
3. PyIceberg Lab (Storage)
4. dbt Lab (Transformation)
5. Great Expectations Lab (Quality)
6. Airflow Lab (Orchestration)
7. NoSQL Lab (Multi-model databases)
8. Data Lakehouse Lab (End-to-end integration)
```
**Thời gian**: ~80-100 hours | **Độ khó**: Beginner → Advanced

### Path 5: Beginner-Friendly (Step by Step)
**Mục tiêu**: Học từ cơ bản, không áp đảo
```
Phase 1 - Fundamentals:
1. Kafka Lab (Hiểu về streaming)
2. Spark Lab (Hiểu về processing)

Phase 2 - Storage & Transformation:
3. PyIceberg Lab (Data storage)
4. dbt Lab (Data transformation)

Phase 3 - Quality & Orchestration:
5. Great Expectations Lab (Data quality)
6. Airflow Lab (Workflow management)

Phase 4 - Advanced Topics:
7. NoSQL Lab (Multi-model databases)
8. Data Lakehouse Lab (Complete integration)
```
**Thời gian**: ~90-110 hours | **Độ khó**: Beginner → Advanced

### Path 6: Advanced Integration (For Experienced)
**Mục tiêu**: Tập trung vào integration và production-ready pipelines
```
1. Kafka Lab (Advanced streaming patterns)
2. Spark Lab (Advanced processing)
3. PyIceberg Lab (Advanced lakehouse)
4. dbt Lab + Great Expectations Lab (Transform & Quality)
5. Airflow Lab (Advanced orchestration)
6. Data Lakehouse Lab (Production-ready integration)
```
**Thời gian**: ~60-75 hours | **Độ khó**: Advanced

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose**: Tất cả labs sử dụng Docker
- **Python 3.10+**: Cho Python-based labs
- **Conda/Miniconda**: Cho environment management
- **Git**: Để clone repository
- **Jupyter Notebook**: Cho interactive learning

### Setup

1. **Clone repository:**
```bash
git clone <repository-url>
cd materials
```

2. **Setup environment:**
```bash
cd Kafka_lab
./setup_kafka_lab.sh
```

3. **Start services:**
```bash
export AIRFLOW_UID=$(id -u)
docker compose -f platform/docker-compose.yml --profile lakehouse up -d --build
```

4. **Open Jupyter:**
```bash
conda activate <lab_env>
jupyter notebook
```

## 📖 Lab Details

### Kafka Lab
- **Duration**: ~8-10 hours
- **Difficulty**: Beginner → Intermediate
- **Key Concepts**: Streaming, Consumer groups, Partitioning, Offset management
- **Use Case**: Real-time stock market data processing

### Spark Lab
- **Duration**: ~10-12 hours
- **Difficulty**: Intermediate
- **Key Concepts**: DataFrames, Structured Streaming, MLlib
- **Use Case**: Batch và streaming data processing

### Airflow Lab
- **Duration**: ~12-15 hours
- **Difficulty**: Intermediate → Advanced
- **Key Concepts**: DAGs, Tasks, Operators, XCom, Scheduling
- **Use Case**: Complete workflow orchestration

### dbt Lab
- **Duration**: ~8-10 hours
- **Difficulty**: Intermediate
- **Key Concepts**: Models, Jinja, Testing, Documentation
- **Use Case**: Data warehouse transformations

### Great Expectations Lab
- **Duration**: ~8-10 hours
- **Difficulty**: Intermediate
- **Key Concepts**: Expectations, Checkpoints, Data Docs
- **Use Case**: Data quality validation

### PyIceberg Lab
- **Duration**: ~10-12 hours
- **Difficulty**: Intermediate → Advanced
- **Key Concepts**: Schema evolution, Partitioning, Time travel
- **Use Case**: Data lakehouse storage

### K8s Basics Lab
- **Duration**: ~4-6 hours
- **Difficulty**: Beginner (kubectl và manifest cơ bản, không phải bài vận hành cụm)
- **Key Concepts**: Pods, Deployments, Services, ConfigMaps, Secrets, Storage, HPA
- **Use Case**: Container orchestration và production deployment

### NoSQL Lab
- **Duration**: ~12-15 hours
- **Difficulty**: Intermediate
- **Key Concepts**: Document, Graph, Key-Value stores, SQL on everything
- **Use Case**: Multi-model database architecture

### Data Lakehouse Lab
- **Duration**: ~15-20 hours
- **Difficulty**: Advanced
- **Key Concepts**: End-to-end integration, Medallion architecture
- **Use Case**: Complete data platform

## 🏗️ Repository Structure

```
materials/
├── README.md                    # This file
├── requirements.txt            # Global Python dependencies
├── setup_env.sh                # Global setup script
│
├── Kafka_lab/                  # Kafka streaming lab
│   ├── notebooks/              # 5 Jupyter notebooks
│   ├── docker-compose.yml      # Kafka services
│   └── README.md
│
├── Spark_lab/                  # Spark processing lab
│   ├── notebooks/              # Spark notebooks
│   ├── code/                   # Spark code examples
│   └── README.md
│
├── Airflow_lab/               # Airflow orchestration lab
│   ├── notebooks/             # 7 Jupyter notebooks
│   ├── dags/                  # Sample DAGs
│   └── README.md
│
├── dbt_lab/                   # dbt transformation lab
│   ├── notebooks/             # 5 Jupyter notebooks
│   ├── models/                # dbt models
│   └── README.md
│
├── Great_Expectations_lab/    # GE data quality lab
│   ├── notebooks/             # 6 Jupyter notebooks
│   └── README.md
│
├── pyiceberg/                 # Iceberg storage lab
│   ├── *.ipynb                # 5 Jupyter notebooks
│   └── README.md
│
├── NoSQL_lab/                 # NoSQL databases lab
│   ├── notebooks/             # 6 Jupyter notebooks
│   └── README.md
│
├── Data_Lakehouse_lab/        # Integration lab
│   ├── notebooks/             # 7 Jupyter notebooks
│   ├── dags/                  # Complete pipeline DAGs
│   └── README.md
│
└── K8s_Basics_lab/            # Kubernetes basics lab
    ├── notebooks/             # 7 Jupyter notebooks
    ├── manifests/             # K8s manifest examples
    ├── apps/                  # Sample applications
    └── README.md
```

## 🔧 Technology Stack

### Core Technologies
- **Apache Kafka**: Real-time data streaming
- **Apache Spark**: Big data processing
- **Apache Airflow**: Workflow orchestration
- **Apache Iceberg**: Data lakehouse format

### Data Tools
- **dbt**: Data transformation
- **Great Expectations**: Data quality
- **Trino**: SQL query engine

### Databases
- **PostgreSQL**: Relational database
- **MongoDB**: Document database
- **Neo4j**: Graph database
- **Redis**: Key-Value store

### Infrastructure
- **Docker & Docker Compose**: Containerization
- **Kubernetes**: Container orchestration
- **Jupyter Notebooks**: Interactive learning
- **Python 3.10+**: Programming language

## 📝 Best Practices

### Lab Workflow
1. **Read README**: Đọc kỹ README của từng lab trước khi bắt đầu
2. **Setup Environment**: Chạy setup script và start services
3. **Follow Notebooks**: Làm theo thứ tự notebooks
4. **Experiment**: Thử nghiệm và customize code
5. **Document**: Ghi chú lại những gì học được

### Code Practices
- ✅ Sử dụng version control (Git)
- ✅ Comment code rõ ràng
- ✅ Follow PEP 8 (Python style guide)
- ✅ Test code trước khi submit
- ✅ Document findings và issues

## 🐛 Troubleshooting

### Common Issues

1. **Port Conflicts**:
   - Check ports đang được sử dụng: `lsof -i :<port>`
   - Stop conflicting services hoặc change ports trong docker-compose.yml

2. **Docker Issues**:
   - Ensure Docker daemon đang chạy
   - Check disk space: `docker system df`
   - Clean up: `docker system prune`

3. **Environment Issues**:
   - Activate correct conda environment
   - Check Python version: `python --version`
   - Reinstall dependencies: `pip install -r requirements.txt`

4. **Connection Issues**:
   - Verify services đang chạy: `docker-compose ps`
   - Check logs: `docker-compose logs <service>`
   - Wait for services to be ready (có thể mất vài phút)

## 📚 Additional Resources

### Documentation
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [dbt Documentation](https://docs.getdbt.com/)
- [Great Expectations Documentation](https://docs.greatexpectations.io/)
- [Apache Iceberg Documentation](https://iceberg.apache.org/docs/)

### Learning Resources
- Mỗi lab có README.md riêng với detailed instructions
- Notebooks có comments và explanations chi tiết
- Sample code và use cases thực tế

## 🤝 Contributing

Nếu bạn phát hiện lỗi hoặc muốn cải thiện labs:

1. Create an issue với mô tả chi tiết
2. Fork repository và tạo branch mới
3. Make changes và test thoroughly
4. Submit pull request với description rõ ràng

## 📄 License

Tài liệu này được sử dụng cho mục đích giáo dục trong khóa học Big Data Engineering.

## 👥 Authors

- **Course Instructor**: [Your Name]
- **Institution**: SoICT, HUST

## 🙏 Acknowledgments

- Apache Software Foundation cho các open-source projects
- Community contributors cho documentation và examples
- Students cho feedback và improvements

---

## 📞 Support

Nếu có câu hỏi hoặc cần hỗ trợ:
- Check lab-specific README.md
- Review troubleshooting section
- Contact instructor hoặc TA

---

**Happy Learning! 🚀**

*Last Updated: 2026-11-17*

