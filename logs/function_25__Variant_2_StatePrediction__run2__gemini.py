import pytest
import math
from function_25 import is_prime


def test_is_prime_invalid_inputs():
    # Mutants 6, 7, 8: mutate exception message to None, different string, or uppercase, so check exact exception message.
    with pytest.raises(ValueError, match='^is_prime\\(\\) only accepts positive integers$') as exc_info:
        is_prime(-1)
    assert str(exc_info.value) == 'is_prime() only accepts positive integers'

    with pytest.raises(ValueError):
        is_prime(-100)
    with pytest.raises(ValueError):
        is_prime(3.5)
    with pytest.raises(ValueError):
        is_prime('7')
    with pytest.raises(ValueError):
        is_prime(None)


def test_is_prime_boundary_values():
    assert is_prime(0) is False
    assert is_prime(1) is False
    assert is_prime(2) is True
    assert is_prime(3) is True


def test_is_prime_small_composites():
    # Mutant 16 (< changed to <=) and Mutant 17 (< changed to < 3): 2 becomes evaluated by elif number < 2 / < 3, changing return value for 2 from True to False.
    # Mutant 16: number <= 2 would make 2 return False instead of True.
    # Mutant 17: number < 3 would make 2 return False instead of True.
    assert is_prime(2) is True
    assert is_prime(4) is False
    assert is_prime(6) is False
    assert is_prime(8) is False
    assert is_prime(9) is False
    assert is_prime(10) is False


def test_is_prime_known_primes():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    for p in primes:
        assert is_prime(p) is True


def test_is_prime_larger_composites():
    # Mutant 32: range missing step 6 defaults to step 1, failing or changing behavior on larger numbers needing the step.
    # Mutant 37: range stop changed to + 2 instead of + 1, changing upper limit for sqrt check on numbers like 25 (5*5).
    composites = [25, 35, 49, 51, 55, 57, 63, 65, 69, 75, 77, 85, 87, 91, 93, 95, 99, 100, 119, 121, 143]
    for c in composites:
        assert is_prime(c) is False


def test_is_prime_loop_step_6():
    # 121 is 11 * 11, tests range loop and step 6 logic
    assert is_prime(121) is False
    # 119 is 7 * 17
    assert is_prime(119) is False
    # 127 is prime
    assert is_prime(127) is True


def test_is_prime_mutants_coverage():
    # Mutant 16 (number <= 2): forces number=2 to hit elif condition and return False instead of True via '1 < number < 4'
    assert is_prime(2) is True
    # Mutant 17 (number < 3): forces number=2 to hit elif condition and return False instead of True via '1 < number < 4'
    assert is_prime(2) is True
    # Mutant 32 (range missing step 6): tests that 25 uses step 6 correctly and returns False
    assert is_prime(25) is False
    # Mutant 37 (range stop + 2): tests that 25 (sqrt=5, int+1=6, mutated to +2=7) checks i=7 and incorrectly continues/passes
    assert is_prime(25) is False