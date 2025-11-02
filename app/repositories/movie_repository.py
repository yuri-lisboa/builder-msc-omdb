from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import Movie


class MovieRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, movie_data: dict) -> Movie:
        movie = Movie(**movie_data)
        self.session.add(movie)
        await self.session.commit()
        await self.session.refresh(movie)
        return movie

    async def get_by_id(self, movie_id: int) -> Optional[Movie]:
        result = await self.session.execute(select(Movie).where(Movie.id == movie_id))
        return result.scalar_one_or_none()

    async def get_by_title(self, title: str) -> Optional[Movie]:
        result = await self.session.execute(
            select(Movie).where(Movie.title.ilike(title))
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Movie]:
        result = await self.session.execute(
            select(Movie).offset(skip).limit(limit).order_by(Movie.created_at.desc())
        )
        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.session.execute(select(Movie))
        return len(list(result.scalars().all()))

    async def exists_by_title(self, title: str) -> bool:
        movie = await self.get_by_title(title)
        return movie is not None
