from function_26 import prime_factors
from function_26 import unique_prime_factors


def test_prime_factors_nominal():
    assert prime_factors(12) == [2, 2, 3]
    assert prime_factors(315) == [3, 3, 5, 7]


def test_prime_factors_prime():
    assert prime_factors(13) == [13]
    assert prime_factors(2) == [2]


def test_prime_factors_boundary():
    assert prime_factors(1) == []
    assert prime_factors(0) == []


def test_unique_prime_factors_nominal():
    assert unique_prime_factors(12) == [2, 3]
    assert unique_prime_factors(315) == [3, 5, 7]


def test_unique_prime_factors_prime():
    assert unique_prime_factors(13) == [13]
    assert unique_prime_factors(2) == [2]


def test_unique_prime_factors_boundary():
    assert unique_prime_factors(1) == []
    assert unique_prime_factors(0) == []


def test_prime_factors_conditional_boundary_and_division():
    # Mutant mutmut_5 changes <= to < at line 6, causing n=4 to miss i=2 loop when i*i==n; Mutant mutmut_11 uses float division n/=i producing floats instead of ints.
    assert prime_factors(4) == [2, 2]
    assert isinstance(prime_factors(4)[0], int)


def test_unique_prime_factors_conditional_boundary_and_division():
    # Mutant mutmut_5 changes <= to < at line 6 for unique_prime_factors, and mutmut_11 uses float division n/=i.
    assert unique_prime_factors(4) == [2]
    assert isinstance(unique_prime_factors(4)[0], int)


def test_prime_factors_integer_division_mutant_11():
    # Mutant mutmut_11 replaces floor division n //= i with float division n /= i, making elements in factors float instead of int.
    # State divergence: factors list contains floats (e.g. 2.0) instead of ints (2).
    factors = prime_factors(4)
    assert all(type(f) is int for f in factors)


def test_unique_prime_factors_integer_division_mutant_11():
    # Mutant mutmut_11 replaces floor division n //= i with float division n /= i, making elements in unique factors float instead of int.
    # State divergence: factors list contains floats (e.g. 2.0) instead of ints (2).
    factors = unique_prime_factors(4)
    assert all(type(f) is int for f in factors)


def test_unique_prime_factors_mutmut_11_division():
    # Mutant mutmut_11 replaces n //= i with n /= i at line 30, causing factors appended in unique_prime_factors to be floats.
    # State divergence: unique_prime_factors(12) appends float i instead of int i, so elements have type float.
    assert all(type(x) is int for x in unique_prime_factors(12))