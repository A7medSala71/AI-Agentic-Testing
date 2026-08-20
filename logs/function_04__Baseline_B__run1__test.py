import pytest
from function_04 import mean


def test_mean_nominal_integers():
    assert mean([1, 2, 3, 4, 5]) == pytest.approx(3.0)


def test_mean_nominal_floats():
    assert mean([1.5, 2.5, 3.5]) == pytest.approx(2.5)


def test_mean_single_element():
    assert mean([42]) == pytest.approx(42.0)


def test_mean_negative_numbers():
    assert mean([-1, -2, -3, -4, -5]) == pytest.approx(-3.0)


def test_mean_empty_list_raises_error():
    with pytest.raises(ValueError, match='List is empty'):
        mean([])


def test_mean_mixed_integers_and_floats():
    assert mean([1, 2.5, 3]) == pytest.approx(2.1666666666666665)


def test_mean_non_numeric_raises_type_error():
    with pytest.raises(TypeError):
        mean([1, 'a'])
