from function_11 import bucket_sort
import pytest


def test_bucket_sort_empty_list():
    assert bucket_sort([]) == []


def test_bucket_sort_invalid_bucket_count():
    assert bucket_sort([1, 2, 3], bucket_count=0) == []
    assert bucket_sort([1, 2, 3], bucket_count=-5) == []


def test_bucket_sort_all_identical_elements():
    assert bucket_sort([5, 5, 5, 5]) == [5, 5, 5, 5]


def test_bucket_sort_nominal_case():
    unsorted = [0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51]
    sorted_res = bucket_sort(unsorted, bucket_count=5)
    assert sorted_res == sorted(unsorted)


def test_bucket_sort_integers():
    unsorted = [54, 26, 93, 17, 77, 31, 44, 55, 20]
    assert bucket_sort(unsorted, bucket_count=5) == sorted(unsorted)


def test_bucket_sort_boundary_max_value_mapping():
    unsorted = [10, 20, 30, 30]
    assert bucket_sort(unsorted, bucket_count=3) == [10, 20, 30, 30]


def test_bucket_sort_default_bucket_count():
    # Kills mutmut_1 (default bucket count = 10 vs 11)
    unsorted = list(range(10))
    # With default bucket_count=10, 10 items 0..9 mapped into 10 buckets will place each item in its own bucket.
    # If default is mutated to 11, behavior might differ or we can explicitly test calling with no arguments on a specific distribution.
    assert bucket_sort(unsorted) == sorted(unsorted)
    
    # Another explicit check for default bucket_count=10
    # Let's pass a list of length where 10 buckets matter specifically
    res = bucket_sort([9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
    assert res == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_bucket_sort_bucket_count_one():
    # Kills mutmut_6 (bucket_count <= 1 vs <= 0)
    unsorted = [3, 1, 2]
    assert bucket_sort(unsorted, bucket_count=1) == [1, 2, 3]


def test_bucket_sort_bucket_size_arithmetic():
    # Kills mutmut_12 (* instead of / for bucket_size)
    # Kills mutmut_13 (+ instead of - for max_value - min_value)
    # Kills mutmut_22 (* instead of / for val - min_value / bucket_size)
    # Kills mutmut_23 (+ instead of - for val - min_value)
    unsorted = [1, 5, 9]
    assert bucket_sort(unsorted, bucket_count=2) == [1, 5, 9]
    
    # Additional test specifically sensitive to bucket size calculation (* vs / and + vs -)
    # With min=0, max=10, bucket_count=2 -> bucket_size = (10 - 0) / 2 = 5.0.
    # If mutated to (10 - 0) * 2 = 20.0, or (10 + 0) / 2 = 5.0 (wait, for min=0 max=10 + gives 10/2=5 too, let's use min=2, max=10).
    # min=2, max=10, bucket_count=2 -> bucket_size = (10 - 2) / 2 = 4.0.
    # Mutated + gives (10 + 2) / 2 = 6.0.
    # val = 6:
    # Original: (6 - 2) / 4.0 = 4.0 / 4.0 = 1.0 -> index 1.
    # Mutated (+): (6 + 2) / 4.0 = 8.0 / 4.0 = 2.0 -> clamped to index 1. Wait, let's use val = 5:
    # Original: (5 - 2) / 4.0 = 3.0 / 4.0 = 0.75 -> int -> 0.
    # Mutated (+): (5 + 2) / 4.0 = 7.0 / 4.0 = 1.75 -> int -> 1. Different bucket!
    unsorted2 = [2, 5, 10]
    assert bucket_sort(unsorted2, bucket_count=2) == [2, 5, 10]


def test_bucket_sort_max_value_index_boundary():
    # Kills mutmut_25 (bucket_count - 2 vs bucket_count - 1)
    # Ensures that the maximum value maps to bucket_count - 1 and doesn't get clamped/lost or placed in wrong bucket
    unsorted = [0, 10]
    assert bucket_sort(unsorted, bucket_count=2) == [0, 10]
    
    # Test maximum element explicitly with multiple elements hitting the last bucket
    unsorted_max = [0, 5, 10]
    assert bucket_sort(unsorted_max, bucket_count=2) == [0, 5, 10]