import pytest
from function_11 import bucket_sort


def test_bucket_sort_empty_list():
    assert bucket_sort([]) == []


def test_bucket_sort_invalid_bucket_count():
    assert bucket_sort([1, 2, 3], bucket_count=0) == []
    assert bucket_sort([1, 2, 3], bucket_count=-5) == []


def test_bucket_sort_identical_elements():
    assert bucket_sort([5, 5, 5, 5]) == [5, 5, 5, 5]


def test_bucket_sort_nominal():
    unsorted = [0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51]
    expected = sorted(unsorted)
    assert bucket_sort(unsorted, bucket_count=5) == expected


def test_bucket_sort_integers():
    unsorted = [42, 32, 33, 52, 37, 47, 51]
    expected = sorted(unsorted)
    assert bucket_sort(unsorted, bucket_count=4) == expected


def test_bucket_sort_single_element():
    assert bucket_sort([42]) == [42]


def test_bucket_sort_boundary_max_value():
    unsorted = [10, 20, 30, 40, 50]
    # Max value mapped with index should not go out of bounds due to min(..., bucket_count - 1)
    assert bucket_sort(unsorted, bucket_count=3) == [10, 20, 30, 40, 50]


def test_bucket_sort_default_bucket_count_parameter():
    # Mutant mutmut_1 changes default bucket_count from 10 to 11, diverging the function signature default value.
    import inspect
    sig = inspect.signature(bucket_sort)
    assert sig.parameters['bucket_count'].default == 10


def test_bucket_sort_bucket_count_one():
    # Mutator changes bucket_count <= 0 to <= 1; bucket_count=1 should return sorted list, not []
    assert bucket_sort([3, 1, 2], bucket_count=1) == [1, 2, 3]


def test_bucket_sort_bucket_size_multiplication_mutant():
    # Mutant mutmut_12 replaces division with multiplication in bucket_size calculation, changing bucket_size from 5.0 to 20.0.
    unsorted = [0.0, 10.0]
    assert bucket_sort(unsorted, bucket_count=2) == [0.0, 10.0]


def test_bucket_sort_bucket_size_addition_mutant():
    # Mutant mutmut_13 replaces subtraction with addition in bucket_size calculation, changing bucket_size from 5.0 to 15.0.
    unsorted = [10.0, 20.0]
    assert bucket_sort(unsorted, bucket_count=2) == [10.0, 20.0]


def test_bucket_sort_index_val_multiplication_mutant():
    # Mutant mutmut_22 replaces division with multiplication in index calculation, changing val-min division by bucket_size to multiplication.
    unsorted = [1.0, 2.0]
    assert bucket_sort(unsorted, bucket_count=2) == [1.0, 2.0]


def test_bucket_sort_index_val_addition_mutant():
    # Mutant mutmut_23 replaces subtraction with addition in index calculation, changing (val - min_value) to (val + min_value).
    assert bucket_sort([3.0, 4.0], bucket_count=2) == [3.0, 4.0]


def test_bucket_sort_bucket_count_minus_two_mutant():
    # Mutant mutmut_25 changes bucket_count - 1 to bucket_count - 2, causing max element to be incorrectly clamped or misplaced.
    unsorted = [0.0, 10.0]
    assert bucket_sort(unsorted, bucket_count=2) == [0.0, 10.0]