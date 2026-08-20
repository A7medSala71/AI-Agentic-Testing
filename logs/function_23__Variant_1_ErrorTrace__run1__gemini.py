from function_23 import quick_select, median


def test_quick_select_nominal():
    items = [9, 1, 5, 3, 7, 2, 8, 4, 6]
    assert quick_select(items, 0) == 1
    assert quick_select(items, 4) == 5
    assert quick_select(items, 8) == 9


def test_quick_select_duplicates():
    items = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    sorted_items = sorted(items)
    for i in range(len(items)):
        assert quick_select(items, i) == sorted_items[i]


def test_quick_select_out_of_bounds():
    items = [10, 20, 30]
    assert quick_select(items, -1) is None
    assert quick_select(items, 3) is None
    assert quick_select(items, 100) is None


def test_quick_select_single_element():
    items = [42]
    assert quick_select(items, 0) == 42
    assert quick_select(items, 1) is None


def test_median_odd_length():
    items = [7, 1, 3, 5, 9]
    assert median(items) == 5
    items_single = [42]
    assert median(items_single) == 42


def test_median_even_length():
    items = [1, 2, 3, 4]
    assert median(items) == 2.5
    items_neg = [-5, 10, 3, 1]
    # sorted: -5, 1, 3, 10 -> median of (1 + 3) / 2 = 2.0
    assert median(items_neg) == 2.0


def test_quick_select_pivot_equal_handling():
    # Ensures exact matches on pivot (the 'else' branch in partition) are correctly
    # counted and returned, killing mutants where equal elements are appended as None
    # or count initialization/mutation bugs occur.
    items = [5, 5, 5, 5, 5]
    assert quick_select(items, 0) == 5
    assert quick_select(items, 2) == 5
    assert quick_select(items, 4) == 5


def test_quick_select_boundary_m_greater_than_index():
    # Tests the branch `elif m > index:` vs `elif m >= index:`
    # When m == index, the pivot itself should be returned. If mutated to m >= index,
    # it would incorrectly recurse into `smaller` and fail or return incorrect results.
    items = [10, 20, 30]
    # sorted: [10, 20, 30]
    # index 1 should return 20 (which is the pivot if chosen, and m == 1)
    assert quick_select(items, 1) == 20