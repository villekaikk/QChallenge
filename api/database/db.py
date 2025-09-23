from typing import Optional

from sqlmodel import SQLModel, create_engine, Session, select

from models.Message import Message
from models.User import User
from models.Customer import Customer


class Database:

    instance = None

    def __init__(self, db_url: str):

        self._engine = create_engine(db_url)
        SQLModel.metadata.create_all(self._engine)

    @classmethod
    def get_db(cls, db_url: str = None):

        if cls.instance is None:
            if db_url is None:
                raise ValueError("db_url cannot be None")

            cls.instance = Database(db_url)

        return cls.instance

    def create_user(self, new_user: User) -> User:

        try:
            with Session(self._engine) as session:
                session.add(new_user)
                session.commit()
                print(f"Created new user with id {new_user.id}")

                return new_user

        except Exception as e:
            print(f"Failed to create new user: {e}")
            raise Exception("Failed to nwe create user")

    def update_user(self, user_id: int, user: User) -> Optional[User]:

        try:
            with Session(self._engine) as session:
                statement = select(User).where(User.id == user_id)
                existing: User | None = session.exec(statement).first()
                if not existing:
                    return None

                existing.name = user.name
                existing.email = user.email
                session.commit()
                print(f"Updated user with id {existing.id}")

                return existing

        except Exception as e:
            print(f"Failed to update user: {e}")
            raise Exception("Failed to update user")

    def create_customer(self, new_customer: Customer) -> Customer:

        try:
            with Session(self._engine) as session:
                session.add(new_customer)
                session.commit()
                print(f"Created new customer with id {new_customer.id}")

                return new_customer

        except Exception as e:
            print(f"Failed to create new customer: {e}")
            raise Exception("Failed to new create customer")

    def create_message(self, new_message: Message):

        try:
            with Session(self._engine) as session:
                session.add(new_message)
                session.commit()
                print(f"Created new message with id {new_message.id}")

                return new_message

        except Exception as e:
            print(f"Failed to create new message: {e}")
            raise Exception("Failed to new create message")


    def get_all_messages(self) -> list[Message]:

        try:
            with Session(self._engine) as session:
                statement = select(Message).order_by(Message.created_at)
                messages = session.exec(statement).all()
                return messages or []

        except Exception as e:
            print(f"Failed to query for messages: {e}")
            raise Exception("Failed to query for messages")
