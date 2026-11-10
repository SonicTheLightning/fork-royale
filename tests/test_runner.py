import json
import sys
from pathlib import Path

from fork_royale.bots.protocol import Observation
from fork_royale.bots.runner import SubprocessBot
from fork_royale.core.world import World
from fork_royale.config import GameConfig


def test_external_sample_bot_uses_json_protocol():
    repo_root = Path(__file__).resolve().parents[2]
    config = GameConfig()
    world = World.two_player_arena(config, "sample", "idle")
    observation = Observation.from_world("sample", world, config.fixed_dt)
    bot = SubprocessBot([sys.executable, str(repo_root / "examples" / "sample_bot" / "main.py")], timeout_seconds=5.0, cwd=repo_root)
    action = bot.decide(observation)
    assert action.move.length() <= 1.0
    assert action.fire is False
