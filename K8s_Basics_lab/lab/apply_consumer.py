"""Apply consumer lên cụm đang trỏ bởi kubectl và kiểm tra endpoint."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

KUBECTL = os.environ.get("KUBECTL", "kubectl")
ROOT = Path(__file__).resolve().parents[1]
HEALTHY = ROOT / "manifests" / "trade-consumer.yaml"
BROKEN = ROOT / "manifests" / "trade-consumer-broken.yaml"


def _run(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run([KUBECTL, *args], check=check, capture_output=True, text=True)


def _apply(namespace: str, manifest: Path) -> subprocess.CompletedProcess:
    _run(["create", "namespace", namespace], check=False)
    return _run(["apply", "-n", namespace, "-f", str(manifest)], check=False)


def _endpoints(namespace: str) -> list[str]:
    raw = _run(["get", "endpoints", "trade-consumer", "-n", namespace, "-o", "json"])
    document = json.loads(raw.stdout)
    addresses = []
    for subset in document.get("subsets") or []:
        for address in subset.get("addresses") or []:
            addresses.append(address["ip"])
    return addresses


def _pod_ready(namespace: str) -> bool:
    raw = _run(["get", "pods", "-n", namespace, "-l", "app=trade-consumer", "-o", "json"])
    document = json.loads(raw.stdout)
    for pod in document.get("items") or []:
        for condition in pod["status"].get("conditions") or []:
            if condition["type"] == "Ready" and condition["status"] == "True":
                return True
    return False


def run() -> dict:
    healthy_apply = _apply("trade", HEALTHY)
    if healthy_apply.returncode != 0:
        raise AssertionError(healthy_apply.stderr)
    _run(["rollout", "status", "deployment/trade-consumer", "-n", "trade", "--timeout=180s"])
    healthy_addresses = _endpoints("trade")
    if not healthy_addresses or not _pod_ready("trade"):
        raise AssertionError(healthy_addresses)
    broken_apply = _apply("trade-broken", BROKEN)
    broken_text = broken_apply.stdout + broken_apply.stderr
    if broken_apply.returncode == 0 or "must be less than or equal to memory limit" not in broken_text:
        raise AssertionError(broken_text)
    broken_addresses = _endpoints("trade-broken")
    broken_ready = _pod_ready("trade-broken")
    if broken_addresses or broken_ready:
        raise AssertionError((broken_addresses, broken_ready, broken_text))
    return {
        "healthy": healthy_addresses,
        "broken_rejected": True,
        "broken_endpoints": broken_addresses,
    }


if __name__ == "__main__":
    print(run())
