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


def test_odd_even_sort_empty():
    arr = []
    res = odd_even_sort(arr)
    assert res == []


def test_odd_even_sort_single_element():
    arr = [42]
    res = odd_even_sort(arr)
    assert res == [42]


def test_odd_even_sort_duplicates():
    arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    res = odd_even_sort(arr)
    assert res == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]


def test_odd_even_sort_negative_numbers():
    arr = [-3, 5, 0, -1, 2]
    res = odd_even_sort(arr)
    assert res == [-3, -1, 0, 2, 5]


def test_odd_even_sort_kills_mutmut_5():
    # If is_sorted = None instead of True, a sorted multi-element list enters an infinite loop, raising TypeError when compared or hanging.
    assert odd_even_sort([2, 1, 3, 4]) == [1, 2, 3, 4]


def test_odd_even_sort_kills_mutmut_12_and_32():
    # If the step is removed (default 1), even/odd phases compare overlapping indices and corrupt sorting of a 4-element list.
    arr = [3, 1, 4, 2]
    assert odd_even_sort(arr) == [1, 2, 3, 4]


def test_odd_even_sort_kills_mutmut_15():
    # If range stop is len - 2 instead of len - 1 in even phase, the last pair at indices len-2 and len-1 is skipped, leaving it unsorted.
    arr = [1, 3, 2]
    assert odd_even_sort(arr) == [1, 2, 3]


def test_odd_even_sort_kills_mutmut_25_and_26():
    # If is_sorted becomes None or True instead of False on swap, a single swap causes the loop to terminate immediately without fully sorting.
    arr = [3, 1, 2]
    assert odd_even_sort(arr) == [1, 2, 3]