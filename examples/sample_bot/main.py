"""External sample bot: reads one observation JSON object and prints one action."""

import json
import math
import sys


def main() -> int:
    observation = json.load(sys.stdin)
    own_x, own_y = observation["self"]["position"]
    opponents = observation.get("opponents", [])
    if not opponents:
        print(json.dumps({"move": [0, 0], "aim": [0, 0], "fire": False}))
        return 0
    target = min(opponents, key=lambda item: (item["position"][0] - own_x) ** 2 + (item["position"][1] - own_y) ** 2)
    dx = target["position"][0] - own_x
    dy = target["position"][1] - own_y
    distance = math.hypot(dx, dy)
    direction = [dx / distance, dy / distance] if distance > 1e-9 else [0, 0]
    action = {"move": direction, "aim": direction, "fire": distance < 430.0}
    print(json.dumps(action))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
