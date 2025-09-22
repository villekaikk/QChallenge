from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.User import User
    from models.Customer import Customer


class Message(SQLModel, table=True):
    id: Optional[int]  = Field(default=None, primary_key=True, index=True)
    body: str = Field(nullable=False)
    customer_id: int = Field(foreign_key="customer.id")
    user_id: int = Field(foreign_key="user.id")
    customer: Optional["Customer"] = Relationship(back_populates="messages")
    user: Optional["User"] = Relationship(back_populates="messages")
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now())
