import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lab"))

from platform_inspect import compose_services

ROOT = Path(__file__).resolve().parents[2]


def test_airflow_services_share_the_airflow_profile():
    text = (ROOT / "platform" / "docker-compose.yml").read_text()
    services = compose_services(text)
    assert "airflow" in services["airflow-scheduler"]
    assert "minio" in services
