from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import Book
from schemas import BookCreate, BookResponse

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Club API")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Club API"}


@app.get("/books", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    """Get all books."""
    return db.query(Book).all()


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get a specific book by ID."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Add a curated book to the club."""
    # Check if book already exists by Google Books ID
    if book.google_books_id:
        existing = db.query(Book).filter(Book.google_books_id == book.google_books_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Book already in collection")
    
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    """Update an existing book."""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for field, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book, field, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book


@app.patch("/books/{book_id}/current-pick", response_model=BookResponse)
def set_current_pick(book_id: int, db: Session = Depends(get_db)):
    """Set a book as the current club pick."""
    # Clear previous current pick
    db.query(Book).filter(Book.is_current_pick == 1).update({"is_current_pick": 0})
    
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db_book.is_current_pick = 1
    db.commit()
    db.refresh(db_book)
    return db_book


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book."""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return None