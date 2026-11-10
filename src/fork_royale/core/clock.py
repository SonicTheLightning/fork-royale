"""Fixed timestep accumulator for real-time front ends."""

from dataclasses import dataclass


@dataclass(slots=True)
class FixedStepClock:
    step_seconds: float
    max_steps_per_frame: int = 8
    accumulator: float = 0.0

    def __post_init__(self) -> None:
        if self.step_seconds <= 0:
            raise ValueError("step_seconds must be positive")
        if self.max_steps_per_frame < 1:
            raise ValueError("max_steps_per_frame must be at least 1")

    def advance(self, elapsed_seconds: float, callback) -> int:
        """Run callback(step_seconds) for available steps; drop excess backlog."""
        if elapsed_seconds < 0:
            raise ValueError("elapsed_seconds cannot be negative")
        self.accumulator += elapsed_seconds
        steps = 0
        while self.accumulator >= self.step_seconds and steps < self.max_steps_per_frame:
            callback(self.step_seconds)
            self.accumulator -= self.step_seconds
            steps += 1
        if steps == self.max_steps_per_frame and self.accumulator >= self.step_seconds:
            self.accumulator %= self.step_seconds
        return steps
