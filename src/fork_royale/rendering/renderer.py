"""ASCII top-down renderer for debugging. Its character cells are visual only."""

from fork_royale.core.world import World
from fork_royale.rendering.camera import Camera


class AsciiRenderer:
    def __init__(self, columns: int = 60, rows: int = 22):
        if columns < 10 or rows < 5:
            raise ValueError("renderer dimensions are too small")
        self.columns = columns
        self.rows = rows

    def render(self, world: World) -> str:
        camera = Camera(world.width, world.height, self.columns, self.rows)
        canvas = [[" " for _ in range(self.columns)] for _ in range(self.rows)]
        for obstacle in world.obstacles:
            x, y = camera.world_to_screen(obstacle.position)
            canvas[y][x] = "O"
        for projectile in world.projectiles:
            x, y = camera.world_to_screen(projectile.position)
            canvas[y][x] = "."
        for entity in world.entities.values():
            x, y = camera.world_to_screen(entity.position)
            canvas[y][x] = entity.entity_id[0].upper() if entity.alive else "x"
        top = "+" + "-" * self.columns + "+"
        lines = [top]
        lines.extend("|" + "".join(row) + "|" for row in canvas)
        lines.append(top)
        status = "  ".join(f"{e.entity_id}: {e.hp}/{e.max_hp} HP" for e in world.entities.values())
        lines.append(f"Tick {world.tick}  |  {status}")
        lines.append("Rendering is quantized for display only; simulation positions are continuous.")
        return "\n".join(lines)
