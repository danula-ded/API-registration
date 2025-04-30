
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.user_service import transfer_points

router = APIRouter()

class Transfer(BaseModel):
    from_username: str
    to_username: str
    amount: float

@router.post("/transfer")
def transfer(transfer: Transfer):
    if transfer_points(transfer.from_username, transfer.to_username, transfer.amount):
        return {"message": f"Transferred {transfer.amount} points"}
    raise HTTPException(status_code=400, detail="Transfer failed")
