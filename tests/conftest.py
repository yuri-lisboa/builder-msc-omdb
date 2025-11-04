import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """Isolated test database"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    TestSessionLocal = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with TestSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """HTTP test client"""

    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def sample_movie_data() -> dict:
    """Sample movie data for testing"""
    return {
        "title": "The Matrix",
        "year": "1999",
        "director": "Lana Wachowski, Lilly Wachowski",
        "imdb_rating": 8.7,
        "imdb_id": "tt0133093",
        "plot": "A computer hacker learns from mysterious rebels...",
        "released": "31 Mar 1999",
        "runtime": "136 min",
        "genre": "Action, Sci-Fi",
        "rated": "R",
        "writer": "Lana Wachowski, Lilly Wachowski",
        "actors": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
        "language": "English",
        "country": "United States",
        "awards": "Won 4 Oscars",
    }


@pytest.fixture
def omdb_response_success() -> dict:
    """OMDB API successful response"""
    return {
        "Response": "True",
        "Title": "The Matrix",
        "Year": "1999",
        "Rated": "R",
        "Released": "31 Mar 1999",
        "Runtime": "136 min",
        "Genre": "Action, Sci-Fi",
        "Director": "Lana Wachowski, Lilly Wachowski",
        "Writer": "Lana Wachowski, Lilly Wachowski",
        "Actors": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
        "Plot": "A computer hacker learns from mysterious rebels...",
        "Language": "English",
        "Country": "United States",
        "Awards": "Won 4 Oscars",
        "imdbRating": "8.7",
        "imdbVotes": "1,800,000",
        "imdbID": "tt0133093",
    }


@pytest.fixture
def omdb_response_not_found() -> dict:
    """OMDB API not found response"""
    return {"Response": "False", "Error": "Movie not found!"}
