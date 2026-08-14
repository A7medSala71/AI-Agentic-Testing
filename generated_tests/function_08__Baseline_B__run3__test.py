import pytest
from function_08 import num_digits, num_digits_fast, num_digits_faster


def test_num_digits_nominal():
    assert num_digits(0) == 1
    assert num_digits(5) == 1
    assert num_digits(10) == 2
    assert num_digits(99) == 2
    assert num_digits(100) == 3
    assert num_digits(-5) == 1
    assert num_digits(-123) == 3
    assert num_digits(123456789) == 9


def test_num_digits_type_error():
    with pytest.raises(TypeError):
        num_digits(123.45)
    with pytest.raises(TypeError):
        num_digits("123")
    with pytest.raises(TypeError):
        num_digits(None)


def test_num_digits_fast_nominal():
    assert num_digits_fast(0) == 1
    assert num_digits_fast(5) == 1
    assert num_digits_fast(10) == 2
    assert num_digits_fast(99) == 2
    assert num_digits_fast(100) == 3
    assert num_digits_fast(-5) == 1
    assert num_digits_fast(-123) == 3
    assert num_digits_fast(123456789) == 9


def test_num_digits_fast_type_error():
    with pytest.raises(TypeError):
        num_digits_fast(123.45)
    with pytest.raises(TypeError):
        num_digits_fast("123")
    with pytest.raises(TypeError):
        num_digits_fast(None)


def test_num_digits_faster_nominal():
    assert num_digits_faster(0) == 1
    assert num_digits_faster(5) == 1
    assert num_digits_faster(10) == 2
    assert num_digits_faster(99) == 2
    assert num_digits_faster(100) == 3
    assert num_digits_faster(-5) == 1
    assert num_digits_faster(-123) == 3
    assert num_digits_faster(123456789) == 9


def test_num_digits_faster_type_error():
    with pytest.raises(TypeError):
        num_digits_faster(123.45)
    with pytest.raises(TypeError):
        num_digits_faster("123")
    with pytest.raises(TypeError):
        num_digits_faster(None)
