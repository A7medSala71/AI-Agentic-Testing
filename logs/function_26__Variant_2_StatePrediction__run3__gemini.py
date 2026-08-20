from function_26 import prime_factors
from function_26 import unique_prime_factors


def test_prime_factors_nominal():
    assert prime_factors(12) == [2, 2, 3]
    assert prime_factors(315) == [3, 3, 5, 7]
    assert prime_factors(2) == [2]
    assert prime_factors(1) == []


def test_prime_factors_boundaries():
    assert prime_factors(4) == [2, 2]
    assert prime_factors(9) == [3, 3]
    assert prime_factors(13) == [13]


def test_unique_prime_factors_nominal():
    assert unique_prime_factors(12) == [2, 3]
    assert unique_prime_factors(315) == [3, 5, 7]
    assert unique_prime_factors(2) == [2]
    assert unique_prime_factors(1) == []


def test_unique_prime_factors_boundaries():
    assert unique_prime_factors(4) == [2]
    assert unique_prime_factors(9) == [3]
    assert unique_prime_factors(16) == [2]
    assert unique_prime_factors(17) == [17]


def test_prime_factors_division_type_divergence():
    # Mutant replaces integer division n //= i with float division n /= i, making n a float which causes subsequent loop comparisons to behave as floats or produce float factors.
    factors = prime_factors(12)
    assert all(isinstance(f, int) for f in factors)
    assert type(factors[0]) is int


def test_unique_prime_factors_division_type_divergence():
    # Mutant replaces integer division n //= i with float division n /= i, making n a float which alters the internal state type.
    factors = unique_prime_factors(12)
    assert all(isinstance(f, int) for f in factors)
    assert type(factors[0]) is int