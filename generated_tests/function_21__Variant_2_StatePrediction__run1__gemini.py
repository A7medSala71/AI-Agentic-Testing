from function_21 import binary_search


def test_binary_search_empty_list():
    assert binary_search([], 1) is False


def test_binary_search_single_element_found():
    assert binary_search([5], 5) is True


def test_binary_search_single_element_not_found():
    assert binary_search([5], 3) is False


def test_binary_search_multiple_elements_middle():
    assert binary_search([1, 3, 5, 7, 9], 5) is True


def test_binary_search_multiple_elements_left():
    assert binary_search([1, 3, 5, 7, 9], 3) is True


def test_binary_search_multiple_elements_right():
    assert binary_search([1, 3, 5, 7, 9], 7) is True


def test_binary_search_multiple_elements_not_found_smaller():
    assert binary_search([1, 3, 5, 7, 9], 0) is False


def test_binary_search_multiple_elements_not_found_larger():
    assert binary_search([1, 3, 5, 7, 9], 10) is False


def test_binary_search_multiple_elements_not_found_between():
    assert binary_search([1, 3, 5, 7, 9], 4) is False


def test_binary_search_midpoint_division_by_three():
    # Mutant mutmut_6 changes midpoint divisor from 2 to 3, checking length 6 list where index 2 vs 3 diverges.
    assert binary_search([10, 20, 30, 40, 50, 60], 30) is True


def test_binary_search_conditional_boundary_less_than_or_equal():
    # Mutant mutmut_9 changes item < a_list[midpoint] to item <= a_list[midpoint], causing search to go left incorrectly when item equals midpoint.
    assert binary_search([10, 20, 30], 20) is True