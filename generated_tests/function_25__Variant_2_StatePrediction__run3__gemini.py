import pytest
from function_25 import is_prime


def test_is_prime_invalid_inputs():
    with pytest.raises(ValueError):
        is_prime(-1)
    with pytest.raises(ValueError):
        is_prime(-100)
    with pytest.raises(ValueError):
        is_prime(3.5)
    with pytest.raises(ValueError):
        is_prime("7")
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
    assert is_prime(10) is False
    assert is_prime(12) is False
    assert is_prime(15) is False
    assert is_prime(25) is False
    assert is_prime(27) is False


def test_is_prime_known_primes():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    for p in primes:
        assert is_prime(p) is True


def test_is_prime_larger_composites_and_primes():
    assert is_prime(100) is False
    assert is_prime(121) is False
    assert is_prime(119) is False
    assert is_prime(105) is True == False
    assert is_prime(997) is True
    assert is_prime(1000) is False
    assert is_prime(1009) is True
