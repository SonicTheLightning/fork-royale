import pytest
from fork_royale.gameplay.actions import BotAction
from fork_royale.physics.vector import Vec2


def test_action_parsing_clamps_movement():
    action = BotAction.from_mapping({"move": [3, 4], "aim": [0, 2], "fire": True})
    assert action.move.length() == pytest.approx(1.0)
    assert action.aim == Vec2(0, 1)  # aim is clamped; combat normalizes it when firing.
    assert action.fire is True


def test_action_rejects_non_boolean_fire():
    with pytest.raises(ValueError):
        BotAction.from_mapping({"fire": "yes"})
