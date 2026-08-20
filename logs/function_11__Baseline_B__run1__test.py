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


def test_bucket_sort_default_bucket_count():
    unsorted = [5, 1, 12, -3, 8]
    expected = [-3, 1, 5, 8, 12]
    assert bucket_sort(unsorted) == expected


def test_bucket_sort_floats():
    unsorted = [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434]
    expected = [0.1234, 0.3434, 0.565, 0.656, 0.665, 0.897]
    assert bucket_sort(unsorted, bucket_count=3) == expected


def test_bucket_sort_max_value_boundary():
    unsorted = [10, 20, 10, 20]
    expected = [10, 10, 20, 20]
    assert bucket_sort(unsorted, bucket_count=2) == expected


def test_bucket_sort_single_element():
    assert bucket_sort([42]) == [42]
