# Fork Royale Starter Implementation

This source pack creates the first runnable continuous-movement prototype described by the branch architecture.

## Important scope note

The engine is a development starter, not a finished competitive game. Movement, collisions, basic projectile combat, trusted in-process bots, a local subprocess adapter, ASCII rendering and JSONL replay are implemented. Competitive rules, graphical rendering, multiplayer networking, tournament operations and production bot isolation are not implemented.

The values in `src/fork_royale/config.py` are provisional and must be playtested with the other contributor before being treated as final rules.

## Install

```bash
python -m venv .venv
