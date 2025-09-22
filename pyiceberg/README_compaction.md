# Data Compaction & File Management Lab - Apache Iceberg

## 🎯 Lab Overview

This lab demonstrates Apache Iceberg's powerful data compaction and file management capabilities. You'll learn how to solve the **Small File Problem** that commonly affects data lakes and significantly impacts query performance.

## 📚 What You'll Learn

### **Core Concepts:**
- **Small File Problem**: Understanding why small files hurt performance
- **Compaction Strategies**: Different approaches to optimize file sizes
- **File Size Analysis**: Measuring and analyzing file statistics
- **Performance Testing**: Comparing query performance before/after compaction
- **Storage Efficiency**: Reducing costs and improving performance

### **Practical Skills:**
- Creating tables with intentional small files
- Implementing rewrite compaction strategies
- Analyzing file size distributions
- Measuring query performance improvements
- Applying best practices for production

## 🏗️ Lab Structure

### **8 Comprehensive Sections:**

1. **Setup & Imports** - Environment preparation
2. **Warehouse & Catalog** - Iceberg catalog configuration
3. **Dataset Generation** - Creating realistic e-commerce data
4. **Schema & Helpers** - Schema creation and utility functions
5. **Small File Problem** - Demonstrating the small file issue
6. **Compaction Strategies** - Implementing rewrite compaction
7. **Performance Testing** - Measuring query performance improvements
8. **Summary & Best Practices** - Production guidelines and next steps

## 🚀 Getting Started

### **Prerequisites:**
- Python 3.8+
- Conda environment with PyIceberg
- Basic understanding of Apache Iceberg concepts

### **Setup:**
```bash
# Activate the datalab environment
conda activate datalab

# Run the lab
jupyter notebook 4_data_compaction_lab.ipynb
```

### **Expected Runtime:**
- **Setup**: 2-3 minutes
- **Data Generation**: 1-2 minutes
- **Small File Creation**: 3-5 minutes
- **Compaction**: 2-3 minutes
- **Performance Testing**: 2-3 minutes
- **Total**: ~10-15 minutes

## 📊 Lab Dataset

### **E-commerce Sales Data:**
- **100,000 transactions** over 6 months
- **20 fields** including timestamps, categories, amounts
- **Realistic distributions** across regions, categories, and time periods
- **Designed for compaction testing** with varied file sizes

### **Key Fields:**
- `transaction_id`: Unique transaction identifier
- `sale_date`: Date of sale (for time-based analysis)
- `category`: Product category (for categorical analysis)
- `total_amount`: Transaction amount (for amount-based filtering)
- `region`: Geographic region (for geographic analysis)

## 🔧 Compaction Strategies Covered

### **1. Rewrite Compaction:**
- **Purpose**: Merge small files into larger ones
- **Implementation**: Insert all data at once vs. small batches
- **Benefits**: Fewer files, better I/O performance
- **Use Case**: Most common compaction strategy

### **2. File Size Optimization:**
- **Target Size**: 128MB - 1GB per file
- **Minimum Size**: Avoid files < 64KB
- **Maximum Size**: Keep files < 2GB
- **Compression**: Use appropriate compression algorithms

### **3. Performance Analysis:**
- **Query Speed**: Measure execution time improvements
- **File Count**: Track reduction in file count
- **Storage Efficiency**: Monitor storage optimization
- **Memory Usage**: Track memory consumption

## 📈 Expected Results

### **File Statistics:**
```
Before Compaction:
- Total Files: 100+ small files
- Average Size: ~10-50KB per file
- Small Files: 80%+ of total files

After Compaction:
- Total Files: 1-5 large files
- Average Size: ~20-100MB per file
- Small Files: 0% of total files
```

### **Performance Improvements:**
```
Query Performance:
- Full Table Scan: 2-5x faster
- Filtered Queries: 3-10x faster
- Complex Queries: 5-15x faster

File Operations:
- File Count: 20-100x reduction
- I/O Operations: 10-50x reduction
- Metadata Overhead: 50-90% reduction
```

## 🎯 Learning Objectives

### **By the end of this lab, you will:**

✅ **Understand the Small File Problem** and its impact on performance  
✅ **Implement compaction strategies** to optimize file sizes  
✅ **Analyze file statistics** and identify optimization opportunities  
✅ **Measure performance improvements** from compaction  
✅ **Apply best practices** for production data lake management  
✅ **Configure automated compaction** for ongoing optimization  

## 🚨 Common Issues & Solutions

### **Issue 1: Small Files Not Created**
**Problem**: Files are larger than expected  
**Solution**: Reduce batch size in data insertion  
**Code**: Change `batch_size = 1000` to `batch_size = 100`

### **Issue 2: Compaction Not Working**
**Problem**: No improvement in file sizes  
**Solution**: Ensure data is inserted in single operation  
**Code**: Use `table.append(full_table)` instead of multiple batches

### **Issue 3: Performance Results Unclear**
**Problem**: No clear performance difference  
**Solution**: Increase dataset size or use more complex queries  
**Code**: Generate more data with `generate_sales_data(500000)`

## 🔍 Advanced Topics

### **Production Implementation:**
- **Apache Spark**: Use `system.rewrite_data_files()`
- **Trino**: Use `CALL system.rewrite_data_files()`
- **PyIceberg**: Use `table.rewrite_data_files()`

### **Automation Strategies:**
- **Scheduled Compaction**: Run during low-traffic periods
- **Threshold-based**: Trigger when file count exceeds limit
- **Size-based**: Trigger when average file size drops below threshold
- **Time-based**: Run compaction jobs regularly

### **Advanced Compaction:**
- **Bin Packing**: Optimize file sizes for better performance
- **Sort Compaction**: Sort data within files for optimal access
- **Z-Order Compaction**: Optimize for multi-dimensional queries
- **Partition-aware Compaction**: Compaction within partitions

## 📚 Additional Resources

### **Documentation:**
- [Apache Iceberg Compaction](https://iceberg.apache.org/docs/latest/maintenance/)
- [Spark SQL Compaction](https://spark.apache.org/docs/latest/sql-data-sources-iceberg.html#compaction)
- [Trino Iceberg Compaction](https://trino.io/docs/current/connector/iceberg.html#compaction)
- [PyIceberg Compaction](https://py.iceberg.apache.org/operations/compaction/)

### **Related Labs:**
- **Lab 1**: Basic PyIceberg Operations
- **Lab 2**: Advanced Schema Evolution
- **Lab 3**: Data Partitioning Strategies

## 🎉 Next Steps

### **Immediate Actions:**
1. **Run the lab** and experiment with different parameters
2. **Try different batch sizes** to see impact on file creation
3. **Test various compaction strategies** and compare results
4. **Apply to your own data** and measure improvements

### **Production Implementation:**
1. **Identify small file problems** in your data lakes
2. **Implement compaction strategies** for critical tables
3. **Set up automated compaction** for ongoing optimization
4. **Monitor performance improvements** and adjust strategies

### **Advanced Learning:**
1. **Explore other compaction strategies** (bin packing, sort, Z-order)
2. **Implement partition-aware compaction** for partitioned tables
3. **Study compression algorithms** and their impact on performance
4. **Learn about compaction policies** and automation frameworks

**Happy compacting! 🚀**
