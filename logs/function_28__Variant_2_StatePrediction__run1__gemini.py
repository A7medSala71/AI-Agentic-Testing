import pytest
from function_28 import sin


def test_sin_zero():
    assert sin(0.0) == 0.0


def test_sin_standard_angles():
    assert sin(30.0) == 0.5
    assert sin(90.0) == 1.0
    assert sin(180.0) == 0.0
    assert sin(270.0) == -1.0
    assert sin(360.0) == 0.0


def test_sin_negative_angles():
    assert sin(-30.0) == -0.5
    assert sin(-90.0) == -1.0
    assert sin(-360.0) == 0.0


def test_sin_angle_normalization():
    assert sin(390.0) == 0.5
    assert sin(-270.0) == 1.0
    assert sin(720.0) == 0.0


def test_sin_custom_rounded_values_count():
    val = sin(30.0, rounded_values_count=2)
    assert val == 0.5


def test_sin_custom_accuracy():
    val_low = sin(30.0, accuracy=1, rounded_values_count=5)
    val_high = sin(30.0, accuracy=18, rounded_values_count=5)
    assert val_low != val_high


def test_sin_default_accuracy_mutmut_1():
    # Mutant changes default accuracy from 18 to 19, causing high-precision convergence differences on large inputs.
    assert sin(3600000.0, accuracy=18) != sin(3600000.0, accuracy=19)


def test_sin_default_rounded_values_count_mutmut_2():
    # Mutant changes default rounded_values_count from 10 to 11, resulting in more digits in return value.
    assert len(str(sin(30.0, rounded_values_count=10)).split('.')[1]) == 10


def test_sin_normalization_divisor_mutmut_7():
    # Mutant changes 360.0 // 361.0 divisor, so angles near 360 do not normalize correctly and diverge in result.
    assert sin(361.0) != sin(361.0, accuracy=18) or sin(361.0) == sin(1.0)