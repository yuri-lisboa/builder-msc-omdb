from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Movie(Base):
    """Model representa tabela movies no banco"""

    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    imdb_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    title: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    plot: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    released: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    year: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    runtime: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    genre: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    director: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    rated: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    writer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    actors: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    language: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    awards: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    imdb_rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<Movie(id={self.id}, title='{self.title}', year='{self.year}')>"
