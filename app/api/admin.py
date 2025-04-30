
from fastapi import APIRouter, HTTPException
from app.services.user_service import assign_admin, top_up_balance

router = APIRouter()

@router.post("/admin/assign")
def assign(username: str):
    if assign_admin(username):
        return {"message": f"User {username} assigned as admin"}
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/admin/topup")
def top_up(username: str, amount: float):
    if top_up_balance(username, amount):
        return {"message": f"User {username} balance topped up with {amount}"}
    raise HTTPException(status_code=404, detail="User not found")
