from function_11 import bucket_sort
import pytest


def test_bucket_sort_empty_list():
    assert bucket_sort([]) == []


def test_bucket_sort_invalid_bucket_count():
    assert bucket_sort([1, 2, 3], bucket_count=0) == []
    assert bucket_sort([1, 2, 3], bucket_count=-5) == []


def test_bucket_sort_all_elements_equal():
    assert bucket_sort([5, 5, 5, 5]) == [5, 5, 5, 5]


def test_bucket_sort_nominal_case():
    unsorted = [0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51]
    sorted_result = bucket_sort(unsorted, bucket_count=5)
    assert sorted_result == sorted(unsorted)


def test_bucket_sort_integers():
    unsorted = [52, 37, 63, 14, 1, 98, 42]
    assert bucket_sort(unsorted, bucket_count=4) == [1, 14, 37, 42, 52, 63, 98]


def test_bucket_sort_max_value_boundary():
    unsorted = [10, 20, 30]
    # The max value 30 should fall into the last bucket (index bucket_count - 1)
    assert bucket_sort(unsorted, bucket_count=3) == [10, 20, 30]


def test_default_bucket_count_value():
    # Mutant mutmut_1 changes default bucket_count from 10 to 11; verify default argument value via signature inspection.
    import inspect
    sig = inspect.signature(bucket_sort)
    assert sig.parameters['bucket_count'].default == 10


def test_bucket_count_one_allowed():
    # Mutant mutmut_6 changes bucket_count <= 0 to <= 1; verify bucket_count=1 sorts successfully.
    assert bucket_sort([3, 1, 2], bucket_count=1) == [1, 2, 3]


def test_bucket_size_division_operator():
    # Mutant mutmut_12 changes division to multiplication; with max-min=10 and count=2, bucket_size becomes 20 instead of 5, placing all elements in bucket 0 and failing on multi-bucket sorted distribution.
    unsorted = [0, 5, 10]
    assert bucket_sort(unsorted, bucket_count=2) == [0, 5, 10]


def test_bucket_size_subtraction_operator():
    # Mutant mutmut_13 changes min_value - min_value to +; verify with negative values where subtraction vs addition differs.
    unsorted = [-10, 10]
    assert bucket_sort(unsorted, bucket_count=2) == [-10, 10]


def test_index_bucket_size_division_operator():
    # Mutant mutmut_22 changes division to multiplication inside index calculation; index becomes incorrect and elements land in wrong buckets or cause IndexError.
    unsorted = [0, 2, 5]
    assert bucket_sort(unsorted, bucket_count=5) == [0, 2, 5]


def test_index_val_subtraction_operator():
    # Mutant mutmut_23 changes val - min_value to val + min_value inside index calculation; verify with negative min_value.
    unsorted = [-5, 0, 5]
    assert bucket_sort(unsorted, bucket_count=5) == [-5, 0, 5]


def test_max_value_bucket_index_bound():
    # Mutant mutmut_25 changes bucket_count - 1 to bucket_count - 2, causing max value 10 to be clipped to bucket_count - 2 (index 0) instead of bucket_count - 1 (index 1) for bucket_count=2.
    unsorted = [0, 10]
    assert bucket_sort(unsorted, bucket_count=2) == [0, 10]