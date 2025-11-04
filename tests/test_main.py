import pytest
from app.main import app


class TestMainApp:
    """Test suite for main application"""

    def test_app_title(self):
        """Test that app has correct title"""
        assert app.title == "builder-msc-omdb"

    def test_app_version(self):
        """Test that app has correct version"""
        assert app.version == "1.0.0"

    def test_router_is_included(self):
        """Test that movies router is included"""
        routes = [route.path for route in app.routes]
        assert "/api/v1/movies" in routes or any(
            "/api/v1/movies" in route for route in routes
        )

    def test_health_endpoint_exists(self):
        """Test that health endpoint exists"""
        routes = [route.path for route in app.routes]
        assert "/health" in routes

    @pytest.mark.asyncio
    async def test_health_endpoint_response(self, client):
        """Test health endpoint returns correct response"""
        response = await client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_openapi_paths(self):
        """Test that expected paths are in OpenAPI schema"""
        schema = app.openapi()

        assert "/health" in schema["paths"]
        assert "/api/v1/movies" in schema["paths"]
        assert "/api/v1/movies/{movie_id}" in schema["paths"]

    def test_openapi_movies_post_endpoint(self):
        """Test that POST /api/v1/movies endpoint is documented"""
        schema = app.openapi()

        assert "post" in schema["paths"]["/api/v1/movies"]
        post_spec = schema["paths"]["/api/v1/movies"]["post"]
        assert "201" in post_spec["responses"]
        assert "404" in post_spec["responses"]
        assert "409" in post_spec["responses"]
        assert "502" in post_spec["responses"]

    def test_openapi_movies_get_by_id_endpoint(self):
        """Test that GET /api/v1/movies/{movie_id} endpoint is documented"""
        schema = app.openapi()

        assert "get" in schema["paths"]["/api/v1/movies/{movie_id}"]
        get_spec = schema["paths"]["/api/v1/movies/{movie_id}"]["get"]
        assert "200" in get_spec["responses"]

    def test_openapi_movies_list_endpoint(self):
        """Test that GET /api/v1/movies endpoint is documented"""
        schema = app.openapi()

        assert "get" in schema["paths"]["/api/v1/movies"]
        get_spec = schema["paths"]["/api/v1/movies"]["get"]
        assert "200" in get_spec["responses"]
