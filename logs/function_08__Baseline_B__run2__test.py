import pytest
from function_08 import num_digits, num_digits_fast, num_digits_faster


def test_num_digits_zero():
    assert num_digits(0) == 1


def test_num_digits_positive():
    assert num_digits(5) == 1
    assert num_digits(42) == 2
    assert num_digits(999) == 3
    assert num_digits(1000) == 4


def test_num_digits_negative():
    assert num_digits(-7) == 1
    assert num_digits(-523) == 3


def test_num_digits_type_error():
    with pytest.raises(TypeError):
        num_digits(123.45)
    with pytest.raises(TypeError):
        num_digits("123")


def test_num_digits_fast_zero():
    assert num_digits_fast(0) == 1


def test_num_digits_fast_positive():
    assert num_digits_fast(5) == 1
    assert num_digits_fast(42) == 2
    assert num_digits_fast(999) == 3
    assert num_digits_fast(1000) == 4


def test_num_digits_fast_negative():
    assert num_digits_fast(-7) == 1
    assert num_digits_fast(-523) == 3


def test_num_digits_fast_type_error():
    with pytest.raises(TypeError):
        num_digits_fast(123.45)
    with pytest.raises(TypeError):
        num_digits_fast("123")


def test_num_digits_faster_zero():
    assert num_digits_faster(0) == 1


def test_num_digits_faster_positive():
    assert num_digits_faster(5) == 1
    assert num_digits_faster(42) == 2
    assert num_digits_faster(999) == 3
    assert num_digits_faster(1000) == 4


def test_num_digits_faster_negative():
    assert num_digits_faster(-7) == 1
    assert num_digits_faster(-523) == 3


def test_num_digits_faster_type_error():
    with pytest.raises(TypeError):
        num_digits_faster(123.45)
    with pytest.raises(TypeError):
        num_digits_faster("123")
