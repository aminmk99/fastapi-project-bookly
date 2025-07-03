from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import Config

"""
The instructor used an odd way. You've asked him why he did this in comments.
Don't forget to check for his answer.
engine = AsyncEngine(create_engine(url=Config.DATABASE_URL, echo=True))
"""

# The way chatgpt suggests:
engine = create_async_engine(Config.DATABASE_URL, echo=True)


async def init_db():
    async with engine.begin() as conn:
        from src.books.models import Book

        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:

    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
        
    async with Session() as session:
        yield session
