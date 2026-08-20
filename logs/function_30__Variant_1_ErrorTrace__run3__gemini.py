import pytest
from function_30 import perfect_cube
from function_30 import perfect_cube_binary_search


def test_perfect_cube_nominal():
    assert perfect_cube(0) == True
    assert perfect_cube(1) == True
    assert perfect_cube(8) == True
    assert perfect_cube(27) == True
    assert perfect_cube(64) == True


def test_perfect_cube_non_cubes():
    assert perfect_cube(2) == False
    assert perfect_cube(7) == False
    assert perfect_cube(9) == False
    assert perfect_cube(26) == False


def test_perfect_cube_negatives():
    assert perfect_cube(-1) == False
    assert perfect_cube(-8) == False


def test_perfect_cube_binary_search_nominal():
    assert perfect_cube_binary_search(0) == True
    assert perfect_cube_binary_search(1) == True
    assert perfect_cube_binary_search(8) == True
    assert perfect_cube_binary_search(27) == True
    assert perfect_cube_binary_search(125) == True


def test_perfect_cube_binary_search_non_cubes():
    assert perfect_cube_binary_search(2) == False
    assert perfect_cube_binary_search(26) == False
    assert perfect_cube_binary_search(28) == False


def test_perfect_cube_binary_search_negatives():
    assert perfect_cube_binary_search(-1) == True
    assert perfect_cube_binary_search(-8) == True
    assert perfect_cube_binary_search(-27) == True
    assert perfect_cube_binary_search(-2) == False


def test_perfect_cube_binary_search_large():
    assert perfect_cube_binary_search(1000000) == True
    assert perfect_cube_binary_search(999999) == False


def test_perfect_cube_binary_search_type_error():
    with pytest.raises(TypeError):
        perfect_cube_binary_search(8.0)
    with pytest.raises(TypeError):
        perfect_cube_binary_search("8")
