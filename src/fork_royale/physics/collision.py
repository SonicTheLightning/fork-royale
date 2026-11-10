"""Circle collision resolution for entities and static obstacles."""

from itertools import combinations
from fork_royale.config import GameConfig
from fork_royale.core.world import World
from fork_royale.physics.geometry import circle_intersection_depth
from fork_royale.physics.vector import Vec2
from fork_royale.physics.boundaries import constrain_entity


def _fallback_normal(first_id: str, second_id: str) -> Vec2:
    # Stable fallback prevents NaNs when two centers are exactly identical.
    return Vec2(1.0, 0.0) if first_id < second_id else Vec2(-1.0, 0.0)


def resolve_collisions(world: World, config: GameConfig) -> None:
    living = world.living_entities()

    for entity in living:
        for obstacle in world.obstacles:
            depth = circle_intersection_depth(entity.position, entity.radius, obstacle.position, obstacle.radius)
            if depth > 0:
                delta = entity.position - obstacle.position
                normal = delta.normalized() if delta.length_squared() > 1e-12 else Vec2(1.0, 0.0)
                entity.position = entity.position + normal * depth
                inward_speed = entity.velocity.dot(normal)
                if inward_speed < 0:
                    entity.velocity = entity.velocity - normal * ((1.0 + config.collision_restitution) * inward_speed)
            constrain_entity(entity, world.width, world.height)

    for first, second in combinations(living, 2):
        depth = circle_intersection_depth(first.position, first.radius, second.position, second.radius)
        if depth <= 0:
            continue
        delta = second.position - first.position
        normal = delta.normalized() if delta.length_squared() > 1e-12 else _fallback_normal(first.entity_id, second.entity_id)
        correction = normal * (depth / 2.0)
        first.position = first.position - correction
        second.position = second.position + correction

        relative_velocity = second.velocity - first.velocity
        separating_speed = relative_velocity.dot(normal)
        if separating_speed < 0:
            impulse = -(1.0 + config.collision_restitution) * separating_speed / 2.0
            first.velocity = first.velocity - normal * impulse
            second.velocity = second.velocity + normal * impulse

        constrain_entity(first, world.width, world.height)
        constrain_entity(second, world.width, world.height)
