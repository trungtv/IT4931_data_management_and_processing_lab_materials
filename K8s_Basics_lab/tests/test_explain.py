from pathlib import Path

from explain import explain_manifest

MANIFESTS = Path(__file__).resolve().parents[1] / "manifests"


def test_healthy_manifest_has_config_secret_and_volume():
    explained = explain_manifest(MANIFESTS / "trade-consumer.yaml")
    assert explained["config_keys"] == ["KAFKA_BOOTSTRAP", "TOPIC"]
    assert explained["secret_keys"] == ["MINIO_ACCESS_KEY"]
    assert explained["volumes"] == ["config"]
    assert explained["service_port"] == 8080
