"""World-to-screen coordinate conversion for renderers."""

from dataclasses import dataclass
from fork_royale.physics.vector import Vec2


@dataclass(frozen=True, slots=True)
class Camera:
    world_width: float
    world_height: float
    screen_width: int
    screen_height: int

    def world_to_screen(self, position: Vec2) -> tuple[int, int]:
        if self.screen_width < 2 or self.screen_height < 2:
            raise ValueError("screen dimensions must be at least 2")
        x = round(position.x / self.world_width * (self.screen_width - 1))
        y = round(position.y / self.world_height * (self.screen_height - 1))
        return max(0, min(self.screen_width - 1, x)), max(0, min(self.screen_height - 1, y))
