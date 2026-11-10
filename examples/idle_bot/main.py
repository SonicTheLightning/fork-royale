"""External idle bot: reads one observation and returns a neutral action."""

import json
import sys


def main() -> int:
    json.load(sys.stdin)
    print(json.dumps({"move": [0, 0], "aim": [0, 0], "fire": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
