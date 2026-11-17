"""Khóa idempotent và quyết định retry cho task lakehouse.

Thân hàm giữa EXERCISE_START và EXERCISE_END là lời giải.
"""

from __future__ import annotations


def task_output_uri(dag_id: str, task_id: str, logical_date: str) -> str:
    """Một logical date có một URI. Lần retry ghi đè đúng chỗ đó."""
    # EXERCISE_START
    if not dag_id or not task_id or not logical_date:
        raise ValueError("dag_id, task_id và logical_date là bắt buộc")
    if "/" in dag_id or "/" in task_id:
        raise ValueError("dag_id và task_id không chứa dấu /")
    return f"s3://warehouse/airflow/{dag_id}/{task_id}/logical_date={logical_date}/"
    # EXERCISE_END


def retry_decision(error_kind: str, try_number: int, max_tries: int) -> str:
    """timeout và broker_down được chạy lại. schema và assertion thì dừng."""
    # EXERCISE_START
    if try_number < 1 or max_tries < 1:
        raise ValueError("try_number và max_tries bắt đầu từ 1")
    if error_kind in {"schema", "assertion"}:
        return "fail"
    if error_kind in {"timeout", "broker_down"}:
        return "retry" if try_number < max_tries else "fail"
    raise ValueError(f"error_kind không hỗ trợ: {error_kind}")
    # EXERCISE_END
