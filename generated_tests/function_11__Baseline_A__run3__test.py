from function_11 import bucket_sort
import pytest


def test_bucket_sort_empty_list():
    assert bucket_sort([]) == []


def test_bucket_sort_invalid_bucket_count():
    assert bucket_sort([1, 2, 3], bucket_count=0) == []
    assert bucket_sort([1, 2, 3], bucket_count=-5) == []


def test_bucket_sort_all_elements_equal():
    assert bucket_sort([5, 5, 5, 5]) == [5, 5, 5, 5]


def test_bucket_sort_nominal_integers():
    unsorted = [29, 25, 3, 49, 9, 37, 21, 43]
    expected = [3, 9, 21, 25, 29, 37, 43, 49]
    assert bucket_sort(unsorted, bucket_count=5) == expected


def test_bucket_sort_floats():
    unsorted = [0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51]
    expected = [0.32, 0.33, 0.37, 0.42, 0.47, 0.51, 0.52]
    result = bucket_sort(unsorted, bucket_count=3)
    assert result == expected


def test_bucket_sort_single_element():
    assert bucket_sort([42]) == [42]


def test_bucket_sort_max_value_boundary_index():
    unsorted = [10, 20, 30, 30]
    expected = [10, 20, 30, 30]
    assert bucket_sort(unsorted, bucket_count=3) == expected
