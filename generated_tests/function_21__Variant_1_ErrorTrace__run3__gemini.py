from function_21 import binary_search


def test_binary_search_empty_list():
    assert binary_search([], 5) is False


def test_binary_search_single_item_found():
    assert binary_search([10], 10) is True


def test_binary_search_single_item_not_found():
    assert binary_search([10], 5) is False


def test_binary_search_midpoint_match():
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


def test_binary_search_even_length_list():
    assert binary_search([2, 4, 6, 8], 6) is True
    assert binary_search([2, 4, 6, 8], 4) is True
    assert binary_search([2, 4, 6, 8], 5) is False


def test_binary_search_longer_list_tests_midpoint_and_less_than_boundary():
    # Kills mutant 6: midpoint = len(a_list) // 3
    # Kills mutant 9: if item <= a_list[midpoint]:
    # With a list of length 4, e.g. [1, 2, 3, 4], // 2 is index 2 (val 3).
    # // 3 is index 1 (val 2).
    # Also, searching for duplicate elements or testing items equal to midpoint on a larger list.
    assert binary_search([1, 2, 3, 4], 2) is True
    assert binary_search([10, 20, 30, 40], 20) is True
    assert binary_search([10, 20, 30, 40], 30) is True
    # If item == a_list[midpoint], it should return True immediately (not go to the left branch via <=)
    # Let's test with duplicate values to ensure <= vs < behaves correctly on duplicates
    assert binary_search([1, 2, 2, 3], 2) is True