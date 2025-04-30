
from app.models.user import User
from app.core.db import engine
from sqlalchemy.orm import Session
from app.core.security import verify_password
from app.core.config import DATABASE_URL

def get_balance(username: str):
    db = Session(bind=engine)
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if user:
        return user.balance
    return None

def transfer_points(from_username: str, to_username: str, amount: float):
    db = Session(bind=engine)
    from_user = db.query(User).filter(User.username == from_username).first()
    to_user = db.query(User).filter(User.username == to_username).first()
    
    if from_user and to_user and from_user.balance >= amount:
        from_user.balance -= amount
        to_user.balance += amount
        db.commit()
        db.refresh(from_user)
        db.refresh(to_user)
        db.close()
        return True
    db.close()
    return False

def get_leaderboard():
    db = Session(bind=engine)
    users = db.query(User).order_by(User.balance.desc()).limit(10).all()
    db.close()
    return [{"username": user.username, "balance": user.balance} for user in users]

def assign_admin(username: str):
    db = Session(bind=engine)
    user = db.query(User).filter(User.username == username).first()
    if user:
        user.is_admin = True
        db.commit()
        db.refresh(user)
        db.close()
        return True
    db.close()
    return False

def top_up_balance(username: str, amount: float):
    db = Session(bind=engine)
    user = db.query(User).filter(User.username == username).first()
    if user:
        user.balance += amount
        db.commit()
        db.refresh(user)
        db.close()
        return True
    db.close()
    return False
