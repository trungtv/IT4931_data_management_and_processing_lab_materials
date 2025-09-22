# NoSQL Lab - Multi-Model Database Architecture

## 🎯 Objectives
This lab helps students understand and practice with different NoSQL database types in a real-world microservices architecture.

## 📚 Lab Content

### Lab 1: MongoDB - Document Store
- Flexible schema design
- CRUD operations
- Aggregation pipelines
- Indexing strategies

### Lab 2: Neo4j - Graph Database  
- Graph modeling
- Cypher queries
- Relationship analysis
- Recommendation algorithms

### Lab 3: Redis - Key-Value Store
- Caching strategies
- Session management
- Rate limiting
- Data structures

### Lab 4: Integration - Multi-Database Architecture
- Cross-service data synchronization
- Consistency patterns
- Performance optimization
- Monitoring & observability

## 🚀 Setup Instructions

### 1. Environment Preparation
```bash
# Activate existing conda environment
conda activate datalab

# Install dependencies for NoSQL lab
pip install -r requirements.txt
```

### 2. Start Databases
```bash
# Start all databases
docker-compose up -d

# Check status
docker-compose ps
```

### 3. Database Access
- **MongoDB**: `mongodb://admin:password123@localhost:27017`
- **Neo4j Browser**: http://localhost:7474 (neo4j/password123)
- **Redis**: `redis://localhost:6379`
- **Redis Commander**: http://localhost:8081

### 4. Run Notebooks
```bash
# Open Jupyter Lab
jupyter lab

# Or open individual notebooks
jupyter notebook 01_setup_and_connections.ipynb
```

## 📁 Directory Structure

```
NoSQL_lab/
├── requirements.txt          # Dependencies
├── docker-compose.yml       # Database setup
├── README.md               # This guide
├── data/                   # Sample data
│   ├── mongodb/
│   ├── neo4j/
│   └── redis/
├── notebooks/              # Jupyter notebooks
│   ├── 01_setup_and_connections.ipynb
│   ├── 02_mongodb_exercises.ipynb
│   ├── 03_neo4j_exercises.ipynb
│   ├── 04_redis_exercises.ipynb
│   └── 05_integration_exercises.ipynb
├── src/                    # Python modules
│   ├── services/
│   ├── models/
│   └── utils/
└── tests/                  # Unit tests
```

## 🔧 Troubleshooting

### Database Connection Issues
```bash
# Check containers
docker-compose ps

# Restart services
docker-compose restart

# View logs
docker-compose logs mongodb
docker-compose logs neo4j
docker-compose logs redis
```

### Port Conflicts
If you have port conflicts, modify `docker-compose.yml`:
```yaml
ports:
  - "27018:27017"  # MongoDB
  - "7475:7474"   # Neo4j HTTP
  - "7688:7687"   # Neo4j Bolt
  - "6380:6379"   # Redis
```

## 📊 Use Case: E-commerce Platform

The lab uses an e-commerce platform use case with:
- **User Service** (Neo4j): Social connections & recommendations
- **Product Service** (MongoDB): Flexible product catalog
- **Order Service** (MongoDB): Order management
- **Cache Service** (Redis): Session & performance optimization

## 🎓 Learning Outcomes

After completing this lab, students will:
1. Understand polyglot persistence and database selection criteria
2. Design microservices architecture with proper data boundaries
3. Implement data consistency patterns in distributed systems
4. Optimize performance across multiple database types
5. Setup monitoring for multi-database environments

## 📝 Assessment

- **Technical Implementation (40%)**: Code quality, architecture patterns
- **Architecture Decisions (25%)**: Database selection rationale
- **Performance & Scalability (20%)**: Query optimization, caching
- **Monitoring & Operations (15%)**: Observability, health monitoring
