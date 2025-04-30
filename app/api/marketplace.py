
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.marketplace_service import create_item, accept_offer

router = APIRouter()

class MarketplaceItem(BaseModel):
    username: str
    item_name: str
    description: str
    price: float

@router.post("/marketplace/create")
def create(item: MarketplaceItem):
    if create_item(item.username, item.item_name, item.price):
        return {"message": "Item created successfully"}
    return {"message": "Failed to create item"}

@router.post("/marketplace/accept")
def accept(item_name: str, username: str):
    if accept_offer(item_name, username):
        return {"message": "Offer accepted"}
    return {"message": "Failed to accept offer"}
