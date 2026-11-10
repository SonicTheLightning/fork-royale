"""Simple append-only event log for debugging and replay."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class GameEvent:
    tick: int
    kind: str
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"tick": self.tick, "kind": self.kind, "data": self.data}


@dataclass(slots=True)
class EventLog:
    events: list[GameEvent] = field(default_factory=list)

    def emit(self, tick: int, kind: str, **data: Any) -> GameEvent:
        event = GameEvent(tick=tick, kind=kind, data=data)
        self.events.append(event)
        return event

    def since(self, index: int) -> list[GameEvent]:
        return self.events[index:]
