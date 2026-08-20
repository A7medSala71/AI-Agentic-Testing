import pytest
from function_30 import perfect_cube
from function_30 import perfect_cube_binary_search


def test_perfect_cube_positive_true():
    assert perfect_cube(0) is True
    assert perfect_cube(1) is True
    assert perfect_cube(8) is True
    assert perfect_cube(27) is True
    assert perfect_cube(125) is True


def test_perfect_cube_positive_false():
    assert perfect_cube(2) is False
    assert perfect_cube(7) is False
    assert perfect_cube(9) is False
    assert perfect_cube(26) is False
    assert perfect_cube(28) is False


def test_perfect_cube_negative():
    assert perfect_cube(-1) is True
    assert perfect_cube(-8) is True
    assert perfect_cube(-27) is True
    assert perfect_cube(-2) is False


def test_perfect_cube_binary_search_positive_true():
    assert perfect_cube_binary_search(0) is True
    assert perfect_cube_binary_search(1) is True
    assert perfect_cube_binary_search(8) is True
    assert perfect_cube_binary_search(27) is True
    assert perfect_cube_binary_search(64) is True
    assert perfect_cube_binary_search(1000) is True


def test_perfect_cube_binary_search_positive_false():
    assert perfect_cube_binary_search(2) is False
    assert perfect_cube_binary_search(7) is False
    assert perfect_cube_binary_search(9) is False
    assert perfect_cube_binary_search(26) is False
    assert perfect_cube_binary_search(28) is False


def test_perfect_cube_binary_search_negative():
    assert perfect_cube_binary_search(-1) is True
    assert perfect_cube_binary_search(-8) is True
    assert perfect_cube_binary_search(-27) is True
    assert perfect_cube_binary_search(-2) is False


def test_perfect_cube_binary_search_type_error():
    with pytest.raises(TypeError):
        perfect_cube_binary_search(8.0)
    with pytest.raises(TypeError):
        perfect_cube_binary_search('8')
