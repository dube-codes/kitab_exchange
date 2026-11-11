from sqlmodel import SQLModel, Relationship, Field
from typing import Optional
from datetime import datetime, timezone


# Database model for the User Table
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)
    phone_number: Optional[str] = Field(default=None, index=True)
    college: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": "CURRENT_TIMESTAMP"},
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={
            "server_default": "CURRENT_TIMESTAMP",
            "onupdate": datetime.now(timezone.utc),
        },
    )

    # one user can have many books,
    books: list["Book"] = Relationship(back_populates="owner")


# request model for creating a new user
class UserCreate(SQLModel):
    name: str
    email: str
    phone_number: Optional[str] = None
    college: str


# request model for updating an existing user
class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    college: Optional[str] = None


# response model for returning user data
class UserRead(SQLModel):
    id: int
    name: str
    email: str
    phone_number: Optional[str] = None
    college: str
    created_at: datetime
    updated_at: datetime


# avoid circular import by importing Book at the end of the file
from models.book import Book

User.model_rebuild()
