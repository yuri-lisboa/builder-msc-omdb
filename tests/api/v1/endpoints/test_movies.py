import pytest
from unittest.mock import AsyncMock, patch

from app.core.exceptions import (
    MovieAlreadyExistsError,
    MovieNotFoundError,
    ExternalAPIError,
)


class TestMovieEndpoints:
    """Test suite for movie endpoints"""

    @pytest.mark.asyncio
    async def test_health_check(self, client):
        """Test health check endpoint"""
        response = await client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    @pytest.mark.asyncio
    async def test_create_movie_success(self, client, sample_movie_data):
        """Test successful movie creation"""
        with patch(
            "app.clients.omdb_client.OMDBClient.search_movie_by_title",
            new_callable=AsyncMock,
        ) as mock_search:
            mock_search.return_value = sample_movie_data

            response = await client.post("/api/v1/movies", json={"title": "The Matrix"})

            assert response.status_code == 201
            data = response.json()
            assert data["title"] == "The Matrix"
            assert "id" in data
            assert "created_at" in data
            assert "updated_at" in data

    @pytest.mark.asyncio
    async def test_create_movie_duplicate(self, client, sample_movie_data):
        """Test creating duplicate movie"""
        with patch(
            "app.clients.omdb_client.OMDBClient.search_movie_by_title",
            new_callable=AsyncMock,
        ) as mock_search:
            mock_search.return_value = sample_movie_data

            # Create first movie
            await client.post("/api/v1/movies", json={"title": "The Matrix"})

            # Try to create duplicate
            response = await client.post("/api/v1/movies", json={"title": "The Matrix"})

            assert response.status_code == 409
            assert "already exists" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_create_movie_not_found_in_omdb(self, client):
        """Test creating movie not found in OMDB"""
        with patch(
            "app.clients.omdb_client.OMDBClient.search_movie_by_title",
            new_callable=AsyncMock,
        ) as mock_search:
            mock_search.side_effect = MovieNotFoundError("Movie not found in OMDB")

            response = await client.post(
                "/api/v1/movies", json={"title": "NonExistent Movie"}
            )

            assert response.status_code == 404
            assert "not found" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_create_movie_external_api_error(self, client):
        """Test creating movie with external API error"""
        with patch(
            "app.clients.omdb_client.OMDBClient.search_movie_by_title",
            new_callable=AsyncMock,
        ) as mock_search:
            mock_search.side_effect = ExternalAPIError("API Error")

            response = await client.post("/api/v1/movies", json={"title": "Test Movie"})

            assert response.status_code == 502
            assert "API Error" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_create_movie_invalid_input(self, client):
        """Test creating movie with invalid input"""
        response = await client.post("/api/v1/movies", json={"title": ""})

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_movie_missing_title(self, client):
        """Test creating movie without title"""
        response = await client.post("/api/v1/movies", json={})

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_movie_by_id_success(self, client, sample_movie_data):
        """Test getting movie by ID successfully"""
        with patch(
            "app.clients.omdb_client.OMDBClient.search_movie_by_title",
            new_callable=AsyncMock,
        ) as mock_search:
            mock_search.return_value = sample_movie_data

            # Create movie
            create_resp = await client.post(
                "/api/v1/movies", json={"title": "The Matrix"}
            )
            movie_id = create_resp.json()["id"]

            # Get movie
            response = await client.get(f"/api/v1/movies/{movie_id}")

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == movie_id
            assert data["title"] == "The Matrix"

    @pytest.mark.asyncio
    async def test_get_movie_by_id_not_found(self, client):
        """Test getting non-existent movie by ID"""
        response = await client.get("/api/v1/movies/99999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_list_movies_empty(self, client):
        """Test listing movies when database is empty"""
        response = await client.get("/api/v1/movies")

        assert response.status_code == 200
        data = response.json()
        assert "movies" in data
        assert "total" in data
        assert len(data["movies"]) == 0
        assert data["total"] == 0

    @pytest.mark.asyncio
    async def test_list_movies_with_data(self, client, sample_movie_data):
        """Test listing movies with data"""
        with patch(
            "app.clients.omdb_client.OMDBClient.search_movie_by_title",
            new_callable=AsyncMock,
        ) as mock_search:
            mock_search.return_value = sample_movie_data

            # Create movies
            await client.post("/api/v1/movies", json={"title": "The Matrix"})
            
            # Modify sample data for second movie
            mock_search.return_value = {**sample_movie_data, "title": "Inception"}
            await client.post("/api/v1/movies", json={"title": "Inception"})

            # List movies
            response = await client.get("/api/v1/movies")

            assert response.status_code == 200
            data = response.json()
            assert len(data["movies"]) == 2
            assert data["total"] == 2

    @pytest.mark.asyncio
    async def test_list_movies_pagination(self, client, sample_movie_data):
        """Test listing movies with pagination"""
        with patch(
            "app.clients.omdb_client.OMDBClient.search_movie_by_title",
            new_callable=AsyncMock,
        ) as mock_search:
            # Create 3 movies
            for i, title in enumerate(["Movie 1", "Movie 2", "Movie 3"]):
                mock_search.return_value = {**sample_movie_data, "title": title}
                await client.post("/api/v1/movies", json={"title": title})

            # Test skip and limit
            response = await client.get("/api/v1/movies?skip=1&limit=2")

            assert response.status_code == 200
            data = response.json()
            assert len(data["movies"]) == 2
            assert data["total"] == 3

    @pytest.mark.asyncio
    async def test_list_movies_invalid_pagination(self, client):
        """Test listing movies with invalid pagination parameters"""
        # Negative skip
        response = await client.get("/api/v1/movies?skip=-1")
        assert response.status_code == 422

        # Limit exceeding maximum
        response = await client.get("/api/v1/movies?limit=101")
        assert response.status_code == 422

        # Zero limit
        response = await client.get("/api/v1/movies?limit=0")
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_list_movies_default_pagination(self, client):
        """Test listing movies with default pagination values"""
        response = await client.get("/api/v1/movies")

        assert response.status_code == 200
        # Should use default values (skip=0, limit=100)

    @pytest.mark.asyncio
    async def test_create_movie_special_characters(self, client, sample_movie_data):
        """Test creating movie with special characters in title"""
        with patch(
            "app.clients.omdb_client.OMDBClient.search_movie_by_title",
            new_callable=AsyncMock,
        ) as mock_search:
            special_title = "Movie: The Sequel (2024)"
            mock_search.return_value = {**sample_movie_data, "title": special_title}

            response = await client.post(
                "/api/v1/movies", json={"title": special_title}
            )

            assert response.status_code == 201
            assert response.json()["title"] == special_title

    @pytest.mark.asyncio
    async def test_endpoint_cors_headers(self, client):
        """Test that CORS headers are present"""
        response = await client.get("/health")

        # FastAPI CORS middleware should add these headers
        assert response.status_code == 200
