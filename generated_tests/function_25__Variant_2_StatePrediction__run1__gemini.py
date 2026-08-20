import pytest
from function_25 import is_prime


def test_is_prime_invalid_inputs():
    # Mutant mutmut_6/7/8: Checks exact exception message string value when ValueError is raised
    with pytest.raises(ValueError, match='is_prime\(\) only accepts positive integers'):
        is_prime(-1)


def test_is_prime_boundaries_small():
    assert is_prime(0) is False
    assert is_prime(1) is False
    assert is_prime(2) is True
    # Mutant mutmut_16/17: Number 2 is tested above (returns True), test 2 vs 2 boundary or 3
    assert is_prime(3) is True


def test_is_prime_even_numbers():
    assert is_prime(4) is False
    assert is_prime(6) is False
    assert is_prime(8) is False
    assert is_prime(100) is False


def test_is_prime_divisible_by_three():
    assert is_prime(9) is False
    assert is_prime(15) is False
    assert is_prime(21) is False


def test_is_prime_nominal_primes():
    assert is_prime(5) is True
    assert is_prime(7) is True
    assert is_prime(11) is True
    assert is_prime(13) is True
    assert is_prime(17) is True
    assert is_prime(19) is True
    assert is_prime(23) is True
    assert is_prime(97) is True


def test_is_prime_larger_composites_and_primes():
    # Mutant mutmut_32/37: Test a composite number requiring the step-6 loop with sqrt boundary (e.g., 25, 121)
    assert is_prime(25) is False
    assert is_prime(121) is False
    assert is_prime(119) is False
    assert is_prime(101) is True
    assert is_prime(103) is True
    # Test larger numbers to fully exercise loop step and upper bound mutants
    assert is_prime(143) is False
    assert is_prime(169) is False