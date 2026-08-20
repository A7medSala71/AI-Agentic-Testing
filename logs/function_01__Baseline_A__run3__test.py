from function_01 import slow_primes, primes, fast_primes


def test_slow_primes_nominal():
    assert list(slow_primes(10)) == [2, 3, 5, 7]


def test_slow_primes_edge_cases():
    assert list(slow_primes(1)) == []
    assert list(slow_primes(2)) == [2]


def test_primes_nominal():
    assert list(primes(20)) == [2, 3, 5, 7, 11, 13, 17, 19]


def test_primes_edge_cases():
    assert list(primes(0)) == []
    assert list(primes(2)) == [2]


def test_fast_primes_nominal():
    res = sorted(list(fast_primes(20)))
    assert res == [2, 3, 5, 7, 11, 13, 17, 19]


def test_fast_primes_edge_cases():
    assert list(fast_primes(1)) == []
    assert list(fast_primes(2)) == [2]
    assert sorted(list(fast_primes(3))) == [2, 3]
