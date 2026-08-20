import pytest
from function_23 import quick_select, median, _partition


def test_quick_sub_nominal():
    items = [7, 2, 1, 6, 8, 5, 3, 4]
    sorted_items = sorted(items)
    for i in range(len(items)):
        assert quick_select(items, i) == sorted_items[i]


def test_quick_select_out_of_bounds():
    items = [1, 2, 3]
    assert quick_select(items, -1) is None
    assert quick_select(items, 3) is None
    assert quick_select(items, 100) is None


def test_quick_select_duplicates():
    items = [5, 1, 5, 3, 5, 2, 1]
    sorted_items = sorted(items)
    for i in range(len(items)):
        assert quick_select(items, i) == sorted_items[i]


def test_median_odd_length():
    items = [9, 1, 5, 3, 7]
    assert median(items) == 5


def test_median_even_length():
    items = [10, 1, 4, 2]
    sorted_items = sorted(items)
    expected = (sorted_items[1] + sorted_items[2]) / 2
    assert median(items) == expected


def test_median_single_element():
    assert median([42]) == 42


def test_partition_equal_elements():
    # Kills mutants on count = 0 / 1 / None and equal.append(None)
    less, equal, greater = _partition([5, 5, 5], 5)
    assert less == []
    assert equal == [5, 5, 5]
    assert greater == []


def test_quick_select_index_equals_m():
    # Kills mutant changing `elif m > index:` to `elif m >= index:`
    # When m == index, it should fall into the `else` branch (or return pivot),
    # not incorrectly recurse into `smaller`.
    items = [3, 1, 2]
    # sorted: 1, 2, 3. smaller = [1], equal = [2], larger = [3].
    # m = 1 (smaller has len 1), index = 1 -> should return 2 (the pivot).
    # If `m >= index` triggers, it goes to `quick_select(smaller, 1)` which returns None.
    assert quick_select(items, 1) == 2