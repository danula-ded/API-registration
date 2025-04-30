
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.user_service import create_user

router = APIRouter()

class User(BaseModel):
    username: str
    password: str

@router.post("/register")
def register_user(user: User):
    new_user = create_user(user.username, user.password)
    if new_user:
        return {"message": "User successfully registered"}
    raise HTTPException(status_code=400, detail="User already exists")
