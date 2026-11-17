# Airflow Lab - Data Pipeline Orchestration with Apache Airflow

DAG chạy trên nền lab là `trade_quality_gate` trong `dags/trade_quality_gate.py`. Task `stage` gọi `clean_trades`, `choose` rẽ `publish` hoặc `quarantine`, `publish` ghi `symbols.json` lên MinIO và không retry lỗi schema. Notebook 01 dùng `/api/v2/monitor/health`.

## 🎯 Overview

This lab provides hands-on knowledge about **Apache Airflow 3.1.1** - the leading orchestration tool for data pipelines. Students will learn how to design, schedule, and monitor complex workflows in practice.

## 📚 Lab Structure

### **Lab 1: Airflow Basics**
- **Focus**: Introduction to Airflow, installation and configuration
- **Skills**: Understanding Airflow architecture, Web UI, CLI commands
- **Use Case**: Setup environment and run first DAG

### **Lab 2: DAGs and Tasks**
- **Focus**: Creating DAGs with Task SDK (@dag, @task decorators)
- **Skills**: Defining workflows, tasks, dependencies
- **Use Case**: Simple ETL pipeline with Python tasks

### **Lab 3: Operators and Hooks**
- **Focus**: Using common operators (Bash, Python, SQL)
- **Skills**: BashOperator, PythonOperator, SQLExecuteQueryOperator
- **Use Case**: Data extraction and transformation with various operator types

### **Lab 4: Task Dependencies and Branching**
- **Focus**: Managing dependencies, branching logic, trigger rules
- **Skills**: Bitshift operators (>>, <<), BranchPythonOperator
- **Use Case**: Conditional workflows and error handling

### **Lab 5: XCom and Data Sharing**
- **Focus**: Sharing data between tasks with XCom
- **Skills**: Task return values, XCom push/pull, custom XCom backends
- **Use Case**: Data pipeline with data passing between tasks

### **Lab 6: Scheduling and Timetables**
- **Focus**: Scheduling DAGs with cron, timedelta, custom timetables
- **Skills**: Schedule intervals, catchup, data intervals
- **Use Case**: Daily, hourly, and custom scheduling patterns

### **Lab 7: End-to-End Pipeline Integration**
- **Focus**: Integrating Airflow with Kafka, Spark, Databases
- **Skills**: Multi-service orchestration, monitoring, error recovery
- **Use Case**: Complete data pipeline from source → processing → destination

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Install dependencies
./setup_airflow_lab.sh

# Set AIRFLOW_UID (Linux/Mac)
export AIRFLOW_UID=$(id -u)
echo "AIRFLOW_UID=$AIRFLOW_UID" > .env

# Or set manually (Windows)
echo "AIRFLOW_UID=50000" > .env
```

### 2. Initialize Airflow Database
```bash
# Initialize database and create admin user
docker compose up airflow-init

# Wait for initialization to complete
```

### 3. Start Airflow Services
```bash
# Start all services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f airflow-webserver
```

### 4. Access Airflow UI
- **URL**: http://localhost:8080
- **Username**: `airflow`
- **Password**: `airflow`

### 5. Start Jupyter Lab
```bash
# Activate conda environment
conda activate datalab

# Start Jupyter Lab
jupyter lab
```

### 6. Run Labs
Open notebooks in order:
1. `notebooks/01_airflow_basics.ipynb`
2. `notebooks/02_dags_and_tasks.ipynb`
3. `notebooks/03_operators_and_hooks.ipynb`
4. `notebooks/04_task_dependencies.ipynb`
5. `notebooks/05_xcom_data_sharing.ipynb`
6. `notebooks/06_scheduling_timetables.ipynb`
7. `notebooks/07_end_to_end_pipeline.ipynb`

## 🏗️ Architecture

### **Services Included:**
- **Airflow Webserver (API Server)**: Port 8080 (Web UI and REST API)
- **Airflow Scheduler**: Schedules and triggers DAGs
- **Airflow DAG Processor**: Parses and loads DAGs
- **Airflow Triggerer**: Handles deferrable operators
- **PostgreSQL**: Port 5432 (Metadata database)

### **Components:**
- **DAGs**: Workflow definitions in `dags/`
- **Plugins**: Custom operators/hooks in `plugins/`
- **Logs**: Task execution logs in `logs/`
- **Config**: Airflow configuration in `config/`

### **Data Flow:**
```
Source Data → Airflow DAG → Task 1 → Task 2 → ... → Destination
                ↓
            Scheduler monitors
                ↓
            Web UI displays
```

## 📊 Sample DAGs

### **DAG của lab:**
- `trade_quality_gate.py`: stage một batch theo logical date, rẽ publish hoặc quarantine, ghi MinIO

## 🔧 Configuration

### **Environment Variables:**
```bash
# Airflow UID (set in .env)
AIRFLOW_UID=50000

# Admin user (optional)
_AIRFLOW_WWW_USER_USERNAME=airflow
_AIRFLOW_WWW_USER_PASSWORD=airflow
```

### **Airflow Configuration:**
- Executor: `LocalExecutor` (single machine)
- Database: PostgreSQL
- Load Examples: `false` (clean environment)
- DAGs Paused at Creation: `true`

## 🐛 Troubleshooting

### **Common Issues:**

1. **Airflow won't start:**
   ```bash
   # Check logs
   docker compose logs airflow-webserver
   docker compose logs airflow-scheduler
   
   # Restart services
   docker compose restart
   ```

2. **Permission errors:**
   ```bash
   # Set correct AIRFLOW_UID
   export AIRFLOW_UID=$(id -u)
   echo "AIRFLOW_UID=$AIRFLOW_UID" > .env
   
   # Fix permissions
   sudo chown -R $AIRFLOW_UID:0 dags logs plugins config
   ```

3. **DAGs not appearing:**
   ```bash
   # Check DAG processor logs
   docker compose logs airflow-dag-processor
   
   # Test DAG parsing
   docker compose run airflow-cli airflow dags list
   ```

4. **Database connection errors:**
   ```bash
   # Check PostgreSQL health
   docker compose ps postgres
   
   # Restart database
   docker compose restart postgres
   ```

### **Performance Tuning:**
- Increase Docker memory allocation (minimum 4GB)
- Adjust scheduler settings in `config/airflow.cfg`
- Use appropriate executor for your use case

## 📚 Learning Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/3.1.1/)
- [Airflow Task SDK](https://airflow.apache.org/docs/apache-airflow/3.1.1/task-sdk/index.html)
- [Airflow Concepts](https://airflow.apache.org/docs/apache-airflow/3.1.1/core-concepts/index.html)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/3.1.1/best-practices/index.html)

## 🎯 Learning Outcomes

After completing this lab series, students will be able to:

1. **Airflow Fundamentals**:
   - Understand Airflow architecture and components
   - Use Web UI and CLI to manage DAGs
   - Install and configure Airflow environment

2. **DAG Development**:
   - Create DAGs with Task SDK (@dag, @task decorators)
   - Define task dependencies and workflows
   - Implement branching and conditional logic

3. **Operators & Hooks**:
   - Use common operators
   - Create custom operators and hooks
   - Integrate with external systems

4. **Data Management**:
   - Share data between tasks with XCom
   - Handle data passing in pipelines
   - Implement data validation

5. **Scheduling**:
   - Configure scheduling with cron and timetables
   - Understand catchup and data intervals
   - Implement custom scheduling logic

6. **Pipeline Integration**:
   - Integrate Airflow with Kafka, Spark, Databases
   - Build end-to-end data pipelines
   - Monitor and troubleshoot pipelines

## 📋 Assessment Criteria

### **Beginner Level**:
- Complete Lab 1 and 2
- Understand basic concepts of Airflow
- Create a simple DAG

### **Intermediate Level**:
- Complete Labs 1-5
- Understand operators, dependencies, XCom
- Implement branching logic

### **Advanced Level**:
- Complete all labs
- Build end-to-end pipeline
- Integrate with multiple systems
- Optimize performance and reliability

## 🔗 Integration with Other Labs

This lab integrates with:
- **Kafka Lab**: Stream data ingestion
- **Spark Lab**: Data processing
- **NoSQL Lab**: Database operations
- **PyIceberg Lab**: Data lake operations

## 🎉 Next Steps

After completing Airflow Lab, you can:
1. Integrate with dbt Lab (transformation)
2. Add Data Quality Lab (Great Expectations)
3. Implement CI/CD for data pipelines
4. Deploy to production environment

---

**Happy Orchestrating! 🚀**
