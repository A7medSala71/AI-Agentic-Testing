from function_11 import bucket_sort
import pytest


def test_bucket_sort_empty_list():
    assert bucket_sort([]) == []


def test_bucket_sort_invalid_bucket_count():
    assert bucket_sort([1, 2, 3], bucket_count=0) == []
    assert bucket_sort([1, 2, 3], bucket_count=-5) == []


def test_bucket_sort_all_equal_elements():
    assert bucket_sort([5, 5, 5, 5]) == [5, 5, 5, 5]


def test_bucket_sort_nominal():
    res = bucket_sort([9.8, 0.5, 3.2, 1.5, 3.2, 7.1, 4.0], bucket_count=5)
    assert res == [0.5, 1.5, 3.2, 3.2, 4.0, 7.1, 9.8]


def test_bucket_sort_integers():
    res = bucket_sort([42, 7, 19, 3, 88, 55], bucket_count=4)
    assert res == [3, 7, 19, 42, 55, 88]


def test_bucket_sort_single_element():
    assert bucket_sort([42]) == [42]
