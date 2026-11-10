"""Small immutable 2D vector type used throughout the simulation."""

from dataclasses import dataclass
import math
from typing import Any


@dataclass(frozen=True, slots=True)
class Vec2:
    x: float = 0.0
    y: float = 0.0

    def __post_init__(self) -> None:
        if not math.isfinite(self.x) or not math.isfinite(self.y):
            raise ValueError("vector components must be finite")

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vec2":
        return Vec2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vec2":
        return self * scalar

    def __truediv__(self, scalar: float) -> "Vec2":
        if scalar == 0:
            raise ZeroDivisionError("cannot divide a vector by zero")
        return Vec2(self.x / scalar, self.y / scalar)

    def dot(self, other: "Vec2") -> float:
        return self.x * other.x + self.y * other.y

    def length_squared(self) -> float:
        return self.dot(self)

    def length(self) -> float:
        return math.sqrt(self.length_squared())

    def normalized(self) -> "Vec2":
        magnitude = self.length()
        return self / magnitude if magnitude > 1e-12 else Vec2()

    def clamp_length(self, maximum: float) -> "Vec2":
        if maximum < 0:
            raise ValueError("maximum length cannot be negative")
        magnitude = self.length()
        if magnitude <= maximum or magnitude <= 1e-12:
            return self
        return self * (maximum / magnitude)

    def distance_to(self, other: "Vec2") -> float:
        return (self - other).length()

    def to_list(self) -> list[float]:
        return [self.x, self.y]

    @classmethod
    def from_value(cls, value: Any, *, field_name: str = "vector") -> "Vec2":
        """Accept [x, y] or {"x": x, "y": y}; reject malformed values."""
        if isinstance(value, dict):
            x, y = value.get("x", 0.0), value.get("y", 0.0)
        elif isinstance(value, (list, tuple)) and len(value) == 2:
            x, y = value
        else:
            raise ValueError(f"{field_name} must be [x, y] or an x/y object")
        try:
            return cls(float(x), float(y))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{field_name} contains invalid coordinates") from exc
