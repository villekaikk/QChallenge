from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, text

from models.Message import MessageCreate, Message
from models.User import User, UserCreate
from models.Customer import Customer, CustomerCreate


class Database:

    instance = None

    def __init__(self, db_url: str):

        self._engine = create_engine(db_url)
        self._session_gen: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
        SQLModel.metadata.create_all(self._engine)
        if db_url.startswith("sqlite:///"):
            with self._engine.connect() as conn:
                conn.execute(text("PRAGMA foreign_keys=ON"))

    @classmethod
    def get_db(cls, db_url: str = None):

        if cls.instance is None:
            if db_url is None:
                raise ValueError("db_url cannot be None")

            cls.instance = Database(db_url)

        return cls.instance

    def create_user(self, new_user: UserCreate) -> User:

        try:
            with self._session_gen() as session:
                db_user = User.model_validate(new_user)
                session.add(db_user)
                session.commit()
                session.refresh(db_user)
                return db_user

        except Exception as e:
            print(f"Failed to create new user: {e}")
            raise Exception("Failed to create new user")

    def update_user(self, user_id: int, user: UserCreate) -> User | None:

        try:
            with self._session_gen() as session:
                existing: User | None = session.query(User).filter_by(id=user_id).first()
                if not existing:
                    return None

                validated_user = User.model_validate(user)
                existing.name = validated_user.name
                existing.email = validated_user.email
                session.refresh(existing)

                return existing

        except Exception as e:
            print(f"Failed to update user: {e}")
            raise Exception("Failed to update user")

    def create_customer(self, new_customer: CustomerCreate) -> Customer:

        try:
            with self._session_gen() as session:
                db_customer = Customer.model_validate(new_customer)
                session.add(db_customer)
                session.commit()
                session.refresh(db_customer)

                return db_customer

        except Exception as e:
            print(f"Failed to create new customer: {e}")
            raise Exception("Failed to new create customer")

    def create_message(self, new_message: MessageCreate):

        try:
            with self._session_gen() as session:
                db_message = Message.model_validate(new_message)
                session.add(db_message)
                session.commit()
                session.refresh(db_message)

                return db_message

        except Exception as e:
            print(f"Failed to create new message: {e}")
            raise Exception("Failed to new create message")


    def get_all_messages(self) -> list[Message]:

        try:
            with self._session_gen() as session:
                messages = session.query(Message).order_by(Message.created_at).all()
                return messages or []

        except Exception as e:
            print(f"Failed to query for messages: {e}")
            raise Exception("Failed to query for messages")
