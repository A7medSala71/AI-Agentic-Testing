import pytest
from function_06 import mode


def test_mode_empty_list():
    assert mode([]) == []


def test_mode_single_element():
    assert mode([42]) == [42]


def test_mode_unique_elements():
    assert sorted(mode([1, 2, 3])) == [1, 2, 3]


def test_mode_clear_single_mode():
    assert mode([1, 2, 2, 3]) == [2]


def test_mode_multiple_modes():
    assert sorted(mode([1, 1, 2, 2, 3])) == [1, 2]


def test_mode_mixed_types():
    assert mode([1, 'a', 'a', 1]) == [1, 'a']


def test_mode_hashable_and_unhashable():
    # The set comprehension requires hashable elements or will raise TypeError
    # Let's test that lists containing unhashable types like dicts or lists work or raise appropriately
    with pytest.raises(TypeError):
        mode([[1], [1], 2])
