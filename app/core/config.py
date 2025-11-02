from typing import List

from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "builder-msc-omdb"
    VERSION: str = "1.0.0"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    DATABASE_URL: PostgresDsn | None = None

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str | None, info) -> str:
        if isinstance(v, str):
            return v
        data = info.data
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=data.get("POSTGRES_USER"),
                password=data.get("POSTGRES_PASSWORD"),
                host=data.get("POSTGRES_HOST"),
                port=data.get("POSTGRES_PORT"),
                path=f"{data.get('POSTGRES_DB') or ''}",
            )
        )

    OMDB_API_KEY: str
    OMDB_BASE_URL: str = "http://www.omdbapi.com/"

    CORS_ORIGINS: List[str] = ["*"]


settings = Settings()
