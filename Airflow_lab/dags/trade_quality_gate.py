"""DAG chạy được: stage giao dịch, rẽ publish hoặc quarantine, ghi MinIO."""

from __future__ import annotations

import json
import os

import pendulum
from airflow.exceptions import AirflowFailException
from airflow.sdk import DAG, get_current_context, task

from quality_gate import assess, object_key, publish_symbols, staged_trades


def _put(uri_prefix: str, name: str, payload: dict) -> str:
    import boto3

    key = object_key(uri_prefix, name)
    client = boto3.client(
        "s3",
        endpoint_url=os.environ["MINIO_ENDPOINT"],
        aws_access_key_id=os.environ["MINIO_ACCESS_KEY"],
        aws_secret_access_key=os.environ["MINIO_SECRET_KEY"],
    )
    client.put_object(Bucket="warehouse", Key=key, Body=json.dumps(payload).encode())
    return key


with DAG(
    dag_id="trade_quality_gate",
    schedule=None,
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    max_active_runs=1,
    default_args={"retries": 0},
    tags=["airflow", "quality"],
) as dag:

    @task
    def stage() -> dict:
        logical_date = get_current_context()["ds"]
        return assess(staged_trades(logical_date), logical_date)

    @task.branch
    def choose(report: dict) -> str:
        return report["branch"]

    @task(retries=2)
    def publish(report: dict) -> str:
        try:
            symbols = publish_symbols(report["clean"])
        except ValueError as exc:
            raise AirflowFailException(str(exc)) from exc
        return _put(report["output_uri"], "symbols.json", {"symbols": symbols})

    @task
    def quarantine(report: dict) -> str:
        uri = report["output_uri"].replace("/publish/", "/quarantine/")
        return _put(uri, "rejected.json", {"rejected": report["rejected"]})

    @task(trigger_rule="none_failed_min_one_success")
    def finish(published: str | None = None, held: str | None = None) -> str:
        if published:
            return published
        if held:
            return held
        raise AirflowFailException("Không có nhánh nào ghi kết quả")

    report = stage()
    decision = choose(report)
    published = publish(report)
    held = quarantine(report)
    decision >> [published, held]
    finish(published, held)
