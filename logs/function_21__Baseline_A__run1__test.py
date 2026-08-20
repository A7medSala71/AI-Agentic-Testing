from function_21 import binary_search


def test_binary_search_empty_list():
    assert binary_search([], 5) is False


def test_binary_search_single_item_found():
    assert binary_search([10], 10) is True


def test_binary_search_single_item_not_found():
    assert binary_search([10], 5) is False


def test_binary_search_exact_midpoint():
    assert binary_search([1, 3, 5, 7, 9], 5) is True


def test_binary_search_left_half():
    assert binary_search([1, 3, 5, 7, 9], 3) is True


def test_binary_search_right_half():
    assert binary_search([1, 3, 5, 7, 9], 7) is True


def test_binary_search_not_present_smaller():
    assert binary_search([1, 3, 5, 7, 9], 0) is False


def test_binary_search_not_present_larger():
    assert binary_search([1, 3, 5, 7, 9], 10) is False


def test_binary_search_not_present_in_between():
    assert binary_search([1, 3, 5, 7, 9], 4) is False
