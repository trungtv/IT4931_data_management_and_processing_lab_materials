# Time Travel & Versioning Lab - Apache Iceberg

## 🎯 Lab Overview

This lab demonstrates Apache Iceberg's powerful time travel and versioning capabilities. You'll learn how to manage data snapshots, query historical data, and perform rollback operations - essential features for data recovery, auditing, and debugging.

## 📚 What You'll Learn

### **Core Concepts:**
- **Snapshot Management**: Creating and managing data snapshots
- **Time Travel Queries**: Querying data at specific points in time
- **Rollback Operations**: Restoring data to previous versions
- **Version Comparison**: Comparing data between different versions
- **Historical Analysis**: Analyzing data changes over time

### **Practical Skills:**
- Creating multiple snapshots through data operations
- Querying data at specific snapshots and timestamps
- Performing rollback operations to restore previous states
- Comparing data across different versions
- Managing schema evolution with time travel

## 🏗️ Lab Structure

### **8 Comprehensive Sections:**

1. **Setup & Imports** - Environment preparation
2. **Warehouse & Catalog** - Iceberg catalog configuration
3. **Dataset Generation** - Creating evolving customer data
4. **Schema & Initial Table** - Schema creation and initial data load
5. **Snapshot Management** - Creating multiple versions through operations
6. **Time Travel Queries** - Querying historical data at different snapshots
7. **Rollback Operations** - Restoring data to previous versions
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
jupyter notebook 5_time_travel_lab.ipynb
```

### **Expected Runtime:**
- **Setup**: 2-3 minutes
- **Data Generation**: 1-2 minutes
- **Snapshot Creation**: 3-5 minutes
- **Time Travel Queries**: 2-3 minutes
- **Rollback Operations**: 2-3 minutes
- **Total**: ~10-15 minutes

## 📊 Lab Dataset

### **Evolving Customer Data:**
- **1,000+ customers** with realistic profiles
- **19 fields** including personal info, purchase history, and account status
- **Data Evolution** through multiple operations over time
- **Schema Changes** including new column additions

### **Key Fields:**
- `customer_id`: Unique customer identifier
- `customer_segment`: Premium, Standard, Budget, VIP
- `account_status`: Active, Inactive, Suspended, Pending
- `total_spent`: Customer spending amount
- `credit_score`: Added through schema evolution
- `updated_at`: Timestamp for tracking changes

## 🔧 Time Travel Operations Covered

### **1. Snapshot Creation:**
- **Snapshot 1**: Initial customer data (1,000 customers)
- **Snapshot 2**: Added 200 new customers
- **Snapshot 3**: Updated 100 customers to Premium status
- **Snapshot 4**: Deleted inactive customers
- **Snapshot 5**: Added credit_score column through schema evolution

### **2. Time Travel Queries:**
- **Snapshot ID Queries**: Query data at specific snapshot IDs
- **Timestamp Queries**: Query data at specific points in time
- **Historical Comparison**: Compare data across different versions
- **Schema Evolution**: Query data with different schemas

### **3. Rollback Operations:**
- **Data Recovery**: Restore deleted customers
- **Schema Rollback**: Undo schema changes
- **State Restoration**: Restore to any previous state
- **Verification**: Verify rollback success

## 📈 Expected Results

### **Snapshot Evolution:**
```
Snapshot 1: 1,000 customers, 19 columns, original data
Snapshot 2: 1,200 customers, 19 columns, added customers
Snapshot 3: 1,200 customers, 19 columns, updated segments
Snapshot 4: ~900 customers, 19 columns, deleted inactive
Snapshot 5: ~900 customers, 20 columns, added credit_score
```

### **Time Travel Capabilities:**
```
Query Performance:
- Snapshot Queries: Fast access to historical data
- Timestamp Queries: Query data at specific times
- Schema Evolution: Handle different schemas seamlessly
- Rollback Operations: Instant restoration to previous states
```

## 🎯 Learning Objectives

### **By the end of this lab, you will:**

✅ **Understand Snapshot Management** and how each write creates a snapshot  
✅ **Perform Time Travel Queries** to access historical data  
✅ **Execute Rollback Operations** to restore previous states  
✅ **Compare Data Versions** across different snapshots  
✅ **Handle Schema Evolution** with time travel capabilities  
✅ **Apply Best Practices** for production time travel usage  

## 🚨 Common Issues & Solutions

### **Issue 1: Snapshot Not Found**
**Problem**: Snapshot ID doesn't exist  
**Solution**: Check available snapshots with `table.inspect.snapshots()`  
**Code**: Verify snapshot ID before using in queries

### **Issue 2: Schema Mismatch**
**Problem**: Querying snapshot with different schema  
**Solution**: Handle schema evolution gracefully  
**Code**: Check column existence before accessing

### **Issue 3: Rollback Failed**
**Problem**: Rollback operation failed  
**Solution**: Ensure snapshot exists and table is accessible  
**Code**: Verify snapshot ID and table state before rollback

## 🔍 Advanced Topics

### **Production Implementation:**
- **Apache Spark**: Use `VERSION AS OF` and `TIMESTAMP AS OF`
- **Trino**: Use `FOR VERSION AS OF` and `FOR TIMESTAMP AS OF`
- **PyIceberg**: Use `snapshot_id` and `as_of_timestamp` parameters

### **Best Practices:**
- **Snapshot Retention**: Set appropriate retention policies
- **Performance**: Consider performance impact of time travel queries
- **Storage**: Manage storage costs of historical data
- **Monitoring**: Monitor snapshot creation and rollback operations

### **Advanced Features:**
- **Snapshot Expiration**: Configure automatic cleanup
- **Branching**: Create branches for different data versions
- **Tagging**: Tag important snapshots for reference
- **Merge Operations**: Merge branches back to main

## 📚 Additional Resources

### **Documentation:**
- [Apache Iceberg Time Travel](https://iceberg.apache.org/docs/latest/spark-configuration/#time-travel)
- [Spark SQL Time Travel](https://spark.apache.org/docs/latest/sql-data-sources-iceberg.html#time-travel)
- [Trino Iceberg Time Travel](https://trino.io/docs/current/connector/iceberg.html#time-travel)
- [PyIceberg Time Travel](https://py.iceberg.apache.org/operations/time-travel/)

### **Related Labs:**
- **Lab 1**: Basic PyIceberg Operations
- **Lab 2**: Advanced Schema Evolution
- **Lab 3**: Data Partitioning Strategies
- **Lab 4**: Data Compaction & File Management

## 🎉 Next Steps

### **Immediate Actions:**
1. **Run the lab** and experiment with different snapshots
2. **Try different rollback scenarios** and verify results
3. **Test time travel queries** with various filters
4. **Explore schema evolution** with time travel

### **Production Implementation:**
1. **Identify use cases** for time travel in your data lakes
2. **Implement snapshot management** for critical tables
3. **Set up rollback procedures** for data recovery
4. **Monitor time travel operations** and their impact

### **Advanced Learning:**
1. **Explore snapshot expiration** and cleanup strategies
2. **Implement branching and tagging** for complex scenarios
3. **Study performance optimization** for historical queries
4. **Learn about compliance** and audit requirements

**Happy time traveling! ⏰🚀**
