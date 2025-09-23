from fastapi import FastAPI, Depends, HTTPException
from starlette import status

from models.User import User
from models.Customer import Customer
from models.Message import Message

from database.db import Database

DATABASE_URL = "sqlite:///./test.db"
_ = Database.get_db(DATABASE_URL)   # Init DB with the connection string
app = FastAPI()


@app.post("/api/users", status_code=status.HTTP_201_CREATED)
async def create_user(new_user: User, db: Database = Depends(Database.get_db)) -> User:
    created_user = db.create_user(new_user)
    if created_user is None:
        raise HTTPException(status_code=status.INTERNAL_SERVER_ERROR, detail="User creation failed")

    return created_user


@app.put("/api/users/{user_id}", status_code=status.HTTP_200_OK)
async def create_update(user_id: int, user: User, db: Database = Depends(Database.get_db)) -> User:
    updated_user = db.update_user(user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")

    return updated_user


@app.post("/api/customers", status_code=status.HTTP_201_CREATED)
async def create_user(new_customer: Customer, db: Database = Depends(Database.get_db)) -> Customer:
    created_customer = db.create_customer(new_customer)
    if created_customer is None:
        raise HTTPException(status_code=status.INTERNAL_SERVER_ERROR, detail="Customer creation failed")

    return created_customer


@app.post("/api/messages", status_code=status.HTTP_201_CREATED)
async def create_message(new_message: Message, db: Database = Depends(Database.get_db)) -> Message:
    message_created = db.create_message(new_message)
    if message_created is None:
        raise HTTPException(status_code=status.INTERNAL_SERVER_ERROR, detail="Message creation failed")

    return message_created


@app.get("/api/messages")
async def get_all_messages(db: Database = Depends(Database.get_db)) -> list[Message]:
    return db.get_all_messages()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
