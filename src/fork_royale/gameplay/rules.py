"""Match termination rules for the prototype."""

from dataclasses import dataclass
from fork_royale.core.world import World


@dataclass(frozen=True, slots=True)
class MatchResult:
    winner_id: str | None
    reason: str
    draw: bool = False

    def to_dict(self) -> dict:
        return {"winner_id": self.winner_id, "reason": self.reason, "draw": self.draw}


def evaluate_match(world: World, max_ticks: int) -> MatchResult | None:
    living = world.living_entities()
    if len(living) == 1:
        return MatchResult(living[0].entity_id, "last_entity_alive")
    if len(living) == 0:
        return MatchResult(None, "all_entities_eliminated", draw=True)
    if world.tick >= max_ticks:
        ranked = sorted(living, key=lambda entity: (entity.hp, entity.entity_id), reverse=True)
        if len(ranked) > 1 and ranked[0].hp == ranked[1].hp:
            return MatchResult(None, "time_limit_draw", draw=True)
        return MatchResult(ranked[0].entity_id, "time_limit_hp")
    return None
