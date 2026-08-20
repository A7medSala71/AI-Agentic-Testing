from function_23 import quick_select, median


def test_quick_signal_nominal(): items = [3, 1, 4, 1, 5, 9, 2, 6]; sorted_items = sorted(items); for i in range(len(items)): assert quick_select(items, i) == sorted_items[i]


def test_quick_select_out_of_bounds(): items = [1, 2, 3]; assert quick_select(items, -1) is None; assert quick_select(items, 3) is None; assert quick_select(items, 100) is None


def test_quick_select_single_element(): items = [42]; assert quick_select(items, 0) == 42; assert quick_select(items, 1) is None


def test_median_odd_length(): items = [3, 1, 2]; assert median(items) == 2


def test_median_even_length(): items = [4, 1, 3, 2]; assert median(items) == 2.5


def test_median_empty(): assert median([]) is None
