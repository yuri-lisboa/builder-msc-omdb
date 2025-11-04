from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class MovieCreate(BaseModel):
    """Schema para criar filme - apenas título necessário"""

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Movie title",
        examples=["The Matrix"],
    )


class MovieResponse(BaseModel):
    """Schema de resposta - todos os campos"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    imdb_id: Optional[str] = None
    title: str
    plot: Optional[str] = None
    released: Optional[str] = None
    year: Optional[str] = None
    runtime: Optional[str] = None
    genre: Optional[str] = None
    director: Optional[str] = None
    rated: Optional[str] = None
    writer: Optional[str] = None
    actors: Optional[str] = None
    imdb_rating: Optional[float] = None
    awards: Optional[str] = None
    language: Optional[str] = None
    country: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class MovieListResponse(BaseModel):
    """Schema para lista de filmes"""

    movies: list[MovieResponse]
    total: int


class ErrorResponse(BaseModel):
    """Schema para erros"""

    detail: str
