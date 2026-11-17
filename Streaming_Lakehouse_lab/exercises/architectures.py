"""Ba mô hình xử lý. Lakehouse dùng một hàm clean trên một bảng."""

from __future__ import annotations


def processing_model(name: str) -> str:
    models = {
        "lambda": "Batch và speed layer là hai codebase.",
        "kappa": "Mọi thứ đi qua stream, batch chỉ là replay.",
        "lakehouse": "Một hàm clean_trades và một bảng Iceberg cho batch lẫn micro-batch.",
    }
    if name not in models:
        raise ValueError(f"model không hỗ trợ: {name}")
    return models[name]
