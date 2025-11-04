import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.omdb_client import OMDBClient
from app.core.exceptions import (
    ExternalAPIError,
    MovieAlreadyExistsError,
    MovieNotFoundError,
)
from app.db.database import get_db
from app.repositories.movie_repository import MovieRepository
from app.schemas.movie import MovieCreate, MovieListResponse, MovieResponse
from app.services.movie_service import MovieService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/movies", tags=["movies"])


def get_movie_service(db: Annotated[AsyncSession, Depends(get_db)]) -> MovieService:
    """Dependency injection do service"""
    repository = MovieRepository(db)
    omdb_client = OMDBClient()
    return MovieService(repository, omdb_client)


@router.post(
    "",
    response_model=MovieResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Movie created"},
        404: {"description": "Not found in OMDB"},
        409: {"description": "Already exists"},
        502: {"description": "External API error"},
    },
)
async def create_movie(
    movie_create: MovieCreate,
    service: Annotated[MovieService, Depends(get_movie_service)],
) -> MovieResponse:
    try:
        movie = await service.create_movie(movie_create.title)
        return MovieResponse.model_validate(movie)
    except MovieAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except MovieNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ExternalAPIError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))


@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie(
    movie_id: int,
    service: Annotated[MovieService, Depends(get_movie_service)],
) -> MovieResponse:
    try:
        movie = await service.get_movie_by_id(movie_id)
        return MovieResponse.model_validate(movie)
    except MovieNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("", response_model=MovieListResponse)
async def list_movies(
    service: Annotated[MovieService, Depends(get_movie_service)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> MovieListResponse:
    movies, total = await service.get_all_movies(skip=skip, limit=limit)
    return MovieListResponse(
        movies=[MovieResponse.model_validate(m) for m in movies],
        total=total,
    )
