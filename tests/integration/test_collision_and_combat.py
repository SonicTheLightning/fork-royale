from fork_royale.bots.manager import BotManager
from fork_royale.config import GameConfig
from fork_royale.core.engine import GameEngine
from fork_royale.core.world import World
from fork_royale.gameplay.actions import BotAction
from fork_royale.physics.vector import Vec2


class FireRight:
    def decide(self, observation):
        return BotAction(aim=Vec2(1, 0), fire=True)


class Idle:
    def decide(self, observation):
        return BotAction()


def test_projectile_can_damage_opponent():
    config = GameConfig(arena_width=500, arena_height=300, fixed_dt=0.1, max_ticks=100,
                        projectile_speed=500, projectile_range=500, projectile_lifetime=2,
                        fire_cooldown=1, projectile_damage=10, linear_drag=0)
    world = World(500, 300)
    from fork_royale.core.entity import Entity
    world.add_entity(Entity("a", Vec2(100, 150), radius=10, hp=100, max_hp=100))
    world.add_entity(Entity("b", Vec2(180, 150), radius=10, hp=100, max_hp=100))
    engine = GameEngine(world, BotManager({"a": FireRight(), "b": Idle()}), config)
    engine.step()
    engine.step()
    assert world.get_entity("b").hp < 100
