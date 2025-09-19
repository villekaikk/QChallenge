from datetime import datetime

from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class Message(SQLModel, table=True):
    id: int | None  = Field(default=None, primary_key=True)
    body: str = Field(nullable=False)
    created_at: datetime = Field(nullable=False)
    customer_id: int = Field(foreign_key="customer.id")
    user_id: int = Field(foreign_key="user.id")


class MessageCreate(BaseModel):
    body: str
    customer_id: int
    user_id: int
    created_at: datetime
