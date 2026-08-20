from function_21 import binary_search


def test_binary_search_empty_list():
    assert binary_search([], 5) is False


def test_binary_search_single_element_found():
    assert binary_search([5], 5) is True


def test_binary_search_single_element_not_found():
    assert binary_search([3], 5) is False


def test_binary_search_odd_length_found():
    assert binary_search([1, 3, 5, 7, 9], 5) is True


def test_binary_search_even_length_found():
    assert binary_search([1, 3, 5, 7, 9, 11], 7) is True


def test_binary_search_left_branch():
    assert binary_search([1, 3, 5, 7, 9], 1) is True


def test_binary_search_right_branch():
    assert binary_search([1, 3, 5, 7, 9], 9) is True


def test_binary_search_not_present_smaller():
    assert binary_search([2, 4, 6, 8], 1) is False


def test_binary_search_not_present_larger():
    assert binary_search([2, 4, 6, 8], 10) is False


def test_binary_search_not_present_middle():
    assert binary_search([2, 4, 6, 8], 5) is False


def test_binary_search_mutmut_6_midpoint_division():
    # Mutating len(a_list) // 2 to // 3 changes midpoint on length 3 from 1 to 0, causing search for element at index 1 to miss it.
    assert binary_search([10, 20, 30], 20) is True


def test_binary_search_mutmut_9_conditional_boundary():
    # Mutating item < a_list[midpoint] to item <= a_list[midpoint] causes an item equal to midpoint to incorrectly branch left and return False.
    assert binary_search([10, 20, 30], 20) is True


def test_binary_search_mutmut_19_right_slice_offset():
    # Mutating midpoint + 1 to midpoint + 2 skips the element immediately after midpoint in the right branch.
    assert binary_search([10, 20, 30, 40, 50], 40) is True