import pytest
from function_25 import is_prime


def test_is_prime_negative_number():
    with pytest.raises(ValueError) as excinfo:
        is_prime(-1)
    assert str(excinfo.value) == 'is_prime() only accepts positive integers'


def test_is_prime_non_integer():
    with pytest.raises(ValueError) as excinfo:
        is_prime(2.5)
    assert str(excinfo.value) == 'is_prime() only accepts positive integers'


def test_is_prime_zero():
    assert is_prime(0) is False


def test_is_prime_one():
    assert is_prime(1) is False


def test_is_prime_small_primes():
    assert is_prime(2) is True
    assert is_prime(3) is True


def test_is_prime_even_numbers():
    assert is_prime(4) is False
    assert is_prime(6) is False
    assert is_prime(100) is False


def test_is_prime_multiples_of_three():
    assert is_prime(9) is False
    assert is_prime(15) is False
    assert is_prime(21) is False


def test_is_prime_composite_numbers():
    assert is_prime(25) is False
    assert is_prime(35) is False
    assert is_prime(49) is False


def test_is_prime_large_primes():
    assert is_prime(31) is True
    assert is_prime(97) is True
    assert is_prime(101) is True


def test_is_prime_larger_composite():
    # Kills range/sqrt/step mutants like range(5, 6) or range(..., +2) or missing step
    assert is_prime(121) is False  # 11 * 11
    assert is_prime(143) is False  # 11 * 13
    assert is_prime(169) is False  # 13 * 13


def test_is_prime_mutant_killers():
    # Kills mutants on `number < 2` (e.g. number <= 2 or number < 3)
    # 2 is a prime, so is_prime(2) must return True. If `number <= 2` or `number < 3`, 
    # then 2 would hit the elif branch and return False.
    assert is_prime(2) is True