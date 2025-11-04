import pytest

from app.core.exceptions import (
    MovieAPIException,
    MovieNotFoundError,
    MovieAlreadyExistsError,
    ExternalAPIError,
)


class TestExceptions:
    """Test suite for custom exceptions"""

    def test_movie_api_exception_base(self):
        """Test base exception"""
        exc = MovieAPIException("Test error")
        assert str(exc) == "Test error"
        assert isinstance(exc, Exception)

    def test_movie_not_found_error(self):
        """Test MovieNotFoundError"""
        exc = MovieNotFoundError("Movie not found")
        assert str(exc) == "Movie not found"
        assert isinstance(exc, MovieAPIException)

    def test_movie_already_exists_error(self):
        """Test MovieAlreadyExistsError"""
        exc = MovieAlreadyExistsError("Movie already exists")
        assert str(exc) == "Movie already exists"
        assert isinstance(exc, MovieAPIException)

    def test_external_api_error(self):
        """Test ExternalAPIError"""
        exc = ExternalAPIError("API error")
        assert str(exc) == "API error"
        assert isinstance(exc, MovieAPIException)

    def test_exception_inheritance_chain(self):
        """Test that all exceptions inherit from MovieAPIException"""
        assert issubclass(MovieNotFoundError, MovieAPIException)
        assert issubclass(MovieAlreadyExistsError, MovieAPIException)
        assert issubclass(ExternalAPIError, MovieAPIException)
        assert issubclass(MovieAPIException, Exception)
