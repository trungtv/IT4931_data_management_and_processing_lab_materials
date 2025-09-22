#!/bin/bash

# Kafka Lab Setup Script
echo "🚀 Setting up Kafka Lab environment..."

# Check if conda environment exists
if conda info --envs | grep -q "datalab"; then
    echo "✅ Found datalab conda environment"
else
    echo "❌ datalab conda environment not found. Please create it first."
    exit 1
fi

# Activate conda environment
echo "📦 Activating datalab environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate datalab

# Clean up any existing Kafka packages
echo "🧹 Cleaning up existing Kafka packages..."
pip uninstall -y kafka-python confluent-kafka avro-python3 fastavro || true

# Install requirements
echo "📥 Installing Kafka lab dependencies..."
pip install -r requirements.txt

echo "✅ Kafka Lab setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Start Kafka cluster: docker compose up -d"
echo "2. Start Jupyter Lab: jupyter lab"
echo "3. Open notebooks/01_kafka_basics.ipynb"
echo ""
echo "🌐 Kafka UI: http://localhost:8080"
echo "📊 Schema Registry: http://localhost:8081"
echo "🔌 Kafka Connect: http://localhost:8083"
