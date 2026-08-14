import pytest
from function_30 import perfect_cube
from function_30 import perfect_cube_binary_search


def test_perfect_cube_nominal():
    assert perfect_cube(27) is True
    assert perfect_cube(0) is True
    assert perfect_cube(1) is True
    assert perfect_cube(8) is True
    assert perfect_cube(64) is True


def test_perfect_cube_non_cubes():
    assert perfect_cube(2) is False
    assert perfect_cube(26) is False
    assert perfect_cube(28) is False
    assert perfect_cube(9) is False


def test_perfect_cube_negative():
    assert perfect_cube(-27) is True
    assert perfect_cube(-8) is True
    assert perfect_cube(-1) is True
    assert perfect_cube(-2) is False


def test_perfect_cube_binary_search_nominal():
    assert perfect_cube_binary_search(27) is True
    assert perfect_cube_binary_search(0) is True
    assert perfect_cube_binary_search(1) is True
    assert perfect_cube_binary_search(8) is True
    assert perfect_cube_binary_search(125) is True


def test_perfect_cube_binary_search_non_cubes():
    assert perfect_cube_binary_search(2) is False
    assert perfect_cube_binary_search(26) is False
    assert perfect_cube_binary_search(28) is False
    assert perfect_cube_binary_search(99) is False


def test_perfect_cube_binary_search_negative():
    assert perfect_cube_binary_search(-27) is True
    assert perfect_cube_binary_search(-8) is True
    assert perfect_cube_binary_search(-2) is False


def test_perfect_cube_binary_search_type_error():
    with pytest.raises(TypeError):
        perfect_cube_binary_search(27.0)
    with pytest.raises(TypeError):
        perfect_cube_binary_search("27")
