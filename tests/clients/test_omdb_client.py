import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

from app.clients.omdb_client import OMDBClient
from app.core.exceptions import ExternalAPIError, MovieNotFoundError


class TestOMDBClient:
    """Test suite for OMDBClient"""

    @pytest.fixture
    def omdb_client(self):
        """Create an OMDBClient instance"""
        return OMDBClient()

    @pytest.mark.asyncio
    async def test_search_movie_by_title_success(
        self, omdb_client, omdb_response_success
    ):
        """Test successful movie search"""
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = omdb_response_success
            mock_response.raise_for_status = MagicMock()
            mock_get.return_value = mock_response

            result = await omdb_client.search_movie_by_title("The Matrix")

            assert result["title"] == "The Matrix"
            assert result["year"] == "1999"
            assert result["imdb_id"] == "tt0133093"
            assert result["director"] == "Lana Wachowski, Lilly Wachowski"
            assert result["imdb_rating"] == 8.7
            mock_get.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_movie_by_title_not_found(
        self, omdb_client, omdb_response_not_found
    ):
        """Test movie not found in OMDB"""
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = omdb_response_not_found
            mock_response.raise_for_status = MagicMock()
            mock_get.return_value = mock_response

            with pytest.raises(MovieNotFoundError) as exc_info:
                await omdb_client.search_movie_by_title("NonExistentMovie")

            assert "not found in OMDB" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_search_movie_by_title_http_error(self, omdb_client):
        """Test HTTP error handling"""
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_get.side_effect = httpx.HTTPStatusError(
                "Internal Server Error",
                request=MagicMock(),
                response=MagicMock(status_code=500),
            )

            with pytest.raises(ExternalAPIError) as exc_info:
                await omdb_client.search_movie_by_title("The Matrix")

            assert "Failed to fetch from OMDB" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_search_movie_by_title_request_error(self, omdb_client):
        """Test request error handling"""
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_get.side_effect = httpx.RequestError("Connection failed")

            with pytest.raises(ExternalAPIError) as exc_info:
                await omdb_client.search_movie_by_title("The Matrix")

            assert "Failed to connect to OMDB" in str(exc_info.value)

    def test_parse_float_valid(self, omdb_client):
        """Test parsing valid float value"""
        result = omdb_client._parse_float("8.7")
        assert result == 8.7

    def test_parse_float_na(self, omdb_client):
        """Test parsing N/A value"""
        result = omdb_client._parse_float("N/A")
        assert result is None

    def test_parse_float_none(self, omdb_client):
        """Test parsing None value"""
        result = omdb_client._parse_float(None)
        assert result is None

    def test_parse_float_invalid(self, omdb_client):
        """Test parsing invalid value"""
        result = omdb_client._parse_float("invalid")
        assert result is None

    def test_parse_omdb_response(self, omdb_client, omdb_response_success):
        """Test parsing OMDB response"""
        result = omdb_client._parse_omdb_response(omdb_response_success)

        assert result["title"] == "The Matrix"
        assert result["year"] == "1999"
        assert result["imdb_id"] == "tt0133093"
        assert result["imdb_rating"] == 8.7
        assert result["rated"] == "R"

    def test_parse_omdb_response_missing_rated(self, omdb_client):
        """Test parsing response with missing 'Rated' field"""
        response = {
            "Title": "Test Movie",
            "Year": "2000",
            "imdbID": "tt1234567",
            "imdbRating": "7.5",
        }

        result = omdb_client._parse_omdb_response(response)

        assert result["rated"] == "N/A"

    def test_parse_omdb_response_with_na_rating(self, omdb_client):
        """Test parsing response with N/A rating"""
        response = {
            "Title": "Test Movie",
            "imdbRating": "N/A",
        }

        result = omdb_client._parse_omdb_response(response)

        assert result["imdb_rating"] is None
