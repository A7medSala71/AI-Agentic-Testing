from function_23 import quick_select, median, _partition
import pytest


def test_quick_select_nominal():
    items = [9, 1, 5, 3, 7, 2, 8, 4, 6]
    assert quick_select(items, 0) == 1
    assert quick_select(items, 4) == 5
    assert quick_select(items, 8) == 9


def test_quick_select_duplicates():
    items = [5, 1, 5, 3, 3, 5, 2]
    sorted_items = sorted(items)
    for i in range(len(items)):
        assert quick_select(items, i) == sorted_items[i]


def test_quick_select_out_of_bounds():
    items = [1, 2, 3]
    assert quick_select(items, -1) is None
    assert quick_select(items, 3) is None
    assert quick_select(items, 100) is None


def test_median_odd_length():
    items = [3, 1, 4, 1, 5, 9, 2]
    assert median(items) == 3


def test_median_even_length():
    items = [3, 1, 4, 1, 5, 9, 2, 6]
    sorted_items = sorted(items)
    expected = (sorted_items[3] + sorted_items[4]) / 2
    assert median(items) == pytest.approx(expected)


def test_median_single_element():
    items = [42]
    assert median(items) == 42


def test_partition_equal_append_mutation():
    # Mutator changes equal.append(element) to equal.append(None), so equal list contains None instead of element
    # State divergence: equal list will contain [None] instead of [2] for pivot=2
    _, equal, _ = _partition([2], 2)
    assert equal == [2]


def test_quick_select_count_initialization_mutations():
    # Mutator changes count = 0 to count = None or 1, causing count to be wrong for elements equal to pivot
    # State divergence: when selecting an element equal to the pivot, count is miscalculated, causing incorrect branch entry
    items = [5, 5, 5]
    assert quick_select(items, 1) == 5


def test_quick_select_conditional_boundary_m_ge_index():
    # Mutator changes elif m > index to elif m >= index, making m >= index trigger smaller recursive call instead of target or larger
    # State divergence: when m == index, m >= index wrongly enters smaller branch instead of returning pivot
    items = [5, 5, 5]
    assert quick_select(items, 1) == 5