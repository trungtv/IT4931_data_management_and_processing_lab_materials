"""Chạy dbt run rồi dbt test trên bảng Iceberg. Lỗi dbt làm task Airflow thất bại."""

import os
import subprocess
import sys


def main() -> None:
    project = os.environ["DBT_PROJECT_DIR"]
    profiles = os.environ["DBT_PROFILES_DIR"]
    command = [
        "dbt",
        sys.argv[1] if len(sys.argv) > 1 else "build",
        "--project-dir",
        project,
        "--profiles-dir",
        profiles,
    ]
    completed = subprocess.run(command, check=False)
    if completed.returncode != 0:
        sys.exit(completed.returncode)


if __name__ == "__main__":
    main()
