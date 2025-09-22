# Advanced Schema Evolution Lab - Apache Iceberg

## 📋 Overview

This advanced lab explores the sophisticated schema evolution capabilities of Apache Iceberg, focusing on real-world scenarios and complex data structures commonly found in modern data platforms.

## 🎯 Learning Objectives

After completing this lab, you will be able to:

- ✅ **Master Complex Schema Evolution**: Add/remove/modify multiple columns simultaneously
- ✅ **Handle Nested Schema Evolution**: Work with Struct, Array, and Map evolution strategies
- ✅ **Implement Field Evolution**: Rename fields, change types, and modify nullable constraints
- ✅ **Ensure Compatibility**: Maintain backward/forward compatibility across schema versions
- ✅ **Measure Performance Impact**: Understand and measure the performance implications of schema changes
- ✅ **Apply Real-world Patterns**: Use schema evolution in e-commerce, IoT, and financial scenarios

## 🏗️ Schema Evolution Architecture

### Core Principles

- **Additive Changes**: Adding new columns (always safe)
- **Non-breaking Changes**: Making nullable, widening types
- **Breaking Changes**: Removing columns, narrowing types (requires caution)
- **Nested Evolution**: Struct fields can evolve independently

### Compatibility Matrix

| Change Type | Backward Compatible | Forward Compatible | Safe |
|-------------|-------------------|-------------------|------|
| Add column | ✅ | ✅ | ✅ |
| Make nullable | ✅ | ✅ | ✅ |
| Widen type | ✅ | ✅ | ✅ |
| Rename field | ❌ | ❌ | ⚠️ |
| Delete field | ❌ | ✅ | ⚠️ |
| Narrow type | ✅ | ❌ | ⚠️ |

## 🚀 Prerequisites

### Required Knowledge
- Basic understanding of Apache Iceberg
- Familiarity with PyArrow and Pandas
- Python programming experience
- Understanding of data schemas and types

### System Requirements
- Python 3.8+ (recommended Python 3.10)
- Conda or Miniconda
- 4GB+ RAM available
- 2GB+ disk space

## 📦 Installation

### Option 1: Using Conda Environment (Recommended)

```bash
# Make setup script executable
chmod +x setup_env.sh

# Run automated setup
./setup_env.sh
```

The script will:
- Create conda environment named `datalab` with Python 3.10
- Install all dependencies from `requirements.txt`
- Register kernel with Jupyter
- Verify installation success

### Option 2: Manual Installation

```bash
# Create conda environment
conda create -n datalab python=3.10 -y
conda activate datalab

# Install dependencies
pip install -r requirements.txt

# Register kernel with Jupyter
python -m ipykernel install --user --name=datalab --display-name="PyIceberg Lab (datalab)"
```

## 📁 File Structure

```
materials/
├── advanced_schema_evolution_lab.ipynb  # Main advanced lab notebook
├── pyiceberg_lab.ipynb                 # Basic PyIceberg lab
├── requirements.txt                    # Dependencies
├── setup_env.sh                       # Environment setup script
└── README.md                          # This guide
```

## 🏃‍♂️ Running the Lab

1. **Activate conda environment:**
   ```bash
   conda activate datalab
   ```

2. **Open Jupyter Notebook:**
   ```bash
   jupyter notebook advanced_schema_evolution_lab.ipynb
   ```

3. **Select correct kernel:** In Jupyter, choose kernel "PyIceberg Lab (datalab)"

4. **Run cells sequentially** to understand each concept

5. **Experiment** with your own data and scenarios

### 🚀 Quick Start (one command):
```bash
conda activate datalab && jupyter notebook advanced_schema_evolution_lab.ipynb
```

## 📚 Lab Content

### 1. Setup and Environment
- Library imports and configuration
- Warehouse and catalog setup
- Environment verification

### 2. Complex Dataset Creation
- E-commerce product data generation
- Nested structures (structs, arrays, maps)
- Realistic data patterns

### 3. Complex Schema Definition
- Multi-level nested schemas
- Array and map types
- Field ID management

### 4. Advanced Schema Evolution Patterns
- **Additive Evolution**: Adding new fields
- **Nested Evolution**: Modifying struct fields
- **Array Evolution**: Changing array element types
- **Field Renaming**: Safe and unsafe patterns

### 5. Compatibility Testing
- Backward compatibility verification
- Forward compatibility testing
- Migration strategies

### 6. Performance Analysis
- Schema evolution impact measurement
- Query performance comparison
- Storage efficiency analysis

### 7. Real-world Scenarios
- E-commerce platform evolution
- IoT sensor data schema changes
- Financial data compliance updates

## 🔧 Advanced Features Covered

### Schema Evolution Types
- **Column Addition**: Safe additive changes
- **Type Widening**: Int32 → Int64, String → String
- **Nullable Changes**: Required → Optional
- **Nested Modifications**: Struct field evolution
- **Array Evolution**: Element type changes

### Performance Optimization
- **File Size Optimization**: Compression strategies
- **Query Performance**: Predicate pushdown
- **Storage Efficiency**: Columnar storage benefits
- **Metadata Management**: Efficient schema tracking

### Real-world Patterns
- **E-commerce**: Product catalog evolution
- **IoT Data**: Sensor schema versioning
- **Financial**: Compliance-driven changes
- **Analytics**: Metrics schema evolution

## 🎯 Use Cases

### E-commerce Platform
- Product catalog with nested attributes
- Customer behavior tracking
- Order processing and analytics
- Review and rating systems

### IoT Sensor Network
- Temperature, humidity, pressure sensors
- High-frequency data ingestion
- Time-series data management
- Device metadata evolution

### Financial Trading System
- Market data and trade records
- Real-time requirements
- Compliance and audit trails
- Risk management data

## ❓ Troubleshooting

### Common Issues

1. **Kernel not visible in Jupyter:**
   ```bash
   conda activate datalab
   python -m ipykernel install --user --name=datalab --display-name="PyIceberg Lab (datalab)"
   ```

2. **Import errors:**
   - Ensure environment is activated: `conda activate datalab`
   - Check installation: `python -c "import pyiceberg; print(pyiceberg.__version__)"`

3. **Permission errors for /tmp/:**
   - Create alternative directory: `mkdir ~/iceberg_warehouse`
   - Update path in notebook

4. **Schema evolution errors:**
   - Always update schema before adding data with new columns
   - Use `table.update_schema().add_column().commit()` first

### Verification Commands
```bash
conda activate datalab
python -c "
import pyiceberg
import pyarrow as pa
import pandas as pd
print('✅ PyIceberg:', pyiceberg.__version__)
print('✅ PyArrow:', pa.__version__)
print('✅ Pandas:', pd.__version__)
"
```

## 📖 Additional Resources

- [PyIceberg Documentation](https://py.iceberg.apache.org/)
- [Apache Iceberg Specification](https://iceberg.apache.org/spec/)
- [PyArrow Documentation](https://arrow.apache.org/docs/python/)
- [Apache Iceberg GitHub](https://github.com/apache/iceberg)

## 🎉 Next Steps

After completing this advanced lab, consider exploring:

1. **Partitioning Strategies Lab**: Advanced partitioning techniques
2. **Multi-Engine Integration Lab**: Spark, Trino, DuckDB integration
3. **Performance Optimization Lab**: Query and storage optimization
4. **Real-time Data Pipeline Lab**: Streaming data with Iceberg
5. **ML Feature Store Lab**: Machine learning feature management

## 🤝 Contributing

Found an issue or want to improve the lab? Please:
1. Check existing issues
2. Create detailed bug reports
3. Suggest enhancements
4. Contribute improvements

---

*This advanced lab was created to demonstrate the sophisticated schema evolution capabilities of Apache Iceberg in real-world scenarios.*
