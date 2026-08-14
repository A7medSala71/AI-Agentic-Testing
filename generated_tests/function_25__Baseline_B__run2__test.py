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
    with pytest.raises(ValueError):
        is_prime(None)


def test_is_prime_boundary_values():
    assert is_prime(0) is False
    assert is_prime(1) is False
    assert is_prime(2) is True
    assert is_prime(3) is True


def test_is_prime_small_composites():
    assert is_prime(4) is False
    assert is_prime(6) is False
    assert is_prime(8) is False
    assert is_prime(9) is False
    assert is_prime(15) is False


def test_is_prime_known_primes():
    primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    for p in primes:
        assert is_prime(p) is True


def test_is_prime_large_composites_and_primes():
    assert is_prime(101) is True
    assert is_prime(105) is False
    assert is_prime(107) is True
    assert is_prime(109) is True
    assert is_prime(121) is False
    assert is_prime(997) is True
    assert is_prime(1000) is False
    assert is_prime(104729) is True
    assert is_prime(104730) is False
