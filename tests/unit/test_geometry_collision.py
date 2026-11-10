from fork_royale.config import GameConfig
from fork_royale.core.entity import Entity
from fork_royale.core.world import World
from fork_royale.physics.collision import resolve_collisions
from fork_royale.physics.geometry import circles_overlap
from fork_royale.physics.vector import Vec2


def test_circle_overlap():
    assert circles_overlap(Vec2(0, 0), 2, Vec2(3, 0), 2)
    assert not circles_overlap(Vec2(0, 0), 1, Vec2(3, 0), 1)


def test_entity_collision_separates_entities():
    config = GameConfig()
    world = World(500, 300)
    world.add_entity(Entity("a", Vec2(100, 100), radius=20))
    world.add_entity(Entity("b", Vec2(110, 100), radius=20))
    resolve_collisions(world, config)
    a, b = world.entities.values()
    assert a.position.distance_to(b.position) >= 39.999
