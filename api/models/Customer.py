from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .User import User
    from .Message import Message


class Customer(SQLModel, table=True):
    id : Optional[int]  = Field(default=None, primary_key=True, index=True)
    name: str = Field(nullable=False)
    contact_id: int = Field(foreign_key="user.id")
    contact: Optional["User"] = Relationship(back_populates="customers")
    messages: list["Message"] = Relationship(back_populates="customer")
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())
