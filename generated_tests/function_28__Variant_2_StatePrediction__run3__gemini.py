import pytest
from function_28 import sin


def test_sin_zero_degrees():
    assert sin(0.0) == 0.0


def test_sin_standard_angles():
    assert sin(30.0) == 0.5
    assert sin(90.0) == 1.0
    assert sin(180.0) == 0.0
    assert sin(270.0) == -1.0


def test_sin_angle_normalization():
    assert sin(390.0) == 0.5
    assert sin(-330.0) == 0.5
    assert sin(720.0) == 0.0


def test_sin_custom_rounded_values_count():
    res = sin(30.0, rounded_values_count=2)
    assert res == 0.5


def test_sin_custom_accuracy():
    res_low = sin(30.0, accuracy=1)
    res_high = sin(30.0, accuracy=10)
    assert isinstance(res_low, float)
    assert isinstance(res_high, float)


def test_kill_default_accuracy_mutant():
    # Mutator changes default accuracy from 18 to 19; passing explicit accuracy=18 should yield a specific float difference or we can test signature defaults directly.
    import inspect
    sig = inspect.signature(sin)
    assert sig.parameters['accuracy'].default == 18


def test_kill_default_rounded_values_count_mutant():
    # Mutator changes default rounded_values_count from 10 to 11; verify default parameter value in signature.
    import inspect
    sig = inspect.signature(sin)
    assert sig.parameters['rounded_values_count'].default == 10


def test_kill_angle_normalization_divisor_mutant():
    # Mutator changes 360.0 // 361.0 divisor, changing angle normalization for specific inputs like 360.
    # For angle 360.0, 360.0 // 360.0 * 360.0 is 360.0, resulting in 0.0 degrees. With 361.0, 360.0 // 361.0 is 0.0, leaving angle 360.0 unnormalized.
    assert sin(360.0) == 0.0