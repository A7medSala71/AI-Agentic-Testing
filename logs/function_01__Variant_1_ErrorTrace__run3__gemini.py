import pytest
from function_01 import slow_primes, primes, fast_primes


def test_slow_primes_nominal():
    assert list(slow_primes(10)) == [2, 3, 5, 7]


def test_slow_primes_boundary_small():
    assert list(slow_primes(1)) == []
    assert list(slow_primes(2)) == [2]


def test_slow_primes_empty():
    assert list(slow_primes(0)) == []
    assert list(slow_primes(-5)) == []


def test_slow_primes_start_from_one():
    # Kills range(max_n+1) [starts at 0] and range(2, max_n+1) [starts at 2, missing 1]
    # Though 1 is filtered out anyway, testing that 1 is handled in the range/filtering logic
    assert list(slow_primes(1)) == []
    assert list(slow_primes(2)) == [2]


def test_primes_nominal():
    assert list(primes(20)) == [2, 3, 5, 7, 11, 13, 17, 19]


def test_primes_boundary_small():
    assert list(primes(1)) == []
    assert list(primes(2)) == [2]
    assert list(primes(3)) == [2, 3]


def test_primes_negative():
    assert list(primes(-10)) == []


def test_primes_start_from_one():
    # Kills range(max_n+1) and range(2, max_n+1) for primes as well
    assert list(primes(1)) == []


def test_fast_primes_nominal():
    res = sorted(list(fast_primes(20)))
    assert res == [2, 3, 5, 7, 11, 13, 17, 19]


def test_fast_primes_boundary_small():
    assert list(fast_primes(1)) == []
    assert list(fast_primes(2)) == []
    assert list(fast_primes(3)) == [2, 3]


def test_fast_primes_edge_large():
    assert list(fast_primes(9)) == [2, 3, 5, 7]


def test_fast_primes_negative():
    assert list(fast_primes(0)) == []
    assert list(fast_primes(-3)) == []


def test_fast_primes_n_equals_two():
    # Kills fast_primes mutant where `n > 2` becomes `n > 1` or similar, or tests n > 2 boundary.
    # If max_n = 2, fast_primes returns [] because max_n > 2 is False and numbers step=2 misses 2.
    assert list(fast_primes(2)) == []


def test_fast_primes_bound_and_step():
    # Kills bound + 2 (mutmut_21), step omission (mutmut_27), and step=3 (mutmut_29).
    # Specifically, numbers like 9 or 25 or 35 need correct square root bounds and step size 2.
    # For instance, 9 needs to be checked by j=3. If bound is different or step is 3 or missing, composites might slip through.
    assert list(fast_primes(9)) == [2, 3, 5, 7]
    assert list(fast_primes(25)) == [2, 3, 5, 7, 11, 13, 17, 19, 23]