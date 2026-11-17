"""Bốn bài S3: object, MinIO, SDK, layout pipeline. Bucket là warehouse."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))

import boto3

from layout import current_snapshot_readable_by, metadata_key, multipart_plan

BUCKET = "warehouse"
ENDPOINT = "http://localhost:9000"


def client():
    return boto3.client(
        "s3",
        endpoint_url=ENDPOINT,
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin",
    )


def object_name(prefix: str, name: str) -> str:
    """Key là đường dẫn logic. Bucket không có thư mục thật."""
    if not prefix or prefix.startswith("/") or not name or "/" in name:
        raise ValueError("prefix và name không hợp lệ")
    return f"{prefix.strip('/')}/{name}"


def head_bucket() -> str:
    client().head_bucket(Bucket=BUCKET)
    return BUCKET


def put_get_list_delete(key: str, body: bytes) -> bytes:
    """Lab SDK: ghi, liệt kê đúng key, đọc lại, xóa. List không giữ object đã xóa."""
    s3 = client()
    s3.put_object(Bucket=BUCKET, Key=key, Body=body)
    listed = [item["Key"] for item in s3.list_objects_v2(Bucket=BUCKET, Prefix=key).get("Contents", [])]
    if key not in listed:
        raise AssertionError(listed)
    found = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
    if found != body:
        raise AssertionError(found)
    s3.delete_object(Bucket=BUCKET, Key=key)
    after = s3.list_objects_v2(Bucket=BUCKET, Prefix=key).get("Contents", [])
    if any(item["Key"] == key for item in after):
        raise AssertionError(after)
    return found


def pipeline_metadata(table: str, snapshot_id: int) -> str:
    """Key metadata của snapshot. ListObjects không trả lời snapshot hiện tại."""
    if current_snapshot_readable_by("list_objects"):
        raise AssertionError("list không xác định snapshot")
    if not current_snapshot_readable_by("iceberg_metadata"):
        raise AssertionError("metadata phải trả lời snapshot")
    return metadata_key(table, snapshot_id)


def one_part_for_small_object(size_bytes: int) -> list[tuple[int, int]]:
    return multipart_plan(size_bytes, size_bytes)
