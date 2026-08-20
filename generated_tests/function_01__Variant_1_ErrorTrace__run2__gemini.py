import pytest
from function_01 import slow_primes, primes, fast_primes


def test_slow_primes_nominal():
    assert list(slow_primes(10)) == [2, 3, 5, 7]


def test_slow_primes_boundaries():
    assert list(slow_primes(1)) == []
    assert list(slow_primes(2)) == [2]
    assert list(slow_primes(0)) == []


def test_primes_nominal():
    assert list(primes(20)) == [2, 3, 5, 7, 11, 13, 17, 19]


def test_primes_boundaries():
    assert list(primes(1)) == []
    assert list(primes(2)) == [2]
    assert list(primes(3)) == [2, 3]


def test_fast_primes_nominal():
    result = sorted(list(fast_primes(20)))
    assert result == [2, 3, 5, 7, 11, 13, 17, 19]


def test_fast_primes_boundaries():
    assert list(fast_primes(1)) == []
    assert list(fast_primes(2)) == []
    assert list(fast_primes(3)) == [2, 3]


def test_fast_primes_specific_mutants():
    # Kills fast_primes__mutmut_16 (n > 2 instead of n > 1) by checking numbers including 2 via step
    # Kills fast_primes__mutmut_21 (+ 2 instead of + 1 on sqrt bound)
    # Kills fast_primes__mutmut_27 and __mutmut_29 (step in range(3, bound, 2))
    assert list(fast_primes(9)) == [2, 3, 5, 7]
    assert list(fast_primes(25)) == [2, 3, 5, 7, 11, 13, 17, 19, 23]