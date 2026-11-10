"""Deterministic fixed-step match engine."""

from fork_royale.bots.manager import BotManager
from fork_royale.bots.protocol import Observation
from fork_royale.config import GameConfig
from fork_royale.core.events import EventLog
from fork_royale.core.world import World
from fork_royale.gameplay.combat import create_projectile, tick_cooldowns, update_projectiles
from fork_royale.gameplay.rules import MatchResult, evaluate_match
from fork_royale.physics.boundaries import constrain_entity
from fork_royale.physics.collision import resolve_collisions
from fork_royale.physics.movement import integrate_movement


class GameEngine:
    def __init__(self, world: World, bots: BotManager, config: GameConfig | None = None):
        self.config = config or GameConfig(arena_width=world.width, arena_height=world.height)
        if abs(world.width - self.config.arena_width) > 1e-9 or abs(world.height - self.config.arena_height) > 1e-9:
            raise ValueError("world dimensions must match GameConfig")
        if bots.bot_ids != set(world.entities):
            raise ValueError("registered bot IDs must exactly match world entity IDs")
        self.world = world
        self.bots = bots
        self.events = EventLog()
        self.result: MatchResult | None = None

    def step(self) -> MatchResult | None:
        """Advance exactly one fixed simulation tick."""
        if self.result is not None:
            return self.result

        # Every bot receives an observation from the same pre-action world state.
        observations = {
            entity.entity_id: Observation.from_world(entity.entity_id, self.world, self.config.fixed_dt)
            for entity in self.world.living_entities()
        }
        decisions = self.bots.decide_all(observations)
        for bot_id, message in self.bots.last_errors.items():
            self.events.emit(self.world.tick, "bot_error", bot_id=bot_id, message=message)

        for bot_id, action in decisions.items():
            create_projectile(self.world, bot_id, action, self.config, self.events)

        for bot_id, action in decisions.items():
            entity = self.world.get_entity(bot_id)
            if entity.alive:
                integrate_movement(entity, action.move, self.config, self.config.fixed_dt)
                constrain_entity(entity, self.world.width, self.world.height)

        resolve_collisions(self.world, self.config)
        update_projectiles(self.world, self.config, self.config.fixed_dt, self.events)
        tick_cooldowns(self.world, self.config.fixed_dt)

        self.world.tick += 1
        self.result = evaluate_match(self.world, self.config.max_ticks)
        if self.result is not None:
            self.events.emit(self.world.tick, "match_finished", **self.result.to_dict())
        return self.result

    def run(self, max_steps: int | None = None) -> MatchResult | None:
        steps = max_steps if max_steps is not None else self.config.max_ticks
        if steps < 0:
            raise ValueError("max_steps cannot be negative")
        for _ in range(steps):
            if self.step() is not None:
                break
        return self.result
