import logging
from typing import Optional

import httpx

from app.core.config import settings
from app.core.exceptions import ExternalAPIError, MovieNotFoundError

logger = logging.getLogger(__name__)


class OMDBClient:

    def __init__(self) -> None:
        self.base_url = settings.OMDB_BASE_URL
        self.api_key = settings.OMDB_API_KEY
        self.timeout = 10.0

    async def search_movie_by_title(self, title: str) -> dict:
        params = {
            "apikey": self.api_key,
            "t": title,
            "plot": "full",
            "type": "movie",
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("Response") == "False":
                    error_msg = data.get("Error", "Movie not found")
                    logger.warning(f"Movie not found: {title} - {error_msg}")
                    raise MovieNotFoundError(f"Movie '{title}' not found in OMDB")

                return self._parse_omdb_response(data)

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
            raise ExternalAPIError(f"Failed to fetch from OMDB: {e}") from e
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise ExternalAPIError(f"Failed to connect to OMDB: {e}") from e

    def _parse_omdb_response(self, data: dict) -> dict:
        return {
            "imdb_id": data.get("imdbID"),
            "title": data.get("Title"),
            "plot": data.get("Plot"),
            "released": data.get("Released"),
            "year": data.get("Year"),
            "runtime": data.get("Runtime"),
            "genre": data.get("Genre"),
            "rated": data.get("Rated") or data.get("rated") or "N/A",
            "director": data.get("Director"),
            "writer": data.get("Writer"),
            "actors": data.get("Actors"),
            "imdb_rating": self._parse_float(data.get("imdbRating")),
            "awards": data.get("Awards"),
            "language": data.get("Language"),
            "country": data.get("Country"),
        }

    @staticmethod
    def _parse_float(value: Optional[str]) -> Optional[float]:
        if not value or value == "N/A":
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
