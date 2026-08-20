from function_23 import quick_select, median


def test_quick_select_out_of_bounds():
    items = [3, 1, 4, 1, 5, 9]
    assert quick_select(items, -1) is None
    assert quick_select(items, 6) is None
    assert quick_select(items, 100) is None


def test_quick_select_nominal():
    items = [9, 1, 8, 2, 7, 3, 6, 4, 5]
    # Sorted would be [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(len(items)):
        assert quick_select(items, i) == i + 1


def test_quick_select_duplicates():
    items = [5, 2, 5, 1, 2, 5]
    # Sorted: [1, 2, 2, 5, 5, 5]
    sorted_items = sorted(items)
    for i in range(len(items)):
        assert quick_select(items, i) == sorted_items[i]


def test_median_odd_length():
    items = [3, 1, 2]
    assert median(items) == 2
    items2 = [7, 2, 5, 1, 9]
    assert median(items2) == 5


def test_median_even_length():
    items = [4, 1, 3, 2]
    # Sorted: [1, 2, 3, 4], middle elements are 2 and 3, average is 2.5
    assert median(items) == pytest.approx(2.5)
    items2 = [10, 20]
    assert median(items2) == pytest.approx(15.0)
