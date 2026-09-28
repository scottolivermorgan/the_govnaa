from pathlib import Path

import pytest
from app.core.config import AllowedRoot
from app.core.paths import PathEscapeError, resolve_asset_path


def test_resolve_asset_path_stays_inside_root(tmp_path: Path) -> None:
    root = AllowedRoot(id="test", name="Test", path=tmp_path, writable=True)

    resolved = resolve_asset_path(root, "incoming/movie.mkv")

    assert resolved == tmp_path / "incoming" / "movie.mkv"


def test_resolve_asset_path_blocks_escape(tmp_path: Path) -> None:
    root = AllowedRoot(id="test", name="Test", path=tmp_path, writable=True)

    with pytest.raises(PathEscapeError):
        resolve_asset_path(root, "../outside.mkv")
