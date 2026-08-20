import pytest
from function_26 import prime_factors
from function_26 import unique_prime_factors


def test_prime_factors_nominal_composite():
    assert prime_factors(60) == [2, 2, 3, 5]


def test_prime_factors_prime():
    assert prime_factors(13) == [13]


def test_prime_factors_power():
    assert prime_factors(8) == [2, 2, 2]


def test_prime_factors_one():
    assert prime_factors(1) == []


def test_prime_factors_division_type():
    res = prime_factors(4)
    assert res == [2, 2]
    assert isinstance(res[0], int)
    # Check that integer division was used rather than float division (which leaves floats or triggers floats in division)
    for factor in res:
        assert type(factor) is int


def test_unique_prime_factors_nominal_composite():
    assert unique_prime_factors(60) == [2, 3, 5]


def test_unique_prime_factors_prime():
    assert unique_prime_factors(13) == [13]


def test_unique_prime_factors_power():
    assert unique_prime_factors(8) == [2]


def test_unique_prime_factors_one():
    assert unique_prime_factors(1) == []


def test_unique_prime_factors_boundary_square():
    # Tests i * i <= n boundary for unique_prime_factors when n is a square (e.g., 9 = 3*3)
    assert unique_prime_factors(9) == [3]


def test_unique_prime_factors_division_type():
    res = unique_prime_factors(4)
    assert res == [2]
    assert isinstance(res[0], int)
    for factor in res:
        assert type(factor) is int


def test_unique_prime_factors_n_greater_than_one():
    # Tests n > 1 vs n > 2 leftover prime check (e.g., n = 2 after stripping factors of something, or just a prime like 2)
    assert unique_prime_factors(2) == [2]


def test_unique_prime_factors_integer_division_mutant():
    res = unique_prime_factors(8)
    assert res == [2]
    for factor in res:
        assert type(factor) is int