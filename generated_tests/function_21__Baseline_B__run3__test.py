from function_21 import binary_search


def test_binary_search_empty_list():
    assert binary_search([], 5) is False


def test_binary_search_single_item_found():
    assert binary_search([5], 5) is True


def test_binary_search_single_item_not_found():
    assert binary_search([5], 3) is False


def test_binary_search_middle_item():
    assert binary_search([1, 3, 5, 7, 9], 5) is True


def test_binary_search_left_side():
    assert binary_search([1, 3, 5, 7, 9], 3) is True


def test_binary_search_right_side():
    assert binary_search([1, 3, 5, 7, 9], 7) is True


def test_binary_search_lower_bound():
    assert binary_search([1, 3, 5, 7, 9], 1) is True


def test_binary_search_upper_bound():
    assert binary_search([1, 3, 5, 7, 9], 9) is True


def test_binary_search_smaller_than_all():
    assert binary_search([1, 3, 5, 7, 9], 0) is False


def test_binary_search_larger_than_all():
    assert binary_search([1, 3, 5, 7, 9], 10) is False


def test_binary_search_between_elements():
    assert binary_search([1, 3, 5, 7, 9], 4) is False


def test_binary_search_even_length_list():
    assert binary_search([2, 4, 6, 8], 6) is True
    assert binary_search([2, 4, 6, 8], 4) is True
    assert binary_search([2, 4, 6, 8], 5) is False
