from function_26 import prime_factors, unique_prime_factors
import pytest


def test_prime_factors_nominal():
    assert prime_factors(2) == [2]
    assert prime_factors(4) == [2, 2]
    assert prime_factors(12) == [2, 2, 3]
    assert prime_factors(31) == [31]


def test_prime_factors_boundaries():
    assert prime_factors(1) == []
    assert prime_factors(0) == []
    assert prime_factors(100) == [2, 2, 5, 5]


def test_prime_factors_negative():
    assert prime_factors(-12) == [-12]


def test_unique_prime_factors_nominal():
    assert unique_prime_factors(2) == [2]
    assert unique_prime_factors(12) == [2, 3]
    assert unique_prime_factors(100) == [2, 5]
    assert unique_prime_factors(31) == [31]


def test_unique_prime_factors_boundaries():
    assert unique_prime_factors(1) == []
    assert unique_prime_factors(0) == []
    assert unique_prime_factors(27) == [3]


def test_unique_prime_factors_negative():
    assert unique_prime_factors(-12) == [-12]
