from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.sql import func
from datetime import datetime
import uuid


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, server_default=func.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now)) #This doesn't work
    
    def __repr__(self):
        return f"<User {self.username}>"


"""
for password, chatgpt said this way isn't appropriate 
since the password field might not be created as column in db
instead, he suggested this:
from sqlalchemy import Column, String

password_hash: str = Field(
    sa_column=Column(String, nullable=False),
    exclude=True
)

1. sa_column=Column(...) ensures the field becomes a real database column.
2. exclude=True hides it from things like .model_dump(), FastAPI responses, etc.

Why This Is Important
If you don’t use sa_column, Alembic might not generate the column for password_hash,
and your DB won’t store it. Then authentication will break.
"""