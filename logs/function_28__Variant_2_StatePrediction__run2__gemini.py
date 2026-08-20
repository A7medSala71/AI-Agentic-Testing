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
    assert sin(-390.0) == -0.5


def test_sin_custom_rounding():
    val = sin(30.0, rounded_values_count=2)
    assert val == 0.5


def test_sin_accuracy_parameter():
    val_low = sin(30.0, accuracy=1, rounded_values_count=5)
    val_high = sin(30.0, accuracy=18, rounded_values_count=5)
    assert val_low != val_high


def test_mutant_default_accuracy():
    # Mutator changes default accuracy from 18 to 19, causing high-precision divergence for an angle like 450 degrees.
    assert sin(450.0, rounded_values_count=15) != sin(450.0, accuracy=19, rounded_values_count=15)


def test_mutant_default_rounded_values_count():
    # Mutator changes default rounded_values_count from 10 to 11, causing the output length/rounding to differ from expected default precision.
    import inspect
    sig = inspect.signature(sin)
    assert sig.parameters['rounded_values_count'].default == 10


def test_mutant_angle_normalization_mod():
    # Mutator changes 360.0 // 360.0 to 360.0 // 361.0, so an angle of 360.0 normalizes differently and yields incorrect output.
    assert sin(360.0, accuracy=5, rounded_values_count=10) == 0.0