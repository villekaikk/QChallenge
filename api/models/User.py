from typing import TYPE_CHECKING, Optional

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .Message import Message
    from .Customer import Customer


class User(SQLModel, table=True):
    id: Optional[int]  = Field(default=None, primary_key=True, index=True)
    name: str = Field(nullable=False, index=True)
    email: str = Field(nullable=False)
    customers: list["Customer"] = Relationship(back_populates="contact")
    messages: list["Message"] = Relationship(back_populates="user")
