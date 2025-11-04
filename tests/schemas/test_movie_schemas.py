import pytest
from datetime import datetime
from pydantic import ValidationError

from app.schemas.movie import (
    MovieCreate,
    MovieResponse,
    MovieListResponse,
    ErrorResponse,
)


class TestMovieSchemas:
    """Test suite for movie schemas"""

    def test_movie_create_valid(self):
        """Test MovieCreate with valid data"""
        movie = MovieCreate(title="The Matrix")

        assert movie.title == "The Matrix"

    def test_movie_create_empty_title(self):
        """Test MovieCreate with empty title"""
        with pytest.raises(ValidationError):
            MovieCreate(title="")

    def test_movie_create_title_too_long(self):
        """Test MovieCreate with title exceeding max length"""
        with pytest.raises(ValidationError):
            MovieCreate(title="a" * 256)

    def test_movie_create_missing_title(self):
        """Test MovieCreate without title"""
        with pytest.raises(ValidationError):
            MovieCreate()

    def test_movie_response_full_data(self):
        """Test MovieResponse with complete data"""
        data = {
            "id": 1,
            "imdb_id": "tt0133093",
            "title": "The Matrix",
            "plot": "A computer hacker learns...",
            "released": "31 Mar 1999",
            "year": "1999",
            "runtime": "136 min",
            "genre": "Action, Sci-Fi",
            "director": "Wachowskis",
            "rated": "R",
            "writer": "Wachowskis",
            "actors": "Keanu Reeves",
            "imdb_rating": 8.7,
            "awards": "Won 4 Oscars",
            "language": "English",
            "country": "United States",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        movie = MovieResponse(**data)

        assert movie.id == 1
        assert movie.title == "The Matrix"
        assert movie.imdb_rating == 8.7

    def test_movie_response_minimal_data(self):
        """Test MovieResponse with minimal required data"""
        data = {
            "id": 1,
            "title": "Test Movie",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        movie = MovieResponse(**data)

        assert movie.id == 1
        assert movie.title == "Test Movie"
        assert movie.imdb_id is None
        assert movie.plot is None
        assert movie.imdb_rating is None

    def test_movie_response_missing_required_field(self):
        """Test MovieResponse without required fields"""
        with pytest.raises(ValidationError):
            MovieResponse(title="Test Movie")

    def test_movie_list_response_empty(self):
        """Test MovieListResponse with empty list"""
        response = MovieListResponse(movies=[], total=0)

        assert len(response.movies) == 0
        assert response.total == 0

    def test_movie_list_response_with_movies(self):
        """Test MovieListResponse with movies"""
        movies = [
            MovieResponse(
                id=1,
                title="Movie 1",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
            MovieResponse(
                id=2,
                title="Movie 2",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
        ]
        response = MovieListResponse(movies=movies, total=2)

        assert len(response.movies) == 2
        assert response.total == 2
        assert response.movies[0].title == "Movie 1"
        assert response.movies[1].title == "Movie 2"

    def test_error_response(self):
        """Test ErrorResponse schema"""
        error = ErrorResponse(detail="An error occurred")

        assert error.detail == "An error occurred"

    def test_movie_response_from_orm(self):
        """Test MovieResponse with from_attributes config"""
        # This test verifies that the model_config is properly set
        assert MovieResponse.model_config["from_attributes"] is True
