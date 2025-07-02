from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.schemas import BookCreate, BookUpdate
from src.books.models import Book as BookModel
from sqlmodel import select, desc


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

    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(BookModel).where(BookModel.uid == book_uid)
        
        result = await session.exec(statement)
        
        return result.first()

    async def create_book(
        self, book_uid: str, book_data: BookCreate, session: AsyncSession
    ):
        pass

    async def update_book(
        self, book_uid: str, update_data: BookUpdate, session: AsyncSession
    ):
        pass

    async def delete_book(self, book_uid: str, session: AsyncSession):
        pass
