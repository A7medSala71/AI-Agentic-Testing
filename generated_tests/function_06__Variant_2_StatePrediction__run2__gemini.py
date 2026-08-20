import pytest
from function_06 import mode


def test_mode_empty_list():
    assert mode([]) == []


def test_mode_single_element():
    assert mode([42]) == [42]


def test_mode_unique_single_mode():
    assert mode([1, 2, 2, 3]) == [2]


def test_mode_multiple_modes():
    assert mode([1, 1, 2, 2, 3]) == [1, 2]


def test_mode_all_unique():
    assert mode([3, 1, 2]) == [1, 2, 3]


def test_mode_mixed_types():
    # Note: sorting mixed types (like int and str) might fail in Python 3 if they are not comparable,
    # but we can test with types that are safely comparable or just check equal frequency.
    # Let's test with a tuple and string, or integers and floats.
    assert mode([1, 1.0, 2]) == [1, 1.0]


def test_mode_complex_datastructures():
    t1 = (1, 2)
    t2 = (3, 4)
    assert mode([t1, t2, t1]) == [(1, 2)]
