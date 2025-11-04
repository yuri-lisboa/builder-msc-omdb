import pytest

from app.repositories.movie_repository import MovieRepository
from app.models.movie import Movie


class TestMovieRepository:
    """Test suite for MovieRepository"""

    @pytest.mark.asyncio
    async def test_create_movie(self, test_db, sample_movie_data):
        """Test creating a movie"""
        repo = MovieRepository(test_db)

        movie = await repo.create(sample_movie_data)

        assert movie.id is not None
        assert movie.title == sample_movie_data["title"]
        assert movie.year == sample_movie_data["year"]
        assert movie.director == sample_movie_data["director"]
        assert movie.imdb_rating == sample_movie_data["imdb_rating"]
        assert movie.created_at is not None
        assert movie.updated_at is not None

    @pytest.mark.asyncio
    async def test_get_by_id_found(self, test_db, sample_movie_data):
        """Test getting a movie by ID when it exists"""
        repo = MovieRepository(test_db)

        created = await repo.create(sample_movie_data)
        found = await repo.get_by_id(created.id)

        assert found is not None
        assert found.id == created.id
        assert found.title == created.title

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, test_db):
        """Test getting a movie by ID when it doesn't exist"""
        repo = MovieRepository(test_db)

        movie = await repo.get_by_id(99999)

        assert movie is None

    @pytest.mark.asyncio
    async def test_get_by_title_found(self, test_db, sample_movie_data):
        """Test getting a movie by title when it exists"""
        repo = MovieRepository(test_db)

        await repo.create(sample_movie_data)
        found = await repo.get_by_title("The Matrix")

        assert found is not None
        assert found.title == "The Matrix"

    @pytest.mark.asyncio
    async def test_get_by_title_case_insensitive(self, test_db, sample_movie_data):
        """Test that title search is case-insensitive"""
        repo = MovieRepository(test_db)

        await repo.create(sample_movie_data)
        found = await repo.get_by_title("the matrix")

        assert found is not None
        assert found.title == "The Matrix"

    @pytest.mark.asyncio
    async def test_get_by_title_not_found(self, test_db):
        """Test getting a movie by title when it doesn't exist"""
        repo = MovieRepository(test_db)

        movie = await repo.get_by_title("NonExistent Movie")

        assert movie is None

    @pytest.mark.asyncio
    async def test_get_all_empty(self, test_db):
        """Test getting all movies when database is empty"""
        repo = MovieRepository(test_db)

        movies = await repo.get_all()

        assert isinstance(movies, list)
        assert len(movies) == 0

    @pytest.mark.asyncio
    async def test_get_all_with_movies(self, test_db, sample_movie_data):
        """Test getting all movies when database has records"""
        repo = MovieRepository(test_db)

        # Create multiple movies
        await repo.create(sample_movie_data)
        await repo.create({**sample_movie_data, "title": "Inception"})
        await repo.create({**sample_movie_data, "title": "Interstellar"})

        movies = await repo.get_all()

        assert len(movies) == 3

    @pytest.mark.asyncio
    async def test_get_all_with_pagination(self, test_db, sample_movie_data):
        """Test pagination with skip and limit"""
        repo = MovieRepository(test_db)

        # Create 5 movies
        for i in range(5):
            await repo.create({**sample_movie_data, "title": f"Movie {i}"})

        # Test skip and limit
        movies = await repo.get_all(skip=1, limit=2)

        assert len(movies) == 2

    @pytest.mark.asyncio
    async def test_get_all_ordered_by_created_at(self, test_db, sample_movie_data):
        """Test that movies are ordered by created_at descending"""
        repo = MovieRepository(test_db)

        movie1 = await repo.create({**sample_movie_data, "title": "First Movie"})
        movie2 = await repo.create({**sample_movie_data, "title": "Second Movie"})

        movies = await repo.get_all()

        # Most recent should be first
        assert movies[0].id == movie2.id
        assert movies[1].id == movie1.id

    @pytest.mark.asyncio
    async def test_count_empty(self, test_db):
        """Test count when database is empty"""
        repo = MovieRepository(test_db)

        count = await repo.count()

        assert count == 0

    @pytest.mark.asyncio
    async def test_count_with_movies(self, test_db, sample_movie_data):
        """Test count with movies in database"""
        repo = MovieRepository(test_db)

        await repo.create(sample_movie_data)
        await repo.create({**sample_movie_data, "title": "Inception"})

        count = await repo.count()

        assert count == 2

    @pytest.mark.asyncio
    async def test_exists_by_title_false(self, test_db):
        """Test exists_by_title returns False when movie doesn't exist"""
        repo = MovieRepository(test_db)

        exists = await repo.exists_by_title("NonExistent")

        assert exists is False

    @pytest.mark.asyncio
    async def test_exists_by_title_true(self, test_db, sample_movie_data):
        """Test exists_by_title returns True when movie exists"""
        repo = MovieRepository(test_db)

        await repo.create(sample_movie_data)
        exists = await repo.exists_by_title("The Matrix")

        assert exists is True

    @pytest.mark.asyncio
    async def test_exists_by_title_case_insensitive(self, test_db, sample_movie_data):
        """Test that exists_by_title is case-insensitive"""
        repo = MovieRepository(test_db)

        await repo.create(sample_movie_data)
        exists = await repo.exists_by_title("the matrix")

        assert exists is True
