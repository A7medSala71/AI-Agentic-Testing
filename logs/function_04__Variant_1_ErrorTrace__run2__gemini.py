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


def test_mean_mixed_numbers():
    assert mean([-2, 0, 2]) == pytest.approx(0.0)


def test_mean_empty_list_error():
    with pytest.raises(ValueError) as exc_info:
        mean([])
    assert str(exc_info.value) == 'List is empty'