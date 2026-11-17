from idempotency import retry_decision, task_output_uri


def test_retry_writes_the_same_uri():
    first = task_output_uri("data_lakehouse_pipeline", "spark_silver_batch", "2026-11-17")
    second = task_output_uri("data_lakehouse_pipeline", "spark_silver_batch", "2026-11-17")
    assert first == second
    assert first == (
        "s3://warehouse/airflow/data_lakehouse_pipeline/"
        "spark_silver_batch/logical_date=2026-11-17/"
    )


def test_schema_error_does_not_retry_and_broker_down_does():
    assert retry_decision("schema", try_number=1, max_tries=3) == "fail"
    assert retry_decision("broker_down", try_number=1, max_tries=3) == "retry"
    assert retry_decision("broker_down", try_number=3, max_tries=3) == "fail"
