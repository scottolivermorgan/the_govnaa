from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import Column
from sqlalchemy.types import JSON
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(UTC)


class Root(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    path: str
    writable: bool = False
    created_at: datetime = Field(default_factory=utc_now)


class Asset(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    root_id: str = Field(foreign_key="root.id")
    relative_path: str
    original_relative_path: str
    filename: str
    extension: str
    mime_type: str | None = None
    size_bytes: int
    mtime: datetime
    fingerprint: str | None = None
    status: str = "active"
    metadata_json: dict = Field(default_factory=dict, sa_column=Column(JSON))
    first_seen_at: datetime = Field(default_factory=utc_now)
    last_seen_at: datetime = Field(default_factory=utc_now)


class Scan(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    root_id: str = Field(foreign_key="root.id")
    profile_id: str
    status: str = "pending"
    started_at: datetime = Field(default_factory=utc_now)
    completed_at: datetime | None = None
    files_seen: int = 0
    files_new: int = 0
    files_changed: int = 0
    files_ignored: int = 0
    proposals_created: int = 0


class Proposal(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    scan_id: UUID = Field(foreign_key="scan.id")
    asset_id: UUID = Field(foreign_key="asset.id")
    operation: str
    source_relative_path: str
    target_relative_path: str
    confidence: float
    reason: str
    status: str = "pending_review"
    created_at: datetime = Field(default_factory=utc_now)
    reviewed_at: datetime | None = None


class ExecutionBatch(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    scan_id: UUID = Field(foreign_key="scan.id")
    started_at: datetime = Field(default_factory=utc_now)
    completed_at: datetime | None = None
    status: str = "pending"


class ExecutionOperation(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    batch_id: UUID = Field(foreign_key="executionbatch.id")
    proposal_id: UUID = Field(foreign_key="proposal.id")
    operation: str
    source_relative_path: str
    target_relative_path: str
    status: str = "pending"
    executed_at: datetime | None = None
    error: str | None = None
