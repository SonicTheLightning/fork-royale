"""Locate optional repository assets without coupling them to the engine."""

from pathlib import Path


def repository_asset_path(name: str) -> Path:
    if not name or Path(name).name != name:
        raise ValueError("asset name must be a simple filename")
    module_path = Path(__file__).resolve()
    for parent in module_path.parents:
        candidate = parent / "assets" / name
        if candidate.is_file():
            return candidate
    # Return the conventional source-checkout location for a useful error path.
    return module_path.parents[3] / "assets" / name
