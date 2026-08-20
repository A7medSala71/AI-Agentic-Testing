import pytest
from function_06 import mode


def test_mode_empty_list():
    assert mode([]) == []


def test_mode_single_element():
    assert mode([5]) == [5]


def test_mode_unique_mode():
    assert mode([1, 2, 2, 3]) == [2]


def test_mode_multiple_modes():
    assert mode([1, 1, 2, 2, 3]) == [1, 2]


def test_mode_all_unique():
    assert mode([1, 2, 3, 4]) == [1, 2, 3, 4]


def test_mode_mixed_types():
    assert mode([1, "a", 1, "b", "a"]) == [1, "a"]


def test_mode_nested_datastructures():
    t1 = (1, 2)
    t2 = (3, 4)
    assert mode([t1, t2, t1]) == [(1, 2)]
