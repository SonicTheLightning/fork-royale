"""Central configuration for the first playable simulation prototype."""

from dataclasses import dataclass
import math


@dataclass(frozen=True, slots=True)
class GameConfig:
    """Simulation constants. These values are provisional game-design defaults."""

    arena_width: float = 1000.0
    arena_height: float = 700.0
    fixed_dt: float = 1.0 / 30.0
    max_ticks: int = 1800

    acceleration: float = 720.0
    max_speed: float = 260.0
    linear_drag: float = 2.8
    entity_radius: float = 18.0
    starting_hp: int = 100
    collision_restitution: float = 0.15

    projectile_speed: float = 520.0
    projectile_radius: float = 5.0
    projectile_damage: int = 10
    projectile_range: float = 520.0
    projectile_lifetime: float = 1.5
    fire_cooldown: float = 0.55


    def __post_init__(self) -> None:
        positive = {
            "arena_width": self.arena_width,
            "arena_height": self.arena_height,
            "fixed_dt": self.fixed_dt,
            "max_ticks": self.max_ticks,
            "acceleration": self.acceleration,
            "max_speed": self.max_speed,
            "entity_radius": self.entity_radius,
            "starting_hp": self.starting_hp,
            "projectile_speed": self.projectile_speed,
            "projectile_radius": self.projectile_radius,
            "projectile_damage": self.projectile_damage,
            "projectile_range": self.projectile_range,
            "projectile_lifetime": self.projectile_lifetime,
            "fire_cooldown": self.fire_cooldown,
        }
        for name, value in positive.items():
            if not math.isfinite(float(value)) or value <= 0:
                raise ValueError(f"{name} must be a positive finite value")
        if self.linear_drag < 0 or not math.isfinite(self.linear_drag):
            raise ValueError("linear_drag must be finite and non-negative")
        if not 0.0 <= self.collision_restitution <= 1.0:
            raise ValueError("collision_restitution must be between 0 and 1")
        if self.arena_width <= 2 * self.entity_radius:
            raise ValueError("arena_width is too small for the configured entity radius")
        if self.arena_height <= 2 * self.entity_radius:
            raise ValueError("arena_height is too small for the configured entity radius")
