from pydoc import text

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Book
from schemas import BookCreate, BookResponse

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Club API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://book-club-frontend-7kj3.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Execute a simple query to verify the DB connection
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "message": "Backend and Database are communicating correctly!"
        }
    except Exception as e:
        # If the DB connection fails, return a 503 Service Unavailable
        raise HTTPException(
            status_code=503, 
            detail=f"Database connection failed: {str(e)}"
        )

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
