from pathlib import Path

from app.core.config import AllowedRoot


class PathEscapeError(ValueError):
    """Raised when a requested path escapes its configured root."""


def resolve_asset_path(root: AllowedRoot, relative_path: str | Path) -> Path:
    root_path = root.path.resolve()
    candidate = (root_path / relative_path).resolve()

    if candidate != root_path and root_path not in candidate.parents:
        raise PathEscapeError(f"path escapes configured root: {relative_path}")

    return candidate
