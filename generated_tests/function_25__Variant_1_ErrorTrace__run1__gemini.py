import pytest
from function_25 import is_prime


def test_is_prime_invalid_inputs():
    with pytest.raises(ValueError) as exc_info:
        is_prime(-1)
    assert str(exc_info.value) == 'is_prime() only accepts positive integers'

    with pytest.raises(ValueError):
        is_prime(-100)
    with pytest.raises(ValueError):
        is_prime(3.5)
    with pytest.raises(ValueError):
        is_prime("7")
    with pytest.raises(ValueError):
        is_prime(None)


def test_is_prime_boundary_low():
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


def test_is_prime_medium_primes():
    assert is_prime(5) is True
    assert is_prime(7) is True
    assert is_prime(11) is True
    assert is_prime(13) is True
    assert is_prime(17) is True
    assert is_prime(19) is True
    assert is_prime(23) is True
    assert is_prime(29) is True
    assert is_prime(31) is True


def test_is_prime_larger_numbers():
    assert is_prime(25) is False
    assert is_prime(97) is True
    assert is_prime(100) is False
    assert is_prime(101) is True
    assert is_prime(105) is False
    assert is_prime(1009) is True
    assert is_prime(1010) is False


def test_is_prime_complex_composites():
    # Targets numbers that fall into the loop range (>= 25)
    # 121 = 11 * 11 (tested via 6k +/- 1 logic, e.g. 11 is 6(2)-1)
    assert is_prime(121) is False
    # 143 = 11 * 13
    assert is_prime(143) is False
    # 187 = 11 * 17
    assert is_prime(187) is False
    # 253 = 11 * 23
    assert is_prime(253) is False
    # 323 = 17 * 19
    assert is_prime(323) is False