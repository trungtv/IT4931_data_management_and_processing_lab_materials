"""Đọc Compose của nền lab và container Airflow đang chạy."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
from image_review import review_dockerfile


def compose_services(text: str) -> dict[str, list[str]]:
    """Tên service và profile. Service không khai profile thì danh sách rỗng."""
    document = yaml.safe_load(text)
    services = document.get("services") or {}
    return {name: list(spec.get("profiles") or []) for name, spec in services.items()}


def running_airflow() -> dict:
    raw = subprocess.run(
        ["docker", "inspect", "it4931-airflow-scheduler"],
        check=True,
        capture_output=True,
        text=True,
    )
    info = json.loads(raw.stdout)[0]
    mounts = sorted(item["Destination"] for item in info["Mounts"])
    networks = sorted(info["NetworkSettings"]["Networks"])
    image = info["Config"]["Image"]
    if "it4931" not in networks:
        raise AssertionError(networks)
    if "/opt/airflow/dags/trade_quality_gate.py" not in mounts:
        raise AssertionError(mounts)
    return {"image": image, "networks": networks, "mounts": mounts}


def review_airflow_image(dockerfile: Path) -> list[str]:
    return review_dockerfile(dockerfile.read_text())
