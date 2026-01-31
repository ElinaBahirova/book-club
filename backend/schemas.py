from datetime import datetime

from pydantic import BaseModel


class BookBase(BaseModel):
    """Base schema for book data."""
    title: str
    author: str
    google_books_id: str | None = None
    description: str | None = None
    cover_image_url: str | None = None
    published_date: str | None = None
    page_count: int | None = None
    categories: str | None = None


class BookCreate(BookBase):
    """Schema for creating/curating a book (e.g., from Google Books)."""
    pass


class BookResponse(BookBase):
    """Schema for book responses."""
    id: int
    added_at: datetime | None = None
    is_current_pick: int = 0

    class Config:
        from_attributes = True
