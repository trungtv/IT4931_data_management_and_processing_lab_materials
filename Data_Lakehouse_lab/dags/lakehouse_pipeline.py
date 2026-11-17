"""Capstone: Kafka -> Spark Iceberg -> dbt. Mỗi task gọi script thật."""

from datetime import timedelta

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import DAG

PIPELINE = "/opt/airflow/pipeline"

with DAG(
    dag_id="data_lakehouse_pipeline",
    schedule="@daily",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    default_args={
        "retries": 0,
        "retry_delay": timedelta(minutes=2),
    },
    tags=["lakehouse", "capstone"],
) as dag:
    start = EmptyOperator(task_id="start")

    ingest_data = BashOperator(
        task_id="ingest_data_kafka",
        bash_command=f"python {PIPELINE}/generate_trades.py",
    )
    bronze = BashOperator(
        task_id="spark_bronze_stream",
        bash_command=f"python {PIPELINE}/bronze_stream.py",
    )
    silver = BashOperator(
        task_id="spark_silver_batch",
        bash_command=f"python {PIPELINE}/silver.py --mode batch",
    )
    gold = BashOperator(
        task_id="spark_gold",
        bash_command=f"python {PIPELINE}/gold.py",
    )
    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=f"python {PIPELINE}/run_dbt.py build",
    )
    end = EmptyOperator(task_id="end")

    start >> ingest_data >> bronze >> silver >> gold >> dbt_build >> end
