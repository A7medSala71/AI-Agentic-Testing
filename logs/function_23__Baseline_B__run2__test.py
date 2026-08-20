from function_23 import quick_select, median


def test_quick_select_nominal_single_element():
    assert quick_select([42], 0) == 42


def test_quick_select_nominal_unsorted():
    items = [9, 1, 5, 3, 7]
    assert quick_select(items, 0) == 1
    assert quick_select(items, 2) == 5
    assert quick_select(items, 4) == 9


def test_quick_select_boundary_index_out_of_bounds():
    items = [10, 20, 30]
    assert quick_select(items, -1) is None
    assert quick_select(items, 3) is None
    assert quick_select(items, 100) is None


def test_quick_select_duplicates():
    items = [5, 1, 5, 3, 5, 2]
    assert quick_select(items, 0) == 1
    assert quick_select(items, 3) == 5
    assert quick_select(items, 5) == 5


def test_median_odd_length():
    items = [7, 1, 3, 9, 5]
    assert median(items) == 5


def test_median_even_length():
    items = [10, 20, 30, 40]
    assert median(items) == 25.0


def test_median_single_element():
    assert median([99]) == 99


def test_median_empty_list():
    assert median([]) is None
