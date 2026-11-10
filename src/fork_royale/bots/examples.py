"""Built-in reference bots used by the CLI and documentation examples."""

from fork_royale.bots.protocol import Observation
from fork_royale.gameplay.actions import BotAction
from fork_royale.physics.vector import Vec2


class IdleBot:
    """A passive bot useful for checking that the simulation advances."""

    def decide(self, observation: Observation) -> BotAction:
        return BotAction()


class SampleBot:
    """A tiny pursuit strategy. It is a teaching example, not a competitive bot."""

    def decide(self, observation: Observation) -> BotAction:
        if not observation.opponents:
            return BotAction()
        opponent = min(
            observation.opponents,
            key=lambda item: (item.x - observation.self_state.x) ** 2 + (item.y - observation.self_state.y) ** 2,
        )
        delta = Vec2(opponent.x - observation.self_state.x, opponent.y - observation.self_state.y)
        distance = delta.length()
        direction = delta.normalized()
        return BotAction(move=direction, aim=direction, fire=distance < 430.0)
