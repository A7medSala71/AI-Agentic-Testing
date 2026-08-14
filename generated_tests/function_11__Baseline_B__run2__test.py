from function_11 import bucket_sort
import pytest


def test_bucket_sort_empty_list():
    assert bucket_sort([]) == []


def test_bucket_sort_zero_buckets():
    assert bucket_sort([1, 2, 3], bucket_count=0) == []


def test_bucket_sort_negative_buckets():
    assert bucket_sort([1, 2, 3], bucket_count=-5) == []


def test_bucket_sort_identical_elements():
    assert bucket_sort([5, 5, 5, 5]) == [5, 5, 5, 5]


def test_bucket_sort_nominal_case():
    assert bucket_sort([0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51]) == [0.32, 0.33, 0.37, 0.42, 0.47, 0.51, 0.52]


def test_bucket_sort_integers():
    assert bucket_sort([5, 2, 9, 1, 5, 6]) == [1, 2, 5, 5, 6, 9]


def test_bucket_sort_custom_bucket_count():
    assert bucket_sort([10, 2, 5, 8, 1], bucket_count=3) == [1, 2, 5, 8, 10]


def test_bucket_sort_single_element():
    assert bucket_sort([42]) == [42]


def test_bucket_sort_negatives_and_floats():
    assert bucket_sort([-1.5, 2.0, -0.5, 1.1]) == [-1.5, -0.5, 1.1, 2.0]
