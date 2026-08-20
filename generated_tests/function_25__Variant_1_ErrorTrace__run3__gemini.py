import pytest
from function_25 import is_prime


def test_is_prime_invalid_types():
    with pytest.raises(ValueError):
        is_prime(-1)
    with pytest.raises(ValueError):
        is_prime(3.5)
    with pytest.raises(ValueError):
        is_prime('7')


def test_is_prime_edge_cases_0_1_2_3():
    assert is_prime(0) is False
    assert is_prime(1) is False
    assert is_prime(2) is True
    assert is_prime(3) is True


def test_is_prime_small_composites():
    assert is_prime(4) is False
    assert is_prime(6) is False
    assert is_prime(8) is False
    assert is_prime(9) is False


def test_is_prime_known_primes():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    for p in primes:
        assert is_prime(p) is True


def test_is_prime_larger_composites():
    composites = [25, 49, 77, 91, 121, 143]
    for c in composites:
        assert is_prime(c) is False


def test_is_prime_loop_step_coverage():
    assert is_prime(25) is False
    assert is_prime(35) is False
    assert is_prime(319) is False
    assert is_prime(323) is True
