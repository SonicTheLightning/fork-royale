"""Run a local sample match and optionally record a replay."""

import argparse
from pathlib import Path
from fork_royale.bots.manager import BotManager
from fork_royale.config import GameConfig
from fork_royale.core.engine import GameEngine
from fork_royale.core.world import World
from fork_royale.rendering.renderer import AsciiRenderer
from fork_royale.replay.recorder import ReplayRecorder
from fork_royale.bots.examples import IdleBot, SampleBot


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a Fork Royale prototype match")
    parser.add_argument("--ticks", type=int, default=600, help="maximum simulation ticks")
    parser.add_argument("--width", type=float, default=1000.0, help="arena width in world units")
    parser.add_argument("--height", type=float, default=700.0, help="arena height in world units")
    parser.add_argument("--seed", type=int, default=1, help="replay metadata seed")
    parser.add_argument("--replay", type=Path, help="write a JSONL replay to this path")
    parser.add_argument("--no-render", action="store_true", help="skip ASCII arena output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.ticks < 0:
        raise SystemExit("--ticks must be non-negative")
    config = GameConfig(arena_width=args.width, arena_height=args.height, max_ticks=max(1, args.ticks))
    world = World.two_player_arena(config, "sample", "idle", seed=args.seed)
    bots = BotManager({"sample": SampleBot(), "idle": IdleBot()})
    engine = GameEngine(world, bots, config)

    recorder = ReplayRecorder(args.replay) if args.replay else None
    try:
        if recorder:
            recorder.record(world)
        for _ in range(args.ticks):
            event_start = len(engine.events.events)
            result = engine.step()
            if recorder:
                recorder.record(world, engine.events.since(event_start))
            if result is not None:
                break
    finally:
        if recorder:
            recorder.close()

    if not args.no_render:
        print(AsciiRenderer().render(world))
    if engine.result:
        print(f"Result: {engine.result.to_dict()}")
    else:
        print(f"Stopped after {world.tick} ticks without a completed match.")
    if args.replay:
        print(f"Replay written to: {args.replay}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
