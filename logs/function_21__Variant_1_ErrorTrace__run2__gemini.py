from function_21 import binary_search


def test_binary_search_empty_list():
    assert binary_search([], 5) is False


def test_binary_search_single_element_found():
    assert binary_search([5], 5) is True


def test_binary_search_single_element_not_found():
    assert binary_search([5], 3) is False


def test_binary_search_exact_midpoint():
    assert binary_search([1, 3, 5, 7, 9], 5) is True


def test_binary_search_left_branch():
    assert binary_search([1, 3, 5, 7, 9], 3) is True


def test_binary_search_right_branch():
    assert binary_search([1, 3, 5, 7, 9], 7) is True


def test_binary_search_not_present_smaller():
    assert binary_search([1, 3, 5, 7, 9], 0) is False


def test_binary_search_not_present_larger():
    assert binary_search([1, 3, 5, 7, 9], 10) is False


def test_binary_search_not_present_between():
    assert binary_search([1, 3, 5, 7, 9], 4) is False


def test_binary_search_even_length():
    assert binary_search([2, 4, 6, 8], 6) is True
    assert binary_search([2, 4, 6, 8], 4) is True
    assert binary_search([2, 4, 6, 8], 5) is False


def test_binary_search_midpoint_division_and_duplicates():
    # Kills mutants changing `// 2` (e.g. to `// 3`) and `<` to `<=` on duplicate values.
    # With [1, 2, 2, 2, 3], length 5, midpoint index is 2 (value 2).
    # If item is 2, a_list[midpoint] is 2. `item < a_list[midpoint]` (2 < 2) is False,
    # so it goes to the right branch. If mutated to `<=`, 2 <= 2 is True, going left.
    assert binary_search([1, 2, 2, 2, 3], 2) is True
    # Also test an asymmetric list length where // 2 vs // 3 matters for indexing
    assert binary_search([10, 20, 30, 40, 50, 60], 40) is True
    assert binary_search([10, 20, 30, 40, 50, 60], 20) is True