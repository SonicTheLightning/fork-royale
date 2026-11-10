# Game Design Draft

## High-level concept

Fork Royale is a Python bot programming game in a continuous 2D arena. Players write autonomous agents that receive observations and return actions. The simulation engine remains authoritative over movement, collisions, combat and match results.

## Movement direction

The design explicitly rejects tile-based movement. Positions and velocities are continuous floating point vectors. Bots may request movement in any direction. The engine applies acceleration, drag and speed limits.

## Provisional prototype rules

The starter implementation includes provisional defaults for two entities, circular body collision, health, cooldown-based projectiles and a time limit. These defaults are implementation scaffolding, not final competitive rules.

| Rule | Prototype default | Decision status |
|---|---:|---|
| Arena size | 1000 × 700 world units | Provisional |
| Simulation frequency | 30 ticks per second | Provisional |
| Starting health | 100 HP | Provisional |
| Maximum speed | 260 units / second | Provisional |
| Acceleration | 720 units / second² | Provisional |
| Projectile damage | 10 HP | Provisional |
| Fire cooldown | 0.55 seconds | Provisional |
| Maximum match duration | 1800 ticks | Provisional |

## Still to decide

Arena layouts, obstacles, weapons, abilities, respawns, visibility rules, match formats, scoring and final victory conditions require joint design and playtesting.
