from datetime import UTC, datetime
from pathlib import Path

from sqlmodel import Session, select

from app.core.config import AllowedRoot
from app.db.models import Asset, Root, Scan, utc_now

SUPPORTED_MEDIA_EXTENSIONS = {".mkv"}


def scan_media_root(session: Session, root: AllowedRoot, profile_id: str = "jellyfin-media") -> Scan:
    ensure_root(session, root)

    scan = Scan(root_id=root.id, profile_id=profile_id, status="running")
    session.add(scan)
    session.commit()
    session.refresh(scan)

    try:
        for path in iter_files(root.path):
            relative_path = path.relative_to(root.path).as_posix()

            if should_ignore(path):
                scan.files_ignored += 1
                continue

            scan.files_seen += 1
            asset = find_asset(session, root.id, relative_path)
            stat = path.stat()

            if asset is None:
                session.add(build_asset(root.id, relative_path, path, stat.st_size, stat.st_mtime))
                scan.files_new += 1
            elif asset_has_changed(asset, stat.st_size, stat.st_mtime):
                asset.size_bytes = stat.st_size
                asset.mtime = mtime_to_datetime(stat.st_mtime)
                asset.last_seen_at = utc_now()
                scan.files_changed += 1
            else:
                asset.last_seen_at = utc_now()

        scan.status = "completed"
        scan.completed_at = utc_now()
        session.add(scan)
        session.commit()
        session.refresh(scan)
        return scan
    except Exception:
        scan.status = "failed"
        scan.completed_at = utc_now()
        session.add(scan)
        session.commit()
        raise


def ensure_root(session: Session, root: AllowedRoot) -> None:
    existing = session.get(Root, root.id)
    if existing is None:
        session.add(Root(id=root.id, name=root.name, path=str(root.path), writable=root.writable))
    else:
        existing.name = root.name
        existing.path = str(root.path)
        existing.writable = root.writable
    session.commit()


def iter_files(root_path: Path) -> list[Path]:
    if not root_path.exists():
        return []
    return sorted(path for path in root_path.rglob("*") if path.is_file())


def should_ignore(path: Path) -> bool:
    if any(part.startswith(".") for part in path.parts):
        return True
    return path.suffix.lower() not in SUPPORTED_MEDIA_EXTENSIONS


def find_asset(session: Session, root_id: str, relative_path: str) -> Asset | None:
    statement = select(Asset).where(
        Asset.root_id == root_id,
        Asset.relative_path == relative_path,
    )
    return session.exec(statement).first()


def build_asset(
    root_id: str,
    relative_path: str,
    path: Path,
    size_bytes: int,
    mtime: float,
) -> Asset:
    return Asset(
        root_id=root_id,
        relative_path=relative_path,
        original_relative_path=relative_path,
        filename=path.name,
        extension=path.suffix.lower(),
        mime_type="video/x-matroska",
        size_bytes=size_bytes,
        mtime=mtime_to_datetime(mtime),
    )


def asset_has_changed(asset: Asset, size_bytes: int, mtime: float) -> bool:
    return asset.size_bytes != size_bytes or asset.mtime != mtime_to_datetime(mtime)


def mtime_to_datetime(mtime: float) -> datetime:
    return datetime.fromtimestamp(mtime, UTC)
