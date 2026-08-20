import pytest
from function_28 import sin


def test_sin_zero():
    assert sin(0.0) == 0.0


def test_sin_standard_angles():
    assert sin(30.0) == 0.5
    assert sin(90.0) == 1.0
    assert sin(180.0) == 0.0
    assert sin(270.0) == -1.0


def test_sin_angle_normalization():
    assert sin(390.0) == sin(30.0)
    assert sin(-330.0) == sin(30.0)
    assert sin(720.0) == sin(0.0)


def test_sin_custom_accuracy_and_rounding():
    res_low = sin(30.0, accuracy=1, rounded_values_count=2)
    res_high = sin(30.0, accuracy=10, rounded_values_count=5)
    assert isinstance(res_low, float)
    assert isinstance(res_high, float)
    assert sin(30.0, accuracy=18, rounded_values_count=4) == 0.5


def test_sin_default_parameters_inspection():
    import inspect
    sig = inspect.signature(sin)
    assert sig.parameters['accuracy'].default == 18
    assert sig.parameters['rounded_values_count'].default == 10


def test_sin_normalization_boundary_360():
    # Tests value right around 360 to ensure 360.0 vs 361.0 in modulo/normalization matters
    assert sin(360.0) == sin(0.0)
    assert sin(361.0) == sin(1.0)