"""Arena boundary handling."""

from fork_royale.core.entity import Entity
from fork_royale.physics.vector import Vec2


def constrain_entity(entity: Entity, width: float, height: float) -> None:
    """Keep a circular entity inside the rectangular arena."""
    r = entity.radius
    x = min(max(entity.position.x, r), width - r)
    y = min(max(entity.position.y, r), height - r)
    entity.position = Vec2(x, y)
    if x in (r, width - r):
        entity.velocity = Vec2(0.0, entity.velocity.y)
    if y in (r, height - r):
        entity.velocity = Vec2(entity.velocity.x, 0.0)


def is_inside_arena(position: Vec2, width: float, height: float) -> bool:
    return 0.0 <= position.x <= width and 0.0 <= position.y <= height
