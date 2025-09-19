from datetime import datetime

from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class Customer(SQLModel, table=True):
    id : int | None  = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    contact_id: int = Field(foreign_key="user.id")
    created_at : datetime = Field(nullable=False)


class CustomerCreate(BaseModel):
    name: str
    contact_id: int
    created_at: datetime
