"""Observation schema and bot protocol."""

from dataclasses import dataclass
from typing import Protocol
from fork_royale.core.world import World
from fork_royale.gameplay.actions import BotAction


@dataclass(frozen=True, slots=True)
class EntityObservation:
    entity_id: str
    x: float
    y: float
    velocity_x: float
    velocity_y: float
    radius: float
    hp: int
    max_hp: int
    alive: bool

    def to_dict(self) -> dict:
        return {
            "id": self.entity_id,
            "position": [self.x, self.y],
            "velocity": [self.velocity_x, self.velocity_y],
            "radius": self.radius,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "alive": self.alive,
        }


@dataclass(frozen=True, slots=True)
class ObstacleObservation:
    obstacle_id: str
    x: float
    y: float
    radius: float

    def to_dict(self) -> dict:
        return {"id": self.obstacle_id, "position": [self.x, self.y], "radius": self.radius}


@dataclass(frozen=True, slots=True)
class Observation:
    bot_id: str
    tick: int
    dt: float
    arena_width: float
    arena_height: float
    self_state: EntityObservation
    opponents: tuple[EntityObservation, ...]
    obstacles: tuple[ObstacleObservation, ...]

    def to_dict(self) -> dict:
        return {
            "bot_id": self.bot_id,
            "tick": self.tick,
            "dt": self.dt,
            "arena": {"width": self.arena_width, "height": self.arena_height},
            "self": self.self_state.to_dict(),
            "opponents": [opponent.to_dict() for opponent in self.opponents],
            "obstacles": [obstacle.to_dict() for obstacle in self.obstacles],
        }

    @classmethod
    def from_world(cls, bot_id: str, world: World, dt: float) -> "Observation":
        own = world.get_entity(bot_id)
        def convert(entity):
            return EntityObservation(
                entity_id=entity.entity_id,
                x=entity.position.x,
                y=entity.position.y,
                velocity_x=entity.velocity.x,
                velocity_y=entity.velocity.y,
                radius=entity.radius,
                hp=entity.hp,
                max_hp=entity.max_hp,
                alive=entity.alive,
            )
        opponents = tuple(convert(entity) for entity in world.living_entities() if entity.entity_id != bot_id)
        obstacles = tuple(ObstacleObservation(o.obstacle_id, o.position.x, o.position.y, o.radius) for o in world.obstacles)
        return cls(bot_id, world.tick, dt, world.width, world.height, convert(own), opponents, obstacles)


class Bot(Protocol):
    def decide(self, observation: Observation) -> BotAction | dict:
        """Return an action for this simulation tick."""
