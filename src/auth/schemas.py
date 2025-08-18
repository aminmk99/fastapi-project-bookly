from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from src.books.schemas import Book
import uuid


class UserCreate(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class User(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime
    books: List[Book]


class UserLogin(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)    
