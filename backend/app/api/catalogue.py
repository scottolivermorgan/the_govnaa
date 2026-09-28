from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.config import AllowedRoot, get_settings
from app.db.models import Asset, Scan
from app.db.session import get_session
from app.scanner.media import scan_media_root

router = APIRouter()
SessionDep = Depends(get_session)


@router.post("/scans/{root_id}", response_model=Scan)
def create_scan(root_id: str, session: Session = SessionDep) -> Scan:
    root = find_configured_root(root_id)
    if root is None:
        raise HTTPException(status_code=404, detail=f"Unknown root: {root_id}")
    return scan_media_root(session, root)


@router.get("/scans", response_model=list[Scan])
def list_scans(session: Session = SessionDep) -> list[Scan]:
    return list(session.exec(select(Scan).order_by(Scan.started_at.desc())).all())


@router.get("/scans/{scan_id}", response_model=Scan)
def get_scan(scan_id: UUID, session: Session = SessionDep) -> Scan:
    scan = session.get(Scan, scan_id)
    if scan is None:
        raise HTTPException(status_code=404, detail=f"Unknown scan: {scan_id}")
    return scan


@router.get("/assets", response_model=list[Asset])
def list_assets(session: Session = SessionDep) -> list[Asset]:
    return list(session.exec(select(Asset).order_by(Asset.relative_path)).all())


def find_configured_root(root_id: str) -> AllowedRoot | None:
    settings = get_settings()
    return next((root for root in settings.roots if root.id == root_id), None)
