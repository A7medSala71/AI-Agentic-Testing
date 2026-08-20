import pytest
from function_26 import prime_factors, unique_prime_factors


def test_prime_factors_nominal():
    assert prime_factors(2) == [2]
    assert prime_factors(60) == [2, 2, 3, 5]
    assert prime_factors(31) == [31]


def test_prime_factors_boundaries():
    assert prime_factors(1) == []
    assert prime_factors(4) == [2, 2]


def test_prime_factors_large():
    assert prime_factors(1024) == [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    assert prime_factors(123456) == [2, 2, 2, 2, 2, 2, 3, 643]


def test_unique_prime_factors_nominal():
    assert unique_prime_factors(2) == [2]
    assert unique_prime_factors(60) == [2, 3, 5]
    assert unique_prime_factors(31) == [31]


def test_unique_prime_factors_boundaries():
    assert unique_prime_factors(1) == []
    assert unique_prime_factors(4) == [2]


def test_unique_prime_factors_large():
    assert unique_prime_factors(1024) == [2]
    assert unique_prime_factors(123456) == [2, 3, 643]
