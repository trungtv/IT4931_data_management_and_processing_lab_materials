"""Chẩn đoán workload consumer giao dịch không vào được Service hoặc bị OOM.

Thân hàm giữa EXERCISE_START và EXERCISE_END là lời giải.
"""

from __future__ import annotations

from pathlib import Path

import yaml


def diagnose_workload(workload: dict) -> list[str]:
    """Trả về mã lỗi. Workload đúng thì danh sách rỗng."""
    # EXERCISE_START
    required = [
        "pod_labels",
        "service_selector",
        "container_port",
        "readiness_port",
        "memory_request_mi",
        "memory_limit_mi",
        "memory_needed_mi",
        "probe",
        "ready_when",
    ]
    missing = [key for key in required if key not in workload]
    if missing:
        raise ValueError(f"Thiếu trường: {missing}")

    problems: list[str] = []
    labels = workload["pod_labels"]
    if any(labels.get(key) != value for key, value in workload["service_selector"].items()):
        problems.append("selector_mismatch")
    if workload["readiness_port"] != workload["container_port"]:
        problems.append("probe_port_mismatch")
    if workload["memory_request_mi"] > workload["memory_limit_mi"]:
        problems.append("request_exceeds_limit")
    if workload["memory_limit_mi"] < workload["memory_needed_mi"]:
        problems.append("oom_limit")
    if workload["probe"] == "tcp" and workload["ready_when"] == "http_health":
        problems.append("tcp_probe_masks_not_ready")
    return problems
    # EXERCISE_END


def workload_from_manifest(path: Path) -> dict:
    """Đọc Deployment và Service. Bộ nhớ process cần để chạy consumer là 400Mi."""
    documents = list(yaml.safe_load_all(Path(path).read_text()))
    deployment = next(item for item in documents if item["kind"] == "Deployment")
    service = next(item for item in documents if item["kind"] == "Service")
    container = deployment["spec"]["template"]["spec"]["containers"][0]
    probe = container["readinessProbe"]
    if "httpGet" in probe:
        probe_kind = "http"
        probe_port = probe["httpGet"]["port"]
    else:
        probe_kind = "tcp"
        probe_port = probe["tcpSocket"]["port"]
    return {
        "pod_labels": deployment["spec"]["template"]["metadata"]["labels"],
        "service_selector": service["spec"]["selector"],
        "container_port": container["ports"][0]["containerPort"],
        "readiness_port": probe_port,
        "memory_request_mi": int(container["resources"]["requests"]["memory"].removesuffix("Mi")),
        "memory_limit_mi": int(container["resources"]["limits"]["memory"].removesuffix("Mi")),
        "memory_needed_mi": 400,
        "probe": probe_kind,
        "ready_when": "http_health",
    }
