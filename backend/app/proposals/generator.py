from uuid import UUID

from sqlmodel import Session, select

from app.db.models import Asset, Proposal, Scan
from app.profiles.jellyfin import parse_media_filename


def generate_proposals_for_scan(session: Session, scan_id: UUID) -> list[Proposal]:
    scan = session.get(Scan, scan_id)
    if scan is None:
        raise ValueError(f"Unknown scan: {scan_id}")

    assets = session.exec(
        select(Asset).where(Asset.root_id == scan.root_id).order_by(Asset.relative_path)
    ).all()

    proposals: list[Proposal] = []
    for asset in assets:
        if existing_open_proposal(session, scan.id, asset.id):
            continue

        parsed = parse_media_filename(asset.filename)
        if parsed is None:
            proposal = Proposal(
                scan_id=scan.id,
                asset_id=asset.id,
                operation="classify",
                source_relative_path=asset.relative_path,
                target_relative_path=asset.relative_path,
                confidence=0.2,
                reason="Could not detect Jellyfin movie or TV naming pattern",
                status="needs_classification",
            )
        elif parsed.target_relative_path == asset.relative_path:
            continue
        else:
            proposal = Proposal(
                scan_id=scan.id,
                asset_id=asset.id,
                operation="move",
                source_relative_path=asset.relative_path,
                target_relative_path=parsed.target_relative_path,
                confidence=parsed.confidence,
                reason=parsed.reason,
            )

        session.add(proposal)
        proposals.append(proposal)

    scan.proposals_created += len(proposals)
    session.add(scan)
    session.commit()

    for proposal in proposals:
        session.refresh(proposal)

    return proposals


def existing_open_proposal(session: Session, scan_id: UUID, asset_id: UUID) -> Proposal | None:
    return session.exec(
        select(Proposal).where(
            Proposal.scan_id == scan_id,
            Proposal.asset_id == asset_id,
        )
    ).first()
