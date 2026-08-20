from function_23 import quick_select, median


def test_quick_select_nominal():
    items = [9, 1, 5, 3, 7]
    assert quick_select(items, 0) == 1
    assert quick_select(items, 1) == 3
    assert quick_select(items, 2) == 5
    assert quick_select(items, 3) == 7
    assert quick_select(items, 4) == 9


def test_quick_select_duplicates():
    items = [4, 1, 4, 3, 4, 2]
    sorted_items = sorted(items)
    for i in range(len(items)):
        assert quick_select(items, i) == sorted_items[i]


def test_quick_select_boundaries():
    items = [10, 20]
    assert quick_select(items, -1) is None
    assert quick_select(items, 2) is None
    assert quick_select(items, 0) == 10
    assert quick_select(items, 1) == 20


def test_quick_select_empty():
    assert quick_select([], 0) is None


def test_median_odd_length():
    items = [3, 1, 2]
    assert median(items) == 2


def test_median_even_length():
    items = [4, 1, 3, 2]
    assert median(items) == 2.5


def test_median_single_element():
    items = [42]
    assert median(items) == 42


def test_quick_select_m_equals_index_edge_case():
    # Targets the 'm > index' vs 'm >= index' conditional boundary mutant (mutmut_25)
    # and also tests scenarios where equal elements and pivot counts matter.
    items = [5, 5, 5, 5]
    assert quick_select(items, 0) == 5
    assert quick_select(items, 1) == 5
    assert quick_select(items, 2) == 5
    assert quick_select(items, 3) == 5