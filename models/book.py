from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime, timezone


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
    price: int
    is_sold: bool = Field(default=False)
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

    #  foreign key to the User table
    user_id: int = Field(foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="books")


# request model for creating a new Book
class CreateBook(SQLModel):
    title: str
    author: str
    price: str
    user_id: int


#  request model for updating a book
class UpdateBook(SQLModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[str] = None
    is_sold: Optional[bool] = False


# response model for returning user data
class BookRead(SQLModel):
    id: int
    title: str
    author: str
    price: int
    is_sold: bool
    user_id: int
    created_at: datetime
    updated_at: datetime


from models.user import User

Book.model_rebuild()
