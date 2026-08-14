from function_23 import quick_select, median


def test_quick_select_nominal_single():
    assert quick_select([42], 0) == 42


def test_quick_select_nominal_multiple():
    items = [3, 1, 4, 1, 5, 9, 2, 6]
    sorted_items = sorted(items)
    for i in range(len(items)):
        assert quick_select(items, i) == sorted_items[i]


def test_quick_select_out_of_bounds_high():
    assert quick_select([1, 2, 3], 3) is None


def test_quick_select_out_of_bounds_low():
    assert quick_select([1, 2, 3], -1) is None


def test_median_odd_length():
    items = [7, 2, 5, 1, 9]
    assert median(items) == 5


def test_median_even_length():
    items = [7, 2, 5, 1, 9, 3]
    assert median(items) == 4.0
