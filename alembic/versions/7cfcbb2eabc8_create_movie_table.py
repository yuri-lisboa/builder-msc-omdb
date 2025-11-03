"""create movie table

Revision ID: 7cfcbb2eabc8
Revises:
Create Date: 2025-11-03 16:29:34.491183

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7cfcbb2eabc8"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Create movies table with specific validated fields from OMDB.

    Fields included:
    - imdb_id: IMDB unique identifier (required, unique)
    - title: Movie title (required, unique)
    - plot: Movie synopsis
    - released: Release date
    - year: Release year
    - runtime: Movie duration
    - genre: Movie genres
    - rated: Movie rating (PG, R, etc)
    - director: Director name(s)
    - writer: Writer name(s)
    - actors: Actor name(s)
    - imdb_rating: IMDB rating (0-10)
    - awards: Awards received
    - language: Languages
    - country: Countries
    - created_at: Record creation timestamp
    - updated_at: Record update timestamp
    """
    op.create_table(
        "movies",
        # Primary Key
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        # IMDB Unique Identifier (Required)
        sa.Column(
            "imdb_id",
            sa.String(length=20),
            nullable=False,
            comment="IMDB unique identifier (e.g., tt0133093)",
        ),
        # Basic Information (Required)
        sa.Column(
            "title", sa.String(length=255), nullable=False, comment="Movie title"
        ),
        # Plot/Synopsis
        sa.Column("plot", sa.Text(), nullable=True, comment="Movie plot/synopsis"),
        # Release Information
        sa.Column(
            "released",
            sa.String(length=50),
            nullable=True,
            comment="Release date (e.g., '03 Jul 1985')",
        ),
        sa.Column("year", sa.String(length=10), nullable=True, comment="Release year"),
        # Duration
        sa.Column(
            "runtime",
            sa.String(length=50),
            nullable=True,
            comment="Movie runtime (e.g., '116 min')",
        ),
        # Categories
        sa.Column(
            "genre",
            sa.String(length=255),
            nullable=True,
            comment="Movie genres (comma-separated)",
        ),
        sa.Column(
            "rated",
            sa.String(length=10),
            nullable=True,
            comment="Movie rating (e.g., 'PG', 'R', 'PG-13')",
        ),
        # Credits
        sa.Column(
            "director", sa.String(length=255), nullable=True, comment="Director name(s)"
        ),
        sa.Column("writer", sa.Text(), nullable=True, comment="Writer name(s)"),
        sa.Column("actors", sa.Text(), nullable=True, comment="Actor name(s)"),
        # Rating
        sa.Column(
            "imdb_rating", sa.Float(), nullable=True, comment="IMDB rating (0-10)"
        ),
        # Recognition
        sa.Column("awards", sa.Text(), nullable=True, comment="Awards received"),
        # Regional Information
        sa.Column(
            "language",
            sa.String(length=255),
            nullable=True,
            comment="Languages (comma-separated)",
        ),
        sa.Column(
            "country",
            sa.String(length=255),
            nullable=True,
            comment="Countries (comma-separated)",
        ),
        # Metadata Timestamps
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="Record creation timestamp",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            onupdate=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="Record last update timestamp",
        ),
    )

    # Create indexes for better query performance
    op.create_index(op.f("ix_movies_id"), "movies", ["id"], unique=False)
    op.create_index(op.f("ix_movies_imdb_id"), "movies", ["imdb_id"], unique=True)
    op.create_index(op.f("ix_movies_title"), "movies", ["title"], unique=True)
    op.create_index(op.f("ix_movies_year"), "movies", ["year"], unique=False)
    op.create_index(op.f("ix_movies_genre"), "movies", ["genre"], unique=False)
    op.create_index(op.f("ix_movies_director"), "movies", ["director"], unique=False)
    op.create_index(
        op.f("ix_movies_imdb_rating"), "movies", ["imdb_rating"], unique=False
    )


def downgrade() -> None:
    """Drop movies table and all indexes."""
    op.drop_index(op.f("ix_movies_imdb_rating"), table_name="movies")
    op.drop_index(op.f("ix_movies_director"), table_name="movies")
    op.drop_index(op.f("ix_movies_genre"), table_name="movies")
    op.drop_index(op.f("ix_movies_year"), table_name="movies")
    op.drop_index(op.f("ix_movies_title"), table_name="movies")
    op.drop_index(op.f("ix_movies_imdb_id"), table_name="movies")
    op.drop_index(op.f("ix_movies_id"), table_name="movies")
    op.drop_table("movies")
