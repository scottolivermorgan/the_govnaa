from collections.abc import Generator

from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import get_settings


def get_engine() -> Engine:
    settings = get_settings()
    settings.database_path.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(f"sqlite:///{settings.database_path}")


engine = get_engine()


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session
