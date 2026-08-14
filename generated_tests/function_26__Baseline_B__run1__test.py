import pytest
from function_26 import prime_factors
from function_26 import unique_prime_factors


def test_prime_factors_nominal():
    assert prime_factors(60) == [2, 2, 3, 5]
    assert prime_factors(13) == [13]
    assert prime_factors(1) == []


def test_prime_factors_powers():
    assert prime_factors(8) == [2, 2, 2]
    assert prime_factors(27) == [3, 3, 3]
    assert prime_factors(100) == [2, 2, 5, 5]


def test_unique_prime_factors_nominal():
    assert unique_prime_factors(60) == [2, 3, 5]
    assert unique_prime_factors(13) == [13]
    assert unique_prime_factors(1) == []


def test_unique_prime_factors_powers():
    assert unique_prime_factors(8) == [2]
    assert unique_prime_factors(27) == [3]
    assert unique_prime_factors(100) == [2, 5]


def test_prime_factors_edge_cases():
    assert prime_factors(0) == []
    assert prime_factors(-1) == []
    assert prime_factors(-60) == []


def test_unique_prime_factors_edge_cases():
    assert unique_prime_factors(0) == []
    assert unique_prime_factors(-1) == []
    assert unique_prime_factors(-60) == []
