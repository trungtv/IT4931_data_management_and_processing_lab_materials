"""Đọc đủ loại object của consumer: Deployment, Service, ConfigMap, Secret, volume."""

from __future__ import annotations

from pathlib import Path

import yaml


def explain_manifest(path: Path) -> dict:
    documents = [item for item in yaml.safe_load_all(Path(path).read_text()) if item]
    by_kind = {item["kind"]: item for item in documents}
    deployment = by_kind["Deployment"]
    service = by_kind["Service"]
    container = deployment["spec"]["template"]["spec"]["containers"][0]
    volumes = deployment["spec"]["template"]["spec"].get("volumes") or []
    return {
        "replicas": deployment["spec"].get("replicas", 1),
        "pod_labels": deployment["spec"]["template"]["metadata"]["labels"],
        "container_port": container["ports"][0]["containerPort"],
        "service_port": service["spec"]["ports"][0]["port"],
        "service_selector": service["spec"]["selector"],
        "config_keys": sorted((by_kind.get("ConfigMap") or {"data": {}})["data"]),
        "secret_keys": sorted((by_kind.get("Secret") or {"stringData": {}})["stringData"]),
        "volumes": sorted(item["name"] for item in volumes),
        "memory_request": container["resources"]["requests"]["memory"],
        "memory_limit": container["resources"]["limits"]["memory"],
    }
