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


def test_sin_large_angles():
    assert sin(390.0) == 0.5
    assert sin(-330.0) == 0.5


def test_sin_custom_rounding():
    val = sin(30.0, rounded_values_count=2)
    assert val == 0.5


def test_sin_custom_accuracy():
    val_low = sin(30.0, accuracy=1, rounded_values_count=10)
    val_high = sin(30.0, accuracy=20, rounded_values_count=10)
    assert val_low != val_high
    assert val_high == 0.5


def test_default_parameters():
    import inspect
    sig = inspect.signature(sin)
    assert sig.parameters['accuracy'].default == 18
    assert sig.parameters['rounded_values_count'].default == 10


def test_angle_normalization_boundary():
    assert sin(361.0) == sin(1.0)
    assert sin(360.0) == 0.0