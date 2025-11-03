from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Movie(Base):
    """Movie database model."""

    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    year: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    rated: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    released: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    runtime: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    genre: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    director: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    writer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    actors: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    plot: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    language: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    awards: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    imdb_rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    imdb_votes: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    imdb_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    box_office: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<Movie(id={self.id}, title='{self.title}', year='{self.year}')>"
