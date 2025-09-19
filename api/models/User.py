from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id : int | None  = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    email : str = Field(nullable=False)


class UserCreate(BaseModel):
    name: str
    email: str
