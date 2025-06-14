from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from src.config import Config

"""
The instructor used an odd way. You've asked him why he did this in comments.
Don't forget to check for his answer.
engine = AsyncEngine(create_engine(url=Config.DATABASE_URL, echo=True))
"""

#The way chatgpt suggests:
engine = create_async_engine(Config.DATABASE_URL, echo=True)