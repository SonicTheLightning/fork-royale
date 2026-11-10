"""Authoritative world state for one match."""

from dataclasses import dataclass, field
from fork_royale.config import GameConfig
from fork_royale.core.entity import CircleObstacle, Entity, Projectile
from fork_royale.physics.vector import Vec2


@dataclass(slots=True)
class World:
    width: float
    height: float
    entities: dict[str, Entity] = field(default_factory=dict)
    projectiles: list[Projectile] = field(default_factory=list)
    obstacles: list[CircleObstacle] = field(default_factory=list)
    tick: int = 0
    seed: int = 0

    def add_entity(self, entity: Entity) -> None:
        if entity.entity_id in self.entities:
            raise ValueError(f"entity {entity.entity_id!r} already exists")
        if entity.radius * 2 > min(self.width, self.height):
            raise ValueError("entity is too large for this arena")
        self.entities[entity.entity_id] = entity

    def get_entity(self, entity_id: str) -> Entity:
        try:
            return self.entities[entity_id]
        except KeyError as exc:
            raise KeyError(f"unknown entity: {entity_id}") from exc

    def living_entities(self) -> list[Entity]:
        return [entity for entity in self.entities.values() if entity.alive]

    def snapshot(self) -> dict:
        return {
            "tick": self.tick,
            "width": self.width,
            "height": self.height,
            "seed": self.seed,
            "entities": [entity.to_dict() for entity in self.entities.values()],
            "projectiles": [projectile.to_dict() for projectile in self.projectiles],
        }

    @classmethod
    def two_player_arena(cls, config: GameConfig, first_id: str = "player_1", second_id: str = "player_2", seed: int = 0) -> "World":
        world = cls(config.arena_width, config.arena_height, seed=seed)
        y = config.arena_height / 2
        left_x = max(config.entity_radius, config.arena_width * 0.25)
        right_x = min(config.arena_width - config.entity_radius, config.arena_width * 0.75)
        world.add_entity(Entity(first_id, Vec2(left_x, y), radius=config.entity_radius, hp=config.starting_hp, max_hp=config.starting_hp))
        world.add_entity(Entity(second_id, Vec2(right_x, y), radius=config.entity_radius, hp=config.starting_hp, max_hp=config.starting_hp))
        return world
