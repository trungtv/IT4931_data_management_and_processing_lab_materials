#!/bin/bash

# NoSQL Lab Environment Setup Script
# Install dependencies for NoSQL lab in existing conda environment

set -e  # Exit on any error

echo "🚀 Setting up NoSQL Lab environment..."

# Check if conda environment 'datalab' exists
if ! conda env list | grep -q "^datalab "; then
    echo "❌ Conda environment 'datalab' not found."
    echo "Please run setup_env.sh first to create the base environment."
    exit 1
fi

echo "✅ Found conda environment 'datalab'"

# Install NoSQL dependencies
echo "📦 Installing NoSQL dependencies..."
conda run -n datalab pip install -r requirements.txt

# Verify installations
echo "🔍 Verifying installations..."
conda run -n datalab python -c "
import pymongo
import redis
import neo4j
print('✅ PyMongo version:', pymongo.__version__)
print('✅ Redis-py version:', redis.__version__)
print('✅ Neo4j version:', neo4j.__version__)
print('✅ All NoSQL libraries installed successfully!')
"

echo ""
echo "🎉 NoSQL Lab setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Start databases: docker-compose up -d"
echo "2. Activate environment: conda activate datalab"
echo "3. Open Jupyter: jupyter lab"
echo "4. Start with: notebooks/01_setup_and_connections.ipynb"
echo ""
echo "🔗 Database access:"
echo "- MongoDB: mongodb://admin:password123@localhost:27017"
echo "- Neo4j Browser: http://localhost:7474"
echo "- Redis: redis://localhost:6379"
echo "- Redis Commander: http://localhost:8081"
