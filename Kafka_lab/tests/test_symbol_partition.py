import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lab"))

from kafka_course import symbol_partition


def test_one_symbol_stays_on_one_partition():
    assert symbol_partition("fpt", 4) == symbol_partition("FPT", 4)
    assert 0 <= symbol_partition("VNM", 4) < 4
