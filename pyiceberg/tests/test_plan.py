from datetime import datetime

import pytest

from plan import plan_compaction, snapshot_as_of


def test_small_files_pack_without_crossing_target():
    groups = plan_compaction([("a", 40), ("b", 40), ("c", 30)], 100)
    assert groups == [["a", "b"], ["c"]]


def test_large_file_is_not_merged():
    groups = plan_compaction([("a", 10), ("big", 100), ("b", 10)], 100)
    assert groups == [["a"], ["big"], ["b"]]


def test_snapshot_as_of_ignores_the_future_and_breaks_ties_by_id():
    first = datetime(2026, 11, 17, 9, 0)
    same = datetime(2026, 11, 17, 10, 0)
    later = datetime(2026, 11, 17, 11, 0)
    chosen = snapshot_as_of([(1, first), (4, same), (3, same), (9, later)], same)
    assert chosen == 4


def test_snapshot_before_the_table_exists_raises():
    with pytest.raises(ValueError):
        snapshot_as_of([(1, datetime(2026, 11, 17, 10, 0))], datetime(2026, 11, 17, 9, 0))
