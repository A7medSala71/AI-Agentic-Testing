import pytest
from function_07 import decimal_to_fraction


def test_decimal_to_fraction_integer_float():
    assert decimal_to_fraction(5.0) == (5, 1)
    assert decimal_to_fraction(0.0) == (0, 1)
    assert decimal_to_fraction(-3.0) == (-3, 1)


def test_decimal_to_fraction_integer_string():
    assert decimal_to_fraction("5") == (5, 1)
    assert decimal_to_fraction("0") == (0, 1)
    assert decimal_to_fraction("-4.0") == (-4, 1)


def test_decimal_to_fraction_simple_decimals():
    assert decimal_to_fraction(0.5) == (1, 2)
    assert decimal_to_fraction("0.25") == (1, 4)
    assert decimal_to_fraction(0.75) == (3, 4)
    assert decimal_to_fraction(1.25) == (5, 4)


def test_decimal_to_fraction_negative_decimals():
    assert decimal_to_fraction(-0.5) == (-1, 2)


def test_decimal_to_fraction_invalid_input():
    with pytest.raises(ValueError, match="^Please enter a valid number$"):
        decimal_to_fraction("not_a_number")
    with pytest.raises(ValueError, match="^Please enter a valid number$"):
        decimal_to_fraction("1.2.3")


def test_decimal_to_fraction_fractional_part_edge_cases():
    # Kills mutmut_7 and mutmut_8 (fractional_part = None or decimal + int(decimal))
    # For decimal = 1.0, int(1.0) = 1.
    # decimal - int(decimal) = 0.0 (triggers if fractional_part == 0 -> returns (1, 1)).
    # If fractional_part is None, fractional_part == 0 is False, goes to else and raises TypeError or fails.
    # If fractional_part is decimal + int(decimal) = 2.0, fractional_part == 0 is False, goes to else and returns (2, 1) instead of (1, 1).
    assert decimal_to_fraction(1.0) == (1, 1)
    assert decimal_to_fraction(2.0) == (2, 1)


def test_decimal_to_fraction_mutmut_11():
    # Kills mutmut_11 (if fractional_part == 1:)
    # For a decimal like 1.5, fractional_part is 0.5.
    # If the check is mutated to `fractional_part == 1`, then 0.5 == 1 is False, 
    # causing 1.5 to enter the else block instead of falling through or behaving correctly,
    # or more specifically, for 1.0 (fractional_part = 0), `0 == 1` is False, so 1.0 enters 
    # the else branch trying to do len(str(decimal).split('.')[1]) etc.
    assert decimal_to_fraction(1.5) == (3, 2)


def test_decimal_to_fraction_division_types():
    # Kills mutmut_32 and mutmut_33 (float division `/` instead of integer division `//`)
    res = decimal_to_fraction(2.5)
    assert res == (5, 2)
    assert isinstance(res[0], int)
    assert isinstance(res[1], int)
    
    res2 = decimal_to_fraction("0.4")
    assert res2 == (2, 5)
    assert isinstance(res2[0], int)
    assert isinstance(res2[1], int)