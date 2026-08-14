import pytest
from function_25 import is_prime


def test_is_prime_invalid_inputs():
    with pytest.raises(ValueError):
        is_prime(-1)
    with pytest.raises(ValueError):
        is_prime(-100)
    with pytest.raises(ValueError):
        is_prime(2.5)
    with pytest.raises(ValueError):
        is_prime("5")


def test_is_prime_boundary_values():
    assert is_prime(0) is False
    assert is_prime(1) is False
    assert is_prime(2) is True
    assert is_prime(3) is True


def test_is_prime_small_composites_and_evens():
    assert is_prime(4) is False
    assert is_prime(6) is False
    assert is_prime(8) is False
    assert is_prime(9) is False
    assert is_prime(25) is False


def test_is_prime_larger_primes():
    assert is_prime(31) is True
    assert is_prime(97) is True
    assert is_prime(101) is True
    assert is_prime(7919) is True


def test_is_prime_larger_composites():
    assert is_prime(121) is False
    assert is_prime(119) is False
    assert is_prime(1000) is False
    assert is_prime(7921) is False
