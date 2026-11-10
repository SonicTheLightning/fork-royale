"""Velocity integration for free, continuous movement."""

import math
from fork_royale.config import GameConfig
from fork_royale.core.entity import Entity
from fork_royale.physics.vector import Vec2


def integrate_movement(entity: Entity, direction: Vec2, config: GameConfig, dt: float) -> None:
    """Apply a normalized control vector, drag, speed cap and position update."""
    if dt <= 0:
        raise ValueError("dt must be positive")
    control = direction.clamp_length(1.0)
    acceleration = control * config.acceleration
    entity.velocity = entity.velocity + acceleration * dt

    # Exponential drag is stable for different fixed timestep values.
    drag_factor = math.exp(-config.linear_drag * dt)
    entity.velocity = (entity.velocity * drag_factor).clamp_length(config.max_speed)
    entity.position = entity.position + entity.velocity * dt
