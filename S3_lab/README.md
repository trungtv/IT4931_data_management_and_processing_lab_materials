# S3 Lab - Object Storage với Amazon S3 & MinIO

Bài chạy được nằm ở `lab/s3_course.py` và notebook `01`–`04`: key, `head_bucket`, SDK ghi/đọc/xóa, và key metadata snapshot. Multipart vẫn ở `exercises/layout.py`.

## 📋 Overview

Bài lab giới thiệu **object storage** thông qua **Amazon S3** (AWS) và **MinIO** – công cụ lưu trữ object S3-compatible chạy được on-premise hoặc trên Docker. Học viên sẽ nắm khái niệm bucket/object, API S3, và cách dùng MinIO để mô phỏng S3 trong môi trường lab (triển khai bằng Docker).

## 🎯 Learning Objectives

Sau khi hoàn thành lab này, bạn sẽ có thể:

- ✅ Hiểu khái niệm **object storage** và so sánh với file system / block storage
- ✅ Nắm **Amazon S3** cơ bản: buckets, objects, keys, regions, consistency
- ✅ Cài đặt và chạy **MinIO** bằng Docker (S3-compatible API)
- ✅ Sử dụng **MinIO Console** (Web UI) để quản lý buckets và objects
- ✅ Gọi **S3 API** (hoặc SDK) để upload/download/list/delete objects
- ✅ Cấu hình client (AWS CLI, boto3, hoặc SDK khác) kết nối tới MinIO
- ✅ Áp dụng kiến thức S3/MinIO cho các lab khác (Kafka, Iceberg, Lakehouse…)

## 📚 Lab Structure

### **Lab 1: Object Storage & S3 Fundamentals** → `01_s3_fundamentals.ipynb`
- **Focus**: Object storage là gì, so sánh với file/block storage
- **Skills**: Khái niệm bucket, object, key, versioning, consistency model
- **Use Case**: Khi nào dùng S3, use case trong data engineering

### **Lab 2: MinIO với Docker** → `02_minio_docker.ipynb`
- **Focus**: Chạy MinIO trong Docker, MinIO Console
- **Skills**: `docker compose` up/down, tạo bucket, upload/download qua UI
- **Use Case**: Môi trường lab S3-compatible không cần AWS account

### **Lab 3: S3 API & SDK** → `03_s3_api_sdk.ipynb`
- **Focus**: REST API S3, boto3 kết nối MinIO
- **Skills**: Endpoint override, credentials, PutObject/GetObject/ListObjects
- **Use Case**: Tự động hóa upload/download từ script/notebook

### **Lab 4: Ứng dụng trong Data Pipeline** → `04_data_pipeline_integration.ipynb`
- **Focus**: Dùng MinIO/S3 làm storage backend cho công cụ khác
- **Skills**: s3fs, cấu hình Spark/Iceberg trỏ tới MinIO
- **Use Case**: Data lake, staging area, checkpoint storage

## 📁 File Structure

```
S3_lab/
├── 01_s3_fundamentals.ipynb
├── 02_minio_docker.ipynb
├── 03_s3_api_sdk.ipynb
├── 04_data_pipeline_integration.ipynb
├── docker-compose.yml
├── requirements.txt
├── setup_s3_lab.sh
└── README.md
```

## 🚀 Quick Start

### 1. Yêu cầu hệ thống
- Docker và Docker Compose
- Python 3.8+ (boto3, s3fs)
- Trình duyệt (MinIO Console)

### 2. Cài đặt môi trường Python
```bash
cd S3_lab
chmod +x setup_s3_lab.sh
./setup_s3_lab.sh
```

### 3. Khởi động MinIO
```bash
# Từ thư mục S3_lab
docker compose up -d

# Kiểm tra service
docker compose ps
```

### 4. Truy cập MinIO Console
- **URL**: http://localhost:9001
- **Credentials**: `minioadmin` / `minioadmin`

### 5. S3 API endpoint
- **Endpoint**: http://localhost:9000

### 6. Chạy bài lab
```bash
conda activate datalab
jupyter lab
```
Mở lần lượt: `01_s3_fundamentals.ipynb` → `04_data_pipeline_integration.ipynb`

## 🏗️ Architecture

### **Services trong Docker**
| Service | Port | Mô tả |
|--------|------|--------|
| **MinIO Server** | 9000 | S3 API (REST) – dùng cho mọi client S3-compatible |
| **MinIO Console** | 9001 | Giao diện web quản lý buckets, objects, policies |

### **MinIO so với AWS S3**
- **Giống**: API S3 (PutObject, GetObject, ListBuckets, ListObjectsV2…), khái niệm bucket/object/key
- **Khác**: MinIO chạy single node / cluster on-prem, không có toàn bộ dịch vụ AWS (IAM, CloudFront…); phù hợp dev/test và lab

### **Data flow (minh họa)**
```
Client (CLI/SDK/Spark/Iceberg)
         │
         ▼
   MinIO (port 9000)  ←→  S3-compatible API
         │
         ▼
   Buckets / Objects (persistent volume trong Docker)
```

## 📊 Khái niệm chính

### **Object storage**
- **Bucket**: Container lưu objects (tương tự “thư mục gốc”), tên global unique (trong MinIO là unique trong một server)
- **Object**: Dữ liệu + metadata (key, size, content-type, custom metadata)
- **Key**: Tên/đường dẫn của object trong bucket (có thể có “prefix” giống thư mục, vd: `data/2024/01/file.parquet`)

### **S3 API (dùng với MinIO)**
- CreateBucket, ListBuckets
- PutObject, GetObject, DeleteObject
- ListObjectsV2 (list với prefix, pagination)
- Optional: multipart upload, versioning (tùy bài lab sau)

### **Kết nối client tới MinIO**
- **Endpoint**: `http://localhost:9000` (hoặc `http://minio:9000` từ container khác trong cùng Docker network)
- **Access Key / Secret Key**: mặc định `minioadmin` / `minioadmin`
- **Region**: có thể để `us-east-1` hoặc bất kỳ (MinIO không enforce region)
- **Path-style**: nhiều client cần bật path-style khi dùng MinIO (vd: `s3://localhost:9000/bucket/key`)

## 🔧 Configuration

### **Docker Compose**
- Image: `minio/minio:latest`
- Command: `server /data --console-address ":9001"`
- Ports: `9000:9000`, `9001:9001`
- Volume: `minio_data` persist `/data`
- Environment: `MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD` (mặc định minioadmin/minioadmin)

### **Client (boto3)**
```python
endpoint_url = "http://localhost:9000"
aws_access_key_id = "minioadmin"
aws_secret_access_key = "minioadmin"
region = "us-east-1"
# signature_version="s3v4" khi dùng boto3
```

## 🐛 Troubleshooting

### **MinIO không start**
- Kiểm tra port 9000, 9001 đã bị chiếm chưa
- Xem log: `docker compose logs minio`

### **Client không kết nối được**
- Kiểm tra endpoint (localhost vs minio hostname trong Docker network)
- Kiểm tra credentials và path-style/virtual-hosted style
- Nếu chạy client trong container: dùng hostname `minio` thay vì `localhost`

### **Console không mở**
- Đảm bảo map port 9001: `ports: - "9001:9001"`
- Thử http://127.0.0.1:9001

## 📚 Learning Resources

- [Amazon S3 Developer Guide](https://docs.aws.amazon.com/s3/)
- [MinIO Documentation](https://min.io/docs/minio/linux/index.html)
- [MinIO Docker](https://min.io/docs/minio/container/index.html)
- [S3 API Reference](https://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html)
- [boto3 S3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)

## 🎯 Learning Outcomes

Sau khi hoàn thành toàn bộ lab, học viên có thể:

1. **Khái niệm**: Giải thích object storage, bucket/object/key, và khi nào dùng S3/MinIO
2. **MinIO**: Chạy MinIO bằng Docker, dùng Console để tạo bucket, upload/download
3. **API/SDK**: Dùng AWS CLI hoặc boto3 (hoặc SDK khác) kết nối MinIO, thực hiện Put/Get/List
4. **Tích hợp**: Cấu hình một công cụ (vd: Spark, Iceberg, Kafka Connect) dùng MinIO làm S3 backend

## 📋 Assessment Criteria

- **Mức cơ bản**: Hoàn thành Lab 1–2, hiểu object storage và dùng được MinIO Console
- **Mức trung bình**: Hoàn thành Lab 3, gọi S3 API/SDK từ code
- **Mức nâng cao**: Hoàn thành Lab 4, tích hợp MinIO vào pipeline (Spark/Iceberg/…)

## 🔗 Liên quan với các lab khác

- **Streaming Lakehouse Lab / Data Lakehouse Lab**: MinIO có thể dùng làm S3 backend cho Iceberg
- **PyIceberg Lab**: Có thể cấu hình catalog với `s3://` warehouse trỏ tới MinIO
- **Kafka Lab / Airflow Lab**: Có thể lưu checkpoint hoặc artifact trên S3/MinIO

---

*S3 Lab – Object storage với Amazon S3 & MinIO, triển khai Docker + 4 notebook.*
