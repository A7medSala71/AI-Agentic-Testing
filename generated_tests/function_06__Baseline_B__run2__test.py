from function_06 import mode
import pytest


def test_mode_empty_list():
    assert mode([]) == []


def test_mode_single_element():
    assert mode([5]) == [5]


def test_mode_unique_elements():
    assert sorted(mode([1, 2, 3])) == [1, 2, 3]


def test_mode_single_mode():
    assert mode([1, 2, 2, 3]) == [2]


def test_mode_multiple_modes():
    assert sorted(mode([1, 1, 2, 2, 3])) == [1, 2]


def test_mode_mixed_types():
    assert mode([1, "a", "a", 1, 1]) == [1]


def test_mode_complex_datastructures():
    t1 = (1, 2)
    t2 = (3, 4)
    assert mode([t1, t2, t1]) == [t1]


def test_mode_unhashable_types():
    with pytest.raises(TypeError):
        mode([[1, 2], [1, 2]])
