from fork_royale.core.world import World
from fork_royale.physics.vector import Vec2
from fork_royale.replay.recorder import ReplayRecorder
from fork_royale.replay.reader import read_replay


def test_replay_round_trip(tmp_path):
    world = World(100, 80)
    path = tmp_path / "match.jsonl"
    with ReplayRecorder(path) as recorder:
        recorder.record(world)
    frames = list(read_replay(path))
    assert len(frames) == 1
    assert frames[0]["world"]["width"] == 100
