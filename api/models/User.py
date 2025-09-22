from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from models.Message import Message
from models.Customer import Customer


class User(SQLModel, table=True):
    id: Optional[int]  = Field(default=None, primary_key=True, index=True)
    name: str = Field(nullable=False, index=True)
    email: str = Field(nullable=False)
    customers: list["Customer"] = Relationship(back_populates="contact")
    messages: list["Message"] = Relationship(back_populates="user")
