"""
Pydantic schemas for Movie API with specific field validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator


class MovieCreate(BaseModel):
    """Schema for creating a movie."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Movie title",
        examples=["The Matrix"],
    )


class MovieResponse(BaseModel):
    """Schema for movie response with specific validated fields."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Movie ID")
    imdb_id: str = Field(..., description="IMDB unique identifier")
    title: str = Field(..., description="Movie title")
    plot: Optional[str] = Field(None, description="Movie plot/synopsis")
    released: Optional[str] = Field(None, description="Release date")
    year: Optional[str] = Field(None, description="Release year")
    runtime: Optional[str] = Field(None, description="Movie runtime")
    genre: Optional[str] = Field(None, description="Movie genres")
    rated: Optional[str] = Field(None, description="Movie rating (PG, R, etc)")
    director: Optional[str] = Field(None, description="Director name(s)")
    writer: Optional[str] = Field(None, description="Writer name(s)")
    actors: Optional[str] = Field(None, description="Actor name(s)")
    imdb_rating: Optional[float] = Field(None, description="IMDB rating (0-10)")
    awards: Optional[str] = Field(None, description="Awards received")
    language: Optional[str] = Field(None, description="Languages")
    country: Optional[str] = Field(None, description="Countries")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    @field_validator("imdb_rating")
    @classmethod
    def validate_rating(cls, v: Optional[float]) -> Optional[float]:
        """Validate IMDB rating is between 0 and 10."""
        if v is not None and (v < 0 or v > 10):
            raise ValueError("IMDB rating must be between 0 and 10")
        return v


class MovieListResponse(BaseModel):
    """Schema for movie list response."""

    movies: list[MovieResponse] = Field(..., description="List of movies")
    total: int = Field(..., description="Total number of movies")


class ErrorResponse(BaseModel):
    """Schema for error responses."""

    detail: str = Field(..., description="Error message")
