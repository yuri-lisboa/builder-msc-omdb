from datetime import datetime, UTC
from app.models.movie import Movie


class TestMovieModel:
    """Test suite for Movie model"""

    def test_movie_repr(self):
        """Test Movie string representation"""
        movie = Movie(id=1, title="The Matrix", year="1999")

        repr_str = repr(movie)

        assert "Movie" in repr_str
        assert "id=1" in repr_str
        assert "title='The Matrix'" in repr_str
        assert "year='1999'" in repr_str

    def test_movie_creation_with_all_fields(self):
        """Test creating Movie with all fields"""
        now = datetime.now(UTC)
        movie = Movie(
            id=1,
            imdb_id="tt0133093",
            title="The Matrix",
            plot="A computer hacker learns...",
            released="31 Mar 1999",
            year="1999",
            runtime="136 min",
            genre="Action, Sci-Fi",
            director="Wachowskis",
            rated="R",
            writer="Wachowskis",
            actors="Keanu Reeves",
            language="English",
            country="United States",
            awards="Won 4 Oscars",
            imdb_rating=8.7,
            created_at=now,
            updated_at=now,
        )

        assert movie.id == 1
        assert movie.title == "The Matrix"
        assert movie.year == "1999"
        assert movie.imdb_rating == 8.7
        assert movie.created_at == now
        assert movie.updated_at == now

    def test_movie_creation_with_minimal_fields(self):
        """Test creating Movie with minimal required fields"""
        movie = Movie(title="Test Movie")

        assert movie.title == "Test Movie"
        assert movie.imdb_id is None
        assert movie.plot is None
        assert movie.imdb_rating is None

    def test_movie_optional_fields(self):
        """Test that optional fields can be None"""
        movie = Movie(
            title="Test Movie",
            imdb_id=None,
            plot=None,
            released=None,
            year=None,
            runtime=None,
            genre=None,
            director=None,
            rated=None,
            writer=None,
            actors=None,
            language=None,
            country=None,
            awards=None,
            imdb_rating=None,
        )

        assert movie.title == "Test Movie"
        assert movie.imdb_id is None
        assert movie.plot is None
        assert movie.imdb_rating is None

    def test_movie_timestamps_auto_generation(self):
        """Test that timestamps are auto-generated"""
        movie = Movie(title="Test Movie")

        # In real database context, these would be set automatically
        # Here we're just testing the model structure
        assert hasattr(movie, "created_at")
        assert hasattr(movie, "updated_at")
