import pytest
from function_08 import num_digits, num_digits_fast, num_digits_faster


def test_num_digits_nominal():
    assert num_digits(0) == 1
    assert num_digits(5) == 1
    assert num_digits(9) == 1
    assert num_digits(10) == 2
    assert num_digits(99) == 2
    assert num_digits(100) == 3
    assert num_digits(123456789) == 9


def test_num_digits_negative():
    assert num_digits(-5) == 1
    assert num_digits(-10) == 2
    assert num_digits(-999) == 3


def test_num_digits_type_error():
    # Mutants 2, 3, 4, 5 change the exact exception message string; assert it matches 'Input must be an integer' precisely.
    with pytest.raises(TypeError) as excinfo:
        num_digits(10.5)
    assert str(excinfo.value) == 'Input must be an integer'
    with pytest.raises(TypeError):
        num_digits("100")
    with pytest.raises(TypeError):
        num_digits(None)


def test_num_digits_fast_nominal():
    assert num_digits_fast(0) == 1
    assert num_digits_fast(5) == 1
    assert num_digits_fast(9) == 1
    assert num_digits_fast(10) == 2
    assert num_digits_fast(99) == 2
    assert num_digits_fast(100) == 3
    assert num_digits_fast(123456789) == 9


def test_num_digits_fast_negative():
    assert num_digits_fast(-5) == 1
    assert num_digits_fast(-10) == 2
    assert num_digits_fast(-999) == 3


def test_num_digits_fast_type_error():
    # Fast mutants 2, 3, 4, 5 change the exact exception message string; assert it matches 'Input must be an integer' precisely.
    with pytest.raises(TypeError) as excinfo:
        num_digits_fast(10.5)
    assert str(excinfo.value) == 'Input must be an integer'
    with pytest.raises(TypeError):
        num_digits_fast("100")
    with pytest.raises(TypeError):
        num_digits_fast(None)


def test_num_digits_faster_nominal():
    assert num_digits_faster(0) == 1
    assert num_digits_faster(5) == 1
    assert num_digits_faster(9) == 1
    assert num_digits_faster(10) == 2
    assert num_digits_faster(99) == 2
    assert num_digits_faster(100) == 3
    assert num_digits_faster(123456789) == 9


def test_num_digits_faster_negative():
    assert num_digits_faster(-5) == 1
    assert num_digits_faster(-10) == 2
    assert num_digits_faster(-999) == 3


def test_num_digits_faster_type_error():
    # Mutants 2, 3, 4, 5 mutate the TypeError message string in num_digits_faster; assert exact exception message string.
    with pytest.raises(TypeError) as excinfo:
        num_digits_faster(10.5)
    assert str(excinfo.value) == 'Input must be an integer'
    with pytest.raises(TypeError) as excinfo:
        num_digits_faster("100")
    assert str(excinfo.value) == 'Input must be an integer'
    with pytest.raises(TypeError) as excinfo:
        num_digits_faster(None)
    assert str(excinfo.value) == 'Input must be an integer'