import pytest
from function_25 import is_prime


def test_is_prime_invalid_types_and_negative():
    with pytest.raises(ValueError):
        is_prime(-1)
    with pytest.raises(ValueError):
        is_prime(-10)
    with pytest.raises(ValueError):
        is_prime(2.5)
    with pytest.raises(ValueError):
        is_prime("5")
    with pytest.raises(ValueError):
        is_prime(None)


def test_is_prime_small_numbers_boundary():
    assert is_prime(0) is False
    assert is_prime(1) is False
    assert is_prime(2) is True
    assert is_prime(3) is True


def test_is_prime_small_composites_and_evens():
    assert is_prime(4) is False
    assert is_prime(6) is False
    assert is_prime(8) is False
    assert is_prime(9) is False
    assert is_prime(12) is False
    assert is_prime(15) is False


def test_is_prime_nominal_primes():
    assert is_prime(5) is True
    assert is_prime(7) is True
    assert is_prime(11) is True
    assert is_prime(13) is True
    assert is_prime(17) is True
    assert is_prime(19) is True
    assert is_prime(23) is True
    assert is_prime(29) is True
    assert is_prime(97) is True


def test_is_prime_larger_composites():
    assert is_prime(25) is False
    assert is_prime(49) is False
    assert is_prime(91) is False
    assert is_prime(100) is False
    assert is_prime(121) is False


def test_is_prime_loop_step_coverage():
    # Test numbers that require stepping through the 6k+/-1 loop
    assert is_prime(35) is False
    assert is_prime(77) is False
    assert is_prime(101) is True
    assert is_prime(103) is True
    assert is_prime(105) is False
