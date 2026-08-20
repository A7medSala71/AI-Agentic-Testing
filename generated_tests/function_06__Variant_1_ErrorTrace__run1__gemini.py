import pytest
from function_06 import mode


def test_mode_empty_list():
    assert mode([]) == []


def test_mode_single_element():
    assert mode([5]) == [5]


def test_mode_single_mode():
    assert mode([1, 2, 2, 3]) == [2]


def test_mode_multiple_modes():
    assert mode([1, 1, 2, 2, 3]) == [1, 2]


def test_mode_all_unique():
    assert sorted(mode([1, 2, 3, 4])) == [1, 2, 3, 4]


def test_mode_mixed_types():
    # Comparing different types like int and float, or strings
    assert mode([1, 1, 'a', 'a', 'a', 2]) == ['a']


def test_mode_complex_datastructures():
    d1 = (1, 2)
    d2 = (1, 2)
    d3 = (3, 4)
    assert mode([d1, d2, d3]) == [(1, 2)]
