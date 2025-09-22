# Trino SQL Engine Lab Setup

## 🚀 Quick Start

### 1. Start Trino Cluster
```bash
# Start all databases including Trino cluster
docker compose up -d

# Check if all services are running
docker compose ps
```

### 2. Access Trino Web UI
- **Trino Web UI**: http://localhost:8080
- **Username**: admin (or any username)
- **Password**: (no password required)

### 3. Run Trino Lab Notebook
```bash
# Start Jupyter Lab
jupyter lab

# Open: notebooks/06_trino_exercises.ipynb
```

## 🏗️ Architecture

### Services Included:
- **Trino Coordinator**: Port 8080 (Web UI + Query coordination)
- **Trino Worker**: Query execution
- **MongoDB**: Port 27017 (Document store)
- **Neo4j**: Port 7474/7687 (Graph database)
- **Redis**: Port 6379 (Key-value store)
- **PostgreSQL**: Port 5432 (Relational database)

### Data Sources Connected:
- **MongoDB**: Product catalog, orders
- **PostgreSQL**: Transaction data, analytics
- **CSV Files**: Historical data, logs

## 📊 Available Catalogs

### MongoDB Catalog
```sql
-- Show schemas
SHOW SCHEMAS FROM mongodb;

-- Show tables
SHOW TABLES FROM mongodb.ecommerce;

-- Query products
SELECT * FROM mongodb.ecommerce.products LIMIT 10;
```

### PostgreSQL Catalog
```sql
-- Show schemas
SHOW SCHEMAS FROM postgresql;

-- Show tables
SHOW TABLES FROM postgresql.public;

-- Query orders
SELECT * FROM postgresql.public.orders LIMIT 10;
```

## 🔧 Configuration

### Trino Config Files:
- `trino-config/config.properties`: Coordinator configuration
- `trino-config/node.properties`: Node configuration
- `trino-config/catalog/mongodb.properties`: MongoDB connector
- `trino-config/catalog/postgresql.properties`: PostgreSQL connector

### Memory Settings:
- Query max memory: 5GB
- Query max memory per node: 1GB
- Query max total memory per node: 2GB

## 🐛 Troubleshooting

### Common Issues:

1. **Trino won't start**:
   ```bash
   # Check logs
   docker compose logs trino-coordinator
   
   # Restart services
   docker compose restart
   ```

2. **Can't connect to MongoDB**:
   ```bash
   # Check MongoDB is running
   docker compose ps mongodb
   
   # Test MongoDB connection
   docker exec -it nosql_mongodb mongosh --eval "db.runCommand('ping')"
   ```

3. **Query fails**:
   - Check Trino Web UI for error details
   - Verify data sources are accessible
   - Check catalog configuration

### Performance Tuning:
- Increase memory limits in `config.properties`
- Add more worker nodes
- Optimize query patterns

## 📚 Learning Resources

- [Trino Documentation](https://trino.io/docs/)
- [Trino Connectors](https://trino.io/docs/current/connector.html)
- [SQL Functions](https://trino.io/docs/current/functions.html)

## 🎯 Lab Objectives

1. **Single-Source Queries**: Query individual data sources
2. **Federated Queries**: Join data across multiple sources
3. **Data Lakehouse Analytics**: Advanced analytics patterns
4. **Query Optimization**: Performance tuning techniques
5. **Real-time Analytics**: Streaming data processing

---

**Happy Querying! 🚀**
