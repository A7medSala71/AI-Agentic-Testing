import pytest
from function_28 import sin


def test_sin_zero():
    assert sin(0.0) == 0.0


def test_sin_standard_angles():
    assert sin(30.0) == pytest.approx(0.5)
    assert sin(90.0) == pytest.approx(1.0)
    assert sin(180.0) == pytest.approx(0.0)
    assert sin(270.0) == pytest.approx(-1.0)
    assert sin(360.0) == pytest.approx(0.0)


def test_sin_normalization():
    assert sin(390.0) == pytest.approx(0.5)
    assert sin(-330.0) == pytest.approx(0.5)
    assert sin(720.0) == pytest.approx(0.0)


def test_sin_rounding():
    res = sin(30.0, accuracy=5, rounded_values_count=2)
    assert res == 0.5


def test_sin_accuracy_parameter():
    res_low = sin(45.0, accuracy=1, rounded_values_count=10)
    res_high = sin(45.0, accuracy=20, rounded_values_count=10)
    assert res_low != res_high


def test_sin_default_parameters():
    # Kills mutants changing default values of accuracy (18 -> 19) 
    # and rounded_values_count (10 -> 11).
    # We check the exact string representation or float precision.
    import inspect
    sig = inspect.signature(sin)
    assert sig.parameters['accuracy'].default == 18
    assert sig.parameters['rounded_values_count'].default == 10


def test_sin_normalization_361():
    # Kills angle_in_degrees // 361.0 * 360.0 mutant
    # For angle 361.0, 361 // 360 * 360 = 360, angle becomes 1.0.
    # But 361 // 361 * 360 = 360, angle becomes 1.0 as well? Wait.
    # Let's test an angle where 360 vs 361 makes a difference, e.g., angle = 360.0 or 720.0 or something around 360.
    # If angle = 360.0:
    # Original: 360.0 // 360.0 * 360.0 = 1.0 * 360.0 = 360.0. 360.0 - 360.0 = 0.0.
    # Mutated (361.0): 360.0 // 361.0 * 360.0 = 0.0 * 360.0 = 0.0. 360.0 - 0.0 = 360.0.
    # sin(360.0) is 0.0 in both, but what about sin(360.0, rounded_values_count=...) or checking intermediate?
    # Wait, sin(360.0) on original returns 0.0. On mutated with 360.0, angle_in_degrees becomes 360.0, 
    # which normalizes to radians(360.0), whose sin is also ~0.0.
    # What about angle = 720.0?
    # Original: 720 // 360 * 360 = 720. 720 - 720 = 0.
    # Mutated: 720 // 361 * 360 = 1 * 360 = 360. 720 - 360 = 360. Still sin(360) = 0.
    # What about angle = 361.0?
    # Original: 361 // 360 * 360 = 360. 361 - 360 = 1.0.
    # Mutated: 361 // 361 * 360 = 360. 361 - 360 = 1.0.
    # What about angle = 721.0?
    # Original: 721 // 360 * 360 = 720. 721 - 720 = 1.0.
    # Mutated: 721 // 361 * 360 = 1 * 360 = 360. 721 - 360 = 361.0!
    # sin(361.0 degrees) vs sin(1.0 degrees)! They are different!
    assert sin(721.0) == pytest.approx(sin(1.0))