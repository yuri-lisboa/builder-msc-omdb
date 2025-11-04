import pytest
import os
from unittest.mock import patch

from app.core.config import Settings


class TestSettings:
    """Test suite for Settings configuration"""

    def test_default_values(self):
        """Test default configuration values"""
        with patch.dict(
            os.environ,
            {
                "POSTGRES_USER": "testuser",
                "POSTGRES_PASSWORD": "testpass",
                "POSTGRES_HOST": "localhost",
                "POSTGRES_DB": "testdb",
                "OMDB_API_KEY": "test_key",
            },
        ):
            settings = Settings()

            assert settings.PROJECT_NAME == "builder-msc-omdb"
            assert settings.VERSION == "1.0.0"
            assert settings.POSTGRES_USER == "testuser"
            assert settings.POSTGRES_PASSWORD == "testpass"
            assert settings.POSTGRES_HOST == "localhost"
            assert settings.POSTGRES_PORT == 5432
            assert settings.POSTGRES_DB == "testdb"
            assert settings.OMDB_API_KEY == "test_key"
            assert settings.OMDB_BASE_URL == "http://www.omdbapi.com/"
            assert settings.CORS_ORIGINS == ["*"]

    def test_database_url_assembly(self):
        """Test DATABASE_URL is properly assembled"""
        with patch.dict(
            os.environ,
            {
                "POSTGRES_USER": "user",
                "POSTGRES_PASSWORD": "pass",
                "POSTGRES_HOST": "db",
                "POSTGRES_PORT": "5432",
                "POSTGRES_DB": "moviedb",
                "OMDB_API_KEY": "key",
            },
        ):
            settings = Settings()

            assert settings.DATABASE_URL is not None
            db_url = str(settings.DATABASE_URL)
            assert "postgresql+asyncpg://" in db_url
            assert "user" in db_url
            assert "pass" in db_url
            assert "db" in db_url
            assert "moviedb" in db_url

    def test_custom_port(self):
        """Test custom PostgreSQL port"""
        with patch.dict(
            os.environ,
            {
                "POSTGRES_USER": "user",
                "POSTGRES_PASSWORD": "pass",
                "POSTGRES_HOST": "localhost",
                "POSTGRES_PORT": "5433",
                "POSTGRES_DB": "testdb",
                "OMDB_API_KEY": "key",
            },
        ):
            settings = Settings()

            assert settings.POSTGRES_PORT == 5433
            assert "5433" in str(settings.DATABASE_URL)

    def test_predefined_database_url(self):
        """Test using a predefined DATABASE_URL"""
        custom_url = "postgresql+asyncpg://custom:pass@host:5432/db"
        with patch.dict(
            os.environ,
            {
                "DATABASE_URL": custom_url,
                "POSTGRES_USER": "user",
                "POSTGRES_PASSWORD": "pass",
                "POSTGRES_HOST": "localhost",
                "POSTGRES_DB": "testdb",
                "OMDB_API_KEY": "key",
            },
        ):
            settings = Settings()

            assert str(settings.DATABASE_URL) == custom_url
