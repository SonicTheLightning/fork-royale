"""Write deterministic match snapshots to a JSON Lines file."""

import json
from pathlib import Path
from fork_royale.core.events import GameEvent
from fork_royale.core.world import World


class ReplayRecorder:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._handle = self.path.open("w", encoding="utf-8")
        self._write({"type": "header", "format": "fork-royale-replay", "version": 1})

    def _write(self, value: dict) -> None:
        self._handle.write(json.dumps(value, separators=(",", ":"), sort_keys=True) + "\n")
        self._handle.flush()

    def record(self, world: World, events: list[GameEvent] | None = None) -> None:
        self._write({
            "type": "frame",
            "world": world.snapshot(),
            "events": [event.to_dict() for event in (events or [])],
        })

    def close(self) -> None:
        if not self._handle.closed:
            self._handle.close()

    def __enter__(self) -> "ReplayRecorder":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
