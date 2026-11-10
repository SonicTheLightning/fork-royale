import math
import pytest
from fork_royale.physics.vector import Vec2


def test_vector_addition_and_subtraction():
    assert Vec2(2, 3) + Vec2(4, -1) == Vec2(6, 2)
    assert Vec2(6, 2) - Vec2(4, -1) == Vec2(2, 3)


def test_normalize_and_clamp_length():
    assert Vec2(3, 4).normalized().length() == pytest.approx(1.0)
    assert Vec2(6, 8).clamp_length(5).length() == pytest.approx(5.0)


def test_zero_vector_normalizes_to_zero():
    assert Vec2().normalized() == Vec2()


def test_non_finite_vector_is_rejected():
    with pytest.raises(ValueError):
        Vec2(math.inf, 0)
