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
    assert bucket_sort([9, 1, 5, 3, 7, 2, 8, 4, 6], bucket_count=3) == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_bucket_sort_floats():
    assert bucket_sort([0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51]) == [0.32, 0.33, 0.37, 0.42, 0.47, 0.51, 0.52]


def test_bucket_sort_single_element():
    assert bucket_sort([42]) == [42]


def test_bucket_sort_negative_numbers():
    assert bucket_sort([-3, 5, -1, 0, 2, -5], bucket_count=4) == [-5, -3, -1, 0, 2, 5]


def test_bucket_sort_duplicates():
    assert bucket_sort([4, 1, 4, 2, 1, 3, 2], bucket_count=3) == [1, 1, 2, 2, 3, 4, 4]
