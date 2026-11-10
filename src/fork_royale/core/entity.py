"""Runtime entities used by the simulation."""

from dataclasses import dataclass, field
from fork_royale.physics.vector import Vec2


@dataclass(slots=True)
class Entity:
    entity_id: str
    position: Vec2
    velocity: Vec2 = field(default_factory=Vec2)
    radius: float = 18.0
    hp: int = 100
    max_hp: int = 100
    fire_cooldown_remaining: float = 0.0
    alive: bool = True

    def apply_damage(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("damage cannot be negative")
        if not self.alive or amount == 0:
            return 0
        actual = min(self.hp, amount)
        self.hp -= actual
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            self.velocity = Vec2()
        return actual

    def to_dict(self) -> dict:
        return {
            "id": self.entity_id,
            "position": self.position.to_list(),
            "velocity": self.velocity.to_list(),
            "radius": self.radius,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "alive": self.alive,
        }


@dataclass(slots=True)
class Projectile:
    owner_id: str
    position: Vec2
    velocity: Vec2
    radius: float
    damage: int
    remaining_range: float
    remaining_lifetime: float

    def to_dict(self) -> dict:
        return {
            "owner_id": self.owner_id,
            "position": self.position.to_list(),
            "velocity": self.velocity.to_list(),
            "radius": self.radius,
            "damage": self.damage,
            "remaining_range": self.remaining_range,
            "remaining_lifetime": self.remaining_lifetime,
        }


@dataclass(frozen=True, slots=True)
class CircleObstacle:
    position: Vec2
    radius: float
    obstacle_id: str = "obstacle"

    def __post_init__(self) -> None:
        if self.radius <= 0:
            raise ValueError("obstacle radius must be positive")
