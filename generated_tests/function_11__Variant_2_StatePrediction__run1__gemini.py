from function_11 import bucket_sort
import pytest
import inspect


def test_bucket_sort_empty_list():
    assert bucket_sort([]) == []


def test_bucket_sort_invalid_bucket_count():
    assert bucket_sort([1, 2, 3], bucket_count=0) == []
    assert bucket_sort([1, 2, 3], bucket_count=-5) == []


def test_bucket_sort_all_elements_equal():
    assert bucket_sort([5, 5, 5, 5]) == [5, 5, 5, 5]


def test_bucket_sort_nominal():
    unsorted = [0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51]
    sorted_list = bucket_sort(unsorted, bucket_count=5)
    assert sorted_list == [0.32, 0.33, 0.37, 0.42, 0.47, 0.51, 0.52]


def test_bucket_sort_integers():
    unsorted = [45, 23, 11, 89, 77, 98, 4, 28, 65, 43]
    sorted_list = bucket_sort(unsorted, bucket_count=5)
    assert sorted_list == [4, 11, 23, 28, 43, 45, 65, 77, 89, 98]


def test_bucket_sort_boundary_max_value():
    unsorted = [1, 10]
    sorted_list = bucket_sort(unsorted, bucket_count=3)
    assert sorted_list == [1, 10]


def test_bucket_sort_default_bucket_count():
    # Mutmut_1: Mutating default bucket_count to 11 causes the default signature parameter to change, which we inspect directly.
    sig = inspect.signature(bucket_sort)
    assert sig.parameters['bucket_count'].default == 10


def test_bucket_sort_bucket_count_one():
    # Mutmut_6: changes bucket_count <= 0 to <= 1, causing bucket_count=1 to return [] instead of sorted list.
    assert bucket_sort([3, 1, 2], bucket_count=1) == [1, 2, 3]


def test_bucket_sort_bucket_size_multiplication():
    # Mutmut_12: Mutating division to multiplication changes bucket_size from 5.0 to 125.0, resulting in all elements placed into bucket index 0.
    unsorted = [0, 50, 100]
    buckets_count = 2
    # With original bucket_size = 50.0 / 2 = 25.0, elements land in separate buckets. With multiplication it's 50.0 * 2 = 100.0, all land in 0.
    assert bucket_sort(unsorted, bucket_count=buckets_count) == [0, 50, 100]


def test_bucket_sort_bucket_size_addition():
    # Mutmut_13: Mutating minus to plus in (max_value + min_value) changes bucket_size from (10-0)/2 = 5 to (10+0)/2 = 5, wait let's use min_value > 0: [10, 20], min=10, max=20. Original size = 10/2=5; mutated size = 30/2=15.
    unsorted = [10, 20]
    assert bucket_sort(unsorted, bucket_count=2) == [10, 20]


def test_bucket_sort_index_multiplication():
    # Mutmut_22: Mutating / bucket_size to * bucket_size in index calculation produces completely wrong indices, scrambling or misplacing elements.
    unsorted = [1, 2, 3]
    assert bucket_sort(unsorted, bucket_count=3) == [1, 2, 3]


def test_bucket_sort_index_addition():
    # Mutmut_23: Mutating (val - min_value) to (val + min_value) shifts index calculation entirely, causing wrong sorting or IndexError/misplacement.
    unsorted = [10, 15, 20]
    assert bucket_sort(unsorted, bucket_count=2) == [10, 15, 20]


def test_bucket_sort_index_bucket_count_minus_two():
    # Mutmut_25: Mutating bucket_count - 1 to bucket_count - 2 clamps the maximum element index to bucket_count - 2 instead of bucket_count - 1, causing an IndexError or misplaced max element when multiple elements fall into the capped bucket.
    unsorted = [1, 10, 10]
    assert bucket_sort(unsorted, bucket_count=3) == [1, 10, 10]