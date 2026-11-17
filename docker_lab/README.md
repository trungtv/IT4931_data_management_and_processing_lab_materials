# Docker Lab - Container Fundamentals

Bài chấm được nằm ở `exercises/image_review.py` và notebook `06_layer_cache_and_image_review.ipynb`: đếm layer phải build lại, và soát Dockerfile của image Airflow.

## 📋 Overview

Notebook 1–5 gọi `exercises/image_review.py` trên `platform/airflow/Dockerfile`. Image này phải không còn lỗi `unpinned_base`, `add_instead_of_copy`, `runs_as_root`, `apt_lists_kept`, `pip_cache_kept`. Không kéo `alpine:latest`.

## 🎯 Learning Objectives

Sau khi hoàn thành lab này, bạn sẽ có thể:

- ✅ Hiểu **container** là gì và so sánh với VM
- ✅ Chạy container từ image: `docker run`, `docker ps`, `docker logs`
- ✅ Viết **Dockerfile** và build image
- ✅ Dùng **Docker Compose** để định nghĩa multi-container stack
- ✅ Làm việc với **networks** và **volumes**
- ✅ Áp dụng best practices: layer tối ưu, multi-stage build, security cơ bản
- ✅ Chuẩn bị nền tảng cho Kubernetes Lab và các lab khác (Kafka, S3, Airflow)

## 📚 Lab Structure

### **Lab 1: Docker Fundamentals** → `01_docker_fundamentals.ipynb`
- **Focus**: Image, container, registry; chạy container cơ bản
- **Skills**: `docker run`, `docker ps`, `docker logs`, `docker exec`, `docker stop/rm`
- **Use Case**: Chạy service (nginx, redis) và tương tác từ host

### **Lab 2: Dockerfile & Build** → `02_dockerfile_build.ipynb`
- **Focus**: Viết Dockerfile, build image, hiểu layers
- **Skills**: FROM, RUN, COPY, ADD, CMD, ENTRYPOINT; `docker build`; multi-stage build
- **Use Case**: Đóng gói ứng dụng Python/Node thành image

### **Lab 3: Docker Compose** → `03_docker_compose.ipynb`
- **Focus**: Định nghĩa multi-service với Compose
- **Skills**: `docker compose up/down`, services, ports, env, depends_on
- **Use Case**: Stack gồm app + database + cache (giống Kafka lab, S3 lab)

### **Lab 4: Networks & Volumes** → `04_networks_volumes.ipynb`
- **Focus**: Network driver, volume persist data
- **Skills**: `docker network`, `docker volume`; compose networks/volumes
- **Use Case**: Container giao tiếp với nhau, dữ liệu không mất khi restart

### **Lab 5: Best Practices & Integration** → `05_best_practices.ipynb`
- **Focus**: Layer tối ưu, security cơ bản, tích hợp với các lab khác
- **Skills**: Giảm kích thước image, non-root user, .dockerignore; liên kết với Kafka/S3/Airflow lab
- **Use Case**: Production-ready Docker và chuẩn bị cho K8s

## 📁 File Structure

```
Docker_lab/
├── 01_docker_fundamentals.ipynb
├── 02_dockerfile_build.ipynb
├── 03_docker_compose.ipynb
├── 04_networks_volumes.ipynb
├── 05_best_practices.ipynb
├── examples/
│   ├── Dockerfile.simple
│   ├── Dockerfile.multistage
│   └── docker-compose.demo.yml
├── setup_docker_lab.sh
└── README.md
```

## 🚀 Quick Start

### 1. Yêu cầu hệ thống
- **Docker Engine** (Desktop hoặc CE)
- **Docker Compose** v2+ (thường đi kèm Docker Desktop)
- Hệ điều hành: Linux, macOS, hoặc Windows (WSL2)

### 2. Cài đặt Docker

**macOS / Windows:**  
Tải [Docker Desktop](https://www.docker.com/products/docker-desktop/) và cài đặt.

**Linux (Ubuntu/Debian):**
```bash
# Install Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Đăng xuất/đăng nhập lại để áp dụng group
```

### 3. Kiểm tra cài đặt
```bash
docker --version
docker compose version
docker run hello-world
```

### 4. Chạy bài lab (Jupyter)
```bash
cd Docker_lab
chmod +x setup_docker_lab.sh
./setup_docker_lab.sh   # Kiểm tra Docker, tạo env nếu cần

conda activate datalab   # hoặc python env của bạn
jupyter lab
```
Mở lần lượt: `01_docker_fundamentals.ipynb` → `05_best_practices.ipynb`. Các cell chạy lệnh shell (`!docker ...` hoặc `%%bash`).

### 5. Lưu ý
- Một số lệnh cần **Docker daemon** đang chạy (Docker Desktop phải bật trên Mac/Windows).
- Trên Linux, user cần nằm trong group `docker` hoặc dùng `sudo` cho lệnh docker.

## 🏗️ Architecture

### **Docker kiến trúc cơ bản**
```
┌─────────────────────────────────────────────────────────┐
│  Docker Client (CLI: docker, docker compose)             │
└─────────────────────────┬───────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  Docker Daemon (dockerd)                                 │
│  - Images, Containers, Networks, Volumes                 │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  Container Runtime (containerd / runc)                   │
│  - Namespaces, cgroups, Union FS                         │
└─────────────────────────────────────────────────────────┘
```

### **Image vs Container**
- **Image**: Template read-only (layers). VD: `nginx:alpine`, `python:3.10-slim`.
- **Container**: Instance đang chạy từ image (có writable layer trên cùng).

### **Liên quan với các lab khác**
- **Kafka_lab**, **S3_lab**, **Airflow_lab**: Dùng `docker compose` để chạy broker, MinIO, Airflow.
- **K8s_Basics_lab**: Kubernetes chạy container (image build từ Dockerfile); hiểu Docker trước khi học K8s.

## 📖 Key Concepts

### Lệnh Docker cơ bản
```bash
# Image
docker pull <image>
docker images
docker rmi <image>

# Container
docker run -d --name myapp -p 8080:80 nginx:alpine
docker ps
docker logs myapp
docker exec -it myapp sh
docker stop myapp
docker rm myapp

# Build
docker build -t myimage:tag .

# Compose
docker compose up -d
docker compose down
docker compose ps
```

### Docker Compose (YAML)
- **services**: Mỗi service = một container (image, ports, env, volumes).
- **networks**: Container cùng network gọi nhau qua tên service.
- **volumes**: Persist data (named volume hoặc bind mount).

## 🐛 Troubleshooting

### Docker daemon không chạy
- **Mac/Windows**: Mở Docker Desktop và đợi icon sáng.
- **Linux**: `sudo systemctl start docker` và `sudo systemctl enable docker`.

### Permission denied (Linux)
```bash
sudo usermod -aG docker $USER
# Đăng xuất và đăng nhập lại
```

### Port đã được sử dụng
- Đổi port map: `-p 8081:80` thay vì `-p 80:80`.
- Hoặc tắt process đang chiếm port: `lsof -i :80` rồi kill.

### Container thoát ngay (exit 0)
- Chạy với `-it` để giữ stdin mở: `docker run -it alpine sh`.
- Kiểm tra CMD/ENTRYPOINT trong image có process chạy lâu dài không.

### Build chậm / hết dung lượng
- Dọn image/container không dùng: `docker system prune -a` (cẩn thận xóa hết).
- Dùng `.dockerignore` để bỏ file không cần vào build context.

## 📋 Assessment Criteria

- **Mức cơ bản**: Hoàn thành Lab 1–2; chạy container, build image từ Dockerfile.
- **Mức trung bình**: Hoàn thành Lab 3–4; viết docker-compose với nhiều service, dùng network và volume.
- **Mức nâng cao**: Hoàn thành Lab 5; áp dụng best practices và hiểu cách các lab Kafka/S3/Airflow dùng Docker.

## 📚 Learning Resources

- [Docker Documentation](https://docs.docker.com/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Compose Specification](https://docs.docker.com/compose/compose-file/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## 🔗 Liên quan với các lab khác

- **S3_lab**, **Kafka_lab**, **Airflow_lab**: Chạy services bằng `docker compose`; hiểu Compose giúp chỉnh sửa và debug dễ hơn.
- **K8s_Basics_lab**: Prerequisite – Kubernetes quản lý container; image thường build bằng Docker.

---

*Docker Lab – Nền tảng container cho toàn bộ hệ thống bài lab Big Data.*
