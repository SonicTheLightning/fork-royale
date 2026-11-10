"""Collect decisions from trusted in-process bots."""

from typing import Mapping
from fork_royale.bots.protocol import Bot, Observation
from fork_royale.gameplay.actions import BotAction


class BotManager:
    def __init__(self, bots: Mapping[str, Bot]):
        if not bots:
            raise ValueError("at least one bot is required")
        self._bots = dict(bots)
        self.last_errors: dict[str, str] = {}

    @property
    def bot_ids(self) -> set[str]:
        return set(self._bots)

    def decide_all(self, observations: Mapping[str, Observation]) -> dict[str, BotAction]:
        decisions: dict[str, BotAction] = {}
        self.last_errors = {}
        for bot_id, observation in observations.items():
            bot = self._bots.get(bot_id)
            if bot is None:
                self.last_errors[bot_id] = "No bot registered for this entity"
                decisions[bot_id] = BotAction()
                continue
            try:
                response = bot.decide(observation)
                decisions[bot_id] = response if isinstance(response, BotAction) else BotAction.from_mapping(response)
            except Exception as exc:  # A broken bot must not crash the entire simulation.
                self.last_errors[bot_id] = f"{type(exc).__name__}: {exc}"
                decisions[bot_id] = BotAction()
        return decisions
