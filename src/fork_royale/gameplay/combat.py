"""Simple projectile combat for the first simulation prototype."""

from fork_royale.config import GameConfig
from fork_royale.core.entity import Projectile
from fork_royale.core.events import EventLog
from fork_royale.core.world import World
from fork_royale.gameplay.actions import BotAction
from fork_royale.physics.geometry import circles_overlap
from fork_royale.physics.vector import Vec2
from fork_royale.physics.boundaries import is_inside_arena


def create_projectile(world: World, owner_id: str, action: BotAction, config: GameConfig, events: EventLog) -> None:
    owner = world.get_entity(owner_id)
    if not owner.alive or not action.fire or owner.fire_cooldown_remaining > 0:
        return
    direction = action.aim.normalized()
    if direction.length_squared() <= 1e-12:
        return
    muzzle = owner.position + direction * (owner.radius + config.projectile_radius + 1.0)
    velocity = direction * config.projectile_speed
    world.projectiles.append(Projectile(
        owner_id=owner_id,
        position=muzzle,
        velocity=velocity,
        radius=config.projectile_radius,
        damage=config.projectile_damage,
        remaining_range=config.projectile_range,
        remaining_lifetime=config.projectile_lifetime,
    ))
    owner.fire_cooldown_remaining = config.fire_cooldown
    events.emit(world.tick, "projectile_fired", owner_id=owner_id, position=muzzle.to_list())


def update_projectiles(world: World, config: GameConfig, dt: float, events: EventLog) -> None:
    survivors: list[Projectile] = []
    for projectile in world.projectiles:
        old_position = projectile.position
        displacement = projectile.velocity * dt
        travel = displacement.length()
        projectile.position = old_position + displacement
        projectile.remaining_range -= travel
        projectile.remaining_lifetime -= dt

        hit_entity = None
        for target in world.living_entities():
            if target.entity_id == projectile.owner_id:
                continue
            if circles_overlap(projectile.position, projectile.radius, target.position, target.radius):
                hit_entity = target
                break

        if hit_entity is not None:
            damage = hit_entity.apply_damage(projectile.damage)
            events.emit(world.tick, "projectile_hit", owner_id=projectile.owner_id, target_id=hit_entity.entity_id, damage=damage, hp=hit_entity.hp)
            if not hit_entity.alive:
                events.emit(world.tick, "entity_eliminated", entity_id=hit_entity.entity_id, by=projectile.owner_id)
            continue

        blocked = any(circles_overlap(projectile.position, projectile.radius, obstacle.position, obstacle.radius) for obstacle in world.obstacles)
        if blocked:
            events.emit(world.tick, "projectile_blocked", owner_id=projectile.owner_id)
            continue
        if projectile.remaining_range <= 0 or projectile.remaining_lifetime <= 0 or not is_inside_arena(projectile.position, world.width, world.height):
            continue
        survivors.append(projectile)
    world.projectiles = survivors


def tick_cooldowns(world: World, dt: float) -> None:
    for entity in world.entities.values():
        entity.fire_cooldown_remaining = max(0.0, entity.fire_cooldown_remaining - dt)
