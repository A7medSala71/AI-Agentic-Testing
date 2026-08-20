import pytest
from function_07 import decimal_to_fraction


def test_decimal_to_fraction_integer_float():
    assert decimal_to_fraction(5.0) == (5, 1)
    assert decimal_to_fraction(-3.0) == (-3, 1)


def test_decimal_to_fraction_integer_string():
    assert decimal_to_fraction("7") == (7, 1)
    assert decimal_to_fraction("0") == (0, 1)


def test_decimal_to_fraction_simple_decimals():
    assert decimal_to_fraction(0.5) == (1, 2)
    assert decimal_to_fraction(0.25) == (1, 4)
    assert decimal_to_fraction("0.75") == (3, 4)


def test_decimal_to_fraction_negative_decimals():
    assert decimal_to_fraction(-0.5) == (-1, 2)
    assert decimal_to_fraction("-0.125") == (-1, 8)


def test_decimal_to_fraction_invalid_input():
    # Mutant 4: Expects exact error message 'Please enter a valid number'
    with pytest.raises(ValueError, match="^Please enter a valid number$"):
        decimal_to_fraction("not_a_number")


def test_decimal_to_fraction_fractional_part_arithmetic_and_branch():
    # Mutants 7, 8, 11: fractional_part subtraction, replacement by None, or + instead of -, and equality check against 0 vs 1
    # For decimal 1.5, decimal - int(decimal) is 0.5; if mutated to None it fails on comparison, if + it gives 2.0 != 0, if == 1 it incorrectly treats 1.5 as integer branch returning (1.5, 1) or crashing.
    assert decimal_to_fraction(1.5) == (3, 2)


def test_decimal_to_fraction_integer_division_float_mutants():
    # Mutants 32, 33: division operator changed from // to / on numerator or denominator, which would result in float values like (0.5, 1) instead of int tuple (1, 2)
    res = decimal_to_fraction(0.5)
    assert res == (1, 2)
    assert isinstance(res[0], int)
    assert isinstance(res[1], int)


def test_decimal_to_fraction_fractional_part_none_or_plus_or_one():
    # Mutants 7, 8, 11: For decimal 1.5, fractional_part becomes None (TypeError on == 0), 2.0 (takes else branch wrongly instead of integer if integer was tested, or 1.5 causes incorrect branch), or == 1 compares 0.5 == 1 incorrectly. Testing 1.0 ensures fractional_part=0 vs mutated 1, while non-zero fractional parts catch None/plus.
    # Mutant 7: fractional_part = None causes TypeError on `fractional_part == 0`.
    # Mutant 8: fractional_part = decimal + int(decimal) causes 1.5 + 1 = 2.5 != 0, forcing non-integer path for 1.0 if tested, or altering behavior.
    # Mutant 11: if fractional_part == 1 makes `decimal_to_fraction(1.0)` take the else branch instead of `(1, 1)`.
    assert decimal_to_fraction(1.0) == (1, 1)
    assert decimal_to_fraction(2.5) == (5, 2)