# Data Partitioning Lab - Apache Iceberg Performance Optimization

## 🎯 Lab Objectives

In this lab, we will explore Apache Iceberg's powerful partitioning capabilities to optimize query performance and storage efficiency:

1. **Partition Strategies**: Learn different partitioning approaches
2. **Performance Testing**: Measure query performance improvements
3. **Real-world Scenarios**: Apply partitioning to realistic datasets
4. **Best Practices**: Understand partitioning guidelines and trade-offs
5. **Storage Optimization**: Optimize file sizes and storage costs

## 🏗️ Partitioning Architecture

### Iceberg Partitioning Types:
- **Identity Partitions**: Direct column partitioning
- **Bucket Partitions**: Hash-based partitioning
- **Truncate Partitions**: String truncation partitioning
- **Hidden Partitions**: Computed column partitioning

### Performance Benefits:
- **Partition Pruning**: Skip irrelevant data files
- **Query Acceleration**: Faster data access
- **Storage Efficiency**: Better file organization
- **Cost Reduction**: Reduced scan costs

## 📊 Dataset: Multi-Dimensional E-commerce Data

We will work with comprehensive e-commerce data including:
- **Sales Transactions**: Time-series sales data
- **Product Catalog**: Hierarchical product information
- **Customer Data**: Geographic and demographic data
- **Performance Metrics**: Query timing and optimization

## 🚀 Prerequisites

### Required Knowledge
- Basic understanding of Apache Iceberg
- Familiarity with PyArrow and Pandas
- Understanding of data partitioning concepts
- Python programming experience

### System Requirements
- Python 3.8+ (recommended Python 3.10)
- Conda environment `datalab` (from previous labs)
- 4GB+ RAM available
- 2GB+ disk space

## 📦 Installation

### Using Existing Environment
```bash
# Activate existing conda environment
conda activate datalab

# Verify PyIceberg installation
python -c "import pyiceberg; print('✅ PyIceberg version:', pyiceberg.__version__)"
```

### Additional Dependencies
```bash
# Install additional packages for performance testing
pip install psutil memory-profiler
```

## 📁 File Structure

```
materials/
├── data_partitioning_lab.ipynb     # Main partitioning lab notebook
├── pyiceberg_lab.ipynb            # Basic PyIceberg lab
├── advanced_schema_evolution_lab.ipynb  # Advanced schema lab
├── requirements.txt               # Dependencies
├── setup_env.sh                  # Environment setup script
└── README.md                     # Basic lab documentation
```

## 🏃‍♂️ Running the Lab

1. **Activate conda environment:**
   ```bash
   conda activate datalab
   ```

2. **Open Jupyter Notebook:**
   ```bash
   jupyter notebook data_partitioning_lab.ipynb
   ```

3. **Select correct kernel:** Choose "PyIceberg Lab (datalab)"

4. **Run cells sequentially** to understand each partitioning concept

5. **Experiment** with different partitioning strategies

### 🚀 Quick Start:
```bash
conda activate datalab && jupyter notebook data_partitioning_lab.ipynb
```

## 📚 Lab Content

### 1. Setup and Data Generation
- Environment configuration
- Generate realistic e-commerce dataset
- Create time-series sales data

### 2. Unpartitioned Baseline
- Create unpartitioned table
- Measure baseline performance
- Establish performance benchmarks

### 3. Date Partitioning
- Implement daily partitioning
- Monthly partitioning strategies
- Query performance comparison

### 4. Category Partitioning
- Product category partitioning
- Hierarchical partitioning
- Multi-level partition strategies

### 5. Bucket Partitioning
- Hash-based partitioning
- Bucket sizing optimization
- Even data distribution

### 6. Multi-Dimensional Partitioning
- Combined partitioning strategies
- Partition interaction effects
- Complex query optimization

### 7. Performance Analysis
- Query timing measurements
- File size analysis
- Storage efficiency metrics

### 8. Real-world Scenarios
- E-commerce analytics queries
- Time-series analysis
- Customer segmentation

### 9. Best Practices
- Partition sizing guidelines
- Query optimization tips
- Maintenance strategies

### 10. Advanced Techniques
- Hidden partitions
- Partition evolution
- Dynamic partitioning

## 🔧 Key Partitioning Features Covered

### Partition Types
- **Identity**: Direct column partitioning
- **Bucket**: Hash-based distribution
- **Truncate**: String prefix partitioning
- **Hidden**: Computed column partitioning

### Performance Optimization
- **Partition Pruning**: Automatic data skipping
- **File Organization**: Optimal file layout
- **Query Acceleration**: Faster data access
- **Storage Efficiency**: Reduced storage costs

### Real-world Applications
- **E-commerce**: Sales data partitioning
- **IoT**: Time-series sensor data
- **Analytics**: Multi-dimensional analysis
- **Data Lakes**: Large-scale data organization

## 🌟 Quick Partitioning Example

```python
from pyiceberg.catalog import load_catalog
from pyiceberg.partitioning import PartitionSpec, PartitionField
from pyiceberg.transforms import IdentityTransform, BucketTransform

# Configure catalog
catalog = load_catalog("default", **{
    'type': 'sql',
    "uri": "sqlite:///warehouse/catalog.db",
    "warehouse": "file://warehouse",
})

# Create partitioned table
table = catalog.create_table(
    "default.sales_partitioned",
    schema=sales_schema,
    partition_spec=PartitionSpec(
        PartitionField(1, "sale_date", IdentityTransform()),
        PartitionField(2, "category", BucketTransform(10))
    )
)

# Query with partition pruning
result = table.scan(
    row_filter="sale_date >= '2023-01-01' AND category = 'Electronics'"
).to_arrow()
```

## 🚀 Next Steps

After completing this partitioning lab, consider exploring:

1. **Time Travel Lab**: Snapshot management and versioning
2. **Cloud Integration Lab**: S3, GCS, Azure storage
3. **Multi-Engine Lab**: Spark, Trino, DuckDB integration
4. **Real-time Pipeline Lab**: Streaming data ingestion
5. **Performance Tuning Lab**: Advanced optimization techniques

## 📖 Additional Resources

- [Iceberg Partitioning Documentation](https://iceberg.apache.org/docs/latest/partitioning/)
- [PyIceberg Partitioning Guide](https://py.iceberg.apache.org/partitioning/)
- [Query Performance Optimization](https://iceberg.apache.org/docs/latest/query-planning/)
- [Storage Optimization Best Practices](https://iceberg.apache.org/docs/latest/storage/)

## ❓ Troubleshooting

### Common Issues

1. **Partition pruning not working:**
   - Check filter conditions match partition columns
   - Verify partition spec configuration
   - Use appropriate data types

2. **Query performance issues:**
   - Analyze query execution plans
   - Check partition statistics
   - Consider partition sizing

3. **Storage space concerns:**
   - Monitor partition sizes
   - Implement partition cleanup
   - Use appropriate compression

### Performance Verification
```bash
# Check partition statistics
python -c "
import pyiceberg
table = catalog.load_table('default.sales_partitioned')
print('Partition spec:', table.spec())
print('Partition stats:', table.inspect.partitions())
"
```

## 🎉 Conclusion

Congratulations on completing the Data Partitioning Lab! You have learned how to optimize Apache Iceberg performance through strategic partitioning. Continue exploring advanced features and real-world applications!

---
*Lab created by AI Assistant with comprehensive partitioning strategies*
