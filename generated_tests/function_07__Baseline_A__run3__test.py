import pytest
from function_07 import decimal_to_fraction


def test_decimal_to_fraction_integer_float():
    assert decimal_to_fraction(5.0) == (5, 1)
    assert decimal_to_fraction(-3.0) == (-3, 1)


def test_decimal_to_fraction_integer_string():
    assert decimal_to_fraction("4") == (4, 1)
    assert decimal_to_fraction("0.0") == (0, 1)


def test_decimal_to_fraction_simple_decimal():
    assert decimal_to_fraction(0.5) == (1, 2)
    assert decimal_to_fraction(0.25) == (1, 4)
    assert decimal_to_fraction("0.75") == (3, 4)


def test_decimal_to_fraction_complex():
    assert decimal_to_fraction(0.1) == (1, 10)
    assert decimal_to_fraction(1.125) == (9, 8)


def test_decimal_to_fraction_negative_decimals():
    assert decimal_to_fraction(-0.5) == (-1, 2)
    assert decimal_to_fraction("-0.75") == (-3, 4)


def test_decimal_to_fraction_invalid_input():
    with pytest.raises(ValueError, match='Please enter a valid number'):
        decimal_to_fraction('not_a_number')
    with pytest.raises(ValueError):
        decimal_to_fraction(None)
