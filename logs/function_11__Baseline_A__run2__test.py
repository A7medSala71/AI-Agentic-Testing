import pytest
from function_11 import bucket_sort


def test_bucket_sort_empty_list():
    assert bucket_sort([]) == []


def test_bucket_sort_zero_buckets():
    assert bucket_sort([1, 2, 3], bucket_count=0) == []


def test_bucket_sort_negative_buckets():
    assert bucket_sort([1, 2, 3], bucket_count=-5) == []


def test_bucket_sort_all_same_values():
    assert bucket_sort([5, 5, 5, 5]) == [5, 5, 5, 5]


def test_bucket_sort_nominal():
    assert bucket_sort([4.5, 2.1, 5.5, 1.0, 3.2]) == [1.0, 2.1, 3.2, 4.5, 5.5]


def test_bucket_sort_custom_bucket_count():
    assert bucket_sort([10, 2, 5, 8, 1, 9], bucket_count=3) == [1, 2, 5, 8, 9, 10]
