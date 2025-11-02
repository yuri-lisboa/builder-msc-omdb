# tests/test_endpoints.py
from unittest.mock import AsyncMock, patch

import pytest


class TestMovieEndpoints:

    @pytest.mark.asyncio
    async def test_create_movie_success(self, client):
        with patch(
            "app.clients.omdb_client.OMDBClient.search_movie_by_title",
            new_callable=AsyncMock,
        ) as mock_search:
            mock_search.return_value = {
                "title": "The Matrix",
                "year": "1999",
                "director": "Wachowskis",
            }

            response = await client.post("/api/v1/movies", json={"title": "The Matrix"})

            assert response.status_code == 201
            data = response.json()
            assert data["title"] == "The Matrix"
            assert "id" in data

    @pytest.mark.asyncio
    async def test_create_movie_duplicate(self, client):
        with patch(
            "app.clients.omdb_client.OMDBClient.search_movie_by_title",
            new_callable=AsyncMock,
        ) as mock_search:
            mock_search.return_value = {"title": "The Matrix", "year": "1999"}

            # Primeira criação
            await client.post("/api/v1/movies", json={"title": "The Matrix"})

            # Segunda criação (duplicata)
            response = await client.post("/api/v1/movies", json={"title": "The Matrix"})

            assert response.status_code == 409
            assert "already exists" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_get_movie_by_id(self, client):
        with patch(
            "app.clients.omdb_client.OMDBClient.search_movie_by_title",
            new_callable=AsyncMock,
        ) as mock_search:
            mock_search.return_value = {"title": "The Matrix", "year": "1999"}

            create_resp = await client.post(
                "/api/v1/movies", json={"title": "The Matrix"}
            )
            movie_id = create_resp.json()["id"]

            response = await client.get(f"/api/v1/movies/{movie_id}")

            assert response.status_code == 200
            assert response.json()["id"] == movie_id

    @pytest.mark.asyncio
    async def test_list_movies(self, client):
        response = await client.get("/api/v1/movies")

        assert response.status_code == 200
        data = response.json()
        assert "movies" in data
        assert "total" in data
