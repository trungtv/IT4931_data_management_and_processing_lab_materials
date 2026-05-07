#!/bin/bash
set -euo pipefail

# Kafka Lab Setup Script
echo "🚀 Setting up Kafka Lab environment..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"
PYTHON_BIN="/Users/trungtv/miniforge3/envs/datalab/bin/python"

# Check if conda environment exists
if conda info --envs | grep -q "datalab"; then
    echo "✅ Found datalab conda environment"
else
    echo "❌ datalab conda environment not found. Please create it first."
    exit 1
fi

# Verify requirements file
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo "❌ requirements.txt not found at: $REQUIREMENTS_FILE"
    exit 1
fi

if [ ! -x "$PYTHON_BIN" ]; then
    echo "❌ Python interpreter not found at: $PYTHON_BIN"
    exit 1
fi

echo "🐍 Using Python: $PYTHON_BIN"

# Clean up any existing Kafka packages
echo "🧹 Cleaning up existing Kafka packages..."
"$PYTHON_BIN" -m pip uninstall -y kafka-python confluent-kafka avro-python3 avro fastavro || true

# Install requirements
echo "📥 Installing Kafka lab dependencies..."
PYTHONNOUSERSITE=1 "$PYTHON_BIN" -m pip install --no-user -r "$REQUIREMENTS_FILE"

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
