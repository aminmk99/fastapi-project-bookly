from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.service import BookService
from src.books.schemas import Book, BookUpdate, BookCreate
from src.db.main import get_session


book_router = APIRouter()
book_service = BookService()


# READ ALL BOOKS
@book_router.get("/", response_model=List[Book])
async def get_books(session: AsyncSession = Depends(get_session)):

    books = await book_service.get_all_books(session)
    return books


# READ A BOOK
@book_router.get("/{book_uid}", response_model=Book)
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    book = await book_service.get_book(book_uid, session)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")


# CREATE
@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate, session: AsyncSession = Depends(get_session)
) -> Book:  # Which return type is correct? Book or Dictionary?

    new_book = await book_service.create_book(book_data, session)
    return new_book


# UPDATE
@book_router.patch("/{book_uid}", response_model=Book)
async def update_book(
    book_uid: str, update_data: BookUpdate, session: AsyncSession = Depends(get_session)
) -> Book:
    updated_book = await book_service.update_book(
        book_uid,
        update_data,
        session,
    )

    if update_book:
        return update_book
    else:
        raise HTTPException(status_code=404, detail="Book not found")


# DELETE
@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    deleted_book = await book_service.delete_book(book_uid, session)
    
    if deleted_book:
        return None
    else:
        raise HTTPException(status_code=404, detail="Book not found")
