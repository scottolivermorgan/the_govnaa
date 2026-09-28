from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AllowedRoot(BaseModel):
    id: str
    name: str
    path: Path
    writable: bool = False


class Settings(BaseSettings):
    app_name: str = "Data Governor"
    database_path: Path = Path("dev-data/governor.db")
    execution_enabled: bool = False
    roots: list[AllowedRoot] = Field(
        default_factory=lambda: [
            AllowedRoot(
                id="test-media",
                name="Test Media",
                path=Path("/data/test-media"),
                writable=True,
            )
        ]
    )

    model_config = SettingsConfigDict(
        env_prefix="GOVERNOR_",
        env_nested_delimiter="__",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
