#!/bin/bash

# PyIceberg Lab Environment Setup Script
# Tạo và cấu hình môi trường conda cho bài lab PyIceberg

set -e  # Exit on any error

echo "🚀 Bắt đầu setup môi trường conda cho PyIceberg Lab..."

# Kiểm tra conda có được cài đặt không
if ! command -v conda &> /dev/null; then
    echo "❌ Conda chưa được cài đặt. Vui lòng cài đặt Anaconda hoặc Miniconda trước."
    echo "📥 Tải về tại: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo "✅ Conda đã được cài đặt"

# Tên môi trường
ENV_NAME="datalab"

# Kiểm tra xem môi trường đã tồn tại chưa
if conda env list | grep -q "^${ENV_NAME} "; then
    echo "⚠️  Môi trường '${ENV_NAME}' đã tồn tại."
    read -p "Bạn có muốn xóa và tạo lại không? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Xóa môi trường cũ..."
        conda env remove -n ${ENV_NAME} -y
    else
        echo "📦 Cập nhật môi trường hiện tại..."
        conda run -n ${ENV_NAME} pip install -r requirements.txt
        conda run -n ${ENV_NAME} pip install jupyter jupyterlab ipykernel
        conda run -n ${ENV_NAME} python -m ipykernel install --user --name=${ENV_NAME} --display-name="PyIceberg Lab (${ENV_NAME})"
        echo "✅ Cập nhật hoàn tất!"
        exit 0
    fi
fi

# Tạo môi trường mới với Python 3.10
echo "🐍 Tạo môi trường conda mới với Python 3.10..."
conda create -n ${ENV_NAME} python=3.10 -y

# Cài đặt pip và upgrade
echo "📦 Cài đặt và upgrade pip..."
conda install -n ${ENV_NAME} pip -y
conda run -n ${ENV_NAME} pip install --upgrade pip

# Cài đặt các thư viện từ requirements.txt
echo "📚 Cài đặt các thư viện từ requirements.txt..."
conda run -n ${ENV_NAME} pip install -r requirements.txt

# Cài đặt thêm Jupyter notebook và extensions
echo "📓 Cài đặt Jupyter notebook và extensions..."
conda run -n ${ENV_NAME} pip install jupyter jupyterlab ipykernel

# Đăng ký kernel với Jupyter
echo "🔗 Đăng ký kernel với Jupyter..."
conda run -n ${ENV_NAME} python -m ipykernel install --user --name=${ENV_NAME} --display-name="PyIceberg Lab (${ENV_NAME})"

# Kiểm tra cài đặt
echo "🔍 Kiểm tra cài đặt..."
conda run -n ${ENV_NAME} python -c "
import pyiceberg
import pyarrow as pa
import pandas as pd
print('✅ PyIceberg version:', pyiceberg.__version__)
print('✅ PyArrow version:', pa.__version__)
print('✅ Pandas version:', pd.__version__)
print('✅ Tất cả thư viện đã được cài đặt thành công!')
"

echo ""
echo "🎉 Setup hoàn tất!"
echo ""
echo "📋 Hướng dẫn sử dụng:"
echo "1. Kích hoạt môi trường: conda activate ${ENV_NAME}"
echo "2. Mở Jupyter: jupyter notebook pyiceberg_lab.ipynb"
echo "3. Trong Jupyter, chọn kernel: 'PyIceberg Lab (${ENV_NAME})'"
echo ""
echo "💡 Hoặc chạy trực tiếp:"
echo "   conda activate ${ENV_NAME} && jupyter notebook pyiceberg_lab.ipynb"
echo ""
echo "🧹 Để xóa môi trường sau này: conda env remove -n ${ENV_NAME}"
