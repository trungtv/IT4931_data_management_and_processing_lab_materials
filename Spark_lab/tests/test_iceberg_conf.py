import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lab"))

import pytest

from iceberg_conf import ICEBERG_PACKAGE, WAREHOUSE, iceberg_configs


def test_catalog_matches_the_capstone_and_not_the_notebook_comment():
    assert ICEBERG_PACKAGE.endswith(":1.6.1")
    assert "1.4.0" not in ICEBERG_PACKAGE
    conf = iceberg_configs("http://minio:9000")
    assert conf["spark.sql.catalog.lake.warehouse"] == WAREHOUSE
    assert conf["spark.sql.catalog.lake.warehouse"].startswith("s3a://")
    assert conf["spark.hadoop.fs.s3a.endpoint"] == "http://minio:9000"


def test_missing_endpoint_is_an_error():
    with pytest.raises(ValueError):
        iceberg_configs("")
