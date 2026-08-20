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
    # Mutant num_digits mutates the exact TypeError message string; verify the exact message matches 'Input must be an integer'.
    with pytest.raises(TypeError) as excinfo:
        num_digits(1.5)
    assert str(excinfo.value) == 'Input must be an integer'


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
    # Mutant num_digits_fast mutates the exact TypeError message string; verify the exact message matches 'Input must be an integer'.
    with pytest.raises(TypeError) as excinfo:
        num_digits_fast(1.5)
    assert str(excinfo.value) == 'Input must be an integer'


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
    # Mutants num_digits_faster mutates TypeError message to None, XX..., lowercase, or uppercase; assert exact message.
    with pytest.raises(TypeError) as excinfo:
        num_digits_faster(1.5)
    assert str(excinfo.value) == 'Input must be an integer'
    with pytest.raises(TypeError):
        num_digits_faster("10")
    with pytest.raises(TypeError):
        num_digits_faster(None)