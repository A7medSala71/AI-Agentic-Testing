import pytest
from function_08 import num_digits, num_digits_fast, num_digits_faster


def test_num_digits_nominal():
    assert num_digits(0) == 1
    assert num_digits(5) == 1
    assert num_digits(10) == 2
    assert num_digits(99) == 2
    assert num_digits(100) == 3
    assert num_digits(9999) == 4
    assert num_digits(10000) == 5


def test_num_digits_negative():
    assert num_digits(-5) == 1
    assert num_digits(-10) == 2
    assert num_digits(-999) == 3


def test_num_digits_type_error():
    with pytest.raises(TypeError) as exc_info:
        num_digits(1.5)
    assert str(exc_info.value) == 'Input must be an integer'

    with pytest.raises(TypeError) as exc_info:
        num_digits("100")
    assert str(exc_info.value) == 'Input must be an integer'

    with pytest.raises(TypeError) as exc_info:
        num_digits(None)
    assert str(exc_info.value) == 'Input must be an integer'


def test_num_digits_fast_nominal():
    assert num_digits_fast(0) == 1
    assert num_digits_fast(7) == 1
    assert num_digits_fast(10) == 2
    assert num_digits_fast(99) == 2
    assert num_digits_fast(100) == 3
    assert num_digits_fast(123456) == 6


def test_num_digits_fast_negative():
    assert num_digits_fast(-7) == 1
    assert num_digits_fast(-10) == 2
    assert num_digits_fast(-9999) == 4


def test_num_digits_fast_type_error():
    with pytest.raises(TypeError) as exc_info:
        num_digits_fast(1.5)
    assert str(exc_info.value) == 'Input must be an integer'

    with pytest.raises(TypeError) as exc_info:
        num_digits_fast("100")
    assert str(exc_info.value) == 'Input must be an integer'

    with pytest.raises(TypeError) as exc_info:
        num_digits_fast(None)
    assert str(exc_info.value) == 'Input must be an integer'


def test_num_digits_faster_nominal():
    assert num_digits_faster(0) == 1
    assert num_digits_faster(3) == 1
    assert num_digits_faster(10) == 2
    assert num_digits_faster(99) == 2
    assert num_digits_faster(100) == 3
    assert num_digits_faster(987654321) == 9


def test_num_digits_faster_negative():
    assert num_digits_faster(-3) == 1
    assert num_digits_faster(-10) == 2
    assert num_digits_faster(-98765) == 5


def test_num_digits_faster_type_error():
    with pytest.raises(TypeError) as exc_info:
        num_digits_faster(1.5)
    assert str(exc_info.value) == 'Input must be an integer'

    with pytest.raises(TypeError) as exc_info:
        num_digits_faster("100")
    assert str(exc_info.value) == 'Input must be an integer'

    with pytest.raises(TypeError) as exc_info:
        num_digits_faster(None)
    assert str(exc_info.value) == 'Input must be an integer'