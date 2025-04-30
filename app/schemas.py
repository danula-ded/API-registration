from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from .models import UserRole, ListingStatus

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    email: str
    is_admin: bool
    balance: int

    class Config:
        from_attributes = True

class TransferRequest(BaseModel):
    to_user_id: int
    amount: int

class TransferResponse(BaseModel):
    msg: str
    new_balance: int

class BalanceResponse(BaseModel):
    balance: int

class LeaderboardEntry(BaseModel):
    id: int
    email: str
    balance: int

    class Config:
        from_attributes = True

class MarketplaceListingCreate(BaseModel):
    title: str
    description: str
    points_required: int

class MarketplaceListingResponse(MarketplaceListingCreate):
    id: int
    owner_id: int
    status: ListingStatus
    created_at: datetime

    class Config:
        from_attributes = True

class MarketplaceOfferCreate(BaseModel):
    title: str
    description: str
    price: int

class MarketplaceOfferResponse(BaseModel):
    msg: str
    offer_id: int

class MarketplaceAcceptRequest(BaseModel):
    offer_id: int

class MarketplaceAcceptResponse(BaseModel):
    msg: str

class AdminAssignRequest(BaseModel):
    user_id: int

class AdminAssignResponse(BaseModel):
    msg: str

class AdminTopupRequest(BaseModel):
    user_id: int
    amount: int

class AdminTopupResponse(BaseModel):
    msg: str
    new_balance: int 