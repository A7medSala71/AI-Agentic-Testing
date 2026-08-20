import pytest
from function_26 import prime_factors
from function_26 import unique_prime_factors


def test_prime_factors_nominal():
    assert prime_factors(60) == [2, 2, 3, 5]
    assert prime_factors(31) == [31]
    assert prime_factors(1) == []


def test_prime_factors_powers():
    assert prime_factors(8) == [2, 2, 2]
    assert prime_factors(9) == [3, 3]


def test_prime_factors_division_type():
    # Kills mutant that changes //= to /= in prime_factors, ensuring result elements are ints
    res = prime_factors(4)
    assert res == [2, 2]
    assert isinstance(res[0], int)
    assert isinstance(res[1], int)


def test_unique_prime_factors_nominal():
    assert unique_prime_factors(60) == [2, 3, 5]
    assert unique_prime_factors(31) == [31]
    assert unique_prime_factors(1) == []


def test_unique_prime_factors_powers():
    assert unique_prime_factors(8) == [2]
    assert unique_prime_factors(27) == [3]


def test_unique_prime_factors_conditional_boundary_and_n_gt_2():
    # Kills unique_prime_factors conditional boundary (i*i < n vs i*i <= n)
    # and n > 2 mutant (when remaining prime is 2, e.g., n = 2 after division, or n = 2 initially)
    assert unique_prime_factors(4) == [2]
    assert unique_prime_factors(2) == [2]
    assert unique_prime_factors(9) == [3]


def test_unique_prime_factors_division_type():
    # Kills mutant that changes //= to /= in unique_prime_factors
    res = unique_prime_factors(4)
    assert res == [2]
    assert isinstance(res[0], int)
    
    # Specifically targets `n //= i` in unique_prime_factors when float division `n /= i` 
    # would leave a float (e.g. 4.0) instead of an int (2), breaking subsequent loop logic or types.
    res2 = unique_prime_factors(12)
    assert res2 == [2, 3]
    assert isinstance(res2[0], int)
    assert isinstance(res2[1], int)