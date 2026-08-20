import pytest
from function_26 import prime_factors
from function_26 import unique_prime_factors


def test_prime_factors_nominal():
    assert prime_factors(12) == [2, 2, 3]
    assert prime_factors(315) == [3, 3, 5, 7]


def test_prime_factors_prime():
    assert prime_factors(13) == [13]
    assert prime_factors(2) == [2]


def test_prime_factors_boundaries():
    assert prime_factors(1) == []
    assert prime_factors(0) == []
    # Kills <= vs < for prime_factors (e.g. 4 = 2*2, i*i == n)
    assert prime_factors(4) == [2, 2]
    assert prime_factors(9) == [3, 3]
    # Kills //= vs /= (division type / return type)
    res = prime_factors(4)
    assert isinstance(res[0], int)
    assert res == [2, 2]


def test_unique_prime_factors_nominal():
    assert unique_prime_factors(12) == [2, 3]
    assert unique_prime_factors(315) == [3, 5, 7]


def test_unique_prime_factors_prime():
    assert unique_prime_factors(13) == [13]
    assert unique_prime_factors(2) == [2]


def test_unique_prime_factors_boundaries():
    assert unique_prime_factors(1) == []
    assert unique_prime_factors(0) == []
    # Kills <= vs < for unique_prime_factors
    assert unique_prime_factors(4) == [2]
    assert unique_prime_factors(9) == [3]
    # Kills //= vs /= (division type / return type)
    res = unique_prime_factors(4)
    assert isinstance(res[0], int)
    assert res == [2]