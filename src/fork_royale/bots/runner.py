"""Minimal JSON subprocess adapter for local bot development.

This is a convenience runner, NOT a security sandbox. Do not use it to execute
untrusted community submissions on a machine with sensitive data.
"""

import json
import subprocess
from pathlib import Path
from typing import Sequence
from fork_royale.bots.protocol import Observation
from fork_royale.gameplay.actions import BotAction


class BotExecutionError(RuntimeError):
    pass


class SubprocessBot:
    """Run a local bot command once per decision using stdin/stdout JSON."""

    def __init__(self, command: Sequence[str], timeout_seconds: float = 1.0, cwd: str | Path | None = None):
        if not command:
            raise ValueError("command cannot be empty")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self.command = list(command)
        self.timeout_seconds = timeout_seconds
        self.cwd = str(cwd) if cwd is not None else None

    def decide(self, observation: Observation) -> BotAction:
        try:
            completed = subprocess.run(
                self.command,
                input=json.dumps(observation.to_dict()),
                text=True,
                capture_output=True,
                timeout=self.timeout_seconds,
                cwd=self.cwd,
                check=False,
                shell=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise BotExecutionError(f"bot exceeded {self.timeout_seconds:.3f}s decision limit") from exc
        except OSError as exc:
            raise BotExecutionError(f"could not start bot process: {exc}") from exc
        if completed.returncode != 0:
            detail = completed.stderr.strip()[:500]
            raise BotExecutionError(f"bot exited with code {completed.returncode}: {detail}")
        try:
            payload = json.loads(completed.stdout)
            return BotAction.from_mapping(payload)
        except (json.JSONDecodeError, ValueError) as exc:
            raise BotExecutionError(f"bot returned invalid JSON action: {exc}") from exc
