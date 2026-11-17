from pathlib import Path

from image_review import layers_rebuilt, review_dockerfile


def test_changing_the_last_copy_rebuilds_one_layer():
    before = ["FROM python:3.11", "COPY requirements.txt .", "RUN pip install -r requirements.txt", "COPY src src"]
    after = ["FROM python:3.11", "COPY requirements.txt .", "RUN pip install -r requirements.txt", "COPY app app"]
    assert layers_rebuilt(before, after) == 1


def test_airflow_image_is_clean_and_a_tour_dockerfile_is_not():
    dockerfile = Path(__file__).resolve().parents[2] / "platform" / "airflow" / "Dockerfile"
    assert review_dockerfile(dockerfile.read_text()) == []
    broken = """
    FROM python
    ADD app.py /app/app.py
    RUN apt-get update && apt-get install -y curl
    RUN pip install pandas
    USER root
    """
    assert review_dockerfile(broken) == [
        "unpinned_base",
        "add_instead_of_copy",
        "runs_as_root",
        "apt_lists_kept",
        "pip_cache_kept",
    ]
