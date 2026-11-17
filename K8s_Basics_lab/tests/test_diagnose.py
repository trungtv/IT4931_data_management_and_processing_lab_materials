from pathlib import Path

from diagnose import diagnose_workload, workload_from_manifest

MANIFESTS = Path(__file__).resolve().parents[1] / "manifests"


def _workload(**overrides):
    workload = {
        "pod_labels": {"app": "trade-consumer"},
        "service_selector": {"app": "trade-consumer"},
        "container_port": 8080,
        "readiness_port": 8080,
        "memory_request_mi": 256,
        "memory_limit_mi": 512,
        "memory_needed_mi": 400,
        "probe": "http",
        "ready_when": "http_health",
    }
    workload.update(overrides)
    return workload


def test_a_healthy_consumer_has_no_findings():
    assert diagnose_workload(_workload()) == []
    assert diagnose_workload(workload_from_manifest(MANIFESTS / "trade-consumer.yaml")) == []


def test_selector_oom_and_tcp_probe_are_all_reported():
    found = diagnose_workload(
        _workload(
            service_selector={"app": "trades"},
            memory_limit_mi=128,
            memory_request_mi=256,
            probe="tcp",
        )
    )
    assert found == [
        "selector_mismatch",
        "request_exceeds_limit",
        "oom_limit",
        "tcp_probe_masks_not_ready",
    ]
    broken = diagnose_workload(workload_from_manifest(MANIFESTS / "trade-consumer-broken.yaml"))
    assert broken == [
        "selector_mismatch",
        "probe_port_mismatch",
        "request_exceeds_limit",
        "oom_limit",
        "tcp_probe_masks_not_ready",
    ]
