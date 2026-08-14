import pytest
from function_06 import mode


def test_mode_empty_list():
    assert mode([]) == []


def test_mode_single_element():
    assert mode([5]) == [5]


def test_mode_unique_elements():
    assert mode([1, 2, 3]) == [1, 2, 3]


def test_mode_single_mode():
    assert mode([1, 2, 2, 3]) == [2]


def test_mode_multiple_modes():
    assert mode([1, 1, 2, 2, 3]) == [1, 2]


def test_mode_mixed_types():
    assert mode([1, "a", 1, "b"]) == [1]


def test_mode_complex_datastructures():
    assert mode([(1, 2), (1, 2), (3,), (3,)]) == [(1, 2), (3,)]


def test_mode_unhashable_type_raises_type_error():
    with pytest.raises(TypeError):
        mode([[1, 2], [1, 2]])
