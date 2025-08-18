from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.schemas import BookCreate, BookUpdate
from src.books.models import Book as BookModel
from sqlmodel import select, desc
from datetime import datetime


class BookService:
    async def get_all_books(self, session: AsyncSession):
        """
        Bonus Suggestion for Later: Add Pagination
        If your app grows and you get thousands of books, you’ll eventually want to add pagination:
        statement = select(BookModel).order_by(desc(BookModel.created_at)).offset(skip).limit(limit)
        """

        statement = select(BookModel).order_by(desc(BookModel.created_at))

        result = await session.exec(statement)

        return result.all()

    async def get_user_books(self, user_uid: str, session: AsyncSession):

        statement = (
            select(BookModel)
            .where(BookModel.user_id == user_uid)
            .order_by(desc(BookModel.created_at))
        )

        result = await session.exec(statement)

        return result.all()

    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(BookModel).where(BookModel.uid == book_uid)

        result = await session.exec(statement)

        book = result.first()

        return book if book is not None else None

    async def create_book(
        self, book_data: BookCreate, user_uid: str, session: AsyncSession
    ):
        book_data_dict = book_data.model_dump()

        new_book = BookModel(**book_data_dict)

        new_book.published_date = datetime.strptime(
            book_data_dict["published_date"], "%Y-%m-%d"
        )

        new_book.user_id = user_uid

        session.add(new_book)

        await session.commit()

        return new_book

    async def update_book(
        self, book_uid: str, update_data: BookUpdate, session: AsyncSession
    ):
        book_to_update = await self.get_book(book_uid, session)

        if book_to_update is not None:
            update_data_dict = update_data.model_dump(exclude_unset=True)

            for key, value in update_data_dict.items():
                if hasattr(book_to_update, key):
                    setattr(book_to_update, key, value)

            await session.commit()

            return book_to_update
        else:
            return None

    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)

            await session.commit()

            return {}

        else:
            return None
