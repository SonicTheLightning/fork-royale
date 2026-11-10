from fork_royale.config import GameConfig
from fork_royale.core.entity import Entity
from fork_royale.physics.movement import integrate_movement
from fork_royale.physics.vector import Vec2


def test_movement_is_continuous_and_not_tile_based():
    config = GameConfig()
    entity = Entity("a", Vec2(100.0, 100.0), radius=config.entity_radius)
    integrate_movement(entity, Vec2(1, 0.3), config, config.fixed_dt)
    assert entity.position.x != round(entity.position.x)
    assert entity.position.y != round(entity.position.y)
    assert entity.position.x > 100.0
    assert entity.position.y > 100.0


def test_speed_is_capped():
    config = GameConfig()
    entity = Entity("a", Vec2(100.0, 100.0), velocity=Vec2(10000, 0), radius=config.entity_radius)
    integrate_movement(entity, Vec2(1, 0), config, config.fixed_dt)
    assert entity.velocity.length() <= config.max_speed + 1e-9
