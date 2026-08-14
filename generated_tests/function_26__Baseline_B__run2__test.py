from function_26 import prime_factors
from function_26 import unique_prime_factors


def test_prime_factors_nominal():
    assert prime_factors(12) == [2, 2, 3]
    assert prime_factors(315) == [3, 3, 5, 7]
    assert prime_factors(2) == [2]


def test_prime_factors_boundaries_and_small():
    assert prime_factors(1) == []
    assert prime_factors(0) == []
    assert prime_factors(13) == [13]


def test_unique_prime_factors_nominal():
    assert unique_prime_factors(12) == [2, 3]
    assert unique_prime_factors(315) == [3, 5, 7]
    assert unique_prime_factors(2) == [2]


def test_unique_prime_factors_boundaries():
    assert unique_prime_factors(1) == []
    assert unique_prime_factors(0) == []
    assert unique_prime_factors(13) == [13]


def test_prime_factors_negative():
    assert prime_factors(-12) == []
    assert unique_prime_factors(-12) == []
