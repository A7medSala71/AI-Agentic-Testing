from function_16 import odd_even_sort


def test_odd_even_sort_nominal():
    data = [4, 3, 2, 1]
    result = odd_even_sort(data)
    assert result == [1, 2, 3, 4]
    assert data is result


def test_odd_even_sort_already_sorted():
    data = [1, 2, 3, 4, 5]
    result = odd_even_sort(data)
    assert result == [1, 2, 3, 4, 5]


def test_odd_even_sort_reverse_sorted():
    data = [5, 4, 3, 2, 1]
    result = odd_even_sort(data)
    assert result == [1, 2, 3, 4, 5]


def test_odd_even_sort_empty_list():
    data = []
    result = odd_even_sort(data)
    assert result == []


def test_odd_even_sort_single_element():
    data = [42]
    result = odd_even_sort(data)
    assert result == [42]


def test_odd_even_sort_duplicates():
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    result = odd_even_sort(data)
    assert result == [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]


def test_odd_even_sort_mutmut_5_and_25_and_26():
    # Mutant 5/25/26: changes is_sorted assignment to None or True, causing infinite loops or premature loop termination on unsorted data.
    data = [2, 1]
    result = odd_even_sort(data)
    assert result == [1, 2]


def test_odd_even_sort_mutmut_12_and_32():
    # Mutant 12/32: removes step argument in range() (defaults step to 1 instead of 2), causing incorrect indexing and sorting failure.
    data = [3, 1, 2]
    result = odd_even_sort(data)
    assert result == [1, 2, 3]