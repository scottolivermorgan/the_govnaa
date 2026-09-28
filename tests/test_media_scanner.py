from pathlib import Path

from app.core.config import AllowedRoot
from app.db.models import Asset, Scan
from app.scanner.media import scan_media_root
from sqlmodel import Session, SQLModel, create_engine, select


def test_scan_media_root_catalogues_supported_files(tmp_path: Path) -> None:
    root_path = tmp_path / "media"
    root_path.mkdir()
    (root_path / "Alien.1979.mkv").touch()
    (root_path / "poster.jpg").touch()
    (root_path / ".hidden").touch()

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        scan = scan_media_root(
            session,
            AllowedRoot(id="test-media", name="Test Media", path=root_path, writable=True),
        )
        assets = session.exec(select(Asset)).all()
        scans = session.exec(select(Scan)).all()

    assert scan.files_seen == 1
    assert scan.files_new == 1
    assert scan.files_ignored == 2
    assert scan.status == "completed"
    assert len(scans) == 1
    assert len(assets) == 1
    assert assets[0].relative_path == "Alien.1979.mkv"


def test_scan_media_root_updates_existing_asset_last_seen(tmp_path: Path) -> None:
    root_path = tmp_path / "media"
    root_path.mkdir()
    (root_path / "Alien.1979.mkv").touch()

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    root = AllowedRoot(id="test-media", name="Test Media", path=root_path, writable=True)
    with Session(engine) as session:
        first_scan = scan_media_root(session, root)
        second_scan = scan_media_root(session, root)
        first_files_new = first_scan.files_new
        second_files_seen = second_scan.files_seen
        second_files_new = second_scan.files_new
        second_files_changed = second_scan.files_changed
        assets = session.exec(select(Asset)).all()

    assert first_files_new == 1
    assert second_files_seen == 1
    assert second_files_new == 0
    assert second_files_changed == 0
    assert len(assets) == 1
