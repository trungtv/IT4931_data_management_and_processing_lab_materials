import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lab"))

from s3_course import object_name, one_part_for_small_object, pipeline_metadata


def test_object_name_rejects_a_leading_slash():
    try:
        object_name("/raw", "a.txt")
    except ValueError:
        return
    raise AssertionError("key tuyệt đối phải bị từ chối")


def test_small_object_is_one_part():
    assert one_part_for_small_object(100) == [(0, 100)]


def test_pipeline_key_is_metadata():
    assert pipeline_metadata("silver_trades", 3).endswith("snap-3.avro")
