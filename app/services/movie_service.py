import logging

from app.clients.omdb_client import OMDBClient
from app.core.exceptions import MovieAlreadyExistsError, MovieNotFoundError
from app.models.movie import Movie
from app.repositories.movie_repository import MovieRepository

logger = logging.getLogger(__name__)


class MovieService:
    def __init__(self, repository: MovieRepository, omdb_client: OMDBClient) -> None:
        self.repository = repository
        self.omdb_client = omdb_client

    async def create_movie(self, title: str) -> Movie:
        if await self.repository.exists_by_title(title):
            logger.warning(f"Duplicate movie: {title}")
            raise MovieAlreadyExistsError(f"Movie '{title}' already exists")

        logger.info(f"Fetching from OMDB: {title}")
        movie_data = await self.omdb_client.search_movie_by_title(title)

        movie = await self.repository.create(movie_data)
        logger.info(f"Movie created: {movie.id} - {movie.title}")
        return movie

    async def get_movie_by_id(self, movie_id: int) -> Movie:
        movie = await self.repository.get_by_id(movie_id)
        if not movie:
            logger.warning(f"Movie not found: {movie_id}")
            raise MovieNotFoundError(f"Movie {movie_id} not found")
        return movie

    async def get_all_movies(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[list[Movie], int]:
        movies = await self.repository.get_all(skip=skip, limit=limit)
        total = await self.repository.count()
        return movies, total
