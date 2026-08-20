from function_21 import binary_search


def test_binary_search_empty_list():
    assert binary_search([], 1) is False


def test_binary_search_single_element_found():
    assert binary_search([5], 5) is True


def test_binary_search_single_element_not_found():
    assert binary_search([5], 3) is False


def test_binary_search_found_at_midpoint():
    assert binary_search([1, 3, 5, 7, 9], 5) is True


def test_binary_search_found_in_left_half():
    assert binary_search([1, 3, 5, 7, 9], 3) is True


def test_binary_search_found_in_right_half():
    assert binary_search([1, 3, 5, 7, 9], 7) is True


def test_binary_search_not_found_smaller_than_all():
    assert binary_search([10, 20, 30], 5) is False


def test_binary_search_not_found_larger_than_all():
    assert binary_search([10, 20, 30], 35) is False


def test_binary_search_not_found_between_elements():
    assert binary_search([10, 20, 30], 15) is False


def test_binary_search_even_length_list():
    assert binary_search([2, 4, 6, 8], 6) is True
    assert binary_search([2, 4, 6, 8], 4) is True
    assert binary_search([2, 4, 6, 8], 5) is False
