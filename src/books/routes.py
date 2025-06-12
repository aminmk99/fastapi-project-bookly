from typing import List
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from src.books.book_data import books
from src.books.schemas import Book, BookUpdate


book_router = APIRouter()


# READ ALL BOOKS
@book_router.get("/", response_model=List[Book])
async def get_books():
    return books


# READ A BOOK
@book_router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


# CREATE
@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: Book) -> Book:  # Shouldn't return type be dictionary?
    for b in books:
        if b["id"] == book.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book with this ID already exists",
            )

    # Convert Book model to dict
    new_book = book.model_dump()
    books.append(new_book)
    return new_book


# UPDATE
@book_router.patch("/{book_id}", response_model=Book)
async def update_book(book_id: int, update: BookUpdate):
    for book in books:
        if book["id"] == book_id:
            updated_data = update.model_dump(exclude_unset=True)
            book.update(updated_data)
            return book
    raise HTTPException(status_code=404, detail="Book not found")


# DELETE
@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {}
    raise HTTPException(status_code=404, detail="Book not found")
