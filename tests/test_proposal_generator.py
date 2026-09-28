from pathlib import Path

from app.core.config import AllowedRoot
from app.db.models import Proposal
from app.proposals.generator import generate_proposals_for_scan
from app.scanner.media import scan_media_root
from sqlmodel import Session, SQLModel, create_engine, select


def test_generate_proposals_for_scan_creates_media_moves(tmp_path: Path) -> None:
    root_path = tmp_path / "media"
    root_path.mkdir()
    (root_path / "Dune.2021.2160p.mkv").touch()
    (root_path / "Severance.S01E02.2160p.mkv").touch()
    (root_path / "badly_named_file.mkv").touch()

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        scan = scan_media_root(
            session,
            AllowedRoot(id="test-media", name="Test Media", path=root_path, writable=True),
        )
        proposals = generate_proposals_for_scan(session, scan.id)

    targets = {proposal.source_relative_path: proposal.target_relative_path for proposal in proposals}
    statuses = {proposal.source_relative_path: proposal.status for proposal in proposals}

    assert targets["Dune.2021.2160p.mkv"] == "Movies/Dune (2021)/Dune (2021).mkv"
    assert targets["Severance.S01E02.2160p.mkv"] == (
        "TV/Severance/Season 01/Severance - S01E02.mkv"
    )
    assert statuses["badly_named_file.mkv"] == "needs_classification"


def test_generate_proposals_for_scan_is_idempotent(tmp_path: Path) -> None:
    root_path = tmp_path / "media"
    root_path.mkdir()
    (root_path / "Dune.2021.2160p.mkv").touch()

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        scan = scan_media_root(
            session,
            AllowedRoot(id="test-media", name="Test Media", path=root_path, writable=True),
        )
        generate_proposals_for_scan(session, scan.id)
        generate_proposals_for_scan(session, scan.id)
        proposals = session.exec(select(Proposal)).all()

    assert len(proposals) == 1


def test_generate_proposals_skips_already_correct_asset(tmp_path: Path) -> None:
    root_path = tmp_path / "media"
    existing_path = root_path / "Movies" / "Alien (1979)"
    existing_path.mkdir(parents=True)
    (existing_path / "Alien (1979).mkv").touch()

    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        scan = scan_media_root(
            session,
            AllowedRoot(id="test-media", name="Test Media", path=root_path, writable=True),
        )
        proposals = generate_proposals_for_scan(session, scan.id)

    assert proposals == []
