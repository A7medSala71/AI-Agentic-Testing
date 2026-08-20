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
    unsorted = [0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51]
    sorted_res = bucket_sort(unsorted, bucket_count=5)
    assert sorted_res == sorted(unsorted)


def test_bucket_sort_integers():
    unsorted = [55, 12, 42, 3, 19, 88, 72]
    assert bucket_sort(unsorted, bucket_count=4) == [3, 12, 19, 42, 55, 72, 88]


def test_bucket_sort_boundary_index():
    unsorted = [10, 100]
    # Max value mapped with index logic should fall safely into bucket_count - 1
    assert bucket_sort(unsorted, bucket_count=2) == [10, 100]


def test_bucket_sort_default_bucket_count():
    # Tests default argument bucket_count=10 vs 11 (mutmut_1)
    unsorted = [0, 9]
    # With bucket_count=10, 9 goes to bucket 9. With bucket_count=11, 9 goes to bucket 9 as well,
    # but let's use a dataset where default 10 vs 11 behaves differently or test explicitly.
    # Actually, mutmut_1 mutates default bucket_count from 10 to 11 in the signature.
    # We can check behavior when bucket_count isn't specified, or explicitly test default parameter value.
    import inspect
    sig = inspect.signature(bucket_sort)
    assert sig.parameters['bucket_count'].default == 10
    unsorted = list(range(20, 0, -1))
    assert bucket_sort(unsorted) == sorted(unsorted)


def test_bucket_sort_bucket_count_one():
    # Tests bucket_count <= 0 vs <= 1 (mutmut_6)
    assert bucket_sort([1, 2, 3], bucket_count=1) == [1, 2, 3]


def test_bucket_sort_arithmetic_operators():
    # Catches arithmetic mutations like division vs multiplication, minus vs plus in bucket_size / index
    unsorted = [10, 20, 30, 40]
    assert bucket_sort(unsorted, bucket_count=3) == [10, 20, 30, 40]
    
    # Specifically target mutations in bucket_size:
    # bucket_size = (max_value - min_value) / bucket_count
    # Mutated to * or +:
    # Let min=0, max=10, bucket_count=2. bucket_size = 10/2 = 5.
    # If mutated to *, bucket_size = 0 * 2 = 0 (causes ZeroDivisionError or wrong distribution).
    # If mutated to +, bucket_size = 10 / 2 = 5 (wait, (max+min)/k = (10+0)/2 = 5). Let's use min=2, max=10, k=2.
    # Original: (10 - 2) / 2 = 4.0
    # Mutated (+): (10 + 2) / 2 = 6.0 -> changes index calculation for values like 6.
    unsorted2 = [2, 6, 10]
    assert bucket_sort(unsorted2, bucket_count=2) == [2, 6, 10]


def test_bucket_sort_max_value_bucket_count_two():
    # Catches bucket_count - 2 vs bucket_count - 1 (mutmut_25)
    # And catches val - min_value vs val + min_value (mutmut_23)
    # And catches / bucket_size vs * bucket_size (mutmut_22)
    unsorted = [1, 10]
    assert bucket_sort(unsorted, bucket_count=2) == [1, 10]