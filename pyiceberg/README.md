# PyIceberg Lab - Apache Iceberg with Python

## 📋 Overview

This lab will guide you through using **PyIceberg** - the official Python library for Apache Iceberg. You will learn how to create, manage, and analyze data with Iceberg tables through Python.

## 🎯 Learning Objectives

After completing this lab, you will be able to:

- ✅ Install and configure PyIceberg
- ✅ Create and manage Iceberg catalogs
- ✅ Create Iceberg tables and manipulate data
- ✅ Perform schema evolution
- ✅ Query and analyze data
- ✅ Understand snapshot management and time travel

## 🚀 Installation

### System Requirements
- Python 3.8+ (recommended Python 3.10)
- Conda or Miniconda
- pip (package manager)

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
├── pyiceberg_lab.ipynb    # Main lab notebook
├── requirements.txt       # Required dependencies
├── setup_env.sh          # Conda environment setup script
└── README.md             # This guide
```

## 🏃‍♂️ Running the Lab

1. **Activate conda environment:**
   ```bash
   conda activate datalab
   ```

2. **Open Jupyter Notebook:**
   ```bash
   jupyter notebook pyiceberg_lab.ipynb
   ```

3. **Select correct kernel:** 
   - In Jupyter Notebook, click **Kernel** → **Change kernel** → **PyIceberg Lab (datalab)**
   - Or click on the top-right corner of the notebook to see current kernel and select new kernel

4. **Run cells sequentially** to understand each step

5. **Experiment** with your own data

### 🚀 Quick Start (one command):
```bash
conda activate datalab && jupyter notebook pyiceberg_lab.ipynb
```

## 📚 Lab Content

### 1. Installation and Import
- Install PyIceberg with dependencies
- Import necessary libraries

### 2. Catalog Configuration
- Create warehouse directory
- Configure SQL catalog with SQLite

### 3. Create Sample Data
- Create namespace
- Prepare sample taxi trip data

### 4. Create Iceberg Table
- Create table from PyArrow schema
- Understand table metadata

### 5. Data Ingestion
- Add data to table
- Use append operations

### 6. Query and Filtering
- Perform basic queries
- Filter data by conditions

### 7. Schema Evolution
- Add new column to table
- Overwrite with new schema

### 8. Snapshot Management
- View snapshot history
- Understand file structure

### 9. Append Operations
- Add new data
- Manage multiple snapshots

### 10. Statistical Analysis
- Overview statistics
- Group analysis
- Top records

### 11. Warehouse Structure
- Explore storage structure
- Understand Iceberg file organization

## 🔧 Key Features of Apache Iceberg

### Schema Evolution
- Add/remove/modify columns without rewriting data
- Backward and forward compatibility

### Time Travel
- Access data at different points in time
- Rollback to previous snapshots

### ACID Transactions
- Ensure data consistency
- Isolation levels

### Partitioning
- Optimize query performance
- Multiple partitioning strategies

### Metadata Management
- Efficient metadata management
- Versioning and lineage

## 🌟 Quick Code Example

```python
from pyiceberg.catalog import load_catalog
import pyarrow as pa

# Configure catalog
catalog = load_catalog(
    "default",
    **{
        'type': 'sql',
        "uri": "sqlite:///warehouse/pyiceberg_catalog.db",
        "warehouse": "file://warehouse",
    },
)

# Create table
table = catalog.create_table(
    "default.my_table",
    schema=pa.schema([
        pa.field("id", pa.int64()),
        pa.field("name", pa.string()),
    ])
)

# Add data
data = pa.table({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"]})
table.append(data)

# Query data
result = table.scan().to_arrow()
print(result.to_pandas())
```

## 🚀 Next Steps

After completing this basic lab, you can:

1. **Experiment with larger datasets**
2. **Configure with cloud storage** (S3, GCS, Azure)
3. **Integrate with query engines** (Spark, Trino, DuckDB)
4. **Implement partitioning strategies**
5. **Optimize performance** with compression and indexing

## 📖 References

- [PyIceberg Documentation](https://py.iceberg.apache.org/)
- [Apache Iceberg Specification](https://iceberg.apache.org/spec/)
- [PyArrow Documentation](https://arrow.apache.org/docs/python/)
- [Apache Iceberg GitHub](https://github.com/apache/iceberg)

## ❓ Troubleshooting

### Common Issues:

1. **Kernel not visible in Jupyter:**
   ```bash
   conda activate datalab
   python -m ipykernel install --user --name=datalab --display-name="PyIceberg Lab (datalab)"
   ```

2. **Import pyiceberg error:**
   - Ensure environment is activated: `conda activate datalab`
   - Check installation: `python -c "import pyiceberg; print(pyiceberg.__version__)"`

3. **Permission error writing to /tmp/:**
   - Create alternative directory: `mkdir ~/pyiceberg_warehouse`
   - Update path in notebook

4. **setup_env.sh script won't run:**
   ```bash
   chmod +x setup_env.sh
   ./setup_env.sh
   ```

### Verification Commands:
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

## 🎉 Conclusion

Congratulations on completing the PyIceberg lab! You have learned the basics of Apache Iceberg and how to use it with Python. Continue exploring and experimenting with advanced features!

---
*Lab created by AI Assistant with Context7 documentation*
