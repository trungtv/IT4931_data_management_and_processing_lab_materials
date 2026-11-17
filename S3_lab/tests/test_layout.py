import pytest

from layout import current_snapshot_readable_by, metadata_key, multipart_plan


def test_last_part_is_short_and_a_small_object_is_one_part():
    five = 5 * 1024 * 1024
    assert multipart_plan(five + 10, five) == [(0, five), (five, 10)]
    assert multipart_plan(100, five) == [(0, 100)]


def test_undersized_middle_part_and_too_many_parts_raise():
    five = 5 * 1024 * 1024
    with pytest.raises(ValueError, match="5MiB"):
        multipart_plan(10 * 1024 * 1024, 1024)
    with pytest.raises(ValueError, match="10000"):
        multipart_plan(five * 10001, five)


def test_listing_the_bucket_does_not_identify_the_current_snapshot():
    assert metadata_key("silver_trades", 7) == "iceberg/lab/silver_trades/metadata/snap-7.avro"
    assert current_snapshot_readable_by("iceberg_metadata") is True
    assert current_snapshot_readable_by("list_objects") is False
