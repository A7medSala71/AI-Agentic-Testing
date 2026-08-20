from function_16 import odd_even_sort


def test_odd_even_sort_nominal():
    arr = [4, 3, 2, 1, 5]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3, 4, 5]
    assert arr == [1, 2, 3, 4, 5]


def test_odd_even_sort_already_sorted():
    arr = [1, 2, 3, 4, 5]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3, 4, 5]


def test_odd_even_sort_reverse_sorted():
    arr = [5, 4, 3, 2, 1]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3, 4, 5]


def test_odd_even_sort_empty_and_single():
    assert odd_even_sort([]) == []
    assert odd_even_sort([42]) == [42]


def test_odd_even_sort_duplicates_and_negatives():
    arr = [-1, 3, -1, 0, 5, 3, 2]
    res = odd_even_sort(arr)
    assert res == [-1, -1, 0, 2, 3, 3, 5]


def test_odd_even_sort_needs_multiple_passes_and_exact_indices():
    # Specific arrays to test odd-even phase bounds, steps, sorting stability, and swapping behavior
    # Array requiring swaps in both even and odd phase loops to trigger is_sorted = False and range limits
    arr = [2, 1, 4, 3]
    res = odd_even_sort(arr)
    assert res == [1, 2, 3, 4]

    # Array with duplicate elements to kill conditional boundary mutants (> vs >=)
    # Also ensures stable sorting doesn't change order of equal elements
    arr_dup = [2, 2, 1, 1]
    res_dup = odd_even_sort(arr_dup)
    assert res_dup == [1, 1, 2, 2]