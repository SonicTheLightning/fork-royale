"""Read and validate the lightweight JSON Lines replay format."""

import json
from pathlib import Path
from typing import Iterator


class ReplayFormatError(ValueError):
    pass


def read_replay(path: str | Path) -> Iterator[dict]:
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as handle:
        first = handle.readline()
        try:
            header = json.loads(first)
        except json.JSONDecodeError as exc:
            raise ReplayFormatError("replay header is not valid JSON") from exc
        if header.get("type") != "header" or header.get("format") != "fork-royale-replay":
            raise ReplayFormatError("unrecognized replay format")
        if header.get("version") != 1:
            raise ReplayFormatError("unsupported replay version")
        for line_number, line in enumerate(handle, start=2):
            if not line.strip():
                continue
            try:
                frame = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ReplayFormatError(f"invalid JSON on line {line_number}") from exc
            if frame.get("type") != "frame" or not isinstance(frame.get("world"), dict):
                raise ReplayFormatError(f"invalid frame on line {line_number}")
            yield frame
