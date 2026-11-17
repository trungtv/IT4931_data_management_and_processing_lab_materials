import pandas as pd

from sessions import sessionize


def test_gap_equal_to_the_threshold_stays_in_one_session():
    gap = pd.Timedelta(minutes=5)
    times = [
        pd.Timestamp("2026-11-17 09:00"),
        pd.Timestamp("2026-11-17 09:05"),
        pd.Timestamp("2026-11-17 09:10:01"),
    ]
    assert sessionize(times, gap) == [
        (times[0], times[1], 2),
        (times[2], times[2], 1),
    ]


def test_unsorted_input_and_duplicate_timestamps():
    later = pd.Timestamp("2026-11-17 09:02")
    earlier = pd.Timestamp("2026-11-17 09:00")
    sessions = sessionize([later, earlier, earlier], pd.Timedelta(minutes=5))
    assert sessions == [(earlier, later, 3)]


def test_empty_input():
    assert sessionize([], pd.Timedelta(minutes=1)) == []
