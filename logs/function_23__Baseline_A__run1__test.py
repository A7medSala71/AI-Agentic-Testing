from function_23 import quick_select, median


def test_quick_select_nominal(): items = [7, 1, 4, 1, 8, 2, 3, 5]; assert quick_select(items, 3) == 3


def test_quick_select_boundary_index(): items = [10, 20, 30]; assert quick_select(items, 0) == 10; assert quick_select(items, 2) == 30


def test_quick_select_out_of_bounds(): items = [1, 2, 3]; assert quick_select(items, -1) is None; assert quick_select(items, 3) is None


def test_median_odd_length(): items = [3, 1, 2]; assert median(items) == 2


def test_median_even_length(): items = [4, 1, 3, 2]; assert median(items) == pytest.approx(2.5)


def test_median_single_element(): items = [42]; assert median(items) == 42
