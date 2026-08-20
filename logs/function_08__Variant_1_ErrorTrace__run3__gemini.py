import pytest
from function_08 import num_digits, num_digits_fast, num_digits_faster


def test_num_digits_zero():
    assert num_digits(0) == 1
    assert num_digits_fast(0) == 1
    assert num_digits_faster(0) == 1


def test_num_digits_positive():
    assert num_digits(5) == 1
    assert num_digits(10) == 2
    assert num_digits(99) == 2
    assert num_digits(100) == 3
    assert num_digits_fast(5) == 1
    assert num_digits_fast(10) == 2
    assert num_digits_fast(99) == 2
    assert num_digits_fast(100) == 3
    assert num_digits_faster(5) == 1
    assert num_digits_faster(10) == 2
    assert num_digits_faster(99) == 2
    assert num_digits_faster(100) == 3


def test_num_digits_negative():
    assert num_digits(-5) == 1
    assert num_digits(-10) == 2
    assert num_digits(-999) == 3
    assert num_digits_fast(-5) == 1
    assert num_digits_fast(-10) == 2
    assert num_digits_fast(-999) == 3
    assert num_digits_faster(-5) == 1
    assert num_digits_faster(-10) == 2
    assert num_digits_faster(-999) == 3


def test_num_digits_boundary_powers_of_ten():
    assert num_digits(9) == 1
    assert num_digits(10) == 2
    assert num_digits(99) == 2
    assert num_digits(100) == 3
    assert num_digits_fast(9) == 1
    assert num_digits_fast(10) == 2
    assert num_digits_fast(99) == 2
    assert num_digits_fast(100) == 3
    assert num_digits_faster(9) == 1
    assert num_digits_faster(10) == 2
    assert num_digits_faster(99) == 2
    assert num_digits_faster(100) == 3


def test_num_digits_type_error():
    with pytest.raises(TypeError) as exc_info:
        num_digits(10.5)
    assert str(exc_info.value) == 'Input must be an integer'

    with pytest.raises(TypeError) as exc_info:
        num_digits("100")
    assert str(exc_info.value) == 'Input must be an integer'

    with pytest.raises(TypeError) as exc_info:
        num_digits_fast(10.5)
    assert str(exc_info.value) == 'Input must be an integer'

    with pytest.raises(TypeError) as exc_info:
        num_digits_fast("100")
    assert str(exc_info.value) == 'Input must be an integer'

    with pytest.raises(TypeError) as exc_info:
        num_digits_faster(10.5)
    assert str(exc_info.value) == 'Input must be an integer'

    with pytest.raises(TypeError) as exc_info:
        num_digits_faster("100")
    assert str(exc_info.value) == 'Input must be an integer'