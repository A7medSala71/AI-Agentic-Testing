pytest
from function_08 import num_digits, num_digits_fast, num_digits_faster


def test_num_digits_nominal():
    assert num_digits(0) == 1
    assert num_digits(5) == 1
    assert num_digits(10) == 2
    assert num_digits(99) == 2
    assert num_digits(100) == 3
    assert num_digits(999999) == 6


def test_num_digits_negative():
    assert num_digits(-5) == 1
    assert num_digits(-10) == 2
    assert num_digits(-999) == 3


def test_num_digits_type_error():
    with pytest.raises(TypeError):
        num_digits(3.14)
    with pytest.raises(TypeError):
        num_digits("123")
    with pytest.raises(TypeError):
        num_digits(None)


def test_num_digits_fast_nominal():
    assert num_digits_fast(0) == 1
    assert num_digits_fast(7) == 1
    assert num_digits_fast(10) == 2
    assert num_digits_fast(99) == 2
    assert num_digits_fast(100) == 3
    assert num_digits_fast(123456789) == 9


def test_num_digits_fast_negative():
    assert num_digits_fast(-7) == 1
    assert num_digits_fast(-10) == 2
    assert num_digits_fast(-12345) == 5


def test_num_digits_fast_type_error():
    with pytest.raises(TypeError):
        num_digits_fast(3.14)
    with pytest.raises(TypeError):
        num_digits_fast("100")
    with pytest.raises(TypeError):
        num_digits_fast(None)


def test_num_digits_faster_nominal():
    assert num_digits_faster(0) == 1
    assert num_digits_faster(3) == 1
    assert num_digits_faster(10) == 2
    assert num_digits_faster(555) == 3
    assert num_digits_faster(999999999) == 9


def test_num_digits_faster_negative():
    assert num_digits_faster(-3) == 1
    assert num_digits_faster(-10) == 2
    assert num_digits_faster(-555) == 3


def test_num_digits_faster_type_error():
    with pytest.raises(TypeError):
        num_digits_faster(2.718)
    with pytest.raises(TypeError):
        num_digits_faster("abc")
    with pytest.raises(TypeError):
        num_digits_faster(None)
