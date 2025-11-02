import pytest

from app.repositories.movie_repository import MovieRepository


class TestMovieRepository:

    @pytest.mark.asyncio
    async def test_create_movie(self, test_db, sample_movie_data):
        repo = MovieRepository(test_db)

        movie = await repo.create(sample_movie_data)

        assert movie.id is not None
        assert movie.title == sample_movie_data["title"]
        assert movie.year == sample_movie_data["year"]

    @pytest.mark.asyncio
    async def test_get_by_id(self, test_db, sample_movie_data):
        repo = MovieRepository(test_db)

        created = await repo.create(sample_movie_data)
        found = await repo.get_by_id(created.id)

        assert found is not None
        assert found.id == created.id

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, test_db):
        repo = MovieRepository(test_db)

        movie = await repo.get_by_id(99999)

        assert movie is None

    @pytest.mark.asyncio
    async def test_exists_by_title(self, test_db, sample_movie_data):
        repo = MovieRepository(test_db)

        exists = await repo.exists_by_title("The Matrix")
        assert exists is False

        await repo.create(sample_movie_data)

        exists = await repo.exists_by_title("The Matrix")
        assert exists is True
