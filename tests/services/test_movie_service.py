import pytest
from unittest.mock import AsyncMock, MagicMock

from app.services.movie_service import MovieService
from app.core.exceptions import MovieAlreadyExistsError, MovieNotFoundError
from app.models.movie import Movie


class TestMovieService:
    """Test suite for MovieService"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return MagicMock()

    @pytest.fixture
    def mock_omdb_client(self):
        """Create a mock OMDB client"""
        return MagicMock()

    @pytest.fixture
    def movie_service(self, mock_repository, mock_omdb_client):
        """Create a MovieService instance with mocked dependencies"""
        return MovieService(mock_repository, mock_omdb_client)

    @pytest.mark.asyncio
    async def test_create_movie_success(
        self, movie_service, mock_repository, mock_omdb_client, sample_movie_data
    ):
        """Test successful movie creation"""
        # Setup mocks
        mock_repository.exists_by_title = AsyncMock(return_value=False)
        mock_omdb_client.search_movie_by_title = AsyncMock(
            return_value=sample_movie_data
        )

        mock_movie = Movie(**sample_movie_data)
        mock_movie.id = 1
        mock_repository.create = AsyncMock(return_value=mock_movie)

        # Execute
        result = await movie_service.create_movie("The Matrix")

        # Assert
        assert result.id == 1
        assert result.title == "The Matrix"
        mock_repository.exists_by_title.assert_called_once_with("The Matrix")
        mock_omdb_client.search_movie_by_title.assert_called_once_with("The Matrix")
        mock_repository.create.assert_called_once_with(sample_movie_data)

    @pytest.mark.asyncio
    async def test_create_movie_already_exists(
        self, movie_service, mock_repository, mock_omdb_client
    ):
        """Test creating a movie that already exists"""
        # Setup mocks
        mock_repository.exists_by_title = AsyncMock(return_value=True)

        # Execute and Assert
        with pytest.raises(MovieAlreadyExistsError) as exc_info:
            await movie_service.create_movie("The Matrix")

        assert "already exists" in str(exc_info.value)
        mock_repository.exists_by_title.assert_called_once_with("The Matrix")
        mock_omdb_client.search_movie_by_title.assert_not_called()
        mock_repository.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_movie_not_found_in_omdb(
        self, movie_service, mock_repository, mock_omdb_client
    ):
        """Test creating a movie not found in OMDB"""
        # Setup mocks
        mock_repository.exists_by_title = AsyncMock(return_value=False)
        mock_omdb_client.search_movie_by_title = AsyncMock(
            side_effect=MovieNotFoundError("Movie not found in OMDB")
        )

        # Execute and Assert
        with pytest.raises(MovieNotFoundError):
            await movie_service.create_movie("NonExistent Movie")

        mock_repository.exists_by_title.assert_called_once()
        mock_omdb_client.search_movie_by_title.assert_called_once()
        mock_repository.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_movie_by_id_found(
        self, movie_service, mock_repository, sample_movie_data
    ):
        """Test getting a movie by ID when it exists"""
        # Setup mocks
        mock_movie = Movie(**sample_movie_data)
        mock_movie.id = 1
        mock_repository.get_by_id = AsyncMock(return_value=mock_movie)

        # Execute
        result = await movie_service.get_movie_by_id(1)

        # Assert
        assert result.id == 1
        assert result.title == "The Matrix"
        mock_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_movie_by_id_not_found(self, movie_service, mock_repository):
        """Test getting a movie by ID when it doesn't exist"""
        # Setup mocks
        mock_repository.get_by_id = AsyncMock(return_value=None)

        # Execute and Assert
        with pytest.raises(MovieNotFoundError) as exc_info:
            await movie_service.get_movie_by_id(999)

        assert "not found" in str(exc_info.value)
        mock_repository.get_by_id.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_get_all_movies_empty(self, movie_service, mock_repository):
        """Test getting all movies when database is empty"""
        # Setup mocks
        mock_repository.get_all = AsyncMock(return_value=[])
        mock_repository.count = AsyncMock(return_value=0)

        # Execute
        movies, total = await movie_service.get_all_movies()

        # Assert
        assert len(movies) == 0
        assert total == 0
        mock_repository.get_all.assert_called_once_with(skip=0, limit=100)
        mock_repository.count.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_movies_with_results(
        self, movie_service, mock_repository, sample_movie_data
    ):
        """Test getting all movies with results"""
        # Setup mocks
        mock_movies = [
            Movie(**{**sample_movie_data, "title": "Movie 1"}),
            Movie(**{**sample_movie_data, "title": "Movie 2"}),
        ]
        mock_repository.get_all = AsyncMock(return_value=mock_movies)
        mock_repository.count = AsyncMock(return_value=2)

        # Execute
        movies, total = await movie_service.get_all_movies()

        # Assert
        assert len(movies) == 2
        assert total == 2
        mock_repository.get_all.assert_called_once_with(skip=0, limit=100)
        mock_repository.count.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_movies_with_pagination(
        self, movie_service, mock_repository, sample_movie_data
    ):
        """Test getting all movies with custom pagination"""
        # Setup mocks
        mock_movies = [Movie(**sample_movie_data)]
        mock_repository.get_all = AsyncMock(return_value=mock_movies)
        mock_repository.count = AsyncMock(return_value=10)

        # Execute
        movies, total = await movie_service.get_all_movies(skip=5, limit=5)

        # Assert
        assert len(movies) == 1
        assert total == 10
        mock_repository.get_all.assert_called_once_with(skip=5, limit=5)
        mock_repository.count.assert_called_once()
