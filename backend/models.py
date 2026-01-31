from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class Book(Base):
    """SQLAlchemy model for books table."""
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    google_books_id = Column(String(50), unique=True, index=True)  # Google Books volume ID
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    description = Column(Text)
    cover_image_url = Column(String(500))
    published_date = Column(String(20))  # Google returns various formats
    page_count = Column(Integer)
    categories = Column(String(255))  # Comma-separated
    
    # Curation fields
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    is_current_pick = Column(Integer, default=0)  # 1 = currently reading