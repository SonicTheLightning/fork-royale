"""Validated bot decisions. Movement and aim vectors are direction inputs."""

from dataclasses import dataclass, field
from typing import Any
from fork_royale.physics.vector import Vec2


@dataclass(frozen=True, slots=True)
class BotAction:
    move: Vec2 = field(default_factory=Vec2)
    aim: Vec2 = field(default_factory=Vec2)
    fire: bool = False

    @classmethod
    def from_mapping(cls, payload: Any) -> "BotAction":
        if not isinstance(payload, dict):
            raise ValueError("bot response must be a JSON object")
        move = Vec2.from_value(payload.get("move", [0, 0]), field_name="move").clamp_length(1.0)
        aim = Vec2.from_value(payload.get("aim", [0, 0]), field_name="aim").clamp_length(1.0)
        fire = payload.get("fire", False)
        if not isinstance(fire, bool):
            raise ValueError("fire must be a boolean")
        return cls(move=move, aim=aim, fire=fire)

    def to_dict(self) -> dict:
        return {"move": self.move.to_list(), "aim": self.aim.to_list(), "fire": self.fire}
