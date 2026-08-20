from function_21 import binary_search


def test_binary_search_empty_list():
    assert binary_search([], 5) is False


def test_binary_search_single_element_found():
    assert binary_search([5], 5) is True


def test_binary_search_single_element_not_found():
    assert binary_search([5], 3) is False


def test_binary_search_middle_element():
    assert binary_search([1, 3, 5, 7, 9], 5) is True


def test_binary_search_left_half():
    assert binary_search([1, 3, 5, 7, 9], 3) is True


def test_binary_search_right_half():
    assert binary_search([1, 3, 5, 7, 9], 7) is True


def test_binary_search_not_present_smaller():
    assert binary_search([1, 3, 5, 7, 9], 0) is False


def test_binary_search_not_present_larger():
    assert binary_search([1, 3, 5, 7, 9], 10) is False


def test_binary_search_not_present_between():
    assert binary_search([1, 3, 5, 7, 9], 4) is False


def test_binary_search_even_length_list():
    assert binary_search([2, 4, 6, 8], 6) is True
    assert binary_search([2, 4, 6, 8], 4) is True
    assert binary_search([2, 4, 6, 8], 5) is False
