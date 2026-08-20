from function_21 import binary_search


def test_binary_search_empty_list():
    assert binary_search([], 5) is False


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


def test_binary_search_multiple_elements_boundaries():
    assert binary_search([1, 3, 5, 7, 9], 1) is True
    assert binary_search([1, 3, 5, 7, 9], 9) is True


def test_binary_search_multiple_elements_not_found():
    assert binary_search([1, 3, 5, 7, 9], 4) is False
    assert binary_search([1, 3, 5, 7, 9], 0) is False
    assert binary_search([1, 3, 5, 7, 9], 10) is False


def test_binary_search_midpoint_division_by_three():
    # Mutant mutmut_6 changes midpoint = len(a_list) // 2 to // 3, shifting index calculation for length 4 list [10, 20, 30, 40] with item 30 from index 2 to index 1.
    assert binary_search([10, 20, 30, 40], 30) is True


def test_binary_search_conditional_boundary_less_than_or_equal():
    # Mutant mutmut_9 changes item < a_list[midpoint] to item <= a_list[midpoint], causing a search in the left slice when item equals midpoint.
    assert binary_search([1, 3, 5, 7, 9], 5) is True