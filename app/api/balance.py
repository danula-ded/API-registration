
from fastapi import APIRouter, HTTPException
from app.services.user_service import get_balance

router = APIRouter()

@router.get("/balance")
def balance(username: str):
    user_balance = get_balance(username)
    if user_balance is not None:
        return {"balance": user_balance}
    raise HTTPException(status_code=404, detail="User not found")
