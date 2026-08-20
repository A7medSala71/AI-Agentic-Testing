from function_06 import mode
import pytest


def test_mode_empty_list():
    assert mode([]) == []


def test_mode_single_element():
    assert mode([42]) == [42]


def test_mode_unique_elements():
    res = mode([1, 2, 3])
    assert sorted(res) == [1, 2, 3]


def test_mode_single_mode():
    assert mode([1, 2, 2, 3]) == [2]


def test_mode_multiple_modes():
    assert mode([1, 1, 2, 2, 3]) == [1, 2]


def test_mode_mixed_types():
    res = mode([1, "a", 1, "a", 2])
    assert sorted(res, key=str) == [1, "a"]


def test_mode_nested_structures():
    t1 = (1, 2)
    t2 = (1, 2)
    assert mode([t1, t2, (3, 4)]) == [(1, 2)]


def test_mode_unhashable():
    with pytest.raises(TypeError):
        mode([[1, 2], [1, 2]])
