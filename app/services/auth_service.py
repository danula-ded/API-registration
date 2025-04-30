
from app.models.user import User
from app.core.security import get_password_hash
from app.core.db import engine
from sqlalchemy.orm import Session
from app.core.config import DATABASE_URL

def create_user(username: str, password: str):
    db = Session(bind=engine)
    user = User(username=username, hashed_password=get_password_hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user
