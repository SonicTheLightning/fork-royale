from fork_royale.bots.manager import BotManager
from fork_royale.config import GameConfig
from fork_royale.core.engine import GameEngine
from fork_royale.core.world import World
from fork_royale.gameplay.actions import BotAction
from fork_royale.physics.vector import Vec2


class MoveRight:
    def decide(self, observation):
        return BotAction(move=Vec2(1, 0))


class MoveLeft:
    def decide(self, observation):
        return BotAction(move=Vec2(-1, 0))


def test_engine_advances_free_movement():
    config = GameConfig(arena_width=500, arena_height=300, max_ticks=20)
    world = World.two_player_arena(config, "a", "b")
    engine = GameEngine(world, BotManager({"a": MoveRight(), "b": MoveLeft()}), config)
    start_a = world.get_entity("a").position
    engine.step()
    assert world.tick == 1
    assert world.get_entity("a").position.x > start_a.x


def test_match_stops_at_tick_limit():
    config = GameConfig(arena_width=500, arena_height=300, max_ticks=2)
    world = World.two_player_arena(config, "a", "b")
    engine = GameEngine(world, BotManager({"a": MoveRight(), "b": MoveLeft()}), config)
    result = engine.run()
    assert result is not None
    assert world.tick == 2
