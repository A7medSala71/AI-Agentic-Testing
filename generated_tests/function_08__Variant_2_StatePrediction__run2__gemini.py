import pytest
from function_08 import num_digits
from function_08 import num_digits_fast
from function_08 import num_digits_faster


def test_num_digits_zero():
    assert num_digits(0) == 1


def test_num_digits_positive():
    assert num_digits(5) == 1
    assert num_digits(99) == 2
    assert num_digits(100) == 3
    assert num_digits(123456789) == 9


def test_num_digits_negative():
    assert num_digits(-7) == 1
    assert num_digits(-10) == 2
    assert num_digits(-999) == 3


def test_num_digits_type_error():
    with pytest.raises(TypeError):
        num_digits(1.5)
    with pytest.raises(TypeError):
        num_digits("123")


def test_num_digits_fast_zero():
    assert num_digits_fast(0) == 1


def test_num_digits_fast_positive():
    assert num_digits_fast(1) == 1
    assert num_digits_fast(9) == 1
    assert num_digits_fast(10) == 2
    assert num_digits_fast(99) == 2
    assert num_digits_fast(100) == 3
    assert num_digits_fast(1000) == 4


def test_num_digits_fast_negative():
    assert num_digits_fast(-5) == 1
    assert num_digits_fast(-10) == 2
    assert num_digits_fast(-1234) == 4


def test_num_digits_fast_type_error():
    with pytest.raises(TypeError):
        num_digits_fast(10.0)
    with pytest.raises(TypeError):
        num_digits_fast(None)


def test_num_digits_faster_zero():
    assert num_digits_faster(0) == 1


def test_num_digits_faster_positive():
    assert num_digits_faster(7) == 1
    assert num_digits_faster(42) == 2
    assert num_digits_faster(999) == 3


def test_num_digits_faster_negative():
    assert num_digits_faster(-7) == 1
    assert num_digits_faster(-42) == 2
    assert num_digits_faster(-999) == 3


def test_num_digits_faster_type_error():
    with pytest.raises(TypeError):
        num_digits_faster(123.45)
    with pytest.raises(TypeError):
        num_digits_faster([1, 2])
