"""Đo layer bị build lại và lỗi Dockerfile làm image phình hoặc chạy root.

Thân hàm giữa EXERCISE_START và EXERCISE_END là lời giải.
"""

from __future__ import annotations


def layers_rebuilt(before: list[str], after: list[str]) -> int:
    """Số instruction từ điểm khác nhau đầu tiên trở đi phải build lại."""
    # EXERCISE_START
    if len(before) != len(after):
        raise ValueError("Hai lịch sử layer phải cùng số instruction")
    for index, (left, right) in enumerate(zip(before, after)):
        if left != right:
            return len(after) - index
    return 0
    # EXERCISE_END


def review_dockerfile(text: str) -> list[str]:
    """Trả về mã lỗi, theo thứ tự phát hiện."""
    # EXERCISE_START
    lines = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped and not stripped.startswith("#"):
            lines.append(stripped)
    issues: list[str] = []
    for line in lines:
        if not line.upper().startswith("FROM "):
            continue
        image = line.split()[1]
        name = image.split("@", 1)[0]
        if ":" not in name or name.endswith(":latest"):
            issues.append("unpinned_base")
    if any(line.upper().startswith("ADD ") for line in lines):
        issues.append("add_instead_of_copy")
    users = [line for line in lines if line.upper().startswith("USER ")]
    if not users or users[-1].split()[1] == "root":
        issues.append("runs_as_root")
    runs = "\n".join(line for line in lines if line.upper().startswith("RUN "))
    if "apt-get install" in runs and "rm -rf /var/lib/apt/lists" not in runs:
        issues.append("apt_lists_kept")
    if "pip install" in runs and "--no-cache-dir" not in runs:
        issues.append("pip_cache_kept")
    return issues
    # EXERCISE_END
